import httpx
from decouple import config
from domain.lead import Lead
from domain.repositories import ILeadCRUD
from fastapi import HTTPException
from mappers import HunterMapper

BASE_URL = "https://api.hunter.io/v2"

def headers():
    return config("API_KEY")

def validated_response(response : httpx.Response):
    if not response.is_success:
        raise HTTPException(
            status_code=response.status_code,
            detail= response.json()['details']
        )

    return response.json()

class HunterLeadCrud(ILeadCRUD):
    def create(lead:Lead):
        response = httpx.post(
            BASE_URL+"/leads",
            HunterMapper.to_api(lead),
            headers=headers()
        )
        response = validated_response(response)
        return HunterMapper.to_entity(response)

    def retrieve(id):
        response = httpx.put(
            BASE_URL+"/leads/"+str(id),
            headers=headers(),
        )
        response = validated_response(response)
        return HunterMapper.to_entity(response)

    def update(id, lead):
        response = httpx.post(
            BASE_URL+"/leads/"+str(id),
            HunterMapper.to_api(lead),
            headers=headers()
        )
        response = validated_response(response)

    def delete(id):
        response = httpx.put(
            BASE_URL+"/leads/"+str(id),
            headers=headers(),
        )
        response = validated_response(response)

