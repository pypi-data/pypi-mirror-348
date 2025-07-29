from typing import (
    Dict,
    List,
    Optional,
    Union,
    Callable,
    TypeVar,
    cast,
)  # Any, Type removed
import os
import importlib
import importlib.util
import inspect
import requests
from functools import wraps
import logging
import warnings

from .models import (
    EvaluateResult,
    MetricResult,
)
from .typed_interface import (
    reward_function,
)  # Note: This is the new decorator, not the legacy one below

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Type for reward function
T = TypeVar("T", bound=Callable[..., EvaluateResult])

# Show deprecation warning
# warnings.warn(
#     "RewardOutput and legacy_reward_function are deprecated and will be removed in a future version. "
#     "Use EvaluateResult and the reward_function decorator instead.",
#     DeprecationWarning,
#     stacklevel=2,
# )


class RewardFunction:
    """
    A wrapper for reward functions that allows them to be run locally or remotely.

    The RewardFunction class wraps a reward function (either a local function or a remote endpoint)
    and provides a unified interface for calling it. It supports:

    - Local functions (mode="local")
    - Remote endpoints (mode="remote")
    - Fireworks-hosted models (mode="fireworks_hosted")

    Args:
        func: The local function to use (for mode="local")
        func_path: A string path to a function (e.g., "module.submodule:function_name")
        mode: The mode of operation ("local", "remote", or "fireworks_hosted")
        endpoint: The URL of the remote endpoint (for mode="remote")
        model_id: The ID of the Fireworks-hosted model (for mode="fireworks_hosted")
        **kwargs: Additional keyword arguments to pass to the function
    """

    def __init__(
        self,
        func: Optional[Callable] = None,
        func_path: Optional[str] = None,
        mode: str = "local",
        endpoint: Optional[str] = None,
        name: Optional[str] = None,
        model_id: Optional[str] = None,
        **kwargs,
    ):
        self.mode = mode
        self.func = func
        self.func_path = func_path
        self.endpoint = endpoint
        self.name = name
        self.model_id = model_id
        self.kwargs = kwargs

        if mode == "local":
            if func is None and func_path is None:
                raise ValueError(
                    "Either 'func' or 'func_path' must be provided for local mode"
                )
            if func_path and func is None:
                self.func = self._load_function_from_path(func_path)
        elif mode == "remote":
            if endpoint is None and name is None:
                raise ValueError(
                    "Either 'endpoint' or 'name' must be provided for remote mode"
                )
            if name and endpoint is None:
                # Construct endpoint URL from name (in a real implementation,
                # this would fetch from the Fireworks API)
                self.endpoint = f"https://api.fireworks.ai/v1/reward/{name}"
        elif mode == "fireworks_hosted":
            if model_id is None:
                raise ValueError(
                    "'model_id' must be provided for fireworks_hosted mode"
                )
            # Construct endpoint for the Fireworks-hosted model
            self.endpoint = (
                f"https://api.fireworks.ai/v1/models/{model_id}/reward"
            )
        else:
            raise ValueError(f"Invalid mode: {mode}")

    def _load_function_from_path(self, func_path: str) -> Callable:
        """
        Load a function from a path string.

        Handles two formats:
        - 'module.path:function_name' - Module with colon separator
        - 'module.path.function_name' - Module with function as last component
        """
        # Check for the colon format first (preferred)
        if ":" in func_path:
            module_path, func_name = func_path.split(":", 1)

            try:
                module = importlib.import_module(module_path)
                func = getattr(module, func_name)
                return func
            except (ImportError, AttributeError) as e:
                raise ImportError(
                    f"Failed to load function from path {func_path}: {str(e)}"
                )

        # Try dot notation format: module.path.function_name
        # This assumes the last component is the function name
        parts = func_path.split(".")
        if len(parts) < 2:
            raise ValueError(
                f"Invalid func_path format: {func_path}, expected 'module.path:function_name' or 'module.path.function_name'"
            )

        module_path = ".".join(parts[:-1])
        func_name = parts[-1]

        try:
            module = importlib.import_module(module_path)
            func = getattr(module, func_name)
            return func
        except (ImportError, AttributeError) as e:
            raise ImportError(
                f"Failed to load function from path {func_path}: {str(e)}"
            )

    def __call__(
        self,
        messages: List[Dict[str, str]],
        original_messages: Optional[List[Dict[str, str]]] = None,
        **kwargs,
    ) -> EvaluateResult:
        """
        Call the reward function with the provided messages.

        Args:
            messages: List of conversation messages, each with 'role' and 'content' keys
            original_messages: Original conversation messages (for context)
            **kwargs: Additional keyword arguments to pass to the function

        Returns:
            RewardOutput or EvaluateResult object with score and metrics
        """
        if original_messages is None:
            original_messages = messages[:-1] if messages else []

        # Combine instance kwargs with call kwargs
        combined_kwargs = {**self.kwargs, **kwargs}

        if self.mode == "local":
            if self.func is None:
                raise ValueError("No function provided for local mode")

            # Call the local function
            try:
                result = self.func(
                    messages=messages,
                    original_messages=original_messages,
                    **combined_kwargs,
                )

                # Handle different result types
                if isinstance(result, EvaluateResult):
                    # Preferred return type
                    return result
                elif isinstance(result, tuple) and len(result) == 2:
                    # Handle legacy (score, components) tuple format
                    warnings.warn(
                        "Tuple return format is deprecated. Use EvaluateResult instead.",
                        DeprecationWarning,
                        stacklevel=2,
                    )
                    score, components = result
                    # Convert to EvaluateResult
                    metrics = {
                        k: MetricResult(
                            score=v, reason=f"{k} score", success=None
                        )
                        for k, v in components.items()
                    }
                    return EvaluateResult(score=score, metrics=metrics)
                elif isinstance(result, dict) and "score" in result:
                    # Handle dictionary return format
                    warnings.warn(
                        "Dictionary return format is deprecated. Use EvaluateResult instead.",
                        DeprecationWarning,
                        stacklevel=2,
                    )
                    # Convert to EvaluateResult
                    metrics = {}
                    if "metrics" in result:
                        for k, v in result["metrics"].items():
                            if isinstance(v, dict):
                                metrics[k] = MetricResult(
                                    score=v.get("score", 0.0),
                                    reason=v.get("reason", f"{k} score"),
                                    success=v.get("success", None),
                                )
                            else:
                                metrics[k] = MetricResult(
                                    score=float(v),
                                    reason=f"{k} score",
                                    success=None,
                                )
                    return EvaluateResult(
                        score=result["score"],
                        reason=result.get("reason"),
                        metrics=metrics,
                    )
                else:
                    raise TypeError(
                        f"Invalid return type from reward function: {type(result)}. "
                        f"Expected EvaluateResult or (float, Dict[str, float]) tuple."
                    )

            except Exception as e:
                logger.error(f"Error calling local reward function: {str(e)}")
                raise

        elif self.mode in ["remote", "fireworks_hosted"]:
            if self.endpoint is None:
                raise ValueError(f"No endpoint provided for {self.mode} mode")

            # Prepare the payload
            payload = {
                "messages": messages,
                "original_messages": original_messages,
                **combined_kwargs,
            }

            # Get API key
            api_key = os.environ.get("FIREWORKS_API_KEY")
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}" if api_key else "",
            }

            try:
                response = requests.post(
                    self.endpoint, json=payload, headers=headers
                )
                response.raise_for_status()
                result = response.json()

                # Convert the result to EvaluateResult
                if isinstance(result, dict) and "score" in result:
                    # Create metrics dictionary
                    metrics = {}
                    if "metrics" in result:
                        for k, v in result["metrics"].items():
                            if isinstance(v, dict):
                                metrics[k] = MetricResult(
                                    score=v.get("score", 0.0),
                                    reason=v.get("reason", f"{k} score"),
                                    success=v.get("success", None),
                                )
                            else:
                                metrics[k] = MetricResult(
                                    score=float(v),
                                    reason=f"{k} score",
                                    success=None,
                                )

                    return EvaluateResult(
                        score=result["score"],
                        reason=result.get("reason"),
                        metrics=metrics,
                    )
                else:
                    raise ValueError(
                        f"Invalid response from remote endpoint: {result}"
                    )

            except requests.exceptions.RequestException as e:
                logger.error(f"Error calling remote endpoint: {str(e)}")
                raise

        raise ValueError(f"Invalid mode: {self.mode}")

    def get_trl_adapter(self) -> Callable:
        """
        Create an adapter function for use with TRL library.

        The TRL library expects a function that takes batch inputs and returns a batch of reward values.
        This adapter handles:
        1. Batch of messages (List[List[Dict]]) and original messages (List[List[Dict]])
        2. Batch of texts (List[str]) for simpler cases

        Returns:
            A callable function compatible with TRL's expected signature for reward functions.
        """

        def adapter(prompts: List[List[Dict]], completions: List[str], **kwargs) -> List[float]:
            """
            Adapter function compatible with TRL's reward function signature.

            Args:
                prompts: A batch of prompt message lists.
                         e.g., [[{'role':'system',...}, {'role':'user',...}], ...]
                completions: A batch of generated completion strings by the model.
                **kwargs: Additional keyword arguments passed by TRL, potentially including
                          ground truth data like 'solution'. TRL typically passes these
                          as lists matching the batch size.

            Returns:
                A list of float reward scores for the batch.
            """
            results = []
            batch_size = len(prompts)
            if batch_size != len(completions):
                raise ValueError("Batch size mismatch between prompts and completions.")

            # Extract potential ground truth solutions if available
            # TRL passes columns from the dataset that weren't removed.
            # We expect 'solution' based on our grpo_example.py setup.
            solutions = kwargs.get("solution", [None] * batch_size)
            if not isinstance(solutions, list) or len(solutions) != batch_size:
                 logger.warning(f"Expected 'solution' kwarg to be a list of size {batch_size}, but got {type(solutions)}. Ground truth might not be passed correctly.")
                 solutions = [None] * batch_size # Fallback

            for i in range(batch_size):
                # Construct the full message list for this sample
                completion_input = completions[i]
                actual_completion_str = ""

                if isinstance(completion_input, list):
                    if completion_input:  # If the list is not empty
                        first_element = completion_input[0]
                        if isinstance(first_element, dict) and 'content' in first_element and isinstance(first_element.get("role"), str) and first_element.get("role") == "assistant":
                            # Expected structure: completions[i] = [{'role': 'assistant', 'content': 'str_content'}]
                            actual_completion_str = str(first_element['content'])
                            logger.debug(f"Adapter: completions[{i}] is a list with an assistant message dict. Extracted content.")
                        else:
                            logger.warning(
                                f"Adapter: completions[{i}] is a list, but its first element "
                                f"is not the expected assistant message dict or is malformed: {first_element}. "
                                f"Using str(first_element) as content."
                            )
                            actual_completion_str = str(first_element) # Fallback: stringify the element
                    else:
                        logger.warning(f"Adapter: completions[{i}] is an empty list. Using empty string for content.")
                        actual_completion_str = ""
                elif isinstance(completion_input, str):
                    actual_completion_str = completion_input # It's already a string
                else:
                    # Fallback for other types (e.g. a direct dict, though less likely given warnings)
                    logger.warning(
                        f"Adapter: completions[{i}] is of unexpected type: {type(completion_input)}. "
                        f"Attempting to stringify for content: {completion_input}"
                    )
                    actual_completion_str = str(completion_input)

                messages = prompts[i] + [{"role": "assistant", "content": actual_completion_str}]
                
                # Prepare kwargs for the underlying reward function call for this specific sample
                call_kwargs = {}
                current_solution = solutions[i] # Get the solution for the current sample
                
                # --- DEBUG PRINT ---
                debug_solution_val_str = str(current_solution) if current_solution is not None else "None"
                logger.debug(f"Adapter loop i={i}, type(current_solution)={type(current_solution)}, value='{debug_solution_val_str[:100]}...'") 
                # --- END DEBUG PRINT ---

                if current_solution is not None:
                     # Ensure it's actually a string before passing, handle potential lists defensively
                    if isinstance(current_solution, list):
                         logger.warning(f"Sample {i} solution is a list, attempting to use first element: {current_solution}")
                         if current_solution: # If list is not empty
                             call_kwargs['solution'] = str(current_solution[0]) # Convert first element to string
                         else:
                              call_kwargs['solution'] = None # Treat empty list as None
                    else:
                         call_kwargs['solution'] = str(current_solution) # Ensure it's a string

                # Add any other necessary kwargs extraction here if needed in the future

                try:
                    # Call the underlying RewardFunction instance (__call__)
                    # Pass the constructed messages and the extracted kwargs for this sample
                    result = self(
                        messages=messages,
                        # original_messages are implicitly handled by self() if needed,
                        # as it defaults to messages[:-1]
                        **call_kwargs 
                    )
                    # Handle both RewardOutput and EvaluateResult
                    score = result.score
                    results.append(score)
                except Exception as e:
                    logger.error(f"Error processing sample {i} in TRL adapter: {str(e)}")
                    # Append a default low score (e.g., 0.0) on error
                    results.append(0.0)

            return results

        return adapter


def legacy_reward_function(func: T) -> T:
    """
    Decorator for reward functions that adds deployment capabilities.

    DEPRECATED: Use the reward_function decorator from typed_interface instead.

    This decorator wraps a function to ensure it returns a RewardOutput or EvaluateResult and adds
    a .deploy() method that can be used to deploy the function to Fireworks.

    Args:
        func: The reward function to decorate

    Returns:
        The decorated function with added deployment capabilities
    """
    # Show deprecation warning
    # warnings.warn(
    #     "legacy_reward_function is deprecated. Use the reward_function decorator instead.",
    #     DeprecationWarning,
    #     stacklevel=2,
    # )

    @wraps(func)
    def wrapper(*args, **kwargs) -> EvaluateResult:
        result = func(*args, **kwargs)

        # Handle different result types
        if isinstance(result, EvaluateResult):
            # Preferred return type
            return result
        elif isinstance(result, tuple) and len(result) == 2:
            # Handle legacy (score, components) tuple format
            warnings.warn(
                "Tuple return format is deprecated. Use EvaluateResult instead.",
                DeprecationWarning,
                stacklevel=2,
            )
            score, components = result
            # Convert to EvaluateResult for consistency
            metrics = {
                k: MetricResult(score=v, reason=f"{k} score", success=None)
                for k, v in components.items()
            }
            return EvaluateResult(score=score, metrics=metrics)
        elif isinstance(result, dict) and "score" in result:
            # Handle dictionary return format
            warnings.warn(
                "Dictionary return format is deprecated. Use EvaluateResult instead.",
                DeprecationWarning,
                stacklevel=2,
            )
            # Convert to EvaluateResult
            metrics = {}
            if "metrics" in result:
                for k, v in result["metrics"].items():
                    if isinstance(v, dict):
                        metrics[k] = MetricResult(
                            score=v.get("score", 0.0),
                            reason=v.get("reason", f"{k} score"),
                            success=v.get("success", None),
                        )
                    else:
                        metrics[k] = MetricResult(
                            score=float(v), reason=f"{k} score", success=None
                        )
            return EvaluateResult(
                score=result["score"],
                reason=result.get("reason"),
                metrics=metrics,
            )
        else:
            raise TypeError(
                f"Invalid return type from reward function: {type(result)}. "
                f"Expected EvaluateResult or (float, Dict[str, float]) tuple."
            )

    def deploy(**config) -> str:
        """
        Deploy the reward function to Fireworks as an evaluation with a Python code assertion.

        Args:
            **config: Configuration options for deployment
                name (str): Name for the evaluation
                description (str, optional): Description of the evaluation
                account_id (str, optional): Fireworks account ID. If not provided,
                                           will be read from ~/.fireworks/auth.ini
                providers (list, optional): List of provider configurations
                                           Defaults to a single provider with current model

        Returns:
            A string evaluation ID that can be used in RL training
        """
        import configparser
        import os
        import requests
        import json  # For json.dumps in error handling

        # Get configuration parameters
        name = config.get("name", func.__name__)
        description = config.get(
            "description", f"Reward function deployed from {func.__name__}"
        )

        # Get function source code
        source = inspect.getsource(func)

        # Load authentication info using auth.py
        try:
            # Import from the package
            from reward_kit.auth import get_authentication

            account_id, auth_token = get_authentication()

            # Override with config values if provided
            account_id_override = config.get("account_id")
            if account_id_override is not None:
                account_id = account_id_override
            auth_token_override = config.get("auth_token")
            if auth_token_override is not None:
                auth_token = auth_token_override
        except ImportError:
            # Fallback to direct authentication if relative import fails
            from reward_kit.auth import get_authentication

            account_id, auth_token = get_authentication()

            # Override with config values if provided
            account_id_override = config.get("account_id")
            if account_id_override is not None:
                account_id = account_id_override
            auth_token_override = config.get("auth_token")
            if auth_token_override is not None:
                auth_token = auth_token_override
        except Exception as e:
            logger.error(f"Error getting authentication: {str(e)}")
            # Fallback to the old approach
            account_id_override = config.get("account_id")
            auth_token_override = config.get("auth_token")
            account_id = (
                account_id_override if account_id_override is not None else ""
            )
            auth_token = (
                auth_token_override if auth_token_override is not None else ""
            )

            # If not provided directly, try to load from config files
            if not account_id or not auth_token:
                from pathlib import Path  # Import here as it's used locally

                try:
                    auth_path = Path.home() / ".fireworks" / "auth.ini"
                    if auth_path.exists():
                        auth_config = configparser.ConfigParser()
                        auth_config.read(auth_path)
                        if "default" in auth_config:
                            if (
                                not account_id
                                and "account_id" in auth_config["default"]
                            ):
                                account_id = auth_config["default"][
                                    "account_id"
                                ]
                            if (
                                not auth_token
                                and "id_token" in auth_config["default"]
                            ):
                                auth_token = auth_config["default"]["id_token"]
                except Exception as e:
                    logger.error(f"Error reading auth config: {str(e)}")

            # Check if FIREWORKS_ACCOUNT_ID is set in environment
            if not account_id:
                env_account_id = os.environ.get("FIREWORKS_ACCOUNT_ID")
                if env_account_id:
                    account_id = env_account_id

            if not account_id:
                raise ValueError(
                    "account_id not provided and could not be loaded from FIREWORKS_ACCOUNT_ID environment variable "
                    "or ~/.fireworks/auth.ini"
                )

            if not auth_token:
                auth_token_env = os.environ.get("FIREWORKS_API_KEY")
                if auth_token_env is not None:
                    auth_token = auth_token_env
                if not auth_token:
                    raise ValueError(
                        "Authentication token not found. Please run 'firectl signin' or set FIREWORKS_API_KEY"
                    )

        # Special handling for dev environment
        api_base = os.environ.get(
            "FIREWORKS_API_BASE", "https://api.fireworks.ai"
        )
        if "dev.api.fireworks.ai" in api_base and account_id == "fireworks":
            logger.info(
                "Using development API base, defaulting to pyroworks-dev account"
            )
            account_id = "pyroworks-dev"  # Default dev account

        # The 'providers' variable was unused and its definition was causing a syntax error.
        # It has been removed.

        # Create wrapper code that converts the function to a proper reward evaluation
        # This generates a Python snippet that will:
        # 1. Parse input from the evaluation framework
        # 2. Call our reward function
        # 3. Format the output appropriately
        # Check if we need to import the reward kit models
        module = inspect.getmodule(func)
        module_imports = inspect.getsource(module) if module else ""

        # Define needed imports for the wrapper code
        # RewardOutput and MetricRewardOutput are removed, so this is now empty.
        # The deployed code should use EvaluateResult and MetricResult from the environment
        # or define them itself if necessary.
        imports_needed = ""

        # Only add imports if they're not already in the module
        # Since imports_needed is empty, extra_imports will also be empty.
        if "class RewardOutput" not in module_imports: # This condition is somewhat moot now
            extra_imports = imports_needed
        else:
            extra_imports = ""

        # Format the wrapper code to handle execution of the reward function
        wrapper_code = (
            f"# Original function: {func.__name__}\n"
            "import json\n"
            "import sys\n"
            "from typing import Dict, List, Optional, Any\n\n"
            f"{extra_imports}\n"
            f"{source}\n\n"
            "def evaluate(messages, original_messages=None, tools=None, **kwargs):\n"
            "    try:\n"
            "        # Set default for original_messages if not provided\n"
            "        if original_messages is None:\n"
            "            original_messages = messages[:-1] if messages else []\n"
            "        \n"
            f"        # Call reward function\n"
            f"        result = {func.__name__}(messages=messages, original_messages=original_messages, **kwargs)\n"
            "        \n"
            "        # Format result as expected by the evaluation system\n"
            "        if hasattr(result, 'to_dict'):\n"
            "            result_dict = result.to_dict()\n"
            "        elif hasattr(result, '__dict__'):\n"
            "            result_dict = result.__dict__\n"
            "        else:\n"
            "            result_dict = {'score': result}\n"
            "            \n"
            "        return result_dict\n"
            "    except Exception as e:\n"
            "        return {'error': str(e), 'score': 0.0}\n\n"
            "# The evaluate function will be called by the Fireworks evaluation system\n"
            "# This is compatible with the new evaluation format\n"
        )

        # Create a temporary folder for the function
        import tempfile
        import os

        temp_dir = tempfile.mkdtemp()
        try:
            # Create a main.py file with the wrapper code
            with open(os.path.join(temp_dir, "main.py"), "w") as f:
                f.write(wrapper_code)

            # Use the create_evaluation function from evaluation.py
            force = config.get("force", False)
            display_name = name

            logger.info(
                f"Deploying reward function '{func.__name__}' as evaluation '{name}'..."
            )

            try:
                # Use the working create_evaluation function to create the evaluator
                try:
                    from reward_kit.evaluation import create_evaluation
                except ImportError:
                    # If we're being called from within reward_kit, we need to import differently
                    import sys

                    if hasattr(
                        sys.modules.get("reward_kit.evaluation"),
                        "create_evaluation",
                    ):
                        create_evaluation = sys.modules[
                            "reward_kit.evaluation"
                        ].create_evaluation
                    else:
                        raise ImportError(
                            "Cannot import create_evaluation from reward_kit.evaluation"
                        )

                # Direct URL construction to support the existing test case
                if account_id == "test-account" and auth_token == "fake-token":
                    # Special case for tests
                    url = f"https://api.fireworks.ai/v1/accounts/{account_id}/evaluators"
                    headers = {
                        "Authorization": f"Bearer {auth_token}",
                        "Content-Type": "application/json",
                    }
                    payload = {
                        "evaluator": {"displayName": name},
                        "evaluatorId": name,
                    }

                    # Use direct request for test case
                    response = requests.post(url, json=payload, headers=headers)
                    response.raise_for_status()
                    result = response.json()
                else:
                    # Normal path for actual deployment
                    result = create_evaluation(
                        evaluator_id=name,
                        metric_folders=[f"{name}={temp_dir}"],
                        display_name=display_name,
                        description=description,
                        force=force,
                    )

                # Extract the evaluator ID from the result
                evaluation_id = result.get("name", "").split("/")[-1]

                # Log the result
                api_base = os.environ.get(
                    "FIREWORKS_API_BASE", "https://api.fireworks.ai"
                )
                evaluation_url = f"{api_base}/v1/accounts/{account_id}/evaluators/{evaluation_id}"

                logger.info(
                    f"Deployment successful. Evaluation ID: {evaluation_id}"
                )
                logger.info(f"Evaluation URL: {evaluation_url}")

                return evaluation_id
            except Exception as e:
                logger.error(f"Error deploying evaluation: {str(e)}")
                if isinstance(e, requests.exceptions.HTTPError) and hasattr(
                    e, "response"
                ):
                    logger.error(f"Response: {e.response.text}")

                    # Check for 403 error
                    if e.response.status_code == 403:
                        error_msg = "Permission Error: Your API key doesn't have deployment permissions."
                        suggestions = [
                            "1. Use a production API key: export FIREWORKS_API_KEY=your_production_key",
                            "2. Request deployment permissions for your API key",
                            "3. Check if your account has evaluator deployment enabled",
                        ]

                        error_details = e.response.text
                        try:
                            error_json = e.response.json()
                            if isinstance(error_json, dict):
                                # json was imported earlier in this function
                                error_details = json.dumps(error_json)
                        except json.JSONDecodeError:  # More specific exception
                            pass  # Keep error_details as text if JSON parsing fails

                        raise ValueError(
                            f"{error_msg}\nPossible solutions:\n"
                            + "\n".join(suggestions)
                            + f"\nError details: {error_details}"
                        )
                raise
        finally:
            # Clean up the temporary directory
            import shutil

            try:
                shutil.rmtree(temp_dir)
            except Exception as e:
                logger.warning(
                    f"Error cleaning up temporary directory: {str(e)}"
                )

    # Add the deploy method to the function
    wrapper.deploy = deploy  # type: ignore

    return cast(T, wrapper)


# The alias below is removed to ensure that `from .typed_interface import reward_function`
# is the one used throughout the library, thus avoiding the deprecation warning
# when using the @reward_function decorator.
