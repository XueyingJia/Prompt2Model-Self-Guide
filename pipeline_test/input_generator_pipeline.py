"""Test Input Generator."""

from prompt2model.dataset_generator.prompt_based import Example
from prompt2model.input_generator import PromptBasedInputGenerator
from prompt2model.prompt_parser import MockPromptSpec, TaskType

generated_examples = [
    Example(
        input_col="Question: What is the capital city of Fran?", output_col="Paris"
    ),
    Example(
        input_col="Question: When was the American Declaration of Independence signed?",
        output_col="July 4, 1776",
    ),
    Example(
        input_col="Question: The tallest mountain in the world?",
        output_col="Mount Everest",
    ),
    Example(
        input_col="Question: How many planets are there in our solar system?",
        output_col="8",
    ),
    Example(
        input_col="Question: Who was the first President of the United States?",
        output_col="George Washington",
    ),
]

prompt_spec = MockPromptSpec(
    task_type=TaskType.TEXT_GENERATION,
    instruction="Your task is to generate an answer to a natural question. In this task, the input is a string that consists of both a question and a context passage. The context is a descriptive passage related to the question and contains the answer. And the question can range from Math, Cultural, Social, Geometry, Biology, History, Sports, Technology, Science, and so on.",  # # noqa E501
    examples="""
input="Question: What city did Super Bowl 50 take place in? Context: Super Bowl 50 was an American football game to determine the champion of the National Football League (NFL) for the 2015 season. The American Football Conference (AFC) champion Denver Broncos defeated the National Football Conference (NFC) champion Carolina Panthers 24–10 to earn their third Super Bowl title. The game was played on February 7, 2016, at Levi's Stadium in the San Francisco Bay Area at Santa Clara, California. As this was the 50th Super Bowl, the league emphasized the "golden anniversary" with various gold-themed initiatives, as well as temporarily suspending the tradition of naming each Super Bowl game with Roman numerals (under which the game would have been known as "Super Bowl L"), so that the logo could prominently feature the Arabic numerals 50."
output="Santa Clara"

input="Question: What river runs through Warsaw? Context: Warsaw (Polish: Warszawa [varˈʂava] ( listen); see also other names) is the capital and largest city of Poland. It stands on the Vistula River in east-central Poland, roughly 260 kilometres (160 mi) from the Baltic Sea and 300 kilometres (190 mi) from the Carpathian Mountains. Its population is estimated at 1.740 million residents within a greater metropolitan area of 2.666 million residents, which makes Warsaw the 9th most-populous capital city in the European Union. The city limits cover 516.9 square kilometres (199.6 sq mi), while the metropolitan area covers 6,100.43 square kilometres (2,355.39 sq mi)."
output="Vistula River"

input="Question: The Ottoman empire controlled territory on three continents, Africa, Asia and which other? Context: The Ottoman Empire was an imperial state that lasted from 1299 to 1923. During the 16th and 17th centuries, in particular at the height of its power under the reign of Suleiman the Magnificent, the Ottoman Empire was a powerful multinational, multilingual empire controlling much of Southeast Europe, Western Asia, the Caucasus, North Africa, and the Horn of Africa. At the beginning of the 17th century the empire contained 32 provinces and numerous vassal states. Some of these were later absorbed into the empire, while others were granted various types of autonomy during the course of centuries."
output="Europe"
""",  # noqa E501
)

input_generator = PromptBasedInputGenerator()

prompt = input_generator.construct_prompt(
    instruction=prompt_spec.instruction,
    few_shot_example_string=prompt_spec.examples,
    generated_examples=generated_examples,
    context_cutoff=3500,
)

inputs = input_generator.generate_inputs(
    generated_examples=generated_examples,
    prompt_spec=prompt_spec,
    inputs_num=12,
    hyperparameter_choices={},
)