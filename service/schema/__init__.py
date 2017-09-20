from graphene import Schema, ObjectType, String, Field, List

from service import packages_table
from .types import Package, PackageSummary, PackageInput, PackageFilter, \
     UserKanbanPackage, UserKanbanPackageInput, User, CurrentUserInput, \
     UserInput, UserConnection, UserConnectionInput
from .resolvers import get_package, get_package_summary, get_packages, get_user, \
     get_user_kanban_packages, create_user, get_current_user, get_user_connections
from .mutations import CreatePackage, CreateUserKanbanPackage, UpdateUserKanbanPackage, \
     DeleteUserKanbanPackage, CreateUser, LoginUser, UpdateUser, CreateUserConnection, DeleteUserConnection


class RootQuery(ObjectType):
    package = Field(
        Package,
        payload=PackageInput(),
        resolver=get_package
    )

    package_summary = Field(
        PackageSummary,
        payload=PackageInput(),
        resolver=get_package_summary
    )

    packages = List(
        PackageSummary,
        filter=PackageFilter(),
        resolver=get_packages
    )

    user_kanban_packages = List(
        UserKanbanPackage,
        payload=UserKanbanPackageInput(),
        resolver=get_user_kanban_packages
    )

    current_user = Field(
        User,
        payload=CurrentUserInput(),
        resolver=get_current_user
    )

    user_connections = List(
        UserConnection,
        payload=UserConnectionInput(),
        resolver=get_user_connections
    )

    user = Field(
        User,
        payload=UserInput(),
        resolver=get_user
    )


class Mutations(ObjectType):
    create_package = CreatePackage.Field()

    create_user_kanban_package = CreateUserKanbanPackage.Field()

    update_user_kanban_package = UpdateUserKanbanPackage.Field()

    delete_user_kanban_package = DeleteUserKanbanPackage.Field()

    create_user = CreateUser.Field()

    login_user = LoginUser.Field()

    update_user = UpdateUser.Field()

    create_user_connection = CreateUserConnection.Field()

    delete_user_connection = DeleteUserConnection.Field()


schema = Schema(query=RootQuery, mutation=Mutations)
