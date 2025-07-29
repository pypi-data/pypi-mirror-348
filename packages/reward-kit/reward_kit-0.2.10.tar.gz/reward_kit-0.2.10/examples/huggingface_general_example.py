"""
Example demonstrating integration with generic HuggingFace datasets for evaluation preview.
"""

import os
import sys
from pathlib import Path

# Ensure reward-kit is in the path
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)

# Check for required environment variables
if not os.environ.get("FIREWORKS_API_KEY"):
    print("Warning: FIREWORKS_API_KEY environment variable is not set.")
    print(
        "Either set this variable or provide an auth_token when calling create_evaluation()."
    )
    print(
        "Example: FIREWORKS_API_KEY=$DEV_FIREWORKS_API_KEY python examples/huggingface_general_example.py"
    )

# Import the evaluation functions
from reward_kit.evaluation import (
    preview_evaluation,
    huggingface_dataset_to_jsonl,
)


def main():
    # Create a simple length-based reward function for demonstration
    print("Setting up a simple reward function for length evaluation...")
    os.makedirs("./temp_metrics/length_metric", exist_ok=True)

    # Create main.py with a simple length-based reward function
    with open("./temp_metrics/length_metric/main.py", "w") as f:
        f.write(
            """
def evaluate(messages, original_messages=None, tools=None, **kwargs):
    # Extract assistant response
    assistant_messages = [m for m in messages if m.get("role") == "assistant"]
    if not assistant_messages:
        return {"score": 0.0, "reasoning": "No assistant messages found"}
    
    # Get the length of the assistant's response
    response_text = assistant_messages[0].get("content", "")
    response_length = len(response_text.split())
    
    # Calculate score based on length (normalize between 0-1)
    # Prefer responses between 50-200 words
    if response_length < 10:
        score = 0.1  # Too short
        reason = f"Response too short ({response_length} words)"
    elif response_length < 50:
        score = 0.1 + (response_length - 10) * 0.02  # Linear increase from 0.1 to 0.9
        reason = f"Response somewhat short ({response_length} words)"
    elif response_length <= 200:
        score = 1.0  # Ideal length
        reason = f"Response ideal length ({response_length} words)"
    elif response_length <= 500:
        score = 1.0 - (response_length - 200) * 0.001  # Gradually decrease
        reason = f"Response somewhat verbose ({response_length} words)"
    else:
        score = 0.7  # Too verbose
        reason = f"Response too verbose ({response_length} words)"
    
    return {
        "score": score,
        "reasoning": reason
    }
"""
        )

    # Try with different HuggingFace datasets
    try:
        # Example 1: Using a summarization dataset
        print("\nPreviewing evaluation with CNN/Daily Mail dataset...")
        preview_result = preview_evaluation(
            metric_folders=["length_metric=./temp_metrics/length_metric"],
            huggingface_dataset="cnn_dailymail",
            huggingface_split="test",
            max_samples=2,
            huggingface_prompt_key="article",
            huggingface_response_key="highlights",
        )
        preview_result.display()

        # Example 2: Using a question-answering dataset
        print("\nPreviewing evaluation with SQuAD dataset...")
        preview_result = preview_evaluation(
            metric_folders=["length_metric=./temp_metrics/length_metric"],
            huggingface_dataset="squad",
            huggingface_split="validation",
            max_samples=2,
            huggingface_prompt_key="question",
            huggingface_response_key="answers",
        )
        preview_result.display()

        # Example 3: Converting custom dataset to JSONL for manual inspection
        print("\nConverting custom dataset to JSONL...")
        jsonl_file = huggingface_dataset_to_jsonl(
            dataset_name="glue",
            split="train",
            max_samples=5,
            prompt_key="sentence",
            response_key="label",  # Note: This will need special handling as it's numeric
        )
        print(f"Dataset converted to JSONL file: {jsonl_file}")

    except ImportError:
        print(
            "Could not load datasets package. Install with: pip install datasets"
        )
    except Exception as e:
        print(f"Error during evaluation: {str(e)}")

    # Clean up temporary files
    import shutil

    shutil.rmtree("./temp_metrics", ignore_errors=True)


if __name__ == "__main__":
    main()
