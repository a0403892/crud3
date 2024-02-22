from django.contrib import admin
# 從crudpractice應用程式中的models.py載入user資料表
# 載入這兩行後才能在admin界面中看到資料表
from crudpractice.models import User 
from crudpractice.models import Profile
from crudpractice.models import Article
from crudpractice.models import AlbumModel
from crudpractice.models import PhotoModel
from crudpractice.models import BoardModel

admin.site.register(User)

class Userprofile(admin.ModelAdmin):
    list_display=('user', 'nickname') # 要顯示的欄位
admin.site.register(Profile, Userprofile)

# 因為要讓article資料表自動新增ID
class Userarticle(admin.ModelAdmin):
    list_display=('id', 'username', 'title', 'content', 'datestart', 'datelast') # 要顯示的欄位
admin.site.register(Article, Userarticle)

class Useralbum(admin.ModelAdmin):
    list_display=('id', 'atitle', 'adesc')
admin.site.register(AlbumModel, Useralbum)

admin.site.register(PhotoModel)

admin.site.register(BoardModel)