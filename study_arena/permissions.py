from rest_framework.permissions import BasePermission
from authenticator.models import User
from django.utils.translation import gettext_lazy as _
class IsManager(BasePermission):
    message = _("You are not a manager.")

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == "M"
        )

class IsTeacher(BasePermission):
    message = 'You Aren\'t A Teacher!'

    def has_permission(self, request, view):
        return request.user.role == 'T'


class IsStudent(BasePermission):
    message = 'You Aren\'t A Student!'

    def has_permission(self, request, view):
        return request.user.role == 'S'


class IsProfileCompleted(BasePermission):
    message = _("Please complete your personal information.")

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_completed()
        )
    
class IsAdmin(BasePermission):
    message = "YOU ARE NOT ADMIN X("

    def has_permission(self, request, view):
        return request.user.is_superuser
