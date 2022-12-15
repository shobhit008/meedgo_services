from rest_framework import permissions


class PharmacistPermission(permissions.BasePermission):
    message = {'msg': 'You are not authorized for this action'}
    
    edit_methods = ("GET", "POST","PUT", "PATCH","DELETE")

    def has_permission(self, request, view):
        if request.user.user_type == "Pharmacists":
            return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        # if request.method in permissions.SAFE_METHODS:
        #     return True

        # if obj.author == request.user:
        #     return True

        # if request.user.is_staff and request.method not in self.edit_methods:
        #     return True

        return False