import graphene

from service import packages_table
from .queries import Package, PackageSummary, PackageInput
from .resolvers import get_package, get_package_summary


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


schema = graphene.Schema(query=RootQuery)
