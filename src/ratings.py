import dspy
import random
import sys
import os
import traceback
import argparse
from pydantic import BaseModel, Field
from dspy import InputField, OutputField, Predict
from dotenv import load_dotenv

from schwartz import ValueInformation, RubricInformation, schwartz_values, generateRubric

from utils import load_lyrics, load_sample
from config import ModelConfig


parser = argparse.ArgumentParser(description="Start rating lyrics.")

# Positional argument
parser.add_argument("model", type=str, help="Model name (mandatory)")

# Optional flags with default values
parser.add_argument("--min", type=int, default=0, help="Minimum value (default: 0)")
parser.add_argument("--max", type=int, default=10, help="Maximum value (default: 10)")

# Mandatory flag (input file)
parser.add_argument("-i", "--input-file", type=str, required=True, help="Path to input file (mandatory)")

parser.add_argument("-t", "--type", type=str, default="lyrics", help="Type of input file (default: lyrics)")

args = parser.parse_args()


# Create output class for answers
# The model will try to output a JSON object with the 
# following constraints
class OutputScore(BaseModel):
    feedback: str = Field(
        description=
        """Write a (max 30 word) analysis that explains how the given value is (or is not) reflected in the text sample. 
            Include specific examples and
            reasons for which the score was chosen.
        """
    )
    score: int = Field(
        ge=args.min,
        le=args.max,
        description="An integer. Refer to the score rubric"
    )
    confidence: float = Field(
        ge=0.,
        le=1.,
        description="The confidence for the score you gave. 0 means complete uncertainty about how the given value is reflected in the sample. 1 means complete certainty."
    )

# Main DSPY singature
# Specifies what values are passed as inputs and what is 
# expected as output
class GenerateScore(dspy.Signature):
    """
    Using the Schwartz Theory of basic Human values, provide an analysis of the text sample.
    Then, give a score, an
    integer between a minimum and maximum value, according to the rubric, based on how important
    the given value is according to the sample.
    Then, tell how confident you are about the
    answer.
    """

    value: ValueInformation = InputField()

    sample: str = InputField(desc="sample to be rated")

    score_rubric: RubricInformation = InputField()

    output: OutputScore = OutputField()


class SampleModel(BaseModel):
    id: int
    sample: str


#
# Start of script
#

def main():
    load_dotenv()

    samples = load_sample(args.input_file)
    header = [
        "id", "achievement", "hedonism", "power", "self-direction",
        "stimulation", "security", "conformity", "tradition", "benevolence", "universalism",
        "achievement_confidence", "hedonism_confidence", "power_confidence", "self-direction_confidence",
        "stimulation_confidence", "security_confidence", "conformity_confidence", "tradition_confidence",
        "benevolence_confidence", "universalism_confidence"
    ]

    score_generator = Predict(GenerateScore)

    model = args.model
    config = {
        "model_name": model,
        "instance_description": f"ratings-{args.type}-{args.min}_{args.max}",
        "container_name": 'ollama',
        "results_header": {
            "": header,
        },
        "temperature": 0.8 + 0.1 * random.uniform(-1, 1)
    }
    lm = dspy.LM(f'ollama_chat/{config['model_name']}', api_base='http://localhost:11434', api_key='', cache=False, temperature=config['temperature'])
    dspy.settings.configure(lm=lm)


    mconfig = ModelConfig(**config)
    mconfig.logger.info(f"Config: {mconfig.__dict__}")

    for s in samples:
        se = SampleModel(id=s.id, sample=s.sample)

        mconfig.logger.info(f"Evaluating the following sample: \n<<\n{se.sample}\n>>")

        outs = []
        scores = []
        confidence_scores = []

        for val in schwartz_values.values:
            mconfig.logger.info(f"Assesing {val.value}...")
            try:
                result = score_generator(
                    value=val,
                    sample=se.sample,
                    score_rubric=generateRubric(args.min, args.max)
                )

                outs.append(result.output)
                scores.append(result.output.score)
                confidence_scores.append(result.output.confidence)
                mconfig.logger.info(f"Finished assesing {val.value}: {result.output.score} (confidence: {result.output.confidence})")
                mconfig.logger.debug(f"Feedback: {result.output.feedback}")
            except Exception:
                mconfig.logger.error(traceback.format_exc())
            finally:
                with open(os.devnull, "w") as sys.stdout:
                    mconfig.logger.debug(f"Prompt: {lm.history[-1]['messages']}")

        mconfig.write([se.id] + scores + confidence_scores)


if __name__ == "__main__":
    main()
