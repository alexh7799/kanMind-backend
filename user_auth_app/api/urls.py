from django.urls import path
from .views import UserProfileList, UserProfileDetail, CheckEmailView, RegistrationView, CustomLoginView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('profiles/', UserProfileList.as_view(), name='userprofile-list'),
    path('profiles/<int:pk>/', UserProfileDetail.as_view(),
         name='userprofile-detail'),
    path('email-check/', CheckEmailView.as_view(), name='email-check'),
]
