from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.dispatch.dispatcher import receiver
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_delete, post_save

# Create your models here.
class BaseModel(models.Model):
	def __getattr__(self, attr):
		if attr in self.__dict__:
			return self.__dict__[attr]

		lang = get_language().split('-')[0]

		try:
			return self.__dict__["{}_{}".format(attr, lang)]
		except:
			raise AttributeError(attr)

	class Meta:
		abstract = True

class Publication(BaseModel):
	title = models.CharField(max_length=255)
	abstract = models.TextField(blank=True)
	authors = models.CharField(max_length=255)
	journal = models.CharField(max_length=100)
	year = models.SmallIntegerField()
	volume = models.CharField(max_length=10, blank=True)
	issue = models.CharField(max_length=10, blank=True)
	pages = models.CharField(max_length=20, blank=True)
	doi = models.CharField(max_length=100)
	pmid = models.CharField(max_length=30, blank=True)
	factor = models.FloatField(default=0, blank=True)
	thumbnail = models.ImageField(upload_to='big/thumbnail/')
	pdf = models.FileField(upload_to='big/paper/', blank=True)
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.title

	class Meta:
		ordering = ['-created']

class Member(BaseModel):
	DEGREES = (
		(0, _("未设置")),
		(1, _("博士")),
		(2, _("硕士")),
		(3, _("学士")),
	)

	POSITIONS = (
		(0, _("未设置")),
		(1, _("研究生")),
		(2, _("本科生")),
		(3, _("博士后")),
		(4, _("教职工")),
		(5, _("访问学者")),
	)

	STATUS = (
		(0, _("未设置")),
		(1, _("在读")),
		(2, _("毕业")),
		(3, _("退学")),
	)

	CHECKS = (
		(0, _("未确认")),
		(1, _("已确认")),
	)

	YEARS = ((i, i) for i in range(2020, timezone.now().year+1))

	#user = models.OneToOneField(User, on_delete=models.CASCADE, db_constraint=False)
	uname = models.CharField(max_length=150)
	email = models.CharField(max_length=255, blank=True)
	name_zh = models.CharField(max_length=30, blank=True)
	name_en = models.CharField(max_length=30, blank=True)
	title_zh = models.CharField(max_length=255, blank=True)
	title_en = models.CharField(max_length=255, blank=True)
	phone = models.CharField(max_length=15, blank=True)
	major_zh = models.CharField(max_length=30, blank=True)
	major_en = models.CharField(max_length=50, blank=True)
	grade = models.IntegerField(choices=YEARS, blank=True, default=2020)
	degree = models.SmallIntegerField(choices=DEGREES, blank=True, default=0)
	position = models.SmallIntegerField(choices=POSITIONS, blank=True, default=0)
	status = models.SmallIntegerField(choices=STATUS, blank=True, default=0)
	direct_zh = models.CharField(max_length=255, blank=True)
	direct_en = models.CharField(max_length=255, blank=True)
	avatar = models.ImageField(upload_to='big/avatar/', blank=True)
	bio_zh = models.TextField(blank=True)
	bio_en = models.TextField(blank=True)
	github = models.CharField(max_length=255, blank=True)
	researchgate = models.CharField(max_length=255, blank=True)
	google = models.CharField(max_length=255, blank=True)
	check = models.SmallIntegerField(choices=CHECKS, blank=True, default=0)

	def __str__(self):
		return self.user.username

	class Meta:
		ordering = ['grade']

class Post(BaseModel):
	APPROVES = (
		(0, _("等待审核")),
		(1, _("通过审核")),
		(2, _("退回修改"))
	)

	slug = models.CharField(max_length=100, unique=True)
	title_zh = models.CharField(max_length=255)
	title_en = models.CharField(max_length=255, blank=True)
	content_zh = models.TextField(blank=True)
	content_en = models.TextField(blank=True)
	thumbnail = models.ImageField(upload_to='big/thumbnail/', blank=True)
	banner = models.ImageField(upload_to='big/banner/', blank=True)
	approve = models.SmallIntegerField(choices=APPROVES, default=0)
	author = models.ForeignKey(Member, on_delete=models.CASCADE)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.title

	class Meta:
		ordering = ['-created']

class Slideshow(BaseModel):
	title_zh = models.CharField(max_length=255, blank=True)
	title_en = models.CharField(max_length=255, blank=True)
	description_zh = models.TextField(blank=True)
	description_en = models.TextField(blank=True)
	image = models.ImageField(upload_to='big/slide/')
	link = models.CharField(max_length=255, blank=True)
	extra_zh = models.CharField(max_length=255, blank=True)
	extra_en = models.CharField(max_length=255, blank=True)
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.title

	class Meta:
		ordering = ['-created']

class Software(BaseModel):
	TYPES = (
		(1, _("软件")),
		(2, _("数据库"))
	)

	name_zh = models.CharField(max_length=100)
	name_en = models.CharField(max_length=100, blank=True)
	url = models.CharField(max_length=255)
	doc = models.CharField(max_length=255, blank=True)
	language = models.CharField(max_length=30, blank=True)
	category = models.SmallIntegerField(choices=TYPES, default=0)
	download = models.CharField(max_length=255, blank=True)
	description_zh = models.TextField(blank=True)
	description_en = models.TextField(blank=True)
	thumbnail = models.ImageField(upload_to='big/thumbnail/', blank=True)
	created = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-created']

class Research(BaseModel):
	direction_zh = models.TextField()
	direction_en = models.TextField(blank=True)
	thumbnail = models.ImageField(upload_to='big/thumbnail/')
	rank = models.SmallIntegerField()
	created = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['rank']

class Media(BaseModel):
	name = models.CharField(max_length=255)
	file = models.FileField(upload_to='big/files/%Y/%m')
	ctype = models.CharField(max_length=100, blank=True)
	size = models.IntegerField()
	uploaded = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-uploaded']

class Option(BaseModel):
	name = models.CharField(max_length=100)
	title_zh = models.CharField(max_length=255, blank=True)
	title_en = models.CharField(max_length=255, blank=True)
	content_zh = models.TextField()
	content_en = models.TextField(blank=True)
	thumbnail = models.ImageField(upload_to='big/thumbnail', blank=True)
	created = models.DateTimeField(auto_now_add=True)

@receiver(pre_delete, sender=Slideshow)
def delete_slide(sender, instance, **kwargs):
	instance.image.delete(True)

@receiver(pre_delete, sender=Post)
def delete_post(sender, instance, **kwargs):
	instance.thumbnail.delete(True)

@receiver(pre_delete, sender=Member)
def delete_member(sender, instance, **kwargs):
	instance.avatar.delete(True)

@receiver(pre_delete, sender=Publication)
def delete_publication(sender, instance, **kwargs):
	instance.thumbnail.delete(True)

@receiver(pre_delete, sender=Software)
def delete_software(sender, instance, **kwargs):
	instance.thumbnail.delete(True)

@receiver(pre_delete, sender=Media)
def delete_media(sender, instance, **kwargs):
	instance.file.delete(True)

@receiver(pre_delete, sender=Research)
def delete_research(sender, instance, **kwargs):
	instance.thumbnail.delete(True)
