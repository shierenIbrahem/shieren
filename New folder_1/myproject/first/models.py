from django.db import models
from django.utils import timezone
# Create your models here.
class User(models.Model):
	username=models.CharField(max_length=50,null=False,blank=False)
	password=models.CharField(max_length=50,null=False,blank=False)
	ssn=models.IntegerField()
	#ready_passport=models.BooleanField()
	#ready_moving=models.BooleanField()
	#ready_staying=models.BooleanField()

class ready(models.Model):
	ssn=models.IntegerField()
	ready=models.IntegerField()


class PassPort(models.Model):
	internal=models.IntegerField()
	normal=models.IntegerField()
	date=models.DateField(default=timezone.now)
	owner=models.ForeignKey(User,on_delete=models.CASCADE)
	confirm=models.BooleanField(default=True)
	#available=models.BooleanField(default=True)

class Moving(models.Model):
	date=models.DateField(default=timezone.now)
	#available=models.BooleanField(default=True)
	owner=models.ForeignKey(User,on_delete=models.CASCADE)
	confirm=models.BooleanField(default=True)

class Staying(models.Model):
	date=models.DateField(default=timezone.now)
	#available=models.BooleanField(default=True)
	owner=models.ForeignKey(User,on_delete=models.CASCADE)
	confirm=models.BooleanField(default=True)

class Holiday(models.Model):
	name=models.CharField(max_length=100,null=False,blank=False)
	date=models.DateField()

class LimitsOfDate(models.Model):
	old_min=models.DateField()
	old_max=models.DateField()
	new_min=models.DateField()
	new_max=models.DateField()

class information(models.Model):
	id_=models.IntegerField()
	duration=models.IntegerField()
	cost=models.FloatField()
	
class Pappers(models.Model):
	id_=models.IntegerField()
	text=models.TextField()
