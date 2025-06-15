from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from .permissions import IsBoardMemberOrOwner
from kanban_app.models import Boards, Tasks, TaskComments
from django.http import Http404
from django.shortcuts import get_object_or_404
from .serializers import (
    BoardSerializer,
    BoardDetailSerializer,
    BoardUpdateSerializer,
    TaskSerializer,
    TaskStatusSerializer,
    TaskCommentSerializer
)


class BoardList(generics.ListCreateAPIView):
    """_summary_
    BoardList is a custom view that handles the listing and creation of boards.
    Returns:
        _type_: _description_
    """
    permission_classes = [IsAuthenticated]
    serializer_class = BoardSerializer

    def get_queryset(self):
        return Boards.objects.filter(members=self.request.user)

    def perform_create(self, serializer):
        board = serializer.save(owner_id=self.request.user)
        board.members.add(self.request.user)
        members_data = self.request.data.get('members', [])
        if members_data:
            board.members.add(*members_data)


class BoardDetail(generics.RetrieveUpdateDestroyAPIView):
    """_summary_
    BoardDetail is a custom view that handles the retrieval, update, and deletion of boards.
    Returns:
        _type_: _description_
    """
    permission_classes = [IsAuthenticated, IsBoardMemberOrOwner]
    queryset = Boards.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['PATCH', 'PUT']:
            return BoardUpdateSerializer
        if self.request.method == 'GET':
            return BoardDetailSerializer
        return BoardSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # Prüfe explizit ob der User der Owner ist
        if instance.owner_id.id != request.user.id:
            return Response(
                {"error": "Only the board owner can delete this board"}, 
                status=status.HTTP_403_FORBIDDEN
            )
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class TaskList(generics.ListCreateAPIView):
    """_summary_
    TaskList is a custom view that handles the listing and creation of tasks.
    Returns:
        _type_: _description_
    """
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer

    def get_queryset(self):
        board_id = self.kwargs.get('board_id')
        if board_id:
            return Tasks.objects.filter(board_id=board_id)
        return Tasks.objects.all()

    def perform_create(self, serializer):
        serializer.save()


class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    """_summary_
    TaskDetail is a custom view that handles the retrieval, update, and deletion of tasks.
    Returns:
        _type_: _description_
    """
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


class AssignedTaskList(generics.ListAPIView):
    """_summary_
    AssignedTaskList is a custom view that handles the listing of tasks assigned to the user.
    Returns:
        _type_: _description_
    """
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Tasks.objects.filter(assignee_id=self.request.user)


class ReviewingTaskList(generics.ListAPIView):
    """_summary_
    ReviewingTaskList is a custom view that handles the listing of tasks assigned to the user.
    Returns:
        _type_: _description_
    """
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Tasks.objects.filter(reviewer_id=self.request.user)


class TaskCommentList(generics.ListCreateAPIView):
    """_summary_
    TaskCommentList is a custom view that handles the listing and creation of task comments.
    Returns:
        _type_: _description_
    """
    permission_classes = [IsAuthenticated]
    serializer_class = TaskCommentSerializer

    def get_queryset(self):
        return TaskComments.objects.filter(task_id=self.kwargs['task_id'])

    def perform_create(self, serializer):
        task = get_object_or_404(Tasks, id=self.kwargs['task_id'])
        serializer.save(task=task, user=self.request.user)
        
    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except Http404:
            return Response(
                {"error": f"Task with id {self.kwargs['task_id']} does not exist"},
                status=status.HTTP_404_NOT_FOUND
            )


class TaskCommentDetail(generics.DestroyAPIView):
    """_summary_
    TaskCommentDetail is a custom view that handles the retrieval, update, and deletion of task comments.
    Returns:
        _type_: _description_
    """
    permission_classes = [IsAuthenticated]
    queryset = TaskComments.objects.all()
