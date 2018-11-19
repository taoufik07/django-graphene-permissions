from .exceptions import GraphQLError, PermissionDenied


def permissions_checker(permissions, manually=False):
	"""
	Checks the given permissions
	"""
	def wrapped_decorator(func):
		def inner(cls, info, *args, **kwargs):
			if check_permissions(permissions, info.context):
				# TODO: Refactor
				if len(args) > 0:
					id = args[0]
					obj = cls._meta.model.objects.get(pk=id)
					if check_object_permissions(permissions, info.context, obj):
						if manually:
							return func(info, *args, **kwargs)
						return func(cls, info, *args, **kwargs)
					else:
						raise PermissionDenied("Permission Denied.")
				return func(cls, info, **kwargs)
			raise PermissionDenied("Permission Denied.")
		return inner
	return wrapped_decorator

def check_permissions(permissions, context):
	"""
	Check if it's permitted.
	Raises an appropriate exception if it's is not permitted.
	"""
	for permission in permissions:
		if not permission.has_permission(context):
			return False
	return True

def check_object_permissions(permissions, context, obj):
	"""
	Check if it's permitted for a given object.
	Raises an appropriate exception if it's is not permitted.
	"""
	for permission in permissions:
		if not permission.has_object_permission(context, obj):
			return False
	return True
