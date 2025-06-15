from rest_framework import serializers
from kanban_app.models import Boards, Tasks, TaskComments
from django.contrib.auth.models import User
from user_auth_app.api.serializers import UserSerializer
from .permissions import IsBoardOwner
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics, status


class TaskCommentSerializer(serializers.ModelSerializer):
    """_summary_
    TaskCommentSerializer is a serializer for the TaskComments model.
    Returns:
        _type_: _description_
    """
    author = serializers.CharField(read_only=True)

    class Meta:
        model = TaskComments
        fields = ['id', 'content', 'author', 'created_at']


class TaskSerializer(serializers.ModelSerializer):
    """_summary_
    TaskSerializer is a serializer for the Tasks model.
    Returns:
        _type_: _description_
    """
    assignee = UserSerializer(source='assignee_id', read_only=True)
    reviewer = UserSerializer(source='reviewer_id', read_only=True)
    assignee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), allow_null=True, write_only=True)
    reviewer_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Tasks
        fields = ['id', 'title', 'description', 'board', 'status', 'priority',
                  'assignee', 'assignee_id', 'reviewer', 'reviewer_id', 'due_date',
                  'comments_count']

    def get_comments_count(self, obj):
        return obj.comments.count()


class TaskStatusSerializer(serializers.ModelSerializer):
    """_summary_
    TaskStatusSerializer is a serializer for the Tasks model's status field.
    Returns:
        _type_: _description_
    """
    class Meta:
        model = Tasks
        fields = ['status']


class BoardSerializer(serializers.ModelSerializer):
    """_summary_
    BoardSerializer is a serializer for the Boards model.
    Returns:
        _type_: _description_
    """
    members = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all(), write_only=True)
    member_count = serializers.SerializerMethodField()
    ticket_count = serializers.SerializerMethodField()
    tasks_to_do_count = serializers.SerializerMethodField()
    tasks_high_prio_count = serializers.SerializerMethodField()
    owner_id = serializers.PrimaryKeyRelatedField(read_only=True) 

    class Meta:
        model = Boards
        fields = ['id', 'title', 'members', 'member_count', 'ticket_count',
                  'tasks_to_do_count', 'tasks_high_prio_count', 'owner_id']
        extra_kwargs = {
            'members': {'write_only': True}
        }

    def get_member_count(self, obj):
        return obj.members.count()

    def get_ticket_count(self, obj):
        return obj.tasks.count()

    def get_tasks_to_do_count(self, obj):
        return obj.tasks.filter(status='to-do').count()

    def get_tasks_high_prio_count(self, obj):
        return obj.tasks.filter(priority='high').count()


class BoardDetailSerializer(serializers.ModelSerializer):
    """_summary_
    BoardDetailSerializer is a serializer for the Boards model with detailed information.
    Returns:
        _type_: _description_
    """
    permission_classes = [IsAuthenticated, IsBoardOwner]
    queryset = Boards.objects.all()
    
    members = UserSerializer(many=True, read_only=True)
    tasks = TaskSerializer(many=True, read_only=True)
    owner_id = serializers.PrimaryKeyRelatedField(read_only=True) 

    class Meta:
        model = Boards
        fields = ['id', 'title', 'members', 'tasks', 'owner_id']
        
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.owner_id != request.user:
            return Response(
                {"error": "Only the board owner can delete this board"}, 
                status=status.HTTP_403_FORBIDDEN
            )
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class BoardUpdateSerializer(serializers.ModelSerializer):
    """_summary_
    BoardUpdateSerializer is a serializer for the Boards model used for updates.
    Args:
        serializers (_type_): _description_
    """
    owner_data = UserSerializer(source='owner_id', read_only=True)
    members_data = UserSerializer(source='members', many=True, read_only=True)

    class Meta:
        model = Boards
        fields = ['id', 'title', 'owner_data', 'members_data']