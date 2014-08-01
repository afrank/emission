from django.db import models

class User(models.Model):
	apiKey = models.CharField(max_length=64)
	apiKey.primary_key = True
	notify_email = models.CharField(max_length=128)
	created_on = models.DateTimeField('date created')

class Log(models.Model):
	id = models.IntegerField()
	id.primary_key = True
	apiKey = models.ForeignKey(User)
	logged_on = models.DateTimeField('date logged')
	status_code = models.IntegerField()
	comment = models.CharField(max_length=255)
	key = models.CharField(max_length=128)

