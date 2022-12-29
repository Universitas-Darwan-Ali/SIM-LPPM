from django.db import models

class Detil(models.Model):
    Laporan = models.CharField(max_length=255)
    Link = models.URLField()

    def __str__(self):
        return self.Laporan

    class Meta:
        verbose_name_plural = 'Detil'