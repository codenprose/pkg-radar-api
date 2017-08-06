import graphene

from .types import Package
from .resolvers import create_package

class CreatePackage(graphene.Mutation):
    class Input:
        owner = graphene.String(required=True)
        name = graphene.String(required=True)

    package = graphene.Field(lambda: Package)

    @staticmethod
    def mutate(root, args, context, info):
        owner = args.get('owner')
        name = args.get('name')

        package = create_package(owner, name, 'admin')
        return CreatePackage(package=package)