from typing import Any, Dict

from domain.lead import Lead


class HunterMapper:
    def to_api(lead:Lead) -> Dict[str,Any]:
        return lead.model_dump()

    def to_entity(lead_info : Dict[str,Any]) -> Lead:
        lead = Lead(
            id=lead_info["id"],
            email=lead_info["email"],
            first_name=lead_info["first_name"],
            last_name=lead_info["last_name"],
            position=lead_info["position"],
            company=lead_info["company"],
        )
        return lead
