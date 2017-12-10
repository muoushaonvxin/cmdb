from django.db import models
from users.models import UserProfile

# Create your models here.

class WebGroup(models.Model):
    name = models.CharField(max_length=64)
    brief = models.CharField(max_length=255, null=True, blank=True)
    owner = models.ForeignKey(UserProfile)
    admins = models.ManyToManyField(UserProfile, blank=True, related_name=u"group_admins")
    members = models.ManyToManyField(UserProfile, blank=True, related_name=u"group_members")
    max_members = models.IntegerField(default=200)


    def __str__(self):
        return self.name