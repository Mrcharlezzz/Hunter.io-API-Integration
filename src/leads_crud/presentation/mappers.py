from datetime import datetime

from domain.lead import Lead
from serializers import ApiInput, ApiOutput


class EndpointMapper:
    def to_entity(input: ApiInput) -> Lead:
        lead = Lead.model_validate(input.model_dump())
        return lead
    def to_client(lead : Lead) -> ApiOutput:
        output = ApiOutput.model_validate(lead.model_dump())
        output.datetime = datetime.now()
        return output
