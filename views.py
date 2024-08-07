import os

from django.urls import reverse
from django.db.models import Sum
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseNotFound, JsonResponse, FileResponse

from .models import *

# Create your views here.
def index(request):
	slides = Slideshow.objects.all()[0:5]
	sliden = slides.count()
	pubs = Publication.objects.all()[0:5]
	posts = Post.objects.filter(approve=1)[0:8]
	introduce = Option.objects.filter(name='introduce').first()
	interest = Option.objects.filter(name='interest').first()
	supports = Option.objects.filter(name='supports')

	return render(request, 'big/index.html', {
		'slides': slides,
		'sliden': sliden,
		'pubs': pubs,
		'posts': posts,
		'introduce': introduce,
		'interest': interest,
		'supports': supports,
	})

def news(request):
	post_list = Post.objects.filter(approve=1)
	paginator = Paginator(post_list, 10)
	page = request.GET.get('page')
	posts = paginator.get_page(page)
	return render(request, 'big/news.html', {
		'posts': posts,
	})

def post(request, slug):
	post = Post.objects.get(slug=slug)
	return render(request, 'big/post.html', {
		'post': post,
	})

def publication(request):
	researches = Publication.objects.all()
	return render(request, 'big/publication.html', {
		'researches': researches,
	})

def member(request, uname=None):
	if uname is None:
		faculties = Member.objects.filter(position=4)
		postgraduates = Member.objects.filter(position=1, status=1)
		undergraduates = Member.objects.filter(position=2, status=1)
		graduates = Member.objects.filter(status=2)
		return render(request, 'big/team.html', {
			'faculties': faculties,
			'postgraduates': postgraduates,
			'undergraduates': undergraduates,
			'graduates': graduates,
		})
	else:
		try:
			member = Member.objects.get(uname=uname)
		except:
			return HttpResponseNotFound("{} does not exists in our research group".format(uname))

		return render(request, 'big/member.html', {'member':member})

def research(request):
	researches = Research.objects.all()
	return render(request, 'big/research.html', {'researches': researches})

def softwares(request):
	software_list = Software.objects.all()
	paginator = Paginator(software_list, 10)
	page = request.GET.get('page')
	softwares = paginator.get_page(page)
	return render(request, 'big/softwares.html', {
		'softwares': softwares,
	})

def software(request, sname):
	try:
		software = Software.objects.get(short=sname)
	except:
		return HttpResponseNotFound("Could not find software {}".format(sname))

	versions = Version.objects.filter(software=software)

	try:
		latest = versions.order_by('-created').first()
		downloads = Download.objects.filter(version=latest, represent=True).order_by('system')
	except:
		downloads = None
		latest = None

	return render(request, 'big/software.html', {
		'software': software,
		'versions': versions,
		'latest': latest,
		'downloads': downloads
	})

def download(request, downid, sname):
	downid = int(downid)
	dlfile = Download.objects.get(pk=downid)
	return FileResponse(
		open(dlfile.file.path, 'rb'),
		as_attachment = True,
		filename = os.path.basename(dlfile.file.path)
	)

def about(request):
	page = Option.objects.filter(name='aboutus').first()
	return render(request, 'big/page.html', {'page': page})

def join(request):
	page = Option.objects.filter(name='joinus').first()
	return render(request, 'big/page.html', {'page': page})

def contact(request):
	page = Option.objects.filter(name='contactus').first()
	return render(request, 'big/page.html', {'page': page})

def signin(request):
	if request.method == 'GET':
		return render(request, 'big/signin.html')

	else:
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			member = Member.objects.get(uname=username)
			if member.avatar:
				request.session['avatar'] = member.avatar.url
			else:
				request.session['avatar'] = None

			return redirect('big:profile')

		else:
			messages.add_message(request, messages.ERROR, _("用户名或密码错误, 忘记帐号密码请联系管理员"))
			return redirect('big:signin')

def signout(request):
	logout(request)
	return redirect('big:index')

def signup(request):
	if request.method == 'GET':
		return render(request, 'big/signup.html')

	elif request.method == 'POST':
		username = request.POST.get('username')
		email = request.POST.get('email')
		name = request.POST.get('name')
		password = request.POST.get('password')

		if len(username) < 4:
			messages.add_message(request, messages.WARNING, _("用户名长度至少为4位字母"))

		elif User.objects.filter(username=username).exists():
			messages.add_message(request, messages.WARNING, _("你输入的用户名已被占用, 请重新输入用户名"))
		
		elif len(password) < 8:
			messages.add_message(request, messages.WARNING, _("密码的长度至少为8位数字或字母"))
		
		else:
			User.objects.create_user(
				username = username,
				password = password,
				email = email,
			)
			Member.objects.create_user(
				uname = username,
				email = email,
			)

			messages.add_message(request, messages.SUCCESS,
			 _('注册成功, 请 <a href="{}">登录</a> 系统, 修改个人资料'.format(reverse('big:signin'))))

		return redirect('big:signup')

@login_required(login_url='/signin')
def profile(request):
	if request.method == 'GET':
		member = Member.objects.get(uname=request.user.username)
		return render(request, 'big/profile.html', {'member': member})

	elif request.method == 'POST':
		data = request.POST
		avatar = request.FILES.get('avatar', None)
		member = Member.objects.get(uname=request.user.username)
		
		if avatar:
			member.avatar = avatar

		member.email = data['email']
		member.name_zh = data['name_zh']
		member.name_en = data['name_en']
		member.title_zh = data['title_zh']
		member.title_en = data['title_en']
		member.phone = data['phone']
		member.major_zh = data['major_zh']
		member.major_en = data['major_en']
		member.grade = int(data['grade'])
		member.degree = int(data['degree'])
		member.position = int(data['position'])
		member.status = int(data['status'])
		member.direct_zh = data['direct_zh']
		member.direct_en = data['direct_en']
		member.bio_zh = data['bio_zh']
		member.bio_en = data['bio_en']
		member.github = data['github']
		member.researchgate = data['researchgate']
		member.google = data['google']
		member.save()

		return redirect('big:profile')

@login_required(login_url='/signin')
def resetpasswd(request):
	if request.method == 'GET':
		return render(request, 'big/resetpasswd.html')

	elif request.method == 'POST':
		oldpasswd = request.POST.get('oldpasswd')
		newpasswd = request.POST.get('newpasswd')
		okpasswd = request.POST.get('okpasswd')

		if len(newpasswd) < 8:
			messages.add_message(request, messages.WARNING, _("密码的长度至少为8位数字或字母"))

		elif newpasswd != okpasswd:
			messages.add_message(request, messages.WARNING, _("两次输入的密码不一致"))

		elif authenticate(username=request.user.username, password=oldpasswd) is None:
			messages.add_message(request, messages.WARNING, _("旧密码不正确"))

		else:
			user = User.objects.get(pk=request.user.id)
			user.set_password(newpasswd)
			user.save()
			return redirect('big:signin')

		return redirect('big:resetpasswd')

@login_required(login_url='/signin')
def postadd(request):
	if request.method == 'GET':
		return render(request, 'big/postadd.html')

	elif request.method == 'POST':
		data = request.POST

		if Post.objects.filter(slug=data['slug']).exists():
			messages.add_message(request, messages.WARNING, _("别名已被占用, 请重新输入"))
			return redirect('big:postadd')

		author = Member.objects.get(uname=request.user.username)

		post = Post.objects.create(
			slug = data['slug'],
			title_zh = data['title_zh'],
			title_en = data['title_en'],
			content_zh = data['content_zh'],
			content_en = data['content_en'],
			author = author,
		)

		img = request.FILES.get('thumbnail', None)
		if img:
			post.thumbnail = img
			post.save()

		return redirect('big:postlist')

@login_required(login_url='/signin')
def postlist(request):
	if request.method == 'GET':
		#member = Member.objects.get(uname=request.user.username)
		post_list = Post.objects.filter(author__uname=request.user.username)
		paginator = Paginator(post_list, 15)
		page = request.GET.get('page')
		posts = paginator.get_page(page)

		return render(request, 'big/postlist.html', {'posts': posts})

@login_required(login_url='/signin')
def postedit(request, slug):
	if request.method == 'GET':
		post = Post.objects.get(slug=slug)
		return render(request, 'big/postedit.html', {'post': post})

	elif request.method == 'POST':
		data = request.POST
		post = Post.objects.get(slug=slug)
		
		if slug != data['slug']:
			if Post.objects.filter(slug=data['slug']).exists():
				messages.add_message(request, messages.WARNING, _("别名已被占用, 请重新输入"))
				return redirect(reverse('big:postedit', kwargs={'slug':slug}))
		
		post.slug = data['slug']
		post.title_zh = data['title_zh']
		post.title_en = data['title_en']
		post.content_zh = data['content_zh']
		post.content_en = data['content_en']
		post.approve = 0

		img = request.FILES.get('thumbnail', None)
		if img:
			post.thumbnail = img
		post.save()

		return redirect('big:postlist')

@login_required(login_url='/signin')
def postdelete(request, slug):
	if request.method == 'GET':
		Post.objects.get(slug=slug).delete()
		return redirect('big:postlist')

@login_required
def upload(request):
	if request.method == 'POST':
		files = request.FILES.getlist('files')

		medias = []
		isimgs = []
		msgs = []
		for file in files:
			media = Media.objects.create(
				name = file.name,
				file = file,
				ctype = file.content_type,
				size = file.size,
			)

			medias.append(media.file.url)
			isimgs.append(media.ctype.startswith('image'))
			msgs.append(media.name)

		return JsonResponse({
			'success': True,
			'time': '',
			'data': {
				'baseurl': '',
				'files': medias,
				'isImages': isimgs,
				'messages': msgs,
			}
		})

@login_required
def browser(request):
	if request.method == 'POST':
		medias = []
		for media in Media.objects.all():
			medias.append({
				'file': media.file.url,
				'name': media.name,
				'size': media.size,
				'isImage': media.ctype.startswith('image'),
			})

		return JsonResponse({
			'success': True,
			'time': '',
			'data': {
				'sources': {
					'a': {
						'path': '',
						'baseurl': '',
						'files': medias,
						'folders': '',
					}
				},
				'code': 200,
				'path': '',
				'name': '',
				'source': '',
			}
		})

@login_required(login_url='/signin')
def fund(request):
	funds = Fund.objects.all()
	return render(request, 'big/fund.html', {'funds':funds})

@login_required(login_url='/signin')
def expense(request, fid):
	fid = int(fid)
	fund = Fund.objects.get(pk=fid)
	expenses = Expense.objects.filter(fund__pk=fid)
	expend = Expense.objects.filter(fund__pk=fid).aggregate(money=Sum('amount'))

	if expend['money'] is None:
		expend['money'] = 0

	return render(request, 'big/expense.html', {
		'expenses':expenses, 'fund':fund,
		'expend': expend
	})
