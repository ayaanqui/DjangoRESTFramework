import json
from django.db import models
from django.contrib.auth.models import User
from django.core.serializers import serialize

def upload_update_image(instance, filename):
    return f'updates/{instance.user}/{filename}'

class UpdatesQuerySet(models.QuerySet):
    def serialize(self):
        listValues = list(self.values('id', 'user', 'content', 'image'))
        return json.dumps(listValues)

class UpdatesManager(models.Manager):
    def get_queryset(self):
        return UpdatesQuerySet(self.model, using=self.db)

class Updates(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to=upload_update_image, blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    objects = UpdatesManager()

    def __str__(self):
        return self.content

    def serialize(self):
        try:
            image = self.image.url
        except:
            image = ""
        data = {
            'id': self.id,
            'content': self.content,
            'user': self.user.id,
            'image': image
        }
        return json.dumps(data)

    class Meta:
        verbose_name_plural = 'Updates'