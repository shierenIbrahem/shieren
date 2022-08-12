from django.shortcuts import render,redirect
from .models import User,Moving,Staying,PassPort,Holiday,LimitsOfDate,Pappers
from django.contrib import  messages
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime,date
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import time
import schedule



def job():
	print('--------------------')
	today=date.today()
	PassPort.objects.filter(date=today).delete()
	Moving.objects.filter(date=today).delete()
	Staying.objects.filter(date=today).delete()

#schedule.every(10).seconds.do(job)
schedule.every().day.at("23:59").do(job)
while True:
	schedule.run_pending()
	time.sleep(1)

def any_holiday():
	today=date.today()
	tomorrow=today+timedelta(days=1)
	try:
		is_holiday=Holiday.objects.get(date=tomorrow)
		passports=PassPort.objects.filter(date=tomorrow)
		movings=Moving.objects.filter(date=tomorrow)
		stayings=Staying.objects.filter(date=tomorrow)
		fill_passport(passports)
		fill_moving(movings)
		fill_staying(stayings)

	except:
		pass

schedule.every(1).hours.do(any_holiday)
while True:
	schedule.run_pending()
	time.sleep(1)

def fill_passport(lt):
	for x in lt:
		i=1
		b=True
		while b:
			day=tomorrow+timedelta(days=i)
			try:
				is_holiday=Holiday.objects.get(date=tomorrow)
				i=i+1
			except:
				count=PassPort.objects.filter(date=date).count()
				if count<50 :
					x.date=day
					x.confirm=False
					b=false
					PassPort.objects.get(owner=x.user).delete()
					x.save()
				else:
					i=i+1

def fill_moving(lt):
	for x in lt:
		i=1
		b=True
		while b:
			day=tomorrow+timedelta(days=i)
			try:
				is_holiday=Holiday.objects.get(date=tomorrow)
				i=i+1
			except:
				count=Moving.objects.filter(date=date).count()
				if count<50 :
					x.date=day
					x.confirm=False
					b=false
					Moving.objects.get(owner=x.user).delete()
					x.save()
				else:
					i=i+1

def fill_staying(lt):
	for x in lt:
		i=1
		b=True
		while b:
			day=tomorrow+timedelta(days=i)
			try:
				is_holiday=Holiday.objects.get(date=tomorrow)
				i=i+1
			except:
				count=Staying.objects.filter(date=date).count()
				if count<50 :
					x.date=day
					x.confirm=False
					b=false
					Staying.objects.get(owner=x.user).delete()
					x.save()
				else:
					i=i+1


@csrf_exempt
def notification(request):
	if request.method == 'POST':
		decoded_body=request.body.decode('utf-8')
		body=json.loads(decoded_body)
		print(body)
		ssn=body['ssn']
		try:
			user=User.objects.get(ssn=ssn)

			ready=ready.objects.filter(ssn=ssn)
			ready_passport=False
			ready_moving=False
			ready_staying=False

			for obj in ready:
				if obj.ready == 1:
					ready_passport=True
				elif ojb.ready == 2:
					ready_moving=True
				else :
					ready_staying=True

			confirm_passport=True
			try:
				confirm_passport=PassPort.objects.get(owner=user).confirm
			except :
				pass
			confirm_moving=True
			try:
				confirm_moving=Moving.objects.get(owner=user).confirm
			except :
				pass
			confirm_staying=True
			try:
				confirm_staying=Staying.objects.get(owner=user).confirm
			except :
				pass

			passport_date=None
			moving_date=None
			staying_date=None

			if confirm_passport == False :
				passport_date=PassPort.objects.get(owner=user).date

			if confirm_moving == False :
				moving_date=Moving.objects.get(owner=user).date

			if confirm_staying == False :
				staying_date=Staying.objects.get(owner=user).date

			return JsonResponse({'result':'true','staying_date':staying_date,'moving_date':moving_date,'passport_date':passport_date,'ready_passport':ready_passport,'ready_moving':ready_moving,'ready_staying':ready_staying,'confirm_passport':confirm_passport,'confirm_moving':confirm_moving,'confirm_staying':confirm_staying}) 
		except :
			return JsonResponse({'result':'false'})

@csrf_exempt
def confirm_passport(request):
	if request.method == 'POST':
                decoded_body=request.body.decode('utf-8')
                body=json.loads(decoded_body)
                print(decoded_body)
                ssn=body['ssn']
                user=User.objects.get(ssn=ssn)
                passport=PassPort.objects.get(owner=user)
                passport.confirm=True
                PassPort.objects.get(owner=user).delete()
                passport.save()

@csrf_exempt
def confirm_moving(request):
	if request.method == 'POST':
                decoded_body=request.body.decode('utf-8')
                body=json.loads(decoded_body)
                print(decoded_body)
                ssn=body['ssn']
                user=User.objects.get(ssn=ssn)
                moving=Moving.objects.get(owner=user)
                moving.confirm=True
                Moving.objects.get(owner=user).delete()
                moving.save()

@csrf_exempt
def confirm_staying(request):
	if request.method == 'POST':
                decoded_body=request.body.decode('utf-8')
                body=json.loads(decoded_body)
                print(decoded_body)
                ssn=body['ssn']
                user=User.objects.get(ssn=ssn)
                staying=Staying.objects.get(owner=user)
                staying.confirm=True
                Staying.objects.get(owner=user).delete()
                staying.save()              

@csrf_exempt
def login(request):
	if request.method == 'POST':
                decoded_body=request.body.decode('utf-8')
                body=json.loads(decoded_body)
                print(decoded_body)
                password=body['password']
                ssn=body['ssn']
                try:
                        user=User.objects.get(ssn=ssn)
                        try:
                                user=User.objects.get(password=password,ssn=ssn)
                                user_asJson=getAsJson(user)
                                del user_asJson['_state']
                                user_asJson['result']='true'
                                mn=LimitsOfDate.objects.last().new_min
								mx=LimitsOfDate.objects.last().new_max
								user_asJson['mn']=mn
								user_asJson['mx']=mx
                                return JsonResponse(user_asJson,safe=False)
                        except:
                               return JsonResponse({'result':'error password'}) 
                except:
                        return JsonResponse({'result':'error ssn'})
                
               # return JsonResponse({'result':'false'})
@csrf_exempt
def signup(request):
	if request.method == 'POST':
		decoded_body=request.body.decode('utf-8')
		body=json.loads(decoded_body)
		print(body)
		password=body['password']
		ssn=body['ssn']
		name=body['name']
		try:
			user=User.objects.get(ssn=ssn)
			return JsonResponse({'result':'exists ssn'}) 
		except :
			user=User(username=name,password=password,ssn=ssn)
			user.save()
			user_asJson=getAsJson(user)
			del user_asJson['_state']
			user_asJson['result']='true'
			mn=LimitsOfDate.objects.last().new_min
			mx=LimitsOfDate.objects.last().new_max
			user_asJson['mn']=mn
			user_asJson['mx']=mx
			return JsonResponse(user_asJson,safe=False)


	
@csrf_exempt
def forgetten_password(request):
	if request.method == 'POST':
				decoded_body=request.body.decode('utf-8')
				body=json.loads(decoded_body)
				print(body)
				ssn=body['ssn']
				try:
					password=User.objects.get(ssn=ssn).password
					print(password)
					password_asJson=getAsJson(password)
					return JsonResponse({'result':'true','password':password})
				except :
					return JsonResponse({'result':'false1'})
				


def pass_port_count(request):
	if request.method == 'POST':
				decoded_body=request.body.decode('utf-8')
				body=json.loads(decoded_body)
				ssn=body['ssn']
				user=User.objects.get(ssn=ssn)
				try:
					passports=PassPort.objects.get(owner=user)
					passpprts_asJson=getAsJson(passports)
					del passports_asJson['_state']
					return JsonResponse(passports_asJson,safe=False)
				except:
					return JsonResponse({'result':'false'})
				return JsonResponse({'result':'false'})

def moving_count(request):
	if request.method == 'POST':
				decoded_body=request.body.decode('utf-8')
				body=json.loads(decoded_body)
				ssn=body['ssn']
				user=User.objects.get(ssn=ssn)
				try:
					movings=Moving.objects.get(owner=user)
					movings_asJson=getAsJson(movings)
					del movings_asJson['_state']
					return JsonResponse(movings_asJson,safe=False)
				except:
					return JsonResponse({'result':'false'})
				return JsonResponse({'result':'false'})

def staying_count(request):
	if request.method == 'POST':
				decoded_body=request.body.decode('utf-8')
				body=json.loads(decoded_body)
				ssn=body['ssn']
				user=User.objects.get(ssn=ssn)
				try:
					stayings=Staying.objects.get(owner=user)
					stayings_asJson=getAsJson(stayings)
					del stayings_asJson['_state']
					return JsonResponse(stayings_asJson,safe=False)
				except:
					return JsonResponse({'result':'false'})
				return JsonResponse({'result':'false'})


def pass_port_cancel(request):
	if request.method == 'POST':
				decoded_body=request.body.decode('utf-8')
				body=json.loads(decoded_body)
				ssn=body['ssn']
				user=User.objects.get(ssn=ssn)
				PassPort.objects.get(owner=user).delete()
				return JsonResponse({'result':'true'})
		


def moving_cancel(request):
	if request.method == 'POST':
				decoded_body=request.body.decode('utf-8')
				body=json.loads(decoded_body)
				ssn=body['ssn']
				user=User.objects.get(ssn=ssn)
				Moving.objects.get(owner=user).delete()
				return JsonResponse({'result':'true'})
		


def staying_cancel(request):
	if request.method == 'POST':
				decoded_body=request.body.decode('utf-8')
				body=json.loads(decoded_body)
				ssn=body['ssn']
				user=User.objects.get(ssn=ssn)
				Staying.objects.get(owner=user).delete()
				return JsonResponse({'result':'true'})
		



def getAsJson(obj):
	return json.loads(json.dumps(obj,default = lambda o:o.__dict__))


def services(request):
	return JsonResponse({'result':'true'})

@csrf_exempt	
def bookPassport(request):
	if request.method == 'POST':
		decoded_body=request.body.decode('utf-8')
		body=json.loads(decoded_body)
		print(body)
		interal=body['passportType']
		normal=body['passportPriority']
		date=body['bookingDate']
		print(date)
		print('_____________________')
		#date=to_date(body['bookingDate'])
		
		result=valid_date(date)
		if result != True :
			return JsonResponse(result)

		ssn=int(body['ssn'])
		user=User.objects.get(ssn=ssn)
		try:
			passport=PassPort.objects.get(owner=user)
			return JsonResponse({'result':'exists booking'})
		except:
			passports=PassPort.objects.filter(date=date)
			if passports.count()<50 :
				passport=PassPort(internal=interal,normal=normal,date=date,owner=user)
				passport.save()
				#passport_asJson=getAsJson(passport)
				#del passport_asJson['_state']
				#passport_asJson['result']='true'
				print('hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh')
				return JsonResponse({'result':'true'})
			else :
				return JsonResponse({'result':'invaled date'})
	#return JsonResponse({'result':'false','type':'1'})



def second_page(request):
	if request.method == 'POST':
		decoded_body=request.body.decode('utf-8')
		body=json.loads(decoded_body)

		date=to_date(body['date'])
		result=valid_date(date)
		if result != True :
			return JsonResponse(result)

		ssn=int(body['ssn'])
		user=User.objects.get(ssn=ssn)
		try:
			moving=Moving.objects.get(owner=user)
			return JsonResponse({'result':'false','type':'2'})
		except:
			movings=Moving.objects.filter(date=date)
			if movings.count()<50:
				moving=Moving(date=date,owner=user)
				moving.save()
				moving_asJson=getAsJson(moving)
				del moving_asJson['_state']
				return JsonResponse(moving_asJson,safe=False)
			else :
				return JsonResponse({'result':'false','type':'1'})
	return JsonResponse({'result':'false','type':'1'})

def third_page(request):
	if request.method == 'POST':
		decoded_body=request.body.decode('utf-8')
		body=json.loads(decoded_body)

		date=to_date(body['date'])
		result=valid_date(date)
		if result != True :
			return JsonResponse(result)

		ssn=int(body['ssn'])
		user=User.objects.get(ssn=ssn)
		try:
			staying=Staying.objects.get(owner=user)
			return JsonResponse({'result':'false','type':'2'})
		except:
			stayings=Staying.objects.filter(date=date)
			if stayings.count()<50:
				staying=Staying(date=date,owner=user)
				staying.save()
				staying_asJson=getAsJson(staying)
				del staying_asJson['_state']
				return JsonResponse(staying_asJson,safe=False)
			else :
				return JsonResponse({'result':'false','type':'1'})
	return JsonResponse({'result':'false','type':'1'})


def four_page(request):
	if request.method == 'POST':
		try:
			pappers=Pappers.objects.all()
			pappers_asJson=getAsJson(pappers)
			del pappers_asJson['_state']
			return JsonResponse(pappers_asJson,safe=False)
		except:
			return JsonResponse({'result':'false'})
	return JsonResponse({'result':'false'})




#def to_date(d):
        
#	return datetime.strptime(d,'%m/-%d/-%Y')
def to_date(d):
        d=d.strftime("%Y-%m-%d")
        return d
#datetime.strptime(d,'%Y-%m-%d')


def valid_date(date):
	try:
                date=datetime.strptime(str(date),'%Y-%m-%d')
                is_holiday=Holiday.objects.get(date=date)
                return {'result':'false','type':'1'}
	except:
		return True
		#today=date.today()
		#today=today.strftime("%Y-%m-%d")
		#today=datetime.strptime(str(today),'%Y-%m-%d')
		#date=date.strftime("%Y-%m-%d")
		#date=datetime.strptime(date,'%Y-%m-%d')

		#if (date-today).days > 365:
			#return {'result':'false','type':'1'}
			
		#mn=LimitsOfDate.objects.all().last().new_min
		#mx=LimitsOfDate.objects.all().last().new_max

		#mn=datetime.strptime(str(mn),'%Y-%m-%d')
		#mn=datetime.strptime(mn,'%Y-%m-%d')
		#mx=datetime.strptime(str(mx),'%Y-%m-%d')
		#mx=datetime.strptime(mx,'%Y-%m-%d')

		#if date<mn or date >mn:
		#	return {'result':'false','type':'1'}
	





