from abc import ABC, abstractmethod

import inject

from leads_crud.domain.repositories import ILeadCRUD


class BaseLeadService(ABC):
    repo_instance: ILeadCRUD

    def __init__(self):
        self.repo_instance = inject.instance(ILeadCRUD)

    @abstractmethod
    async def execute(self,*args,**kwargs):
        pass
