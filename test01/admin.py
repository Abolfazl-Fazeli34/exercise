from django.contrib import admin
from .models import *
from django_jalali.admin.filters import JDateFieldListFilter
# Register your models here.


admin.sites.AdminSite.site_header = 'پنل مدریت جنگو'
admin.sites.AdminSite.site_title = 'پنل'
admin.sites.AdminSite.index_title = 'پنل مدریت'
# admin.sites.AdminSite.site_url = '<UNK>'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'publish', 'status']
    ordering = ['-publish']
    raw_id_fields = ['author']
    readonly_fields = ['publish']
    list_filter = [('publish', JDateFieldListFilter), 'status']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['status']
    search_fields = ['title', 'description']
    date_hierarchy = 'publish'
    list_display_links = ['title', 'author']


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'subject', 'email']
    list_editable = ['subject']
    list_display_links = ['full_name']
    search_fields = ['full_name', 'subject']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'post', 'active']
    list_editable = ['post', 'active']
    raw_id_fields = ['post']
    list_filter = ['name', ('created', JDateFieldListFilter)]
    search_fields = ['name']
    list_display_links = ['name']