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