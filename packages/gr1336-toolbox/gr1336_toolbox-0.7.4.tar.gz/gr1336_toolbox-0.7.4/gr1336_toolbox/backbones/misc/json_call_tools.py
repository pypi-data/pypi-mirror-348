import json
from typing import Optional, Union
from typing import List, Dict, Callable, Any, Optional

# To make this as optional, this was setup.
pydantic_available = False
try:
    from pydantic import BaseModel  # type: ignore

    pydantic_available = True
except ModuleNotFoundError:

    class BaseModel:
        pass


def safe_execute(func: Callable, *args, **kwargs) -> Dict[str, Any]:
    """Executes a function safely, returning errors as a dictionary."""
    try:
        result = func(*args, **kwargs)
        return {"success": True, "result": result}
    except Exception as e:
        return {"success": False, "error": str(e)}


# Validation models
class Action(BaseModel):
    item: str
    args: List[Any] = []
    kwargs: Dict[str, Any] = {}
    result_var: str
    post_processor: Optional[str] = None


class ReturnConfig(BaseModel):
    fn: Optional[str] = None
    args: List[str] = []
    result_var: str


class Command(BaseModel):
    actions: List[Action]
    returns: Optional[Dict[str, ReturnConfig]] = None


# Interpreter class
class CommandInterpreter:
    """Example:
        ```python
        from gr1336_toolbox import (
            compare_texts,
            text_entropy,
            normalize_text,
            Command,
            CommandInterpreter,
        )

        # function map
        function_map = {
            "compare_texts": compare_texts,
            "text_entropy": text_entropy,
            "normalize_text": normalize_text,
        }

    if __name__ == "__main__":
        example_input = {
            "actions": [
                {
                    "item": "normalize_text",
                    "args": ["This is a simple test."],
                    "kwargs": {},
                    "result_var": "normalized_text",
                    "post_processor": None,
                },
                {
                    "item": "text_entropy",
                    "args": [],
                    "kwargs": {"text": "This is a simple test"},
                    "result_var": "text_entropy_value",
                    "post_processor": None,
                },
                {
                    "item": "compare_texts",
                    "args": [],
                    "kwargs": {"text1": "hello world\\nhi there\\nyesterday", "text2": "hello there\\nhi there\\ntoday"},
                    "result_var": "text_comparison",
                    "post_processor": None,
                },
            ],
            "returns": {
                "post_process": {
                    "fn": "lambda x, y: f'Normalized: {x}, Entropy: {y}'",
                    "args": ["normalized_text", "text_entropy_value"],
                    "result_var": "summary",
                }
            },
        }

        interpreter = CommandInterpreter(Command, function_map)
        result_context = interpreter.execute(example_input)
        print(result_context)

        # Results printout:
        result_context = {
            "normalized_text": {"success": True, "result": "this is a simple test."},
            "text_entropy_value": {"success": True, "result": 3.08232813685843},
            "text_comparison": {
                "success": True,
                "result": ["- hello world", "+ hello there", "- yesterday", "+ today"],
            },
            "summary": {
                "success": True,
                "result": "Normalized: this is a simple test., Entropy: 3.08232813685843",
            },
        }
        ```
    """
    def __init__(self, validation_model: BaseModel, function_map: Dict[str, Callable]):
        assert (
            pydantic_available
        ), "Please install pydantic [pip3 install pydantic] to be able to use CommandInterpreter"
        self.validation_model = validation_model
        self.function_map = function_map
        self.context = {}

    def execute_action(self, action: Action):
        func = self.function_map.get(action.item)
        if not func:
            raise ValueError(f"Function {action.item} not found in function map.")

        # Execute function safely
        result = safe_execute(func, *action.args, **action.kwargs)
        self.context[action.result_var] = result

        # Handle post-processing if specified
        if action.post_processor and result["success"]:
            post_processor = eval(action.post_processor, {}, self.context)
            self.context[action.result_var] = {
                "success": True,
                "result": post_processor,
            }

    def execute(self, json_input: Union[dict, str, bytes]):
        try:
            if isinstance(json_input, (str, bytes)):
                json_input = json.loads(json_input)
            parsed_data = self.validation_model(**json_input)
        except Exception as e:
            return {"success": False, "error": str(e)}

        # Execute actions
        for action in parsed_data.actions:
            self.execute_action(action)

        # Handle return configurations
        if parsed_data.returns:
            for key, return_config in parsed_data.returns.items():
                return_fn = (
                    eval(return_config.fn, {}, self.context)
                    if return_config.fn
                    else None
                )
                args = [self.context[arg]["result"] for arg in return_config.args]
                self.context[return_config.result_var] = {
                    "success": True,
                    "result": return_fn(*args) if return_fn else args,
                }

        return self.context
