from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta(object):
        model = User
        fields = 'username','email','password','password2'
        extra_kwargs={
            'password':{'write_only':True},
        }

    def save(self):
        account=User(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
        )
        password=self.validated_data['password']
        password2=self.validated_data['password2']
        if password!=password2:
            raise serializers.ValidationError({'password':'password does not match'})
        account.password = make_password(password)
        account.save()
        return account

