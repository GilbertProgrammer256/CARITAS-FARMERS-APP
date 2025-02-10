from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    def has_permission(self,request,view):
        return request.user and request.user.role=='admin'
    
    
class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self,request,view,obj):
        return obj.created_by ==request.user or request.user.role=='admin'