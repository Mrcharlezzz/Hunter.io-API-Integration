import httpx
from decouple import config
from fastapi import Body, FastAPI, HTTPException, Path
from pydantic import BaseModel

BASE_URL = "https://api.hunter.io/v2"

app = FastAPI(
    title="Hunter.io API Integration",
    description="API service for email discovery and verification using Hunter.io",
    version="1.0.0",
    docs_url="/docs",  # Custom docs URL
)

class Lead(BaseModel):
    email : str
    first_name: str
    last_name: str
    position: str
    company: str

def validated_response(response : httpx.Response):
    if not response.is_success:
        raise HTTPException(
            status_code=response.status_code,
            detail= response.json()
        )

    return response.json()

def parse_lead(lead:Lead):
    data = lead.model_dump()
    return data


@app.post("/leads",
    description = "Create new lead",
)

def create_lead(
    lead : Lead= Body(
        title="Fields of the lead",
        example={
            "email": "alexis@reddit.com",
            "first_name": "Alexis",
            "last_name": "Ohanian",
            "position": "Cofounder",
            "company": "Reddit",
        }
    )
):
    response = httpx.post(
        BASE_URL+"/leads",
        parse_lead(lead),
        headers={"X-API-KEY" : config("API_KEY")}
    )
    return validated_response(response)


@app.get(
    "/leads/{id}" ,
    description="Retrieves all the fields of a lead"
)
def retrieve_lead(
    id:int = Path(
        title="lead id",
        gt=0
    )
):
    response = httpx.get(
        BASE_URL+"/leads/"+str(id),
        headers={"X-API-KEY" : config("API_KEY")}
    )
    return validated_response(response)


@app.put(
    "/leads/{id}",
    description = "Modify specified fields of a lead"
)
def update_lead(
    id:int = Path(
        title="lead id",
        gt=0
    ),
    lead : Lead= Body(
        title="Fields of the lead to be modified",
        example={
            "email": "alexis@reddit.com",
            "first_name": "Alexis",
            "last_name": "Ohanian",
            "position": "Cofounder",
            "company": "Reddit",
        }
    )
):
    response = httpx.put(
        BASE_URL+"/leads/"+str(id),
        parse_lead(lead),
        headers={"X-API-KEY" : config("API_KEY")}
    )
    return validated_response(response)


@app.delete(
    "/leads/{id}",
    description = "Modify specified fields of a lead"
)
def delete_lead(
    id:int = Path(
        title="lead id",
        gt=0
    ),
):
    response = httpx.delete(
        BASE_URL+"/leads/"+str(id),
        headers={"X-API-KEY" : config("API_KEY")}
    )
    return validated_response(response)









