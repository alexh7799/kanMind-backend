"""
URL configuration for kanMind project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .views import (
    BoardList, 
    BoardDetail, 
    TaskList, 
    TaskDetail,
    AssignedTaskList,
    ReviewingTaskList,
    TaskCommentList,
    TaskCommentDetail
)

urlpatterns = [
    path('boards/', BoardList.as_view()),
    path('boards/<int:pk>/', BoardDetail.as_view()),
    path('email-check/<str:email>/', BoardDetail.as_view()),
    path('tasks/', TaskList.as_view()),
    path('tasks/<int:pk>/', TaskDetail.as_view()),
    path('tasks/assigned-to-me/', AssignedTaskList.as_view()),
    path('tasks/reviewing/', ReviewingTaskList.as_view()),
    path('tasks/<int:task_id>/comments/', TaskCommentList.as_view()),
    path('tasks/<int:task_id>/comments/<int:pk>/', TaskCommentDetail.as_view()),
]