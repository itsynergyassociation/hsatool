from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class PredictModel(models.Model):
    pred_id = models.CharField(unique=True, max_length=100, null=True, blank=True, default=None)

    Global_radiation = models.FloatField()
    Surface_temperature = models.FloatField()
    Air_temperature = models.FloatField()
    Relative_Humidity = models.FloatField()
    Wind_speed = models.FloatField()
    Tmrt = models.FloatField(blank=True, null=True)
    PMV = models.FloatField(blank=True, null=True)
    PET = models.FloatField(blank=True, null=True)

    TmrtColor = models.CharField(max_length=200, default='white')
    PMVColor = models.CharField(max_length=200, default='white')
    PETColor = models.CharField(max_length=200, default='white')

    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)

    def save(self, *args, **kwargs):
        if self.pred_id is None and self.created:
            self.pred_id = self.created.strftime("%Y%m%d") + '-' + self.created.strftime("%H:%M")
        return super().save(*args, **kwargs)

    def __str__(self):
        return str(self.pred_id)


class TMRTParams(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ## TMRT
    vlow = models.IntegerField(default=10)
    low = models.IntegerField(default=25)
    medium = models.IntegerField(default=40)
    high = models.IntegerField(default=55)
    vhigh = models.IntegerField(default=55)


class PMVParams(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ## PMV
    hot = models.IntegerField(default=3)
    warm = models.IntegerField(default=2)
    slwarm = models.IntegerField(default=1)
    neutral = models.IntegerField(default=0)
    slcool = models.IntegerField(default=-1)
    cool = models.IntegerField(default=-2)
    cold = models.IntegerField(default=-3)


class PETParams(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ## PET
    vcold = models.IntegerField(default=4)
    cold = models.IntegerField(default=8)
    cool = models.IntegerField(default=13)
    slcool = models.IntegerField(default=18)
    comfort = models.IntegerField(default=23)
    slwarm = models.IntegerField(default=29)
    warm = models.IntegerField(default=35)
    hot = models.IntegerField(default=41)
    vhot = models.IntegerField(default=41)
