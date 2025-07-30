from django.db import models

# Create your models here.

class Province(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class District(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='districts')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Municipality(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='municipalities')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class SubMetropolitan(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='sub_metropolitans')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class RuralMunicipality(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='rural_municipalities')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
