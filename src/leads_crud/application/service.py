import inject
from domain.lead import Lead
from domain.repositories import ILeadCRUD


class Service:
    repo_instance: ILeadCRUD

    def __init__(self):
        self.repo_instance = inject.instance(ILeadCRUD)

    async def create(self,lead: Lead) -> Lead:
        return await self.repo_instance.create(lead)
    async def retrieve(self, id:int) -> Lead:
        return await self.repo_instance.retrieve(id)
    async def update(self, id:int , lead:Lead):
        await self.repo_instance.retrieve(id,lead)
    async def delete(self, id:int):
        await self.repo_instance.delete(id)

