# -*- coding: utf-8 -*-
from django.urls import path, re_path
from . import views

app_name = 'big'

urlpatterns = [
	path('', views.index, name='index'),
	path('post/add', views.postadd, name='postadd'),
	path('post/list', views.postlist, name='postlist'),
	path('post/<slug>/edit', views.postedit, name='postedit'),
	path('post/<slug>/delete', views.postdelete, name='postdelete'),
	path('post/<slug>.html', views.post, name='post'),
	path('news', views.news, name='news'),
	path('publication', views.publication, name='publication'),
	path('research', views.research, name='research'),
	path('softwares', views.softwares, name='softwares'),
	path('software/<sname>', views.software, name='software'),
	path('download/<downid>/<sname>', views.download, name='download'),
	path('member', views.member, name='member'),
	path('member/<uname>', views.member, name='member'),
	path('about', views.about, name='about'),
	path('join', views.join, name='join'),
	path('contact', views.contact, name='contact'),
	path('signin', views.signin, name='signin'),
	path('signout', views.signout, name='signout'),
	path('signup', views.signup, name='signup'),
	path('profile', views.profile, name='profile'),
	path('resetpasswd', views.resetpasswd, name='resetpasswd'),
	path('upload', views.upload, name='upload'),
	path('browser', views.browser, name='browser'),
	path('fund', views.fund, name='fund'),
	path('expense/<fid>', views.expense, name='expense')
]