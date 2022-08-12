from .models import User
from django_cron import CronJobBadse, Schedule



def my_scheduled_job():
	User.objects.create(username1='a',password='123',ssn=123)

class MyCronJob(CronJobBadse):
	RUN_EVERY_MINS =1

	schedule= Schedule(run_every_mins=RUN_EVERY_MINS)
	code ='my_app.my_cron_job'

	def do(self):
		User.objects.create(username1='a',password='123',ssn=123)