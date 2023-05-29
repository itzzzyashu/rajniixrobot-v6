import traceback

from RajniiRobot.modules.sql import BASE, SESSION

from sqlalchemy.sql.sqltypes import BigInteger
from sqlalchemy import Column, String


class SuperUsers(BASE):
    __tablename__ = "royals"

    user_id = Column(BigInteger, primary_key=True)
    role_name = Column(String(255))

    def __init__(self, user_id, role):
        self.user_id = user_id
        self.role_name = role

    def __repr__(self):
        return f"<superuser {self.user_id} with role {self.role_name}>"


SuperUsers.__table__.create(checkfirst=True)


def is_superuser(user_id: int, role: str = None):
    with SESSION() as local_session:
        if role:
            return bool(local_session.query(SuperUsers).get((user_id, role)))
        return bool(local_session.query(SuperUsers).get(user_id))


def get_superuser_role(user_id: int):
    with SESSION() as local_session:
        ret = local_session.query(SuperUsers).get({"user_id": user_id})
        if ret:
            return ret.role_name
    return None


def get_superusers(role: str = None):
    with SESSION() as local_session:
        if not role:
            return local_session.query(SuperUsers).all()
        return local_session.query(SuperUsers).filter(
            SuperUsers.role_name == role).all()


def set_superuser_role(user_id: int, role: str):
    with SESSION() as local_session:
        try:
            # Check if the user exists first and create them if they don't.
            ret = local_session.query(SuperUsers).get({"user_id": user_id})
            if not ret:
                ret = SuperUsers(user_id, role)
                local_session.add(ret)
            else:
                ret.role_name = role
            local_session.commit()
            local_session.flush()
        except Exception:
            traceback.print_exc()
            local_session.rollback()


def remove_superuser(user_id: int):
    with SESSION() as local_session:
        try:
            ret = local_session.query(SuperUsers).get({"user_id": user_id})
            if ret:
                local_session.delete(ret)
            local_session.commit()
        except Exception:
            traceback.print_exc()
            local_session.rollback()
