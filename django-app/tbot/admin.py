from django.contrib import admin
from tbot.models import *

@admin.register(Estate)
class EstateAdmin(admin.ModelAdmin):
    list_display = ('estate_code','_total_real_space')


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('chat_id','title')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id','name','verified')


@admin.register(Estateowning)
class EstateowningAdmin(admin.ModelAdmin):
    list_display = ('estate','user','owning_weight')


