from django.db import models

# Create your models here.
class GeoLocation(models.Model):
    geo_id = models.AutoField(primary_key=True)
    geo_heading = models.CharField(max_length=250)
    geo_body = models.TextField()
