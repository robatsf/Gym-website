from rest_framework import serializers
from .models import userRegistration, membership
from django.contrib.auth.hashers import make_password

class userRegistrationSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model = userRegistration
        fields = 'username','email','password','password2'
        extra_kwargs={
            'password':{'write_only':True},
        }

    def save(self):
        account=userRegistration(
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

class membershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = membership
        fields = '__all__'