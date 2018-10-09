from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
import datetime
import uuid

class Entry(models.Model):
    reason = (
       ('Career Guidance', 'Career Guidance'),
        ('Relationship Advice', 'Relationship Advice'),
        ('Grief Counselling', 'Grief Counselling'),
        ('other', 'other')
    )
    date = models.DateTimeField(("Date"), default=datetime.date.today)
    reason = models.CharField(max_length=150, choices=reason)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    task_id = models.CharField(max_length=50, blank=True, editable=False)
    confirmed = models.BooleanField(default=False)


    def get_absolute_url(self):
        return reverse('appointment:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return 'Entry #{0} - {1}'.format(self.pk, self.creator)

class Friend(models.Model):
    users = models.ManyToManyField(User)
    current_user = models.ForeignKey(User, related_name='owner', null=True)

    @classmethod
    def make_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.add(new_friend)

    @classmethod
    def loose_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.remove(new_friend)
#class EntryInstance(models.Model):
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          #help_text='Unique ID for this particular entry in all appointments')
    #entry = models.ForeignKey('Entry', on_delete=models.SET_NULL, null=True)



    #def __str__(self):
        #return f'{self.id} ({self.entry.name})'