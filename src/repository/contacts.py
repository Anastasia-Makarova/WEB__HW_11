from datetime import timedelta, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.entity.models import Contact
from src.schemas.contact import ContactSchema


async def get_contacts(limit: int, offset: int, db: AsyncSession):
    stmt = select(Contact).offset(offset).limit(limit)
    contacts = await db.execute(stmt)
    return contacts.scalars().all()

async def search_contact_by_name(contact_name: str, db: AsyncSession):
    stmt = select(Contact).filter_by(name=contact_name)
    contact = await db.execute(stmt)
    return contact.scalars().all()


async def search_contact_by_surname(contact_surname: str, db: AsyncSession):
    stmt = select(Contact).filter_by(surname=contact_surname)
    contact = await db.execute(stmt)
    return contact.scalars().all()


async def search_contact_by_email(contact_email: str, db: AsyncSession):
    stmt = select(Contact).filter_by(email=contact_email)
    contact = await db.execute(stmt)
    return contact.scalar_one_or_none()


async def get_contact_by_birthday(n:int, db: AsyncSession):
    start = datetime.now()
    seven_days_later = start+ timedelta(days=n)
    contacts_with_bdays = []

    stmt = select(Contact).where(Contact.birthday != None)
    contacts = await db.execute(stmt)
    contacts = contacts.scalars().all()
    
    for contact in contacts:
        bday_this_year = datetime(year=start.year, month=contact.birthday.month, day=contact.birthday.day)

        if bday_this_year >= start and bday_this_year <= seven_days_later:
            contacts_with_bdays.append(contact)

    return contacts_with_bdays


async def get_contact(contact_id:int, db: AsyncSession):
    stmt = select(Contact).filter_by(id=contact_id)
    contact = await db.execute(stmt)
    return contact.scalar_one_or_none()


async def create_contact(body: ContactSchema, db: AsyncSession):
    contact = Contact(**body.model_dump(exclude_unset=True))
    db.add(contact)
    await db.commit()
    await db.refresh(contact)
    return contact



async def update_contact(contact_id: int, body: ContactSchema, db: AsyncSession):
    stmt = select(Contact).filter_by(id=contact_id)
    result = await db.execute(stmt)
    contact = result.scalar_one_or_none()
    if contact:
        contact.name = body.name
        contact.surname = body.surname
        contact.phone_number = body.phone_number
        contact.email = body.email
        contact.birthday = body.birthday
        contact.notes = body.notes
        await db.commit()
        await db.refresh()
    return contact
    


async def delete_contact(contact_id:int, db: AsyncSession):
    stmt = select(Contact).filter_by(id=contact_id)
    contact = await db.execute(stmt)
    contact = contact.scalar_one_or_none()
    if contact:
        await db.delete(contact)
        await db.commit()
    return contact



  
