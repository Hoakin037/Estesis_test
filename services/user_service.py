from db.models import Users
from db.user_rep import UserBase, UserCreate
from core import Settings
f
class UserService():
    def __init__(self, db: AsyncSession, rep: UserRepository, settings: Settings):
        self.db = db
        self.rep = rep
        self.settings = settings
