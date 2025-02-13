from datetime import datetime

from domain.lead import Lead
from serializers import LeadInput, LeadOutput


class EndpointMapper:
    def to_entity(input: LeadInput) -> Lead:
        lead = Lead.model_validate(input.model_dump())
        return lead
    def to_client(lead : Lead) -> LeadOutput:
        output = LeadOutput.model_validate(lead.model_dump())
        output.datetime = datetime.now()
        return output
