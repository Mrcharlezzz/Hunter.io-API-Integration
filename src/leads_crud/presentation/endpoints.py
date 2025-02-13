import inject
from application.service import Service
from domain.repositories import ILeadCRUD
from fastapi import FastAPI, Path
from infraestructure.hunter.hunter import HunterLeadCrud
from mappers import EndpointMapper
from serializers import LeadInput, LeadOutput


# Configure dependency injection
def configure_injection(binder):
    binder.bind(ILeadCRUD, to=HunterLeadCrud())

# Initialize injection
inject.configure(configure_injection)


app = FastAPI(
    title="Hunter.io API Integration",
    description="API service for email discovery and verification using Hunter.io",
    version="1.0.0",
    docs_url="/docs",  # Custom docs URL
)

@app.post("/leads",
    response_model=LeadOutput,
    description = "Create new lead",
)
def create(input : LeadInput) -> LeadOutput:
    lead = EndpointMapper.to_entity(input)
    service = Service()
    outlead = service.create(lead)
    output = EndpointMapper.to_client(outlead)
    return output

@app.get("/leads/{id}",
    response_model=LeadOutput,
    description = "Retrieve lead by id",
)
def retrieve(
    id:int = Path(
    title="lead id",
    gt=0
    ),
) -> LeadOutput:

    service = Service()
    outlead = service.retrieve(id)
    output = EndpointMapper.to_client(outlead)
    return output

@app.put(
    "/leads/{id}",
    description = "Modify specified fields of a lead",
)
def update(
    input:LeadInput,
    id:int = Path(
        title="lead id",
        gt=0
    ),
):
    lead = EndpointMapper.to_entity(input)
    service = Service()
    service.update(id=id, lead=lead)
    return

@app.delete(
    "/leads/{id}",
    description = "Delete a lead",
)
def delete(
    id:int = Path(
        title="lead id",
        gt=0
    ),
):
    service = Service()
    service.update(id=id)
    return



