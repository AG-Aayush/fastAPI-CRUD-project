from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Note, User
from app.schemas import NoteCreate, UserCreate
from app.auth import hash_password

async def create_user(db: AsyncSession, user: UserCreate):
    db_user = User(
        username = user.username,
        email=user.email,
        password= hash_password(user.password)

    )

    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def get_user_by_email(db: AsyncSession, email:str):
    result= await db.execute(
        select(User).where(User.email == email)
    )
    return result.scalar_one_or_none()

async def create_note(db: AsyncSession, note:NoteCreate):
    db_note = Note(
        title = note.title,
        content = note.content
    )

    db.add(db_note)
    await db.commit()
    await db.refresh(db_note)
    return db_note

async def get_notes(db: AsyncSession):
    result = await db.execute(select(Note))
    return result.scalars().all()

async def get_note(db: AsyncSession, note_id: int):
    result = await db.execute(
        select(Note).where(Note.id == note_id)
    )

    return result.scalar_one_or_none()

async def update_note(db: AsyncSession, note_id: int, data:NoteCreate):
    note = await get_note(db, note_id)

    if not note:
        return None
    
    note.title = data.title
    note.content = data.content

    await db.commit()
    await db.refresh(note)

    return note

async def delete_note(db: AsyncSession, note_id: int):
    note = await get_note(db, note_id)


    if not note:
        return None
    
    await db.delete(note)
    await db.commit()

    return note