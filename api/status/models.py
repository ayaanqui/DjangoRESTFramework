from django.db import models
from django.contrib.auth.models import User

def upload_status_image(instance, filename):
    return f"{instance.user.username}/{filename}"

""" class StatusQuerySet(models.QuerySet):
    pass

class StatusManage(models.Manager):
    def get_queryset(self):
        return StatusQuerySet(self.model, using=self._db) """

class Status(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to=upload_status_image, blank=True, null=True) # Django Storages --> AWS S3
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    # objects = StatusManage()

    def __str__(self):
        return str(self.content)[:50]
    
    class Meta:
        verbose_name = "Status post"
        verbose_name_plural = "Status posts"