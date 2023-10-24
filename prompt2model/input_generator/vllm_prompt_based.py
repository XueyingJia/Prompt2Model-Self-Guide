"""Input Generator based on Prompts."""

import random
import re
from typing import Any

from vllm import LLM, SamplingParams

from prompt2model.dataset_generator.prompt_based import Example
from prompt2model.input_generator import InputGenerator
from prompt2model.input_generator.prompt_template import construct_meta_prompt
from prompt2model.prompt_parser import PromptSpec
from prompt2model.utils import count_tokens_from_string, get_formatted_logger

logger = get_formatted_logger("InputGenerator")


class VLLMPromptBasedInputGenerator(InputGenerator):
    """Generate inputs from prompts."""

    def __init__(
        self,
        pretrained_model_name: str = "lmsys/vicuna-7b-v1.5",
    ) -> None:
        """Create a new instance of the HFPromptBasedInputGenerator.

        Args:
            pretrained_model_name: The name of a pre-trained decoder-only model.
        """
        if pretrained_model_name == "lmsys/vicuna-7b-v1.5":
            self.language_model = LLM(
                model="/data/ckpts/huggingface/models/models--lmsys--vicuna-7b-v1.5/snapshots/de56c35b1763eaae20f4d60efd64af0a9091ebe5"
            )
        else:
            self.language_model = LLM(model=pretrained_model_name)

    def construct_prompt(
        self,
        instruction: str,
        few_shot_example_string: str,
        generated_examples: list[Example],
        context_cutoff: int,
    ) -> str:
        """Generates a prompt string.

        Args:
            instruction: The natural language instruction for the prompt.
            few_shot_example_string: A string representing the few-shot examples
                parsed from the user's prompt, which quality is higher than the
                generated examples.
            generated_examples: A list of currently generated examples.
            context_cutoff: If the total length of the prompt in tokens exceeds this
                value, repeat the prompt generation process to generate a shorter one.

        Returns:
            The generated prompt string.
        """
        while True:
            # Choose a few inputs to add to the prompt if examples exist.
            if len(generated_examples) == 0:
                low_quality_input_string = "N/A\n"
                random_selected_generated_example_num = 0
            else:
                low_quality_input_string = ""
                random_selected_generated_example_num = random.randint(
                    1, min(len(generated_examples), 10)
                )
                random_examples = random.sample(
                    generated_examples, random_selected_generated_example_num
                )
                for example in random_examples:
                    low_quality_input_string += f'[input]="{example.input_col}"\n'

            # Extract inputs from the few-shot examples.
            high_quality_inputs = re.findall(r'input="(.*?)"', few_shot_example_string)
            if len(high_quality_inputs) == 0:
                high_quality_input_string = "N/A\n"
            else:
                high_quality_input_string = ""
                for input in high_quality_inputs:
                    high_quality_input_string += f'[input]="{input}"\n'

            # Construct the prompt.
            prompt = construct_meta_prompt(
                instruction=instruction,
                low_quality_input_string=low_quality_input_string,
                high_quality_input_string=high_quality_input_string,
            )
            if count_tokens_from_string(prompt) < context_cutoff:
                return prompt
            else:
                orginal_input_string = (
                    instruction + few_shot_example_string
                    if few_shot_example_string
                    else instruction
                )
                if count_tokens_from_string(orginal_input_string) > context_cutoff:
                    logger.warning(
                        "The original input prompt is too long. "
                        "Consider writing a shorter prompt."
                    )
                continue

    def generate_inputs(
        self,
        generated_examples: list[Example],
        prompt_spec: PromptSpec,
        inputs_num: int,
        hyperparameter_choices: dict[str, Any],
    ) -> list[str]:
        """Generate new inputs for a given prompt with a pre-trained model.

        Args:
            generated_examples: A list of currently generated examples.
            prompt_spec: A prompt we use to generate new inputs.
            inputs_num: The number of new inputs to generate.
            hyperparameter_choices: A dictionary of hyperparameter choices.
        """
        sampling_params = SamplingParams(
            top_k=hyperparameter_choices.get("top_k", 50),
            temperature=hyperparameter_choices.get("temperature", 0.7),
        )
        prompts = [
            self.construct_prompt(
                instruction=prompt_spec.instruction,
                few_shot_example_string=prompt_spec.examples,
                generated_examples=generated_examples,
                context_cutoff=hyperparameter_choices.get("context_cutoff", 3500),
            )
            for _ in range(inputs_num)
        ]
        outputs = self.language_model.generate(prompts, sampling_params)
        generated_inputs = [each.outputs[0].text for each in outputs]
        return generated_inputs