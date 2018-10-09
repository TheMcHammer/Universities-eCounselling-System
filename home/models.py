from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class UserProfile(models.Model):
    gender = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    user_type = (
        ('Student','Student'),
        ('Counsellor','Counsellor'),
        ('Counsellor','Dean'),
        ('Lecturer','Lecturer')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    university = models.CharField(max_length=200, default='')
    user_type = models.CharField(max_length=100, choices=user_type)
    gender = models.CharField(max_length=100, choices=gender)

    def __str__(self):
        return self.user.username

    def create_profile(sender, **kwargs):
        if kwargs['created']:
            user_profile = UserProfile.objects.create(user=kwargs['instance'])

    post_save.connect(create_profile, sender=User)

