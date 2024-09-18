import dspy
import sys
import os
import traceback
from pydantic import BaseModel, Field
from dspy import InputField, OutputField, TypedChainOfThought
from dotenv import load_dotenv

from schwartz import schwartz_values, SchwartzValues

from utils import load_lyrics
from config import ModelConfig


# Create output class for answers
# The model will try to output a JSON object with the
# following constraints
class OutputScore(BaseModel):
    score: list[str] = Field(
        description="""
                List of the 10 Schwartz values ranked by how important they are
                according to the lyrics.
                """
    )
    # confidence: float = Field(
    #     ge=0.,
    #     le=1.,
    #     description="The confidence for the score, as a float from 0. to 1."
    # )
    # feedback: str = Field(
    #    description="""
    #        Write a detailed feedback that assesses the quality of the
    #        response strictly based on the given ranking, not
    #        evaluating in general. Include specific examples and
    #        reasons for which the score was chosen
    #    """
    # )


# Main DSPY singature
# Specifies what values are passed as inputs and what is
# expected as output
class GenerateScore(dspy.Signature):
    """
    Using the Scwhartz Theory of basic Human Values, rank all the values
    in the order of how important they are according to the lyrics.
    After "Output:" nothing should follow except the required JSON object.
    Your response should contain nothing besides the JSON object.
    """

    values: SchwartzValues = InputField()

    lyrics: str = InputField(desc="lyrics to be rated")

    output: OutputScore = OutputField()


score_generator = TypedChainOfThought(GenerateScore)


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
    "instance_description": "rankings",
    "container_name": 'ollama',
    "results_header": {
        "": header,
    }
}

lm = dspy.OllamaLocal(model=config['model_name'])
dspy.settings.configure(lm=lm)


mconfig = ModelConfig(**config)

for l in lyrics:
    lyi = LyricText(**l)

    mconfig.logger.info(f"Evaluation for lyrics: \n{lyi.lyrics}")

    outs = []
    scores = []
    confidence_scores = []

    try:
        result = score_generator(
            values=schwartz_values,
            lyrics=lyi.lyrics,
        )

        outs.append(result.output)
        scores.append(result.output.score)
        mconfig.logger.info(f"Output: {result.output.score}")
    except Exception:
        mconfig.logger.error(traceback.format_exc())
    finally:
        with open(os.devnull, "w") as sys.stdout:
            mconfig.logger.debug(f"Prompt: {lm.inspect_history(n=1)}")

    mconfig.write([lyi.mxm_id] + scores)
