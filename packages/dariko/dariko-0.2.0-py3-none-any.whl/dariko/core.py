import inspect
import os
from typing import Any, Type, get_type_hints, Optional, List
import json
import requests
import dis
import ast

from pydantic import ValidationError as _PydanticValidationError
from pydantic import TypeAdapter, BaseModel


class ValidationError(Exception):
    """LLM 出力の型検証エラーを表す例外"""

    def __init__(self, original: _PydanticValidationError):
        super().__init__(str(original))
        self.original = original


# APIキー設定
_API_KEY: Optional[str] = None


def configure(api_key: str | None = None) -> None:
    """
    dariko の設定を行う。
    
    Args:
        api_key: LLM APIのキー。Noneの場合は環境変数 DARIKO_API_KEY から取得を試みる。
    """
    global _API_KEY
    _API_KEY = api_key or os.getenv("DARIKO_API_KEY")


def _get_api_key() -> str:
    """設定されたAPIキーを取得する。未設定の場合はエラーを投げる。"""
    if _API_KEY is None:
        raise RuntimeError(
            "APIキーが設定されていません。configure() で設定するか、"
            "環境変数 DARIKO_API_KEY を設定してください。"
        )
    return _API_KEY


def _infer_output_model_from_ast(frame) -> type | None:
    filename = frame.f_code.co_filename
    lineno = frame.f_lineno
    try:
        with open(filename, "r", encoding="utf-8") as f:
            source = f.read()
        tree = ast.parse(source, filename)
        # 直前のAnnAssign（型付き代入）を探索
        last_ann = None
        for node in ast.walk(tree):
            if isinstance(node, ast.AnnAssign) and hasattr(node, "lineno") and node.lineno < lineno:
                if last_ann is None or node.lineno > last_ann.lineno:
                    last_ann = node
        if last_ann and isinstance(last_ann.target, ast.Name):
            varname = last_ann.target.id
            type_str = ast.unparse(last_ann.annotation)
            try:
                model = eval(type_str, frame.f_globals, frame.f_locals)
                if isinstance(model, type) and issubclass(model, BaseModel):
                    return model
                return None
            except Exception:
                return None
    except Exception:
        return None
    return None


def _infer_output_model_from_locals(frame) -> Type[Any] | None:
    func_name = frame.f_code.co_name
    if func_name == "<module>":
        # モジュールスコープの場合はASTで推論する
        return _infer_output_model_from_ast(frame)
    func = frame.f_globals.get(func_name, None)
    if func is not None:
        hints = get_type_hints(func)
        if len(hints) == 1:
            return next(iter(hints.values()))
    hints = frame.f_locals.get("__annotations__", {})
    if len(hints) == 1:
        return next(iter(hints.values()))
    # fallback: ASTで推論
    return _infer_output_model_from_ast(frame)


def _infer_output_model_from_return_type(frame) -> Type[Any] | None:
    """
    呼び出し元関数の戻り値型アノテーションを取得する。
    """
    try:
        # 呼び出し元の関数オブジェクトを取得
        caller_frame = frame.f_back
        if caller_frame is None:
            return None
        
        # 関数名を取得
        func_name = caller_frame.f_code.co_name
        if func_name == "<module>":
            return None
        
        # 関数オブジェクトを取得
        func = caller_frame.f_locals.get(func_name)
        if func is None:
            return None
        
        # 戻り値型を取得
        hints = get_type_hints(func)
        return hints.get("return")
    except Exception:
        return None


def _get_pydantic_model(model):
    origin = getattr(model, '__origin__', None)
    if origin in (list, List):
        model = model.__args__[0]
    if not (isinstance(model, type) and issubclass(model, BaseModel)):
        raise TypeError("output_modelはPydanticモデルである必要がある")
    return model


def ask(prompt: str, *, output_model: Type[Any] | None = None) -> Any:
    """
    LLM へ prompt を投げ、output_model で検証済みのオブジェクトを返す。
    output_model が未指定なら呼び出し元のローカル変数アノテーションを推測。
    関数内で呼ばれた場合は戻り値型アノテーションも考慮する。

    Args:
        prompt: LLMに送信するプロンプト
        output_model: 出力の型。未指定の場合は自動推論を試みる。

    Returns:
        output_model で検証済みのオブジェクト

    Raises:
        ValidationError: 型検証に失敗した場合
        TypeError: 型アノテーションが取得できなかった場合
        RuntimeError: APIキーが設定されていない場合
    """
    model = output_model
    if model is None:
        caller_frame = inspect.currentframe().f_back  # 1 つ上のフレーム
        if caller_frame is None:
            raise TypeError("型アノテーションが取得できませんでした。output_model を指定してください。")
        
        # ローカル変数の型アノテーションを試す
        model = _infer_output_model_from_locals(caller_frame)
        
        # 戻り値型アノテーションを試す
        if model is None:
            model = _infer_output_model_from_return_type(caller_frame)

    if model is None:
        raise TypeError("型アノテーションが取得できませんでした。output_model を指定してください。")

    # Pydanticモデルを取得
    pyd_model = _get_pydantic_model(model)

    # APIキーを取得
    api_key = _get_api_key()

    # LLM APIを呼び出す
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "system",
                    "content": f"以下のJSONスキーマに従って応答してください：\n{pyd_model.model_json_schema()}"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "response_format": {"type": "json_object"}
        }
    )
    
    if response.status_code != 200:
        raise RuntimeError(f"LLM API呼び出しに失敗しました: {response.text}")

    try:
        llm_raw_output = response.json()["choices"][0]["message"]["content"]
        llm_raw_output = json.loads(llm_raw_output)
        llm_raw_output["api_key"] = api_key  # APIキーを追加
        return TypeAdapter(model).validate_python(llm_raw_output)
    except _PydanticValidationError as e:
        raise ValidationError(e) from None
    except json.JSONDecodeError as e:
        raise ValidationError(_PydanticValidationError.from_exception_data(
            "JSONDecodeError",
            [{"loc": (), "msg": f"LLMの出力がJSONとして解析できませんでした: {str(e)}", "type": "value_error"}]
        )) from None


def ask_batch(prompts: list[str], *, output_model: Type[Any] | None = None) -> list[Any]:
    """
    複数のプロンプトをバッチ処理で実行する。

    Args:
        prompts: LLMに送信するプロンプトのリスト
        output_model: 出力の型。未指定の場合は自動推論を試みる。

    Returns:
        output_model で検証済みのオブジェクトのリスト

    Raises:
        ValidationError: 型検証に失敗した場合
        TypeError: 型アノテーションが取得できなかった場合
        RuntimeError: APIキーが設定されていない場合
    """
    # 型アノテーションの取得
    model = output_model
    if model is None:
        caller_frame = inspect.currentframe().f_back
        if caller_frame is None:
            raise TypeError("型アノテーションが取得できませんでした。output_model を指定してください。")
        
        # ローカル変数の型アノテーションを試す
        model = _infer_output_model_from_locals(caller_frame)
        
        # 戻り値型アノテーションを試す
        if model is None:
            model = _infer_output_model_from_return_type(caller_frame)

    if model is None:
        raise TypeError("型アノテーションが取得できませんでした。output_model を指定してください。")

    # Pydanticモデルを取得
    pyd_model = _get_pydantic_model(model)

    # APIキーを取得
    api_key = _get_api_key()

    # 各プロンプトに対してLLM APIを呼び出す
    results = []
    for prompt in prompts:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": "gpt-3.5-turbo",
                "messages": [
                    {
                        "role": "system",
                        "content": f"以下のJSONスキーマに従って応答してください：\n{pyd_model.model_json_schema()}"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "response_format": {"type": "json_object"}
            }
        )
        
        if response.status_code != 200:
            raise RuntimeError(f"LLM API呼び出しに失敗しました: {response.text}")

        try:
            llm_raw_output = response.json()["choices"][0]["message"]["content"]
            llm_raw_output = json.loads(llm_raw_output)
            llm_raw_output["api_key"] = api_key  # APIキーを追加
            result = TypeAdapter(model).validate_python(llm_raw_output)
            results.append(result)
        except _PydanticValidationError as e:
            raise ValidationError(e) from None
        except json.JSONDecodeError as e:
            raise ValidationError(_PydanticValidationError.from_exception_data(
                "JSONDecodeError",
                [{"loc": (), "msg": f"LLMの出力がJSONとして解析できませんでした: {str(e)}", "type": "value_error"}]
            )) from None

    return results
