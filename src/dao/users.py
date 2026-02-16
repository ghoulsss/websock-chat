from src.dao.base import BaseDAO
from src.db.models.users import User


class UsersDAO(BaseDAO):
    model = User
