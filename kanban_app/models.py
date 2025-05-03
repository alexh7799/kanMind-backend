from django.db import models

# Create your models here.
class Boards(models.Model):
    title = models.CharField(max_length=100)
    members = models.ManyToManyField('auth.User', related_name='board_members')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class Tasks(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    board = models.ForeignKey(Boards, related_name='tasks', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[('to-do', 'To-Do'), ('in-progress', 'In-Progress'), ('review', 'Review'), ('done', 'Done')], default='to-do')
    priority = models.CharField(max_length=20, choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], default='medium')
    assignee = models.ForeignKey('auth.User', related_name='assigned_tasks', on_delete=models.CASCADE)
    reviewer = models.ForeignKey('auth.User', related_name='reviewed_tasks', on_delete=models.CASCADE, null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class TaskComments(models.Model):
    task = models.ForeignKey(Tasks, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.task.title}"