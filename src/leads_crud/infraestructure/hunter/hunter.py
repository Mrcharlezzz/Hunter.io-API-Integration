import httpx
from decouple import config
from fastapi import HTTPException

from src.leads_crud.domain.lead import Lead
from src.leads_crud.domain.repositories import ILeadCRUD
from src.leads_crud.infraestructure.hunter.mappers import HunterMapper

BASE_URL = config("BASE_URL")
header = {"X-API-KEY": config("API_KEY")}

client = httpx.AsyncClient()

async def validated_response(response : httpx.Response):
    if not response.is_success:
        error_details = await response.json()
        raise HTTPException(
            status_code=response.status_code,
            detail= error_details['errors'][0]['details']
        )

    data = await response.json()
    return data

class HunterLeadCrud(ILeadCRUD):
    async def create(self,lead:Lead) -> Lead:
        payload = HunterMapper.to_api(lead)
        if("email" not in payload):
            raise HTTPException(
                status_code=400,
                detail="required field 'email' missing"
            )
        response = await client.post(
            BASE_URL+"/leads",
            json = HunterMapper.to_api(lead),
            headers=header
        )
        response = await validated_response(response)
        return HunterMapper.to_entity(response)

    async def retrieve(self,id) -> Lead:
        response = await client.get(
            BASE_URL+"/leads/"+str(id),
            headers=header,
        )
        response = await validated_response(response)
        return HunterMapper.to_entity(response)

    async def update(self, id, lead):
        response = await client.put(
            BASE_URL+"/leads/"+str(id),
            json = HunterMapper.to_api(lead),
            headers=header
        )
        response = await validated_response(response)

    async def delete(self, id):
        response = await client.delete(
            BASE_URL+"/leads/"+str(id),
            headers=header,
        )
        response = await validated_response(response)
        print(response)

