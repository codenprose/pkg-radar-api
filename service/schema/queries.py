import graphene

# Pacakges
class Package(graphene.ObjectType):
    archive = graphene.Int(required=True)
    backlog = graphene.Int(required=True)
    color = graphene.String(required=True)
    created_at = graphene.String()
    created_by = graphene.ID()
    description = graphene.String(required=True)
    id = graphene.ID(required=True)
    issues = graphene.Int(required=True)
    language = graphene.String(required=True)
    last_commit = graphene.Field(lambda: LastCommit)
    last_release = graphene.Field(lambda: LastRelease)
    license = graphene.String()
    mentionable_users = graphene.Int(required=True)
    owner_avatar = graphene.String(required=True)
    owner_name = graphene.String(required=True)
    package_name = graphene.String(required=True)
    package_avatar = graphene.String()
    production = graphene.Int(required=True)
    pull_requests = graphene.Int(required=True)
    readme = graphene.Field(lambda: Readme)
    repo_url = graphene.String(required=True)
    stars = graphene.Int(required=True)
    trial = graphene.Int(required=True)
    updated_at = graphene.String()
    website_url = graphene.String()
    

class PackageSummary(graphene.ObjectType):
    archive = graphene.Int(required=True)
    backlog = graphene.Int(required=True)
    color = graphene.String(required=True)
    description = graphene.String(required=True)
    issues = graphene.Int(required=True)
    language = graphene.String(required=True)
    owner_avatar = graphene.String(required=True)
    owner_name = graphene.String(required=True)
    package_avatar = graphene.String()
    package_name = graphene.String(required=True)
    production = graphene.Int(required=True)
    stars = graphene.Int(required=True)
    trial = graphene.Int(required=True)


class PackageInput(graphene.InputObjectType):
    owner_name = graphene.String(required=True)
    package_name = graphene.String(required=True)


class Readme(graphene.ObjectType):
    extension = graphene.String()
    text = graphene.String()

    def resolve_extension(root, args, context, info):
        return root['extension']

    def resolve_text(root, args, context, info):
        return root['text']
    

class LastRelease(graphene.ObjectType):
    description = graphene.String()
    name = graphene.String(required=True)
    published_at = graphene.String(required=True)
    url = graphene.String(required=True)

    def resolve_description(root, args, context, info):
        return root['description']

    def resolve_name(root, args, context, info):
        return root['name']

    def resolve_published_at(root, args, context, info):
        return root['published_at']

    def resolve_url(root, args, context, info):
        return root['url']


class LastCommit(graphene.ObjectType):
    author = graphene.Field(lambda: Author)
    commit_url = graphene.String(required=True)
    message = graphene.String(required=True)
    oid = graphene.ID(required=True)

    def resolve_author(root, args, context, info):
        return root['author']

    def resolve_commit_url(root, args, context, info):
        return root['commit_url']

    def resolve_message(root, args, context, info):
        return root['message']

    def resolve_oid(root, args, context, info):
        return root['oid']

class Author(graphene.ObjectType):
    date = graphene.String()
    name = graphene.String()
    email = graphene.String()

    def resolve_date(root, args, context, info):
        return root['date']

    def resolve_name(root, args, context, info):
        return root['name']

    def resolve_email(root, args, context, info):
        return root['email']
