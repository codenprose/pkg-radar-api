from graphene import Mutation, String, Field

from .types import Package
from .resolvers import create_package

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


# TODO: Add Create Package Tag mutation


# TODO: Add Delete Package Tag mutation


# TODO: Add Create Package Recommendation mutation


# TODO: Add Delete Package Recommendation mutation


# TODO: Add Create User Kanban Package mutation


# TODO: Add Update User Kanban Package mutation


# TODO: Add Delete User Kanban Package mutation