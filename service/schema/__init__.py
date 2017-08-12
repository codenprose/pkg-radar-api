from graphene import Schema, ObjectType, String, Field, List

from service import packages_table
from .types import Package, PackageSummary, PackageInput, PackageFilter, \
    PackageTag, PackageTagInput, PackageRecommendation, PackageRecommendationsInput, \
    UserKanbanPackage, UserKanbanPackageInput, User, CurrentUserInput
from .resolvers import get_package, get_package_summary, get_packages, get_package_tags, \
    get_package_recommendations, get_user_kanban_packages, create_user, get_current_user
from .mutations import CreatePackage, CreatePackageTag, DeletePackageTag, CreatePackageRecommendation, \
    DeletePackageRecommendation, CreateUserKanbanPackage, UpdateUserKanbanPackage, DeleteUserKanbanPackage, \
    CreateUser, LoginUser


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

    package_tags = List(
        PackageTag,
        payload=PackageTagInput(),
        resolver=get_package_tags
    )

    package_recommendations = List(
        PackageRecommendation,
        payload=PackageRecommendationsInput(),
        resolver=get_package_recommendations
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


class Mutations(ObjectType):
    create_package = CreatePackage.Field()

    create_package_tag = CreatePackageTag.Field()

    delete_package_tag = DeletePackageTag.Field()

    create_package_recommendation = CreatePackageRecommendation.Field()

    delete_package_recommendation = DeletePackageRecommendation.Field()

    create_user_kanban_package = CreateUserKanbanPackage.Field()

    update_user_kanban_package = UpdateUserKanbanPackage.Field()

    delete_user_kanban_package = DeleteUserKanbanPackage.Field()

    create_user = CreateUser.Field()

    login_user = LoginUser.Field()



schema = Schema(query=RootQuery, mutation=Mutations)
