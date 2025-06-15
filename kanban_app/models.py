from django.db import models


class Boards(models.Model):
    """_summary_
    Boards is a model that represents a board in the Kanban application.
    Returns:
        _type_: _description_
    """
    title = models.CharField(max_length=100)
    members = models.ManyToManyField('auth.User', related_name='board_members')
    owner_id = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='owned_boards'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Tasks(models.Model):
    """_summary_
    Tasks is a model that represents a task in the Kanban application.
    Returns:
        _type_: _description_
    """
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    board = models.ForeignKey(
        Boards, related_name='tasks', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[(
        'to-do', 'To-Do'), ('in-progress', 'In-Progress'), ('review', 'Review'), ('done', 'Done')], default='to-do')
    priority = models.CharField(max_length=20, choices=[(
        'low', 'Low'), ('medium', 'Medium'), ('high', 'High')], default='medium')
    assignee_id = models.ForeignKey(
        'auth.User', related_name='assigned_tasks', on_delete=models.CASCADE, null=True, blank=True)
    reviewer_id = models.ForeignKey(
        'auth.User', related_name='reviewed_tasks', on_delete=models.CASCADE, null=False, blank=False)
    due_date = models.CharField(max_length=80, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class TaskComments(models.Model):
    """_summary_
    TaskComments is a model that represents comments on tasks.
    Returns:
        _type_: _description_
    """
    task = models.ForeignKey(
        Tasks, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(
        'auth.User', related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def author(self):
        return f"{self.user.first_name} {self.user.last_name}"

    def __str__(self):
        return f"Comment by {self.user.username} on {self.task.title}"
