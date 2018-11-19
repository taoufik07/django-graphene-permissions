# DGP - Django graphene permissions

Permission system inspired by DRF


## Installation

Install the latest release:

```shell
$ pip3 install django-graphene-permissions
```
Or using pipenv

```shell
$ pipenv install django-graphene-permissions
```

## Usage

### Permission definition
---

You can create new permissions by subclassing `BasePermission` e.g. 

```python
from django_graphene_permissions.permissions import BasePermission

class MyPermission(BasePermission):

    @staticmethod
    def has_permission(context):
        return context.user and context.user.is_authenticated
    
    @staticmethod
    def has_object_permission(context, obj):
        return True


```

This package provides predefined permissions : 

* `AllowAny` : Allow any access.
* `IsAuthenticated` : Allow only authenticated users.


### Node Permission
---

Subclass `PermissionDjangoObjectType` and define the permissions via the static method `permission_classes` that should return an iterable of permission classes


```python
from django_graphene_permissions import PermissionDjangoObjectType
from django_graphene_permissions.permissions import IsAuthenticated

class ExampleNode(PermissionDjangoObjectType):
    class Meta:
        model = Example
        interfaces = (relay.Node,)

    @staticmethod
    def permission_classes():
        return [IsAuthenticated]
```

### Mutation Permission
---

Apply the `permissions_checker([Permission,...])` decorator to `mutate` e.g.

```python
from django_graphene_permissions import permissions_checker
from django_graphene_permissions.permissions import IsAuthenticated

class ExampleDeleteMutation(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        id = graphene.ID()

    @permissions_checker([IsAuthenticated])
    def mutate(self, info, id):
        instance = get_instance(id)
        instance.delete()
        return ExampleDeleteMutation(ok=True)
``` 

### Query Permission
---

Apply the `permissions_checker([Permission,...])` decorator to the field resolver e.g.

```python
from django_graphene_permissions import permissions_checker
from django_graphene_permissions.permissions import IsAuthenticated

class Query(graphene.ObjectType):
    post = relay.Node.Field(PostNode)
    posts = DjangoFilterConnectionField(PostNode)

    @permissions_checker([IsAuthenticated])
    def resolve_posts(self, info, **kwargs):
        return Post.objects.all()
```

## TODO

* Improvements
* Tests
* Add a `PermissionDjangoFilterConnectionField`
* Better docs
