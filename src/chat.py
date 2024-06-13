import dspy
import sys
import os
import traceback
import csv
from pydantic import BaseModel, Field
from dspy import InputField, OutputField, TypedChainOfThought
from dotenv import load_dotenv

from schwartz import ValueInformation, RubricInformation, schwartz_values, rubric

from config import setup_logging, load_lyrics

load_dotenv()
logger = setup_logging(os.getenv('LOG_DIR'))

lyrics = load_lyrics(os.getenv('LYRICS_PATH_IDS'), os.getenv('LYRICS_PATH_FULL'))

lm = dspy.OllamaLocal(model='llama3')
dspy.settings.configure(lm=lm)

# Create output class for answers
# The model will try to output a JSON object with the 
# following constraints
class OutputScore(BaseModel):
    score: int = Field(
        ge=1,
        le=5,
        description="An integer between 1 and 5. Refer to the score rubric"
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
    integer from 1-5, according to the rubric, based on how important
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

    for val in schwartz_values.values:
        logger.info(f"Assesing {val.value}...")
        try:
            result = score_generator(
                value=val,
                lyrics=lyi.lyrics,
                score_rubric=rubric
            )

            outs.append(result.output)
            scores.append(result.output.score)
            logger.info(f"Finished assesing {val.value}: {result.output.score} (confidence: {result.output.confidence})")
            logger.debug(f"Feedback: {result.output.feedback}")
        except Exception:
            logger.error(traceback.format_exc())
        finally:
            with open(os.devnull, "w") as sys.stdout:
                logger.debug(f"Prompt: {lm.inspect_history(n=1)}")

    with open(os.path.join(os.getenv('RESULTS_DIR'), "ratings.csv"), 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([lyi.mxm_id] + scores)
