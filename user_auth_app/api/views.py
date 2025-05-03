from rest_framework import generics
from user_auth_app.models import UserProfile
from .serializers import UserProfileSerializer, RegistrationSerializer
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken

class UserProfileList(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    
class UserProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    
class RegistrationView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        
        data = {}
        if serializer.is_valid():
            saved_account = serializer.save()
            token, created = Token.objects.get_or_create(user=saved_account)
            data = {
                'token': token.key,
                'user_id': saved_account.id,
                'email': saved_account.email,
                'fullname': saved_account.first_name + ' ' + saved_account.last_name
            }
        else:
            data=serializer.errors
            
        return Response(data)
    
class CustomLoginView(ObtainAuthToken):
    permission_classes = [AllowAny]
    
    
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        modified_data = {
            'username': email,
            'password': password
        }
        serializer = self.serializer_class(data=modified_data)
        
        data = {}
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            data = {
                'token': token.key,
                'user_id': user.id,
                'email': user.email,
                'fullname': user.first_name + ' ' + user.last_name
            }
        else:
            data=serializer.errors
            
        return Response(data)