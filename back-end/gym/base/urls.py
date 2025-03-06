from django.urls import path
from . import views

urlpatterns = [
    path('user/', views.userview.as_view()),
    path('user/<int:pk>', views.userDetail.as_view()),
    path('membership/', views.membershipview.as_view()),
    path('membership/<int:pk>', views.membershipDetail.as_view()),
]
