from fastapi import FastAPI, APIRouter, Depends, status
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete
from typing import List

from passlib.context import CryptContext
from scheme import *
from utilities import *
from database import *
from models.models import users
app = FastAPI(title='Task', version='1.0.0')

pwd_contex = CryptContext(schemes=['bcrypt'], deprecated='auto')

router = APIRouter()


@router.post('/registration')
async def register(
        user_data: UserRegistration,
        session: AsyncSession = Depends(get_async_session)
    ):
    if user_data.password1 == user_data.password2:
        email_exists = await session.execute(select(users).where(users.c.email == user_data.email))
        email_exists_value = email_exists.scalar()

        if email_exists_value is not None:
            return {'success': False, 'message': 'Email already exists!'}

        hash_password = pwd_contex.hash(user_data.password1)
        user_in_db = UserDatabase(**dict(user_data), password=hash_password)
        query = insert(users).values(**dict(user_in_db))
        await session.execute(query)
        await session.commit()
        return {'success': True, 'message': 'Account created successfully'}
    else:
        raise HTTPException(status_code=400, detail='Passwords are not the same !')


@router.post('/login')
async def login(
        user_d: LoginUser,
        session: AsyncSession = Depends(get_async_session)
    ):
    query = select(users).where(users.c.email == user_d.email)
    userdata = await session.execute(query)
    user_data = userdata.one_or_none()
    if user_data is None:
        return {'success': False, 'message': 'Email or Password is not correct !'}
    else:
        if pwd_contex.verify(user_d.password, user_data.password):
            token = generate_token(user_data.id)
            return token
        else:
            return {'success': False, 'message': 'Email or Password is not correct!'}


@router.patch('/edit-profile')
async def edit_profile(
        photo: UploadFile = None,
        email: str = None,
        name: str = None,
        session: AsyncSession = Depends(get_async_session),
        token: dict = Depends(verify_token)
):
    if token is None:
        raise HTTPException(status_code=403, detail='Forbidden')

    try:
        user_id = token.get('user_id')
        query = select(users).where(users.c.id == user_id)
        result = await session.execute(query)
        user_data = result.scalar_one_or_none()

        update_values = {}

        if photo is not None:
            out_file = f'user_photos/{photo.filename}'
            async with aiofiles.open(out_file, 'wb') as f:
                content = await photo.read()
                await f.write(content)
            update_values['user_photos'] = out_file

        if email is not None:
            update_values['email'] = email

        if name is not None:
            update_values['name'] = name

        if update_values:
            query = update(users).where(users.c.id == user_data).values(**update_values)
            await session.execute(query)
            await session.commit()

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {'success': True, 'message': 'Profile updated successfully!'}


@router.get('/get_user_info', response_model=List[UserInfo])
async def get_user_info(
        session: AsyncSession = Depends(get_async_session),
        token: dict = Depends(verify_token)
):
    user_id = token.get('user_id')
    res = await session.execute(
        select(users).where(
            (users.c.id == user_id)
        )
    )
    if not res.scalar():
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED)
    result = await session.execute(select(users).where(users.c.id == user_id))
    return result.fetchall()


@router.delete('/delete-profile')
async def delete_profile(
    session: AsyncSession = Depends(get_async_session),
    token: dict = Depends(verify_token)
):
    if token is None:
        raise HTTPException(status_code=403, detail='Forbidden')

    try:
        user_id = token.get('user_id')
        if not user_id:
            raise HTTPException(status_code=400, detail='Invalid token')

        query = select(users).where(users.c.id == user_id)
        result = await session.execute(query)
        user_data = result.scalar_one_or_none()

        if user_data is None:
            raise HTTPException(status_code=404, detail='User not found')

        delete_query = delete(users).where(users.c.id == user_data)
        await session.execute(delete_query)
        await session.commit()

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {'success': True, 'message': 'Profile deleted successfully'}


@router.get('/all_users_info', response_model=List[AllUserInfo])
async def get_users(
        session: AsyncSession = Depends(get_async_session),
        token: dict = Depends(verify_token)
):
    print('token', token)
    user_id = token.get('user_id')
    admin = await session.execute(
        select(users).where(
            (users.c.id == user_id) &
            (users.c.is_admin==True)
        )
    )
    print(user_id)
    if not admin.scalar():
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED)
    result = await session.execute(select(users))
    return result.fetchall()


@router.delete('/delete_user_for_admin')
async def delete_user_for_admin(
        delete_user_id: int,
    session: AsyncSession = Depends(get_async_session),
    token: dict = Depends(verify_token)
):
    if token is None:
        raise HTTPException(status_code=403, detail='Forbidden')

    try:
        user_id = token.get('user_id')
        admin = await session.execute(
            select(users).where(
                (users.c.id == user_id) &
                (users.c.is_admin == True)
            )
        )
        if admin.scalar():
            if not user_id:
                raise HTTPException(status_code=400, detail='Invalid token')

            query = select(users).where(users.c.id == delete_user_id)
            result = await session.execute(query)
            user_data = result.scalar_one_or_none()


            if user_data is None:
                raise HTTPException(status_code=404, detail='User not found')

            delete_query = delete(users).where(users.c.id == delete_user_id)
            await session.execute(delete_query)
            await session.commit()
        else:
            raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {'success': True, 'message': 'User deleted successfully'}

app.include_router(router)
