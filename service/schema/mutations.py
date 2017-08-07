from graphene import Mutation, String, ID, Field

from .types import Package, PackageTag, PackageRecommendation, UserKanbanPackage
from .resolvers import create_package, create_package_tag, delete_package_tag, \
    create_package_recommendation, delete_package_recommendation, create_user_kanban_package, \
    update_user_kanban_package, delete_user_kanban_package


class CreatePackage(Mutation):
    class Input:
        owner = String(required=True)
        name = String(required=True)

    package = Field(lambda: Package)

    @staticmethod
    def mutate(root, args, context, info):
        owner = args.get('owner')
        name = args.get('name')

        package = create_package(owner, name, 'admin')
        return CreatePackage(package=package)


class CreatePackageTag(Mutation):
    class Input:
        tag_name = String(required=True)
        package_id = ID(required=True)
        owner_name = String(required=True)
        package_name = String(required=True)

    package_tag = Field(lambda: PackageTag)

    @staticmethod
    def mutate(root, args, context, info):
        tag_name = args.get('tag_name')
        package_id = args.get('package_id')
        owner_name = args.get('owner_name')
        package_name = args.get('package_name')

        package_tag = create_package_tag(
            tag_name,
            package_id,
            owner_name,
            package_name
        )

        return CreatePackageTag(package_tag=package_tag)


class DeletePackageTag(Mutation):
    class Input:
        tag_name = String(required=True)
        package_id = ID(required=True)

    package_tag = Field(lambda: PackageTag)

    @staticmethod
    def mutate(root, args, context, info):
        package_id = args.get('package_id')
        tag_name = args.get('tag_name')

        package_tag = delete_package_tag(
            package_id,
            tag_name
        )

        return DeletePackageTag(package_tag=package_tag)


class CreatePackageRecommendation(Mutation):
    class Input:
        package_id = ID(required=True)
        owner_name = String()
        package_name = String()
        recommendation_package_id = ID(required=True)
        recommendation_owner_name = String(required=True)
        recommendation_package_name = String(required=True)

    package_recomendation = Field(lambda: PackageRecommendation)

    @staticmethod
    def mutate(root, args, context, info):
        package_id = args.get('package_id')
        owner_name = args.get('owner_name')
        package_name = args.get('package_name')
        recommendation_package_id = args.get('recommendation_package_id')
        recommendation_owner_name = args.get('recommendation_owner_name')
        recommendation_package_name = args.get('recommendation_package_name')

        package_recomendation = create_package_recommendation(
            package_id=package_id,
            owner_name=owner_name,
            package_name=package_name,
            recommendation_package_id=recommendation_package_id,
            recommendation_owner_name=recommendation_owner_name,
            recommendation_package_name=recommendation_package_name
        )

        return CreatePackageRecommendation(package_recomendation=package_recomendation)


class DeletePackageRecommendation(Mutation):
    class Input:
        package_id = ID(required=True)
        recommendation_package_id = ID(required=True)
        recommendation_owner_name = String(required=True)
        recommendation_package_name = String(required=True)

    package_recomendation = Field(lambda: PackageRecommendation)

    @staticmethod
    def mutate(root, args, context, info):
        package_id = args.get('package_id')
        recommendation_package_id = args.get('recommendation_package_id')
        recommendation_owner_name = args.get('recommendation_owner_name')
        recommendation_package_name = args.get('recommendation_package_name')

        package_recomendation = delete_package_recommendation(
            package_id=package_id,
            recommendation_package_id=recommendation_package_id,
            recommendation_owner_name=recommendation_owner_name,
            recommendation_package_name=recommendation_package_name
        )

        return DeletePackageRecommendation(package_recomendation=package_recomendation)


class CreateUserKanbanPackage(Mutation):
    class Input:
        board = String(required=True)
        owner_name = String(required=True)
        package_id = ID(required=True)
        package_name = String(required=True)
        status = String(required=True)
        user_id = ID(required=True)
    
    user_kanban_package = Field(lambda: UserKanbanPackage)

    @staticmethod
    def mutate(root, args, context, info):
        board = args.get('board')
        owner_name = args.get('owner_name')
        package_id = args.get('package_id')
        package_name = args.get('package_name')
        status = args.get('status')
        user_id = args.get('user_id')

        user_kanban_package = create_user_kanban_package(
            board=board,
            owner_name=owner_name,
            package_id=package_id,
            package_name=package_name,
            status=status,
            user_id=user_id
        )

        return CreateUserKanbanPackage(user_kanban_package=user_kanban_package)


# TODO: Add Update User Kanban Package mutation


# TODO: Add Delete User Kanban Package mutation