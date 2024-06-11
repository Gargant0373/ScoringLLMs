import dspy
from pydantic import BaseModel, Field
from dspy import InputField, OutputField, TypedChainOfThought

from schwartz import ValueInformation, RubricInformation, schwartz_values, rubric

lm = dspy.OllamaLocal(model='llama3')
dspy.settings.configure(lm=lm)

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


class GenerateScore(dspy.Signature):
    """
    Using the Scwhartz Theory of basic Human Values, give a score, an 
    integer from 1-5, according to the rubric, based on how important 
    the given value is according to the lyrics.
    Then, on the scale of 0-1 tell how confident you are about the
    answer.
    Lastly, provide a feedback stating why you chose the score.
    """

    value: ValueInformation = InputField()

    lyrics: str = InputField(desc="lyrics to be rated")

    score_rubric: RubricInformation = InputField()

    output: OutputScore = OutputField()


score_generator = TypedChainOfThought(GenerateScore)

class LyricText(BaseModel):
    mxm_id: int
    lyrics: str


test_lyrics = LyricText(mxm_id=1234,
                        lyrics="""
Welcome to the jungle, we got fun and games
We got everything you want, honey, we know the names
We are the people that can find whatever you may need
If you got the money, honey, we got your disease
In the jungle, welcome to the jungle
Watch it bring you to your shun-n-n-n-n-n-n-n-n-n-n-n, knees, knees
Mwah, ah, I wanna watch you bleed
Welcome to the jungle, we take it day by day
If you want it you're going to bleed, but it's the price you pay
And you're a very sexy girl, who's very hard to please
You can taste the bright lights, but you won't get them for free
In the jungle, welcome to the jungle
Feel my, my, my, my serpentine
Oh, ah, I wanna hear you scream
""")

result = score_generator(
    value=schwartz_values.get_value("tradition"),
    lyrics=test_lyrics.lyrics,
    score_rubric=rubric
)

print(f"Score: {result.output.score} (confidence: {result.output.confidence})")
print(result.output.feedback)
