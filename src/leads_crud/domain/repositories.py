from src.leads_crud.domain.lead import Lead


class ILeadCRUD:
    def create(lead : Lead) -> Lead:
        pass
    def retrieve(id : int) -> Lead:
        pass
    def update(id : int, lead : Lead):
        pass
    def delete(id : int):
        pass
