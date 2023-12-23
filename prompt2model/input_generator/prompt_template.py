"""Utilities to construct an LLM "metaprompt" for our dataset generator."""

INPUT_PROMPT_TEMPLATE = """
As an InputGenerator, your task is to generate a new [input] based on the [instruction] and some example [input].

Try your best to ensure that the new [input] you generate is distinct from the provided [input] while maintaining a diverse, detailed, precise, comprehensive, and high-quality response.

Avoid generating a new [input] that is the same as the provided [input].
--------------------------------------------------------------------------------------------
[instruction]

{instruction}
--------------------------------------------------------------------------------------------
Here are some high-quality [input] for the [instruction]. These [input] can provide you with very strict format requirements. You should pay extreme attention to them!!!

Some high-quality [input]:

{high_quality_input_string}
--------------------------------------------------------------------------------------------
These are some addtional [input]. Their formats and contents may not be accurate. However, you may also refer to the content of them.

Some low-quality [input]:

{low_quality_input_string}
--------------------------------------------------------------------------------------------
Afters seeing example inputs, generate a new [input]. Before generating the new [input], ensure that you strictly adhere to the rules of the new [instruction] and follow the format of high-quality [input].

Prioritize the new [instruction] guidelines to maintain consistency and quality.

Think twice before generating a new [input]. Only response the new [input] without any other information.

[input]=
"""

INPUT_FILTER_TEMPLATE = """
A chat between a curious user and an artificial intelligence assistant.
The assistant gives concise answers to the user's questions.
USER:  [task description]: {instruction} The artificial intelligence assistant adjusts the provided [input] to meet the [expected output]. The assistant's main goal is to extract {expected_content} from the [input] and then polish these extracted contents for the response. Instead of strictly following the [task description] to execute the task and provide an explanation, the focus is on pinpointing and improving the extracted contents from the [input].
ASSISTANT: Okay. I will focus on pinpointing and improving the extracted contents from the [input]. I won't execute the task or provide an explanation.
{extraction_example_string}
USER: [input] = {new_input} [expected output] = {label}
ASSISTANT: 
"""  # noqa E501

INPUT_FILTER_TEMPLATE_199 = """
A chat between a curious user and an artificial intelligence assistant.
The assistant gives concise answers to the user's questions.
USER: The task is: {instruction} The artificial intelligence assistant adjusts the provided [input] to meet the [expected output]. The assistant's main goal is to extract {expected_content} from the [input] and then polish these extracted contents for the response. Instead of strictly following the original task instructions, the focus is on pinpointing and improving extracted contents from the [input].
ASSISTANT: Okay. I will focus on pinpointing and improving extracted contents from the [input].
USER: [input] = "Sentence 1: Next to the MGM Grand you will find M and M World. Sentence 2: The candy has many fans who love its attractions." [expected output] = no
ASSISTANT: Sentence 1: Next to the MGM Grand you will find M and M World. Sentence 2: The candy has many fans who love its attractions.
USER: [input] = "Sentence 1: I've forgotten his name now, confessed Tuppence. Sentence 2: Tuppence remembered his name later." [expected output] = no
ASSISTANT: Sentence 1: I've forgotten his name now, confessed Tuppence. Sentence 2: Tuppence remembered his name later.
USER: [input] = "Sentence 1: One of the first organizational realignments taking place is in the Office of the Taxpayer Advocate. Sentence 2: The office of the taxpayer advocate is having an organizational realignment." [expected output] = yes
ASSISTANT: Sentence 1: One of the first organizational realignments taking place is in the Office of the Taxpayer Advocate. Sentence 2: The office of the taxpayer advocate is having an organizational realignment.
USER: [input] = "Sentence 1: yeah I tell you what though if you go price some of those tennis shoes i can see why now you know they're getting up in the hundred dollar range. Sentence 2: The tennis shoes have only one price." [expected output] = yes
ASSISTANT: Sentence 1: yeah I tell you what though if you go price some of those tennis shoes i can see why now you know they're getting up in the hundred dollar range. Sentence 2: The tennis shoes have only one price.
USER: [input] = {new_input} [expected output] = {label}
ASSISTANT: 
"""  # noqa E501

INPUT_FILTER_TEMPLATE_OLD = """
### [EXAMPLE]

{few_shot_examples}

### [NEW INPUT]

{new_input}

### [YOUR TASK]

Extract {expected_content} from [NEW INPUT] similar to the [EXAMPLE] and output as your response.

### [YOUR RESPONSE]

"""  # noqa E501


CONDITIOANL_INPUT_PROMPT_TEMPLATE = """
As an InputGenerator, your task is to generate a new [input] based on the [instruction] and some example [input].

Try your best to ensure that the new [input] you generate is distinct from the provided [input] while maintaining a diverse, detailed, precise, comprehensive, and high-quality response.

Avoid generating a new [input] that is the same as the provided [input].
--------------------------------------------------------------------------------------------
[instruction]

{instruction}
--------------------------------------------------------------------------------------------
Here are some high-quality [input] for the [instruction]. These [input] can provide you with very strict format requirements. You should pay extreme attention to them!!!

Some high-quality [input]:

{high_quality_input_string}
--------------------------------------------------------------------------------------------
These are some addtional [input]. Their formats and contents may not be accurate. However, you may also refer to the content of them.

Some low-quality [input]:

{low_quality_input_string}
--------------------------------------------------------------------------------------------
Afters seeing example inputs, generate a new [input] for which the expected [output] is {conditional_label}. Before generating the new [input], ensure that you strictly adhere to the rules of the new [instruction] and follow the format of high-quality [input].

Prioritize the new [instruction] guidelines to maintain consistency and quality.

Think twice before generating a new [input]. Only response the new [input] without any other information. Note that the expected [output] for the new [input] should be {conditional_label}.

[input]=
"""


def construct_verify_prompt(
    examples: str,
    new_input: str,
    expected_content: str,
    label: str,
    instruction: str,
    extraction_example_string
):
    prompt = INPUT_FILTER_TEMPLATE.format(
        few_shot_examples=examples,
        new_input=new_input,
        expected_content=expected_content,
        label = label,
        instruction = instruction,
        extraction_example_string=extraction_example_string,
    )
    print(prompt)
    return prompt


def construct_meta_prompt(
    instruction: str = None,
    low_quality_input_string: str = None,
    high_quality_input_string: str = None,
) -> str:
    """Constructs a prompt template for the dataset generator.

    Args:
        instruction: The natural language instruction for the prompt.
        low_quality_input_string: A string representing the low quality examples.
        high_quality_input_string: A string representing the high quality examples.

    Returns:
        str: A prompt template, where the `instruction` and `examples` fields
            are filled in.
    """
    return INPUT_PROMPT_TEMPLATE.format(
        instruction=instruction,
        high_quality_input_string=high_quality_input_string,
        low_quality_input_string=low_quality_input_string,
    )


def construct_conditional_generation_prompt(
    instruction: str = None,
    low_quality_input_string: str = None,
    high_quality_input_string: str = None,
    conditional_label: str = None,
) -> str:
    """Constructs a prompt template for the dataset generator.

    Args:
        instruction: The natural language instruction for the prompt.
        low_quality_input_string: A string representing the low quality examples.
        high_quality_input_string: A string representing the high quality examples.
        conditional_label: The expected output for the new input. Used for
            classification tasks.

    Returns:
        str: A prompt template, where the `instruction` and `examples` fields
            are filled in.
    """
    assert conditional_label is not None and conditional_label != ""
    return CONDITIOANL_INPUT_PROMPT_TEMPLATE.format(
        instruction=instruction,
        high_quality_input_string=high_quality_input_string,
        low_quality_input_string=low_quality_input_string,
        conditional_label=conditional_label,
    )
