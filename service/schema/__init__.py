from graphene import Schema, ObjectType, String, Field, List

from service import packages_table
from .types import Package, PackageSummary, PackageInput, PackageFilter, \
    PackageTag, PackageTagInput
from .resolvers import get_package, get_package_summary, get_packages, get_package_tags
from .mutations import CreatePackage


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


class Mutations(ObjectType):
    create_package = CreatePackage.Field()


schema = Schema(query=RootQuery, mutation=Mutations)
