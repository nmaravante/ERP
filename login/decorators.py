from django.core.exceptions import PermissionDenied
from . models import Permissions, User, Role


def permission_required(permission):
    def permission_req(function):
        def wrap(request, *args, **kwargs):
            if request.user.roles.permissions.filter(name=permission).exists() or request.user.permissions.filter(name=permission).exists():
                return function(request, *args, **kwargs)
            else:
                raise PermissionDenied
        wrap.__doc__ = function.__doc__
        wrap.__name__ = function.__name__
        return wrap
    return permission_req
