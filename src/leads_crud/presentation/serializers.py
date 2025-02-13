from pydantic import BaseModel, Field


class LeadInput(BaseModel):
    """
    Represents input data for a lead in the API.
    Allows partial information about a potential business contact.
    """
    email: str = Field(
        default=None,
        description="Email address of the lead",
    )
    first_name: str = Field(
        default=None,
        description="First name of the lead",
    )
    last_name: str = Field(
        default=None,
        description="Last name of the lead",
    )
    position: str = Field(
        default=None,
        description="Job position of the lead",
    )
    company: str = Field(
        default=None,
        description="Company where the lead works",
    )


class LeadOutput(BaseModel):
    """
    Represents the full lead information returned by the API.
    Includes all input fields plus additional metadata.
    """
    id: str = Field(
        description="Unique identifier for the lead",
    )
    email: str = Field(
        description="Email address of the lead",
    )
    first_name: str = Field(
        description="First name of the lead",
    )
    last_name: str = Field(
        description="Last name of the lead",
    )
    position: str = Field(
        description="Job position of the lead",
    )
    company: str = Field(
        description="Company where the lead works",
    )
    datetime: str = Field(
        default=None,
        description="Timestamp of lead creation",
    )
