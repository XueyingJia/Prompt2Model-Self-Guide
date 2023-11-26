"""Test Input Generator."""

import json
from pathlib import Path

from prompt2model.input_generator import VLLMPromptBasedInputGenerator
from prompt2model.prompt_parser import MockPromptSpec, TaskType

# 测试

input_generator = VLLMPromptBasedInputGenerator(gpu_memory_utilization=0.9)


# TODO change task name
task_name = "121"
file_path = "/home/cyzhao/main/NI_tasks/tasks.json"
with open(file_path, "r", encoding="utf-8") as json_file:
    all_tasks = json.load(json_file)
choosen_task = None
for task in all_tasks:
    if task["task_name"] == "task" + task_name:
        task_tuple = (
            task["task_name"],
            task["task_instruction"],
            task["examples"],
            task["expected_content"],
            f"/home/cyzhao/prompt2model_test/testdataset/NI/eval/task{task_name}",
            f"/home/cyzhao/prompt2model_test/testdataset/NI/test/task{task_name}",
            task.get("optional_list", []),
            task.get("metric", "exact_match"),
        )
        choosen_task = task
        break

prompt_spec = MockPromptSpec(
    task_type=TaskType.TEXT_GENERATION,
    instruction=choosen_task["task_instruction"],  # # noqa E501
    examples=choosen_task["examples"],  # noqa E501
)

inputs = input_generator.batch_generation_inputs(
    prompt_spec,
    5,
    10,
    dict(
        top_k=40,
        temperature=0.6,
        min_input_length=50,
    ),
    expected_content=choosen_task["expected_content"],
    optional_list=choosen_task["optional_list"],
)

inputs
