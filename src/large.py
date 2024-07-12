import dspy
import sys
import os
import traceback
import csv
import re
from pydantic import BaseModel, Field
from dspy import InputField, OutputField, TypedChainOfThought
from dotenv import load_dotenv

from schwartz import ValueInformation, RubricInformation, schwartz_values, large_rubric

from config import setup_logging, load_lyrics

load_dotenv()
logger = setup_logging(os.getenv('LOG_DIR'))

lyrics = load_lyrics(os.getenv('LYRICS_PATH_IDS'), os.getenv('LYRICS_PATH_FULL'))

lm = dspy.OllamaLocal(model='llama3')
dspy.settings.configure(lm=lm)

header = [
    "mxm_id", "achievement", "hedonism", "power", "self-direction",
    "stimulation", "security", "conformity", "tradition", "benevolence", "universalism"
    ]   

# Append data to a CSV file
def append_to_csv(file_path, data):
    with open(file_path, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data)

# Write the header if the file is empty
def write_header_if_empty(file_path, header):
    if not os.path.isfile(file_path) or os.path.getsize(file_path) == 0:
        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(header)


results_dir = os.getenv('RESULTS_DIR')

# Create the directory if it doesn't exist
os.makedirs(results_dir, exist_ok=True)

pattern = re.compile(r'ratings_large-\d+\.csv')
count = len([name for name in os.listdir(results_dir) if pattern.match(name)])

result_file_path = os.path.join(results_dir, f"ratings_large-{count}.csv")
weighted_file_path = os.path.join(results_dir, f"weighted_large-{count}.csv")

write_header_if_empty(result_file_path, header)
write_header_if_empty(weighted_file_path, header)

# Create output class for answers
# The model will try to output a JSON object with the 
# following constraints
class OutputScore(BaseModel):
    score: int = Field(
        ge=-100,
        le=100,
        description="An integer between -100 and 100. Refer to the score rubric"
    )
    confidence: float = Field(
        ge=0.,
        le=1.,
        description="The confidence for the score, as a float from 0. to 1."
    )
    feedback: str = Field(
        description="""
            Write a detailed feedback that assesses the quality of the
            response strictly based on the given score rubric, not
            evaluating in general. Include specific examples and
            reasons for which the score was chosen
        """
    )

# Main DSPY singature
# Specifies what values are passed as inputs and what is 
# expected as output
class GenerateScore(dspy.Signature):
    """
    Using the Scwhartz Theory of basic Human Values, give a score, an
    integer in the interval [-100, 100], according to the rubric, based on how important
    the given value is according to the lyrics.
    Then, on the scale of 0-1 tell how confident you are about the
    answer.
    Lastly, provide a feedback stating why you chose the score.
    After "Output:" nothing should follow except the required JSON object.
    Your response should contain nothing besides the JSON object.
    """

    value: ValueInformation = InputField()

    lyrics: str = InputField(desc="lyrics to be rated")

    score_rubric: RubricInformation = InputField()

    output: OutputScore = OutputField()


score_generator = TypedChainOfThought(GenerateScore)

class LyricText(BaseModel):
    mxm_id: int
    lyrics: str

for l in lyrics:
    lyi = LyricText(**l)

    logger.info(f"Evaluation for lyrics: \n{lyi.lyrics}")

    outs = []
    scores = []
    confidence_scores = []

    for val in schwartz_values.values:
        logger.info(f"Assesing {val.value}...")
        try:
            result = score_generator(
                value=val,
                lyrics=lyi.lyrics,
                score_rubric=large_rubric
            )

            outs.append(result.output)
            scores.append(result.output.score)
            confidence_scores.append(result.output.score * result.output.confidence)
            logger.info(f"Finished assesing {val.value}: {result.output.score} (confidence: {result.output.confidence})")
            logger.debug(f"Feedback: {result.output.feedback}")
        except Exception:
            logger.error(traceback.format_exc())
        finally:
            with open(os.devnull, "w") as sys.stdout:
                logger.debug(f"Prompt: {lm.inspect_history(n=1)}")

    append_to_csv(result_file_path, [lyi.mxm_id] + scores)
    append_to_csv(weighted_file_path, [lyi.mxm_id] + confidence_scores)
