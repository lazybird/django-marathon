from django.db import models


class Lock(models.Model):
    """
    This Lock model represents a lock entity in your database.
    Each lock has a unique name and a timestamp that indicates when it was locked.
    """

    name = models.CharField(max_length=255, unique=True)
    locked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
