from django.db import models
from django.utils import timezone

class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class SoftDeleteModel(models.Model):
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = SoftDeleteManager()
    all_objects = SoftDeleteManager()

    def _soft_delete(self):
        """ Marca o objeto como deletado sem removê-lo do banco. """
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()


    def restore(self):
        """ Restaura o objeto deletado. """
        self.is_deleted = False
        self.deleted_at = None
        self.save()

    def delete(self, *args, **kwargs):
        self._soft_delete()

    class Meta:
        abstract = True

