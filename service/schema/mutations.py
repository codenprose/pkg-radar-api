from graphene import Mutation, String, ID, Field

from .types import Package, PackageTag
from .resolvers import create_package, create_package_tag, delete_package_tag


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


# TODO: Add Create Package Recommendation mutation


# TODO: Add Delete Package Recommendation mutation


# TODO: Add Create User Kanban Package mutation


# TODO: Add Update User Kanban Package mutation


# TODO: Add Delete User Kanban Package mutation