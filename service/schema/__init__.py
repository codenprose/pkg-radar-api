from graphene import Schema, ObjectType, String, Field, List

from service import packages_table
from .types import Package, PackageSummary, PackageInput, PackageFilter, \
    PackageTag, PackageTagInput, PackageRecommendation, PackageRecommendationInput
from .resolvers import get_package, get_package_summary, get_packages, get_package_tags, \
    get_package_recommendations
from .mutations import CreatePackage, CreatePackageTag, DeletePackageTag


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
        payload=PackageRecommendationInput(),
        resolver=get_package_recommendations
    )


class Mutations(ObjectType):
    create_package = CreatePackage.Field()

    create_package_tag = CreatePackageTag.Field()

    delete_package_tag = DeletePackageTag.Field()


schema = Schema(query=RootQuery, mutation=Mutations)
