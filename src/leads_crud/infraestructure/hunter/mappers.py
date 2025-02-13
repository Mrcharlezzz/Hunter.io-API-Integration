from typing import Any, Dict

from domain.lead import Lead


class HunterMapper:
    def to_api(lead:Lead) -> Dict[str,Any]:
        return lead.model_dump()

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
