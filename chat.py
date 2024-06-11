import dspy
from pydantic import BaseModel
from dspy import InputField, OutputField, ChainOfThought

lm = dspy.OllamaLocal(model='llama3')
dspy.settings.configure(lm=lm)


class GenerateScore(dspy.Signature):
    """Using the Scwhartz Theory of basic Human Values, give a score from 1-5 according to the rubric,
      based on how important the value ACHIEVEMENT is according to the lyrics."""
    #value: str = InputField(desc="the specific value to be rated in the lyrics")
    #value_description: str = InputField(desc="a description of the specific value to be rated")
    lyrics: str = InputField(desc="lyrics to be rated")
    score_rubric: str = InputField(desc="a rubric to be used for assigning scores to lyrics for each value")
    #feedback: str = OutputField(
    #    desc="Write a detailed feedback that assesses the quality of the response strictly based on the given score "
    #         "rubric, not evaluating in general. Include specific examples for points of improvement if the scores is "
    #         "not 5.")
    score: int = OutputField(desc="an integer between 1 and 5. refer to the score rubric")


score_generator = ChainOfThought(GenerateScore)


class RubricInformation(BaseModel):
    rubric: str


#class ValueInformation(BaseModel):
#    value: str
#    value_description: str


#class SchwartzValues(BaseModel):
#    list(ValueInformation)


class LyricText(BaseModel):
    mxm_id: int
    lyrics: str


rubric = RubricInformation(rubric="""
Score 5: The value is of the highest importance to the speaker of the lyrics. 
Score 4: The value is important to the speaker of the lyrics.  
Score 3: The value is somewhat important to the speaker of the lyrics. 
Score 2: The value is unimportant to the speaker of the lyrics. 
Score 1: The value is irrelevant to the speaker of the lyrics. 
""")

#ACHIEVEMENT = ValueInformation(value="achievement",
#                               value_description="success, capability, ambition")

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

score = score_generator(  #value=ACHIEVEMENT.value,
    #value_description=ACHIEVEMENT.value_description,
    lyrics=test_lyrics.lyrics,
    score_rubric=rubric.rubric)

print(score)
