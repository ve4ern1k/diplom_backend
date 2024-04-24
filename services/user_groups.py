from typing import List
from database import UserGroupLink
from sqlalchemy import delete
from sqlalchemy.orm import Session


class UserGroupService:

    def __init__(self, session: Session):
        self.session = session


    def update_for_user(self, user_id: int, group_list: List[int]) -> List[str]:
        self.session.execute(
            delete(UserGroupLink).where(UserGroupLink.user == user_id)
        )
        self.session.add_all(
            UserGroupLink(
                user=user_id,
                user_group=group_id
            )
            for group_id in group_list
        )
