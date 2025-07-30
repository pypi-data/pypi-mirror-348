import sqlalchemy

from project.sqladmin_.model_view.common import SimpleMV
from project.sqladmin_.util.etc import format_datetime_
from project.sqlalchemy_db_.sqlalchemy_model import UserTokenDBM


class UserTokenMV(SimpleMV, model=UserTokenDBM):
    name = "UserToken"
    name_plural = "UserTokens"
    icon = "fa-solid fa-fingerprint"
    column_list = [
        UserTokenDBM.id,
        UserTokenDBM.long_id,
        UserTokenDBM.slug,
        UserTokenDBM.creation_dt,
        UserTokenDBM.value,
        UserTokenDBM.user,
        UserTokenDBM.is_active,
        UserTokenDBM.extra_data,
    ]
    form_columns = [
        UserTokenDBM.slug,
        UserTokenDBM.creation_dt,
        UserTokenDBM.value,
        UserTokenDBM.user,
        UserTokenDBM.is_active,
        UserTokenDBM.extra_data
    ]
    column_sortable_list = sqlalchemy.inspect(UserTokenDBM).columns
    column_default_sort = [
        (UserTokenDBM.creation_dt, True)
    ]
    column_searchable_list = [
        UserTokenDBM.id,
        UserTokenDBM.long_id,
        UserTokenDBM.slug,
        UserTokenDBM.value,
    ]
    column_formatters = {
        UserTokenDBM.creation_dt: lambda m, _: format_datetime_(m.creation_dt)
    }
    column_formatters_detail = {
        UserTokenDBM.creation_dt: lambda m, _: format_datetime_(m.creation_dt)
    }
