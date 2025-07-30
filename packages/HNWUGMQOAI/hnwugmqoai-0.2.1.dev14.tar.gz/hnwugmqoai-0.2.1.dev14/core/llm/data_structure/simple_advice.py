from pydantic import BaseModel, Field


class advice(BaseModel):
    content: str


class advices(BaseModel):
    """
    This class is used to store the advice for the user.
    """
    advices: list[advice] = Field(default_factory=list)
