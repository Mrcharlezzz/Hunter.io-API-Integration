from datetime import datetime
from pydantic import ValidationError
from fastapi import HTTPException

from src.leads_crud.domain.lead import Lead
from src.leads_crud.presentation.serializers import LeadInput, LeadOutput


class EndpointMapper:
    def to_entity(input: LeadInput) -> Lead:
        try:
            lead = Lead.model_validate(input.model_dump())
        except ValidationError:
            raise HTTPException from None(
                status_code=400,
                detail="Invalid request arguments",
            )

        if all(value is None for value in lead.model_dump().values()):
            raise HTTPException(
                status_code=400,
                detail="All fields are None, invalid lead data",
            )

        return lead
    def to_client(lead : Lead) -> LeadOutput:
        output = LeadOutput.model_validate(lead.model_dump())
        time=datetime.now()
        output.datetime = time.strftime("%d/%m/%Y, %H:%M:%S")
        return output
