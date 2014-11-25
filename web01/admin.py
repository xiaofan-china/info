from django.contrib import admin
from web01.models import *
# Register your models here.
class MachineInfoAdmin(admin.ModelAdmin):
    list_display=( 'ip','ilo_ip','ilo_user','ilo_passwd','memo')
    list_display_links=("memo",)
    search_fields=('sn','ip','ilo_ip','ilo_user','ilo_passwd','memo')
    list_filter =('ip',)
    ordering=('ip',)
admin.site.register(MachineInfo,MachineInfoAdmin)
admin.site.register(Category)
admin.site.register(Article)
admin.site.register(Link)
