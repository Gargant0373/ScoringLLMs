import dspy
from pydantic import BaseModel
from dspy import InputField, OutputField, TypedChainOfThought

from schwartz import ValueInformation, RubricInformation, schwartz_values, rubric

lm = dspy.OllamaLocal(model='llama3')
dspy.settings.configure(lm=lm)

class GenerateScore(dspy.Signature):
    """
    Using the Scwhartz Theory of basic Human Values, give a score from 1-5
    according to the rubric, based on how important the given value is
    according to the lyrics.
    Only the final result, an integer between 1-5, must be present after "Score:".
    """

    value: ValueInformation = InputField(
        desc="the specific value to be rated in the lyrics and the description"
             "of this value"
    )

    lyrics: str = InputField(desc="lyrics to be rated")

    score_rubric: RubricInformation = InputField(
        desc="a rubric to be used for assigning scores to lyrics for each value"
    )

    feedback: str = OutputField(
        desc="""
            Write a detailed feedback that assesses the quality of the
            response strictly based on the given score rubric, not
            evaluating in general. Include specific examples and
            reasons for which the score was chosen
            """
    )

    score: int = OutputField(
        desc="an integer between 1 and 5. refer to the score rubric",
        # ge=1,
        # le=5
    )


score_generator = TypedChainOfThought(GenerateScore)

class LyricText(BaseModel):
    mxm_id: int
    lyrics: str


test_lyrics = LyricText(mxm_id=1234,
                        lyrics="""
Well, look what the stork brung
(What?) Little baby devil with the forked tongue
And it's stickin' out, yeah, like a sore thumb
(Bleah) With a forehead that it grew horns from
Still a white jerk
Pullin' up in a Chrysler to the cypher with the vic's, percs and a Bud Light shirt
Lyrical technician, an electrician y'all light work
And I don't gotta play pretend, it's you I make believe
And you know I'm here to stay 'cause me
If I was to ever take a leave, It would be aspirin to break a feve
If I was to ask for Megan Thee Stallion if she would collab with me
Would I really have a shot at a feat? (Ha!)
I don't know, but I'm glad to be back, like
""")

score = score_generator(
    value=schwartz_values.get_value("power"),
    lyrics=test_lyrics.lyrics,
    score_rubric=rubric)

print(score.score)
# print(score.feedback)
