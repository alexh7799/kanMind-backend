from rest_framework import serializers
from user_auth_app.models import UserProfile
from django.contrib.auth.models import User

"""_summary_
UserProfileSerializer is a serializer for the UserProfile model.
Returns:
    _type_: _description_   
"""
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user', 'bio', 'location']


"""_summary_
UserSerializer is a serializer for the User model.
Returns:
    _type_: _description_
"""
class UserSerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'fullname']

    def get_fullname(self, obj):
        return f"{obj.first_name} {obj.last_name}"


"""_summary_
RegistrationSerializer is a serializer for user registration.
Returns:
    _type_: _description_
"""
class RegistrationSerializer(serializers.ModelSerializer):
    repeated_password = serializers.CharField(write_only=True)
    fullname = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['fullname', 'email', 'password', 'repeated_password']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def validate_fullname(self, value):
        if len(value.split()) < 2:
            raise serializers.ValidationError(
                "your fullname must contain at least a first name and a last name")
        return value

    def saveUser(self, firstname, lastname, pw, email):
        account = User(
            username=email, email=self.validated_data['email'], first_name=firstname, last_name=lastname)
        account.set_password(pw)
        account.save()
        return account
    
    def save(self):
        fullname_parts = self.validated_data['fullname'].split(' ')
        firstname = fullname_parts[0]
        lastname = ' '.join(fullname_parts[1:])
        pw = self.validated_data['password']
        repeated_pw = self.validated_data['repeated_password']
        email = self.validated_data['email']
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {'error': "This email is already in use"})
        if pw != repeated_pw:
            raise serializers.ValidationError({'error': 'password dont match'})
        self.saveUser(firstname, lastname, pw, email)
        
