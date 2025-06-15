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