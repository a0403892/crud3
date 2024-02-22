"""
URL configuration for crud3 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from crudpractice import views #從crudpractice專案資料夾內載入views.py
# 用於在開發中提供媒體文件的伺服器
from django.conf import settings
from django.conf.urls.static import static

app_name = 'crudpractice'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index), # 將空路徑設為首頁
    path('indexb', views.indexb),

    path('create_account', views.create_account),
    path('create_success', views.create_success),
    path('user_profile', views.user_profile),
    path('change_profile', views.change_profile),
    path('change_profilepic', views.change_profilepic),
    path('change_profile_success', views.change_profile_success),
    # path('return_user_profile', views.return_user_profile),
    path('blog', views.blog, name='blog'),
    path('articles/<int:articleid>', views.articles),
    path('new_post', views.new_post),
    path('post_success', views.post_success),
    path('delete_post/<int:articleid>', views.delete_post),
    path('logout', views.logout),
    path('edit_post/<int:articleid>', views.edit_post),
    path('edit_success/<int:articleid>', views.edit_success),
    path('album', views.album),
    path('create_album', views.create_album),
    path('create_album_success', views.create_album_success),
    path('album/<int:albumid>', views.album),
    path('create_photo/<int:albumid>', views.create_photo),
    path('album_delete/<int:albumid>', views.album_delete),
    path('album_edit/<int:albumid>', views.album_edit),
    path('album_edit_success/<int:albumid>', views.album_edit_success),
    path('photo_delete/<int:photoid>', views.photo_delete),
    path('photo_edit/<int:photoid>', views.photo_edit),
    path('photo_edit_success/<int:photoid>', views.photo_edit_success),
    path('board', views.board),
    path('post_message', views.post_message),
    path('post_message_success', views.post_message_success),
    path('delete_message/<int:boardid>', views.delete_message),
    path('guest', views.guest),



    path('v', views.v),
    path('test/<int:articleid>', views.test),
    path('a', views.a),
]
# 在網頁中訪問 MEDIA_URL 中的媒體文件時，Django 將從 MEDIA_ROOT 中提供這些文件。
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)