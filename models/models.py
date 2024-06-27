from datetime import datetime

from sqlalchemy import MetaData, Table, Column, Integer, String, Boolean, TIMESTAMP

metadata = MetaData()


users = Table(
    'users',
    metadata,
    Column('id',Integer, primary_key=True, autoincrement=True),
    Column('name', String),
    Column('password', String),
    Column('email', String),
    Column('user_photos', String, default="You have not profile photo yet !",),
    Column('joined_at', TIMESTAMP, default=datetime.utcnow()),
    Column('is_admin', Boolean, default=True)
)


