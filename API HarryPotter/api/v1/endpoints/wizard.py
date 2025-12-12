from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.wizard_models import WizardModel
from schemas.wizard_schemas import WizardSchema
from core.deps import get_session

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=WizardSchema)
async def post_wizard(wizard: WizardSchema, db: AsyncSession = Depends(get_session)):
    novo_wizard = WizardModel(
        nome=wizard.nome,
        casa=wizard.casa,
        varinha=wizard.varinha,
        patrono=wizard.patrono,
        magia_principal=wizard.magia_principal
    )
    db.add(novo_wizard)
    await db.commit()
    return novo_wizard

@router.get("/", response_model=List[WizardSchema])
async def get_wizards(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(WizardModel)
        result = await session.execute(query)
        wizards: List[WizardModel] = result.scalars().all()
        return wizards

@router.get("/{wizard_id}", response_model=WizardSchema, status_code=status.HTTP_200_OK)
async def get_wizard(wizard_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(WizardModel).filter(WizardModel.id == wizard_id)
        result = await session.execute(query)
        wizard = result.scalar_one_or_none()
        if wizard:
            return wizard
        else:
            raise HTTPException(detail="Bruxo não encontrado", status_code=status.HTTP_404_NOT_FOUND)

@router.put("/{wizard_id}", response_model=WizardSchema, status_code=status.HTTP_202_ACCEPTED)
async def put_wizard(wizard_id: int, wizard: WizardSchema, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(WizardModel).filter(WizardModel.id == wizard_id)
        result = await session.execute(query)
        wizard_up = result.scalar_one_or_none()
        if wizard_up:
            wizard_up.nome = wizard.nome
            wizard_up.casa = wizard.casa
            wizard_up.varinha = wizard.varinha
            wizard_up.patrono = wizard.patrono
            wizard_up.magia_principal = wizard.magia_principal
            await session.commit()
            return wizard_up
        else:
            raise HTTPException(detail="Bruxo não encontrado", status_code=status.HTTP_404_NOT_FOUND)

@router.delete("/{wizard_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_wizard(wizard_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(WizardModel).filter(WizardModel.id == wizard_id)
        result = await session.execute(query)
        wizard_del = result.scalar_one_or_none()
        if wizard_del:
            await session.delete(wizard_del)
            await session.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail="Bruxo não encontrado", status_code=status.HTTP_404_NOT_FOUND)
