from graphene_django import DjangoObjectType

from .decorators import permissions_checker


class PermissionDjangoObjectType(DjangoObjectType):
	"""
	Check if the object    
	"""
	class Meta:
		abstract = True

	@classmethod
	def get_node(cls, info, id):
		return permissions_checker(cls.permission_classes(), manually=True)(
			super().get_node
		)(cls, info, id)

	@staticmethod
	def permission_classes():
		return []


class BasePermission:
	"""
	Base class from which all permission classes should inherit.
	"""
	@staticmethod
	def has_permission(context):
		"""
		Return `True` if permission is granted, `False` otherwise.
		"""
		return True

	@staticmethod
	def has_object_permission(context, obj):
		"""
		Return `True` if permission is granted, `False` otherwise.
		"""
		return True


class AllowAny(BasePermission):
	"""
	Allow any access.
	"""

	@staticmethod
	def has_permission(context):
		return True


class IsAuthenticated(BasePermission):
	"""
	Allows access only to authenticated users.
	"""
	@staticmethod
	def has_permission(context):
		return context.user and context.user.is_authenticated
