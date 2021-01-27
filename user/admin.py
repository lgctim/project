from django.contrib import admin
from .models import *
# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display=('username','password','name','address','email',)
    search_fields=('username','name','address','phone','email',)
class BookAdmin(admin.ModelAdmin):
    list_display=('title','author','sump','good')
    search_fields=('title','author','good',)
    list_filter=('author','good')
class ScoreAdmin(admin.ModelAdmin):
    list_display=('book','num','com','fen',)
    search_fields=('book','num','com','fen',)

class CommenAdmin(admin.ModelAdmin):
    list_display=('user','book','good','addtime',)
    search_fields=('user','book','good',)
    list_filter=('user','book',)
class ActionCommenAdmin(admin.ModelAdmin):
    list_display=('user','action','addtime',)
    search_fields=('user','action',)
    list_filter=('user','action',)
class LiuyanAdmin(admin.ModelAdmin):
    list_display=('user','addtime',)
    search_fields=('user',)
    list_filter=('user',)
class NumAdmin(admin.ModelAdmin):
    list_display=('users','books','commens','actions','liuyans',)
admin.site.register(Tags)
admin.site.register(User,UserAdmin)
admin.site.register(Book,BookAdmin)
admin.site.register(Score,ScoreAdmin)
admin.site.register(Commen,CommenAdmin)
admin.site.register(Liuyan,LiuyanAdmin)
admin.site.register(Num,NumAdmin)
