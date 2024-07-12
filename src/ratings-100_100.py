import dspy
import sys
import os
import traceback
from pydantic import BaseModel, Field
from dspy import InputField, OutputField, TypedChainOfThought
from dotenv import load_dotenv

from schwartz import ValueInformation, RubricInformation, schwartz_values, large_rubric

from utils import load_lyrics
from config import ModelConfig

# Create output class for answers
# The model will try to output a JSON object with the 
# following constraints
class OutputScore(BaseModel):
    score: int = Field(
        ge=-100,
        le=100,
        description="An integer in the interval [-100, 100]. Refer to the score rubric"
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
    the given value is according to the lyrics. Multiple values of 5
    is a sign that something is off.
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


class LyricText(BaseModel):
    mxm_id: int
    lyrics: str


#
# Start of script
#

load_dotenv()

lyrics = load_lyrics(os.getenv('LYRICS_PATH_IDS'), os.getenv('LYRICS_PATH_FULL'))
header = [
    "mxm_id", "achievement", "hedonism", "power", "self-direction",
    "stimulation", "security", "conformity", "tradition", "benevolence", "universalism"
]

score_generator = TypedChainOfThought(GenerateScore)

model = sys.argv[1]
config = {
    "model_name": model,
    "instance_description": 'ratings-100_100',
    "container_name": 'ollama',
    "results_header": {
        "": header,
        "weighted": header
    }
}

lm = dspy.OllamaLocal(model=config['model_name'])
dspy.settings.configure(lm=lm)


mconfig = ModelConfig(**config)
mconfig.add_outfile("weighted")

for l in lyrics:
    lyi = LyricText(**l)

    mconfig.logger.info(f"Evaluation for lyrics: \n{lyi.lyrics}")

    outs = []
    scores = []
    confidence_scores = []

    for val in schwartz_values.values:
        mconfig.logger.info(f"Assesing {val.value}...")
        try:
            result = score_generator(
                value=val,
                lyrics=lyi.lyrics,
                score_rubric=large_rubric
            )

            outs.append(result.output)
            scores.append(result.output.score)
            confidence_scores.append(result.output.score * result.output.confidence)
            mconfig.logger.info(f"Finished assesing {val.value}: {result.output.score} (confidence: {result.output.confidence})")
            mconfig.logger.debug(f"Feedback: {result.output.feedback}")
        except Exception:
            mconfig.logger.error(traceback.format_exc())
        finally:
            with open(os.devnull, "w") as sys.stdout:
                mconfig.logger.debug(f"Prompt: {lm.inspect_history(n=1)}")

    mconfig.write([lyi.mxm_id] + scores)
    mconfig.write([lyi.mxm_id] + confidence_scores, addition="weighted")
