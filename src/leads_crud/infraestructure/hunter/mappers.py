from typing import Any, Dict

from domain.lead import Lead
from fastapi import HTTPException


class HunterMapper:
    def to_api(lead:Lead) -> Dict[str,Any]:
        result = {}

        if lead.email is not None:
            result["email"] = lead.email
        if lead.first_name is not None:
            result["first_name"] = lead.first_name
        if lead.last_name is not None:
            result["last_name"] = lead.last_name
        if lead.position is not None:
            result["position"] = lead.position
        if lead.company is not None:
            result["company"] = lead.company

        if(result=={}):
            raise HTTPException(
                status_code=400,
                detail="Invalid data provided. Empty payload."
            )
        return result

    def to_entity(lead_info : Dict[str,Any]) -> Lead:
        data=lead_info["data"]
        lead = Lead(
            id=data["id"],
            email=data["email"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            position=data["position"],
            company=data["company"],
        )
        return lead
