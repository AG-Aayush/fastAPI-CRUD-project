from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
from app.schemas import NoteCreate, NoteResponse
from app import crud

router = APIRouter(prefix="/notes", tags=['Notes'])

@router.post('/', response_model=NoteResponse)
async def create_note(note: NoteCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_note(db, note)


@router.get('/', response_model=list[NoteResponse])
async def get_notes(db: AsyncSession = Depends(get_db)):
    return await crud.get_notes(db)

@router.get("/{note_id}", response_model=NoteResponse)
async def get_note(note_id: int, db: AsyncSession = Depends(get_db)):
    note = await crud.get_note(db, note_id)

    if not note:
        raise HTTPException(status_code=404, detail="Note Not Found")
    
    return note

@router.put("/{note_id}", response_model = NoteResponse)
async def update_note(note_id: int, data: NoteCreate, db: AsyncSession = Depends(get_db)):
    note = await crud.update_note(db, note_id, data)

    if not note:
        raise HTTPException(status_code=404, detail="Note Not Found")
    
    return note


@router.delete("/{note_id}")
async def delete_note(note_id: int, db: AsyncSession = Depends(get_db)):
    note= await crud.delete_note(db, note_id)

    if not note:
        raise HTTPException(status_code=404, detail="Note Not Found")
    
    return {"message": "Deleted Successfully"}