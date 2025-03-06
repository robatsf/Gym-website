from django.shortcuts import render
from base.models import userRegistration, membership
from base.serializers import userRegistrationSerializer, membershipSerializer
from rest_framework import generics


class userview(generics.ListCreateAPIView):
    queryset = userRegistration.objects.all()
    serializer_class = userRegistrationSerializer

class userDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = userRegistration.objects.all()
    serializer_class = userRegistrationSerializer
    lookup_field='pk'

class membershipview(generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = membership.objects.all()
    serializer_class = membershipSerializer

class membershipDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = membership.objects.all()
    serializer_class = membershipSerializer
    lookup_field='pk'