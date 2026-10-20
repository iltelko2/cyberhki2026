from django.contrib.auth import get_user_model
from django.db import connection
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .models import questions


def find_topic(tid):
	for q in questions:
		if q['id'] == tid:
			return q
	return None


def quizView(request, tid):
	topic = find_topic(tid)
	if topic is None:
		return redirect('/cheater/')

	request.session['topic'] = tid
	request.session['level'] = 0
	request.session['locked'] = False
	request.session['finished'] = False
	return render(request, 'pages/question.html', {'topic': topic, 'question': topic['questions'][0]})


def answerView(request, tid, aid):
	topic = find_topic(tid)
	if topic is None:
		return redirect('/cheater/')

	if request.session.get('locked') or request.session.get('finished'):
		return redirect('/cheater/')

	if request.session.get('topic') != tid:
		return redirect('/cheater/')

	level = request.session.get('level', 0)
	if level < 0 or level >= len(topic['questions']):
		return redirect('/cheater/')

	if topic['questions'][level]['correct'] == aid:
		level += 1
		request.session['level'] = level

		if level == len(topic['questions']):
			request.session['finished'] = True
			return redirect('/finish/')

		return render(request, 'pages/question.html', {'topic': topic, 'question': topic['questions'][level]})

	request.session['locked'] = True
	return redirect('/incorrect/')


def incorrectView(request):
	return render(request, 'pages/incorrect.html')


def finishView(request):
	if not request.session.get('finished'):
		return redirect('/cheater/')
	return render(request, 'pages/finish.html')


def cheaterView(request):
	return render(request, 'pages/cheater.html')


def thanksView(request):
	if not request.session.get('finished'):
		return redirect('/cheater/')
	# Like we were going to pay anyone
	return render(request, 'pages/thanks.html')


def topicView(request, tid):
	topic = find_topic(tid)
	return render(request, 'pages/topic.html', {'topic': topic})


def topicsView(request):
	return render(request, 'pages/topics.html', {'questions': questions})


def securityOverviewView(request):
	flaws = [
		{'name': 'Broken Access Control', 'url': '/security/admin-data/?user=admin'},
		{'name': 'Cryptographic Failures', 'url': '/security/crypto/?api_key=plain-text-secret'},
		{'name': 'Injection', 'url': '/security/search/?term=admin%27%20OR%201%3D1'},
		{'name': 'Identification and Authentication Failures', 'url': '/security/login/'},
		{'name': 'Security Logging and Monitoring Failures', 'url': '/security/logging/?username=admin'},
	]
	return render(request, 'pages/security_demo.html', {'flaws': flaws})


def securityAdminDataView(request):
	user = request.GET.get('user', '')
	if user == 'admin':
		# FIX FOR BROKEN ACCESS CONTROL (#1):
		# if not request.session.get('is_authenticated'):
		#     return HttpResponseForbidden('Forbidden')
		# if request.GET.get('user') != request.session.get('username'):
		#     return HttpResponseForbidden('Forbidden')
		return HttpResponse('admin secret data...')
	return HttpResponse('No data available.')


def securityCryptoView(request):
	api_key = request.GET.get('api_key', '')
	
	if api_key == 'plain-text-secret':
		return HttpResponse('API access granted.')
	return HttpResponse('Access denied')


def securitySearchView(request):
	term = request.GET.get('term', '')
	with connection.cursor() as cursor:
		cursor.execute('CREATE TABLE IF NOT EXISTS logs (id INTEGER PRIMARY KEY AUTOINCREMENT, message TEXT)')
		cursor.execute('SELECT COUNT(*) FROM logs')
		if cursor.fetchone()[0] == 0:
			cursor.execute('INSERT INTO logs (message) VALUES (?)', ('joku login',))
			cursor.execute('INSERT INTO logs (message) VALUES (?)', ('admin loggasi',))
			cursor.execute('INSERT INTO logs (message) VALUES (?)', ('jotain sensitiivistä tapahtui',))
		query = "SELECT id, message FROM logs WHERE message LIKE '%" + term + "%'"
		cursor.execute(query)
		results = cursor.fetchall()

		# FIX FOR SQL INJECTION (#3):
		# cursor.execute('SELECT id, message FROM logs WHERE message LIKE %s', ('%' + term + '%',))
		# results = cursor.fetchall()
	return HttpResponse('Results for "' + term + '": ' + str(results))


def securityLoginView(request):
	if request.method == 'POST':
		username = request.POST.get('username', '')
		password = request.POST.get('password', '')
		# FLAW 4 FIX: uncomment this block, then comment out the vulnerable
		# username lookup and hard-coded password check below.
		# from django.contrib.auth import authenticate, login
		# user = authenticate(request, username=username, password=password)
		# if user is None:
		#     return HttpResponse('Invalid credentials')
		# login(request, user)
		# return HttpResponse(f'Welcome, {user.username}!')

		user = get_user_model().objects.filter(username=username).first()
		if user is None or password != 'password':
			return HttpResponse('Invalid credentials')
		request.session['username'] = user.username
		request.session['is_authenticated'] = True
		return HttpResponse(f'Welcome, {user.username}!')
	return render(request, 'pages/security_login.html')


def securityLoggingView(request):
	username = request.GET.get('username', 'unknown')
	if username.lower() == 'admin':
		# FIX FOR SECURITY LOGGING AND MONITORING FAILURES (#5):
		#import logging
		#logger = logging.getLogger('security.audit')
		#logger.warning('Sensitive admin page viewed', extra={'username': username, 'remote_addr': request.META.get('REMOTE_ADDR', '')})
		return HttpResponse('Sensitive admin page (audited)')
	return HttpResponse(f'Regular user {username} viewed a profile, no monitoring.')
