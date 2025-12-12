from pydantic import BaseModel

class WizardSchema(BaseModel):
    nome: str
    casa: str
    varinha: str
    patrono: str
    magia_principal: str

    class Config:
        orm_mode = True
