import httpx
from decouple import config
from domain.lead import Lead
from domain.repositories import ILeadCRUD
from fastapi import HTTPException
from mappers import HunterMapper

BASE_URL = config("BASE_URL")
header = config("API_KEY")

client = httpx.AsyncClient()


def validated_response(response : httpx.Response):
    if not response.is_success:
        raise HTTPException(
            status_code=response.status_code,
            detail= response.json()['details']
        )

    return response.json()

class HunterLeadCrud(ILeadCRUD):
    async def create(lead:Lead):
        response = await client.post(
            BASE_URL+"/leads",
            HunterMapper.to_api(lead),
            headers=header
        )
        response = validated_response(response)
        return HunterMapper.to_entity(response)

    async def retrieve(id):
        response = await client.put(
            BASE_URL+"/leads/"+str(id),
            headers=header,
        )
        response = validated_response(response)
        return HunterMapper.to_entity(response)

    async def update(id, lead):
        response = await client.post(
            BASE_URL+"/leads/"+str(id),
            HunterMapper.to_api(lead),
            headers=header
        )
        response = validated_response(response)

    async def delete(id):
        response = await client.put(
            BASE_URL+"/leads/"+str(id),
            headers=header,
        )
        response = validated_response(response)

