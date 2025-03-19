from django.conf import settings
from django.shortcuts import render
from rest_framework.decorators import api_view
from . serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status,viewsets
from django.shortcuts import get_object_or_404
from .models import subscription,subscriptionPlan
from .serializers import subscriptionPlanSerializer,subscriptionserializer
from django.core.mail import send_mail
from datetime import date, timedelta

@api_view(['POST'])
def login(request):
    user=get_object_or_404(User, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response({"detail":"incorrect password."},status=status.HTTP_404_NOT_FOUND)
    token, created=Token.objects.get_or_create(user=user)
    serializer=UserSerializer(instance=user)
    return Response({"token":token.key,"user":serializer.data})

@api_view(['POST'])
def signup(request):
    serializer=UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token=Token.objects.create(user=user)
        return Response({"token":token.key,"user":serializer.data})
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class SubscriptionPlanViewSet(viewsets.ModelViewSet):
    queryset=subscriptionPlan.objects.all()
    serializer_class=subscriptionPlanSerializer

@api_view(['POST'])
def subscribe(request):
    user = request.user  

    if not user or not user.is_authenticated:
        return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

    plan_id = request.data.get('plan_id')

    try:
        # Get subscription plan
        plan = subscriptionPlan.objects.get(id=plan_id)

        # Check if user already has a subscription
        user_subscription, created = subscription.objects.get_or_create(user=user)

        # Update subscription details
        user_subscription.plan = plan
        user_subscription.start_date = date.today()
        user_subscription.end_date = date.today() + timedelta(days=plan.duration)
        user_subscription.save()

        # Send Email Notification
        send_mail(
            "Subscription Successful",
            f"Hello {user.username},\n\nYou have successfully subscribed to {plan.name}.",
            settings.EMAIL_HOST_USER,
            [user.email, settings.ADMIN_EMAIL],
            fail_silently=False,
        )

        return Response({"message": "Subscription successful"}, status=status.HTTP_201_CREATED)

    except subscriptionPlan.DoesNotExist:
        return Response({"error": "Plan not found"}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)