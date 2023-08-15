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
	list_display = ('id', 'uname', 'email', 'major_zh', 'grade', 'degree', 'position', 'status')
	list_filter = ('degree',)

@admin.register(Slideshow)
class SlideAdmin(admin.ModelAdmin):
	list_display = ('id', 'title_zh', 'image', 'link', 'created')

@admin.register(Software)
class SoftwareAdmin(admin.ModelAdmin):
	list_display = ('id', 'name_zh', 'url', 'category', 'description_zh', 'created')

@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
	list_display = ('id', 'version', 'software', 'created')

@admin.register(Download)
class DownloadAdmin(admin.ModelAdmin):
	list_display = ('id', 'system', 'file', 'uploaded', 'version')

@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
	list_display = ('id', 'file', 'ctype', 'size', 'uploaded')

@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'title_zh', 'content_zh', 'created')

@admin.register(Fund)
class FundAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'category', 'approve_code', 'approve_amount', 'approve_time')

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
	list_display = ('id', 'fund', 'category', 'amount', 'create_time')
