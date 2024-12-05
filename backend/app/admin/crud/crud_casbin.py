from uuid import UUID

from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from app.admin.model.sys_casbin_rule import CasbinRule
from app.admin.schema.casbin_rule import DeleteAllPoliciesParam


class CRUDCasbin(CRUDPlus[CasbinRule]):
    async def get_list(self, ptype: str, sub: str) -> Select:
        return await self.select_order("id", "desc", ptype=ptype, v0__like=f"%{sub}%")

    async def delete_policies_by_sub(
        self, db: AsyncSession, sub: DeleteAllPoliciesParam
    ) -> int:
        where_list = [sub.role]
        if sub.uuid:
            where_list.append(sub.uuid)
        return await self.delete_model_by_column(
            db, allow_multiple=True, v0__mor={"eq": where_list}
        )

    async def delete_groups_by_uuid(self, db: AsyncSession, uuid: UUID) -> int:
        return await self.delete_model_by_column(db, allow_multiple=True, v0=str(uuid))


casbin_dao: CRUDCasbin = CRUDCasbin(CasbinRule)
