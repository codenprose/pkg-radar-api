from graphene import Mutation, String, ID, Field, List

from .types import Package,PackageRecommendation, UserKanbanPackage, User, \
    KanbanCard, KanbanCardInput, UserConnection
from .resolvers import create_package, create_package_recommendation, delete_package_recommendation,  \
    create_user_kanban_package, update_user_kanban_package, delete_user_kanban_package, \
    create_user, login_user, update_user, create_user_connection, delete_user_connection


class CreateUser(Mutation):
    class Input:
        avatar = String(required=True)
        bio = String(required=True)
        company = String(required=True)
        email = String(required=True)
        github_id = String(required=True)
        location = String(required=True)
        name = String(required=True)
        username = String(required=True)
        website = String(required=True)

    user = Field(lambda: User)

    @staticmethod
    def mutate(root, args, context, info):
        avatar = args.get('avatar')
        bio = args.get('bio')
        company = args.get('company')
        email = args.get('email')
        github_id = args.get('github_id')
        location = args.get('location')
        name = args.get('name')
        username = args.get('username')
        website = args.get('website')

        user = create_user(
            avatar=avatar,
            bio=bio,
            company=company,
            email=email,
            github_id=github_id,
            location=location,
            name=name,
            username=username,
            website=website
        )
        return CreateUser(user=user)


class LoginUser(Mutation):
    class Input:
        username = String(required=True)
        token = String(required=True)

    user = Field(lambda: User)

    @staticmethod
    def mutate(root, args, context, info):
        username = args.get('username')
        token = args.get('token')

        user = login_user(username, token)
        return LoginUser(user=user)


class CreatePackage(Mutation):
    class Input:
        owner = String(required=True)
        name = String(required=True)
        created_by = String(required=True)

    package = Field(lambda: Package)

    @staticmethod
    def mutate(root, args, context, info):
        owner = args.get('owner')
        name = args.get('name')
        created_by = args.get('created_by')

        package = create_package(owner, name, created_by)
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
        owner_name = String(required=True)
        package_id = ID(required=True)
        package_name = String(required=True)
        status = String(required=True)
        username = String(required=True)

    user_kanban_package = Field(lambda: UserKanbanPackage)

    @staticmethod
    def mutate(root, args, context, info):
        owner_name = args.get('owner_name')
        package_id = args.get('package_id')
        package_name = args.get('package_name')
        status = args.get('status')
        username = args.get('username')

        user_kanban_package = create_user_kanban_package(
            owner_name=owner_name,
            package_id=package_id,
            package_name=package_name,
            status=status,
            username=username
        )

        return CreateUserKanbanPackage(user_kanban_package=user_kanban_package)


class DeleteUserKanbanPackage(Mutation):
    class Input:
        package_id = ID(required=True)
        username = String(required=True)

    user_kanban_package = Field(lambda: UserKanbanPackage)

    @staticmethod
    def mutate(root, args, context, info):
        package_id = args.get('package_id')
        username = args.get('username')

        user_kanban_package = delete_user_kanban_package(
            package_id=package_id,
            username=username
        )

        return DeleteUserKanbanPackage(user_kanban_package=user_kanban_package)


class UpdateUserKanbanPackage(Mutation):
    class Input:
        package_id = ID(required=True)
        status = String(required=True)
        username = String(required=True)

    user_kanban_package = Field(lambda: UserKanbanPackage)

    @staticmethod
    def mutate(root, args, context, info):
        package_id = args.get('package_id')
        status = args.get('status')
        username = args.get('username')

        user_kanban_package = update_user_kanban_package(
            package_id=package_id,
            status=status,
            username=username
        )

        return UpdateUserKanbanPackage(user_kanban_package=user_kanban_package)


class UpdateUser(Mutation):
    class Input:
        username = String(required=True)
        kanban_card_positions = List(KanbanCardInput)
        kanban_boards = List(String)

    user = Field(lambda: User)

    @staticmethod
    def mutate(root, args, context, info):
        data = {}

        for item in args:
            data[item] = args.get(item)

        user = update_user(**data)

        return UpdateUser(user=user)


class CreateUserConnection(Mutation):
    class Input:
        user = String(required=True)
        connection = String(required=True)


    user_connection = Field(lambda: UserConnection)

    @staticmethod
    def mutate(root, args, context, info):
        user = args.get('user')
        connection = args.get('connection')

        user_connection = create_user_connection(
            user=user,
            connection=connection
        )

        return CreateUserConnection(user_connection=user_connection)


class DeleteUserConnection(Mutation):
    class Input:
        user = String(required=True)
        connection = String(required=True)

    user_connection = Field(lambda: UserConnection)

    @staticmethod
    def mutate(root, args, context, info):
        user = args.get('user')
        connection = args.get('connection')

        user_connection = delete_user_connection(
            user=user,
            connection=connection
        )

        return DeleteUserConnection(user_connection=user_connection)
