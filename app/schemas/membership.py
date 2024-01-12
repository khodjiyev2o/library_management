from pydantic import BaseModel
from app.models.models import UserMembership


class UserMembershipBase(BaseModel):
    status: UserMembership.MembershipStatus


class UserMembershipCreate(UserMembershipBase):
    pass


class UserMembershipUpdate(UserMembershipBase):
    pass


class UserMembershipResponse(UserMembershipBase):
    id: int
    user_id: int
