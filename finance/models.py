from django.db import models


class Tax(models.Model):
    tax_name = models.CharField(max_length=20)
    tax_percentage = models.FloatField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}  {} %'.format(str(self.tax_name),(self.tax_percentage))
