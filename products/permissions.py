from rest_framework import permissions



class IsAdminOrReadOnly(permissions.BasePermission):
    """
    class defines model level permmison
    model can only be altered by admin
    but can be viwed by both admin and none admin. 
    """
    message = 'only admins can do that bruh!!'

    def has_permission(self,request,view):
        if request.method in permissions.SAFE_METHODS or request.user.is_staff:
            #allow user see data
            return True
        return False

