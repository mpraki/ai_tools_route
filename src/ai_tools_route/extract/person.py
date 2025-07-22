from pydantic import Field, BaseModel


class Person(BaseModel):
    """A class representing a person with basic attributes."""

    name: str = Field(default=None, description="Name of the person")
    age: int = Field(default=None, description="Age of the person")
    gender: str = Field(default=None, description="Gender of the person")


class People(BaseModel):
    """A list of Person objects."""

    people: list[Person] = Field(default_factory=list, description="List of people")
