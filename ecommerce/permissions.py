from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role == 'ADMIN'
    
class IsSeller(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role == 'SELLER'
    
    #Seller can only access their product
    def has_object_permission(self, request, view, obj):
        return obj.store.owner == request.user

class IsBuyer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'BUYER'
    
class IsAdminOrSeller(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and (request.user.role == 'SELLER' or request.user.role == 'ADMIN' )