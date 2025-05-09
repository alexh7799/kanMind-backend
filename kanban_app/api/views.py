from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from kanban_app.models import Boards, Tasks, TaskComments
from .serializers import (
    BoardSerializer,
    BoardDetailSerializer,
    TaskSerializer,
    TaskStatusSerializer,
    TaskCommentSerializer
)

"""_summary_
BoardList is a custom view that handles the listing and creation of boards.
Returns:
    _type_: _description_
"""
class BoardList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BoardSerializer

    def get_queryset(self):
        return Boards.objects.filter(members=self.request.user)

    def perform_create(self, serializer):
        board = serializer.save()
        board.members.add(self.request.user)
        members_data = self.request.data.get('members', [])
        if members_data:
            board.members.add(*members_data)


"""_summary_
BoardDetail is a custom view that handles the retrieval, update, and deletion of boards.
Returns:
    _type_: _description_
"""
class BoardDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Boards.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return BoardDetailSerializer
        return BoardSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        if len(request.data) == 1 and 'members' in request.data:
            instance.members.clear()
            instance.members.add(self.request.user)
            members_data = request.data.get('members', [])
            if members_data:
                instance.members.add(*members_data)
            return Response(serializer.data)
        return super().update(request, *args, **kwargs)


"""_summary_
TaskList is a custom view that handles the listing and creation of tasks.
Returns:
    _type_: _description_
"""
class TaskList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer

    def get_queryset(self):
        # Wenn board_id in URL, dann filter
        board_id = self.kwargs.get('board_id')
        if board_id:
            return Tasks.objects.filter(board_id=board_id)
        return Tasks.objects.all()

    def perform_create(self, serializer):
        # board kommt jetzt aus den POST-Daten
        serializer.save()


"""_summary_
TaskDetail is a custom view that handles the retrieval, update, and deletion of tasks.
Returns:
    _type_: _description_
"""
class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Tasks.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'PATCH' and len(self.request.data) == 1 and 'status' in self.request.data:
            return TaskStatusSerializer
        return TaskSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


"""_summary_
AssignedTaskList is a custom view that handles the listing of tasks assigned to the user.
Returns:
    _type_: _description_
"""
class AssignedTaskList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Tasks.objects.filter(assignee_id=self.request.user)


"""_summary_
ReviewingTaskList is a custom view that handles the listing of tasks assigned to the user.
Returns:
    _type_: _description_
"""
class ReviewingTaskList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Tasks.objects.filter(reviewer_id=self.request.user)


"""_summary_
TaskCommentList is a custom view that handles the listing and creation of task comments.
Returns:
    _type_: _description_
"""
class TaskCommentList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskCommentSerializer

    def get_queryset(self):
        return TaskComments.objects.filter(task_id=self.kwargs['task_id'])

    def perform_create(self, serializer):
        serializer.save(
            task_id=self.kwargs['task_id'],
            user=self.request.user
        )


"""_summary_
TaskCommentDetail is a custom view that handles the retrieval, update, and deletion of task comments.
Returns:
    _type_: _description_
"""
class TaskCommentDetail(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = TaskComments.objects.all()
