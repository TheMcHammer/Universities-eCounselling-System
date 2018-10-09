from django.db import models


class CounselRoom(models.Model):
    """Represents chat rooms that user has been invited to"""
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    slug = models.CharField(max_length=50)

    def __str__(self):
        """Returns human-readable representation of the model instance."""
        return self.name