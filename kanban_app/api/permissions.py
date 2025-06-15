from rest_framework import permissions

class IsBoardOwner(permissions.BasePermission):
    """_summary_
    IsBoardOwner is a custom permission class that checks if the user is the owner of the board.
    Returns:
        _type_: _description_
    Args:
        permissions (_type_): _description_
    """
    def has_object_permission(self, request, view, obj):
        if request.method == 'DELETE':
            return obj.owner_id.id == request.user.id
        return True
    
    
class IsBoardMemberOrOwner(permissions.BasePermission):
    """_summary_
    IsBoardMemberOrOwner is a custom permission class that checks if the user is a member of the board or the owner.
    Returns:
        _type_: _description_
    """
    def has_object_permission(self, request, view, obj):
        if obj.owner_id == request.user:
            return True
            
        # Prüfe ob User ein Member ist
        if request.method in ['GET', 'HEAD', 'OPTIONS', 'PUT', 'PATCH']:
            return obj.members.filter(id=request.user.id).exists()

        # Für andere Methoden (DELETE) muss der User Owner sein
        return obj.owner_id == request.user