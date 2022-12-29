from django.db import models

class Bantuan(models.Model):
    keterangan = models.CharField(max_length=255)
    link = models.URLField()

    def __str__(self):
        return self.keterangan

    class Meta:
        verbose_name_plural = 'Bantuan'