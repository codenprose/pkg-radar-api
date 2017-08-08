from graphene import ObjectType, InputObjectType, String, ID, Int, Field, List


# Pacakges
class Package(ObjectType):
    archive = Int(required=True)
    backlog = Int(required=True)
    color = String(required=True)
    created_at = String()
    created_by = ID()
    description = String(required=True)
    id = ID(required=True)
    issues = Int(required=True)
    language = String(required=True)
    last_commit = Field(lambda: LastCommit)
    last_release = Field(lambda: LastRelease)
    license = String()
    mentionable_users = Int(required=True)
    owner_avatar = String(required=True)
    owner_name = String(required=True)
    package_name = String(required=True)
    package_avatar = String()
    production = Int(required=True)
    pull_requests = Int(required=True)
    readme = Field(lambda: Readme)
    repo_url = String(required=True)
    stars = Int(required=True)
    tags = List(lambda: PackageTag)
    trial = Int(required=True)
    updated_at = String()
    website_url = String()
    

class PackageSummary(ObjectType):
    color = String(required=True)
    description = String(required=True)
    issues = Int(required=True)
    language = String(required=True)
    owner_avatar = String(required=True)
    owner_name = String(required=True)
    package_name = String(required=True)
    stars = Int(required=True)


class PackageInput(InputObjectType):
    owner_name = String(required=True)
    package_name = String(required=True)


class PackageFilter(InputObjectType):
    language = String()


class Readme(ObjectType):
    extension = String()
    text = String()

    def resolve_extension(root, args, context, info):
        return root['extension']

    def resolve_text(root, args, context, info):
        return root['text']
    

class LastRelease(ObjectType):
    description = String()
    name = String(required=True)
    published_at = String(required=True)
    url = String(required=True)

    def resolve_description(root, args, context, info):
        return root['description']

    def resolve_name(root, args, context, info):
        return root['name']

    def resolve_published_at(root, args, context, info):
        return root['published_at']

    def resolve_url(root, args, context, info):
        return root['url']


class LastCommit(ObjectType):
    author = Field(lambda: Author)
    commit_url = String(required=True)
    message = String(required=True)
    oid = ID(required=True)

    def resolve_author(root, args, context, info):
        return root['author']

    def resolve_commit_url(root, args, context, info):
        return root['commit_url']

    def resolve_message(root, args, context, info):
        return root['message']

    def resolve_oid(root, args, context, info):
        return root['oid']


class Author(ObjectType):
    date = String()
    name = String()
    email = String()

    def resolve_date(root, args, context, info):
        return root['date']

    def resolve_name(root, args, context, info):
        return root['name']

    def resolve_email(root, args, context, info):
        return root['email']


# Package Tags
class PackageTag(ObjectType):
    package_id = ID(required=True)
    tag_name = String(required=True)
    owner_name = String()
    package_name = String()


class PackageTagInput(InputObjectType):
    package_id = ID(required=True)
    tag_name = String()


# Package Recommendations
class PackageRecommendation(ObjectType):
    package_id = ID(required=True)
    owner_name = String()
    package_name = String()
    recommendation_package_id = ID(required=True)
    recommendation_owner_name = String(required=True)
    recommendation_package_name = String(required=True)


class PackageRecommendationsInput(InputObjectType):
    package_id = ID(required=True)


# Users
class UserKanbanPackage(ObjectType):
    board = String(required=True)
    owner_name = String(required=True)
    package_id = ID(required=True)
    package_name = String(required=True)
    status = String(required=True)
    user_id = ID(required=True)


class UserKanbanPackageInput(InputObjectType):
    user_id = ID(required=True)