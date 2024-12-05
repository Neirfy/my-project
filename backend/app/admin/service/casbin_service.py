from uuid import UUID

from sqlalchemy import Select

from app.admin.crud.crud_casbin import casbin_dao
from app.admin.schema.casbin_rule import (
    CreatePolicyParam,
    CreateUserRoleParam,
    DeleteAllPoliciesParam,
    DeletePolicyParam,
    DeleteUserRoleParam,
    UpdatePolicyParam,
)
from common.exception import errors
from common.security.rbac import rbac
from database.db_postgres import async_session


class CasbinService:
    @staticmethod
    async def get_casbin_list(*, ptype: str, sub: str) -> Select:
        return await casbin_dao.get_list(ptype, sub)

    @staticmethod
    async def get_policy_list(*, role: int | None = None) -> list:
        enforcer = await rbac.enforcer()
        if role is not None:
            data = enforcer.get_filtered_named_policy('p', 0, str(role))
        else:
            data = enforcer.get_policy()
        return data

    @staticmethod
    async def create_policy(*, p: CreatePolicyParam) -> bool:
        enforcer = await rbac.enforcer()
        data = await enforcer.add_policy(p.sub, p.path, p.method)
        if not data:
            raise errors.ForbiddenError(msg='Разрешение уже существует')
        return data

    @staticmethod
    async def create_policies(*, ps: list[CreatePolicyParam]) -> bool:
        enforcer = await rbac.enforcer()
        data = await enforcer.add_policies([list(p.model_dump().values()) for p in ps])
        if not data:
            raise errors.ForbiddenError(msg='Разрешение уже существует')
        return data

    @staticmethod
    async def update_policy(*, old: UpdatePolicyParam, new: UpdatePolicyParam) -> bool:
        enforcer = await rbac.enforcer()
        _p = enforcer.has_policy(old.sub, old.path, old.method)
        if not _p:
            raise errors.NotFoundError(msg='Разрешения не существует')
        data = await enforcer.update_policy([old.sub, old.path, old.method], [new.sub, new.path, new.method])
        return data

    @staticmethod
    async def update_policies(*, old: list[UpdatePolicyParam], new: list[UpdatePolicyParam]) -> bool:
        enforcer = await rbac.enforcer()
        data = await enforcer.update_policies(
            [list(o.model_dump().values()) for o in old], [list(n.model_dump().values()) for n in new]
        )
        return data

    @staticmethod
    async def delete_policy(*, p: DeletePolicyParam) -> bool:
        enforcer = await rbac.enforcer()
        _p = enforcer.has_policy(p.sub, p.path, p.method)
        if not _p:
            raise errors.NotFoundError(msg='Разрешения не существует')
        data = await enforcer.remove_policy(p.sub, p.path, p.method)
        return data

    @staticmethod
    async def delete_policies(*, ps: list[DeletePolicyParam]) -> bool:
        enforcer = await rbac.enforcer()
        data = await enforcer.remove_policies([list(p.model_dump().values()) for p in ps])
        if not data:
            raise errors.NotFoundError(msg='Разрешения не существует')
        return data

    @staticmethod
    async def delete_all_policies(*, sub: DeleteAllPoliciesParam) -> int:
        async with async_session.begin() as db:
            count = await casbin_dao.delete_policies_by_sub(db, sub)
        return count

    @staticmethod
    async def get_group_list() -> list:
        enforcer = await rbac.enforcer()
        data = enforcer.get_grouping_policy()
        return data

    @staticmethod
    async def create_group(*, g: CreateUserRoleParam) -> bool:
        enforcer = await rbac.enforcer()
        data = await enforcer.add_grouping_policy(g.uuid, g.role)
        if not data:
            raise errors.ForbiddenError(msg='Разрешение уже существует')
        return data

    @staticmethod
    async def create_groups(*, gs: list[CreateUserRoleParam]) -> bool:
        enforcer = await rbac.enforcer()
        data = await enforcer.add_grouping_policies([list(g.model_dump().values()) for g in gs])
        if not data:
            raise errors.ForbiddenError(msg='Разрешение уже существует')
        return data

    @staticmethod
    async def delete_group(*, g: DeleteUserRoleParam) -> bool:
        enforcer = await rbac.enforcer()
        _g = enforcer.has_grouping_policy(g.uuid, g.role)
        if not _g:
            raise errors.NotFoundError(msg='Разрешения не существует')
        data = await enforcer.remove_grouping_policy(g.uuid, g.role)
        return data

    @staticmethod
    async def delete_groups(*, gs: list[DeleteUserRoleParam]) -> bool:
        enforcer = await rbac.enforcer()
        data = await enforcer.remove_grouping_policies([list(g.model_dump().values()) for g in gs])
        if not data:
            raise errors.NotFoundError(msg='Разрешения не существует')
        return data

    @staticmethod
    async def delete_all_groups(*, uuid: UUID) -> int:
        async with async_session.begin() as db:
            count = await casbin_dao.delete_groups_by_uuid(db, uuid)
        return count


casbin_service = CasbinService()