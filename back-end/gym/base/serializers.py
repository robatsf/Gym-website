from rest_framework import serializers
from .models import userRegistration, membership

class userRegistrationSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model = userRegistration
        fields = '__all__'
        extra_kwargs={
            'password':{'write_only':True},
        }

        def save(self):
            password=self.validated_data['password']
            password2=self.validated_data['password2']
            if password != password2:
                raise serializers.ValidationError({'error':'password does not match'})
            else:
                if userRegistration.objects.filter(email=self.validated_data['email']).exists():
                    raise serializers.ValidationError({'error':'email already exists'})
            account=userRegistration(username=self.validated_data['username'],email=self.validated_data['email'],password=self.validated_data['password'])
            account.set_password(account.password)
            account.save()
            return account

class membershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = membership
        fields = '__all__'