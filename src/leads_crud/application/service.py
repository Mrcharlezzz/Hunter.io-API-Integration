from src.base_lead_crud.service import BaseLeadService
from src.leads_crud.domain.lead import Lead


class CreateLeadService(BaseLeadService):
    def __init__(self):
        super().__init__()

    async def execute(self, lead: Lead) -> Lead:
        return await self.repo_instance.create(lead)


class RetrieveLeadService(BaseLeadService):
    def __init__(self):
        super().__init__()

    async def execute(self, id: int) -> Lead:
        return await self.repo_instance.retrieve(id)


class UpdateLeadService(BaseLeadService):
    def __init__(self):
        super().__init__()

    async def execute(self, id: int, lead: Lead):
        await self.repo_instance.update(id, lead)


class DeleteLeadService(BaseLeadService):
    def __init__(self):
        super().__init__()

    async def execute(self, id: int):
        await self.repo_instance.delete(id)

