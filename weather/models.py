from django.db import models

# Create your models here.

class City(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        # shows an actual string representation of the city name.
        return self.name

    class Meta:
        # Makes the plural of city, cities instead of citys.
        verbose_name_plural = 'cities'