from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
	list_display = ('id', 'title_zh', 'created', 'updated')
	search_fields = ('title_zh',)

@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
	list_display = ('id', 'title', 'journal', 'factor', 'created')
	list_filter = ('journal',)
	search_fields = ('title',)

@admin.register(Research)
class ResearchAdmin(admin.ModelAdmin):
	list_display = ('id', 'direction_zh', 'rank', 'created')

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'major_zh', 'grade', 'degree', 'position', 'status')
	list_filter = ('degree',)
	search_fields = ('user.username',)

@admin.register(Slideshow)
class SlideAdmin(admin.ModelAdmin):
	list_display = ('id', 'title_zh', 'image', 'link', 'created')

@admin.register(Software)
class SoftwareAdmin(admin.ModelAdmin):
	list_display = ('id', 'name_zh', 'url', 'category', 'description_zh', 'created')

@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
	list_display = ('id', 'file', 'ctype', 'size', 'uploaded')

@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'title_zh', 'content_zh', 'created')
