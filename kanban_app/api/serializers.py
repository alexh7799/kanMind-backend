from rest_framework import serializers
from kanban_app.models import Boards, Tasks, TaskComments
from django.contrib.auth.models import User
from user_auth_app.api.serializers import UserSerializer

"""_summary_
TaskCommentSerializer is a serializer for the TaskComments model.
Returns:
    _type_: _description_
"""
class TaskCommentSerializer(serializers.ModelSerializer):
    author = serializers.CharField(read_only=True)

    class Meta:
        model = TaskComments
        fields = ['id', 'content', 'author', 'created_at']


"""_summary_
TaskSerializer is a serializer for the Tasks model.
Returns:
    _type_: _description_
"""
class TaskSerializer(serializers.ModelSerializer):
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


"""_summary_
TaskStatusSerializer is a serializer for the Tasks model's status field.
Returns:
    _type_: _description_
"""
class TaskStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = ['status']


"""_summary_
BoardSerializer is a serializer for the Boards model.
Returns:
    _type_: _description_
"""
class BoardSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True, read_only=True)
    member_count = serializers.SerializerMethodField()
    ticket_count = serializers.SerializerMethodField()
    tasks_to_do_count = serializers.SerializerMethodField()
    tasks_high_prio_count = serializers.SerializerMethodField()

    class Meta:
        model = Boards
        fields = ['id', 'title', 'members', 'member_count', 'ticket_count',
                  'tasks_to_do_count', 'tasks_high_prio_count']

    def get_member_count(self, obj):
        return obj.members.count()

    def get_ticket_count(self, obj):
        return obj.tasks.count()

    def get_tasks_to_do_count(self, obj):
        return obj.tasks.filter(status='to-do').count()

    def get_tasks_high_prio_count(self, obj):
        return obj.tasks.filter(priority='high').count()


"""_summary_
BoardDetailSerializer is a serializer for the Boards model with detailed information.
Returns:
    _type_: _description_
"""
class BoardDetailSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True, read_only=True)
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Boards
        fields = ['id', 'title', 'members', 'tasks']
