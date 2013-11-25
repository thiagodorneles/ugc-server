# coding: utf-8
from django.contrib import admin
from ugc.core.models import Publish,Tag, User

class PublishAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'status')
    search_fields = ('title', 'description', 'city', 'created_at')
    date_hierarchy = 'created_at'
    list_filter = ['created_at']

class TagAdmin(admin.ModelAdmin):
    list_display = ('tag', 'created_at', 'status')
    search_fields = ('tag', 'created_at', 'status')
    date_hierarchy = 'created_at'
    list_filter = ['created_at']



admin.site.register(Publish, PublishAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(User)