from pydantic import BaseModel, Field
from typing import List

class RubricInformation(BaseModel):
    rubric: str = Field(description="A rubric to be used for assigning scores to lyrics for each value")

class ValueInformation(BaseModel):
    value: str = Field(description="The specific value to be rated in the lyrics")
    value_description: str = Field(description="The description of the value to be rated")

rubric = RubricInformation(rubric="""
Score 5: The value is of the highest importance to the speaker of the lyrics.
Score 4: The value is important to the speaker of the lyrics.
Score 3: The value is somewhat important to the speaker of the lyrics.
Score 2: The value is unimportant to the speaker of the lyrics.
Score 1: The value is irrelevant to the speaker of the lyrics.
""")

negative_rubric = RubricInformation(rubric="""
Scores are in the [-5, 5] interval.
Score 5: The value is of the highest importance to the speaker of the lyrics.
Score 4: The value is very important to the speaker of the lyrics.
Score 3: The value is important to the speaker of the lyrics.
Score 2: The value is moderately important to the speaker of the lyrics.
Score 1: The value is somewhat important to the speaker of the lyrics.
Score 0: The value is neutral to the speaker of the lyrics.
Score -1: The value is somewhat opposed by the speaker of the lyrics.
Score -2: The value is moderately opposed by the speaker of the lyrics.
Score -3: The value is opposed by the speaker of the lyrics.
Score -4: The value is very opposed by the speaker of the lyrics.
Score -5: The value is completely opposed by the speaker of the lyrics.
""") 

large_rubric = RubricInformation(rubric="""
Scores should be assigned within the [−100,100] range. Use the provided scores as anchor points,
and use intermediate scores to represent intermediate levels of importance or opposition.
Score 100: The value is of the highest importance to the speaker of the lyrics.
Score 50: The value is moderately important to the speaker of the lyrics.
Score 0: The value is neutral to the speaker of the lyrics.
Score -50: The value is moderately opposed by the speaker of the lyrics.
Score -100: The value is completely opposed by the speaker of the lyrics.
""")


# Generate a rubric for a given range
def generateRubric(min, max):
    size = max - min
    rubric = f"""
    Scores should be assigned within the [{min},{max}] range. Use the provided scores as anchor points,
    and use intermediate scores to represent intermediate levels of importance or opposition.
    Please use the whole range.
    Score {max}: The value is of the highest importance to the speaker of the lyrics.
    Score {min}: The value is completely opposed by the speaker of the lyrics.
    """
    return RubricInformation(rubric=rubric)

class SchwartzValues(BaseModel):
    values: List[ValueInformation]

    def get_value(self, name: str):
        for v in self.values:
            if v.value == name:
                return v


schwartz_values = SchwartzValues(values=[
    ValueInformation(
        value="achievement",
        value_description="personal success through demonstrating competence according to social standards"
    ),
    ValueInformation(
        value="hedonism",
        value_description="pleasure or sensuous gratification for oneself"
    ),
    ValueInformation(
        value="power",
        value_description="social status and prestige, control or dominance over people and resources"
    ),
    ValueInformation(
        value="self-direction",
        value_description="independent thought and action—choosing, creating, exploring"
    ),
    ValueInformation(
        value="stimulation",
        value_description="excitement, novelty and challenge in life"
    ),
    ValueInformation(
        value="security",
        value_description="safety, harmony, and stability of society, of relationships, and of self"
    ),
    ValueInformation(
        value="conformity",
        value_description="restraint of actions, inclinations, and impulses likely to upset or harm others and violate social expectations or norms"
    ),
    ValueInformation(
        value="tradition",
        value_description="respect, commitment, and acceptance of the customs and ideas that one's culture or religion provides"
    ),
    ValueInformation(
        value="benevolence",
        value_description="preserving and enhancing the welfare of those with whom one is in frequent personal contact (the 'in-group')"
    ),
    ValueInformation(
        value="universalism",
        value_description="understanding, appreciation, tolerance, and protection for the welfare of all people and for nature"
    ),
    # ValueInformation(
    #     value="spirituality",
    #     value_description=""
    # ),
])
