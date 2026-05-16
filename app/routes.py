from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
from app.schemas import NoteCreate, NoteResponse, UserCreate, UserLogin, Token
from app import crud
from app.crud import create_user, get_user_by_email
from app.auth import verify_password, create_access_token, get_current_user
from app.models import User

router = APIRouter(prefix="/notes", tags=["Notes"])
auth_router = APIRouter(prefix="/notes", tags=["Notes"])

@auth_router.post("/register")
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    existing_user = await get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await create_user(db, user)

@auth_router.post("/login", response_model=Token)
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    db_user = await get_user_by_email(db, user.email)
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    access_token = create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/", response_model=NoteResponse)
async def create_note(
    note: NoteCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)   # ← protected
):
    return await crud.create_note(db, note, current_user.id)

@router.get("/", response_model=list[NoteResponse])
async def get_notes(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)   # ← protected
):
    return await crud.get_notes(db, current_user.id)

@router.get("/{note_id}", response_model=NoteResponse)
async def get_note(
    note_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)   # ← protected
):
    note = await crud.get_note(db, note_id, current_user.id)
    if not note:
        raise HTTPException(status_code=404, detail="Note Not Found")
    return note

@router.put("/{note_id}", response_model=NoteResponse)
async def update_note(
    note_id: int,
    data: NoteCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)   # ← protected
):
    note = await crud.update_note(db, note_id, data, current_user.id)
    if not note:
        raise HTTPException(status_code=404, detail="Note Not Found")
    return note

@router.delete("/{note_id}")
async def delete_note(
    note_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)   # ← protected
):
    note = await crud.delete_note(db, note_id, current_user.id)
    if not note:
        raise HTTPException(status_code=404, detail="Note Not Found")
    return {"message": "Deleted Successfully"}