import inject
from fastapi import FastAPI, Path

from src.leads_crud.application.service import Service
from src.leads_crud.domain.repositories import ILeadCRUD
from src.leads_crud.infraestructure.hunter.hunter import HunterLeadCrud
from src.leads_crud.presentation.mappers import EndpointMapper
from src.leads_crud.presentation.serializers import LeadInput, LeadOutput


# Configure dependency injection
def configure_injection(binder):
    binder.bind(ILeadCRUD, HunterLeadCrud())

# Initialize injection
inject.configure(configure_injection)


app = FastAPI(
    title="Lead API Integration",
    description="API service for email discovery and verification",
    version="1.0.0",
    docs_url="/docs",  # Custom docs URL
)

@app.post("/leads",
    response_model=LeadOutput,
    description = "Create new lead",
)
async def create(input : LeadInput) -> LeadOutput:
    lead = EndpointMapper.to_entity(input)
    service = Service()
    outlead =  await service.create(lead)
    output = EndpointMapper.to_client(outlead)
    return output

@app.get("/leads/{id}",
    response_model=LeadOutput,
    description = "Retrieve lead by id",
)
async def retrieve(
    id:int = Path(
    title="lead id",
    gt=0
    ),
) -> LeadOutput:

    service = Service()
    outlead = await service.retrieve(id)
    output = EndpointMapper.to_client(outlead)
    return output

@app.put(
    "/leads/{id}",
    description = "Modify specified fields of a lead",
    status_code= 204
)
async def update(
    input:LeadInput,
    id:int = Path(
        title="lead id",
        gt=0
    ),
):
    lead = EndpointMapper.to_entity(input)
    service = Service()
    await service.update(id=id, lead=lead)
    return

@app.delete(
    "/leads/{id}",
    description = "Delete a lead",
    status_code=204
)
async def delete(
    id:int = Path(
        title="lead id",
        gt=0
    ),
):
    service = Service()
    await service.delete(id=id)
    return



