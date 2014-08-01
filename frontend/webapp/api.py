from models import *
import datetime, pytz
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def alert(req):
	res = HttpResponse()
	post = req.POST.keys()[0]
	d = json.loads(post)
	user = User.objects.get(apiKey=d['apiKey'])
	log = Log(apiKey=user)
	log.status_code = d['status_code']
	log.key = d['key']
	log.comment = d['comment']
	log.logged_on = datetime.datetime.now(pytz.timezone('US/Pacific'))
	log.save()
	return HttpResponse()

@csrf_exempt
def get_alerts(req):
	res = HttpResponse()
	print req.POST
	print req.GET
	post = req.POST.keys()[0]
	d = json.loads(post)
	user = User.objects.get(apiKey=d['apiKey'])
	log = Log.objects.filter(apiKey=user, key=d['key']).latest('logged_on')
	l = { 'key': log.key, 'status_code': log.status_code, 'comment': log.comment, 'logged_on': int(log.logged_on.strftime("%s")) }
	return HttpResponse(json.dumps(l))


