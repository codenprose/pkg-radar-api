import graphene

from service import packages_table
from .types import Package, PackageSummary, PackageInput
from .resolvers import get_package, get_package_summary
from .mutations import CreatePackage


class RootQuery(graphene.ObjectType):
    package = graphene.Field(
        Package, 
        payload=PackageInput(), 
        resolver=get_package
    )

    package_summary = graphene.Field(
        PackageSummary, 
        payload=PackageInput(),
        resolver=get_package_summary
    )


class Mutations(graphene.ObjectType):
    create_package = CreatePackage.Field()


schema = graphene.Schema(query=RootQuery, mutation=Mutations)
