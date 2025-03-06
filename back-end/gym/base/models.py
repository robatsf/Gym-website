from django.db import models



class userRegistration(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username

class membership(models.Model):
    user = models.ForeignKey(userRegistration, on_delete=models.CASCADE)
    plan = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    
    def __str__(self):
        return self.plan