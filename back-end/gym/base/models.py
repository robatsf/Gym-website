from django.db import models
from django.contrib.auth.models import User
from datetime import date, timedelta,time



class subscriptionPlan(models.Model):
    DURATION_CHOICES = [
        ('1_month', '1 Month'),
        ('3_months', '3 Months'),
        ('6_months', '6 Months'),
        ('1_year', '1 Year'),
    ]

    name=models.CharField(max_length=20,choices=DURATION_CHOICES,unique=True)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    duration=models.IntegerField()

    def __str__(self):
        return self.name

class subscription(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    plan=models.ForeignKey(subscriptionPlan,on_delete=models.SET_NULL,null=True)
    start_date=models.DateField(auto_now_add=True)
    end_date=models.DateField()

    def save(self,*args, **kwargs):
        if not self.end_date:
            self.end_date = date.today()+timedelta(days=self.plan.duration)
            super().save(*args,**kwargs)
    
    def __str__(self):
        return f"{self.user.username}-{self.plan.name}"