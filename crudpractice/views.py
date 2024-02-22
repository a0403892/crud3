from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from crudpractice.models import User
from crudpractice.models import Profile
from crudpractice.models import Article
from crudpractice.models import AlbumModel
from crudpractice.models import PhotoModel
from crudpractice.models import BoardModel
from django.utils import timezone
from .forms import ImageUploadForm
from .forms import UserProfileForm
from django.template.defaultfilters import linebreaksbr
from django.core.paginator import Paginator # 載入Paginator實現分頁功能
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

# Create your views here.
def index(request):
    return render(request, "index.html")

def indexb(request):
    return render(request, "indexb.html")

def create_account(request):
    return render(request, 'create_account.html')

def create_success(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            message = '您輸入的密碼與確認密碼不一樣，請重新輸入'
            return render(request, 'create_account.html', {'message': message})
        
        # 檢查 username 是否符合正則表達式
        alphanumeric_validator = RegexValidator(
            regex='^[a-zA-Z0-9]*$',
            message='只能包含英文和數字。',
        )
        try:
            alphanumeric_validator(username)
        except ValidationError as e:
            message = '帳號名稱不符合條件，請使用英文和數字。'
            return render(request, 'create_account.html', {'message': message})

        if User.objects.filter(username=username).exists():
            message = '此帳號名稱已經註冊，請使用其他名稱'
            return render(request, 'create_account.html', {'message': message})

        if User.objects.filter(email=email).exists():
            message = '此 E-mail 已經註冊，請使用其他信箱'
            return render(request, 'create_account.html', {'message': message})

        unit = User.objects.create(username=username, email=email, password=password, confirm_password=confirm_password)
        unit.save()
        message = '帳號創建成功！'
        return render(request, 'create_success.html', {'message': message})

    else:
        message = '請用POST方法連線至此'
        return render(request, 'error_page.html', {'message':message})

def user_profile(request):
    # 獲取User資料表中名叫'rain'的使用者的id
    # 再獲取Profile資料表中的相同id
    obj = User.objects.get(username='rain')
    id = obj.id
    profile_obj = Profile.objects.get(id=id)
    profilepic = profile_obj.profilepic
    nickname = profile_obj.nickname
    age = profile_obj.age
    gender = profile_obj.gender
    likes = profile_obj.likes
    dislikes = profile_obj.dislikes
    aboutme = profile_obj.aboutme

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user_obj = User.objects.get(username=username, password=password)
            request.session['name'] = username
            name = request.session.get('name')
            return render(request, 'user_profile.html', locals())
        except User.DoesNotExist:
            return render(request, 'error_page.html', {'message': '帳號或密碼錯誤'})
    else:
        name = request.session.get('name')
        return render(request, 'user_profile.html', locals())
# 修改個人資料成功，返回個人資料頁面
# 能從這個URI進來的 一定是已經使用username跟password進來的
# 不然要從user_profile路徑我不知道要怎麼設定
# def return_user_profile(request):
#     if request.method == 'POST':
#         request.session['name'] = 'rain'
#         obj = User.objects.get(username='rain')
#         id = obj.id
#         profile_obj = Profile.objects.get(id=id)
#         nickname = profile_obj.nickname
#         age = profile_obj.age
#         gender = profile_obj.gender
#         likes = profile_obj.likes
#         dislikes = profile_obj.dislikes
#         aboutme = profile_obj.aboutme
#         return render(request, 'user_profile.html', locals())
#     else:
#         message = '請用POST方法連線至此'
#         return render(request, 'error_page.html', {'message':message})

def change_profile(request):
    obj = User.objects.get(username='rain')
    id = obj.id
    profile_obj = Profile.objects.get(id=id)
    nickname = profile_obj.nickname
    age = profile_obj.age
    gender = profile_obj.gender
    likes = profile_obj.likes
    dislikes = profile_obj.dislikes
    aboutme = profile_obj.aboutme

    if request.session['name'] == 'rain':
        return render(request, 'change_profile.html', locals())
    else:
        message = '你的帳號沒有修改權限'
        return render(request, 'error_page.html', {'message':message})
    
def change_profilepic(request):
    obj = User.objects.get(username='rain')
    id = obj.id
    profile_obj = Profile.objects.get(id=id)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile_obj)

        if form.is_valid():
            form.save()
            return redirect('/user_profile')  # 這裡的 'user_profile' 是你的個人資料頁面的 URL 名稱
    else:
        form = UserProfileForm(request.POST, request.FILES, instance=profile_obj)
        return render(request, 'change_profilepic.html', locals())
    
def change_profile_success(request):
    if request.method == 'POST':
        obj = User.objects.get(username='rain')
        id = obj.id
        profile_obj = Profile.objects.get(id=id)
        profile_obj.nickname = request.POST.get('nickname')
        profile_obj.age = request.POST.get('age')
        profile_obj.gender = request.POST.get('gender')
        profile_obj.likes = request.POST.get('likes')
        profile_obj.dislikes = request.POST.get('dislikes')
        profile_obj.aboutme = request.POST.get('aboutme')
        profile_obj.save()
        message = '修改成功！'
        return render(request, 'change_profile_success.html', locals())
    else:
        message = '請用POST方法連線至此'
        return render(request, 'error_page.html', {'message':message})

def blog(request):
    articles = Article.objects.all().order_by('-id')
    name = request.session.get('name')
    return render(request, 'blog.html', locals())

def articles(request, articleid=0):
    article_obj = Article.objects.get(id=articleid)
    title = article_obj.title
    content = article_obj.content
    datestart = article_obj.datestart
    datelast = article_obj.datelast
    return render(request, 'articles.html', locals())

def new_post(request):
    username = request.session.get('name')
    if username == 'rain':
        return render(request, 'new_post.html', locals())
    else:
        message = '請用POST方法連線至此'
        return render(request, 'error_page.html', {'message': message})
    
def post_success(request):
    if request.method == 'POST':
        username = request.session.get('name')
        title = request.POST.get('title')
        content = request.POST.get('content')
        date = timezone.now()

        article_unit = Article.objects.create(username=username, title=title, content=content, date=date)
        article_unit.save()

        # 添加重定向，將用戶轉到 blog.html 頁面
        return redirect('blog')
    else:
        message = '請用POST方法連線至此'
        return render(request, 'error_page.html', {'message': message})
    
def logout(request):
    # 清除用戶的 session 資料
    request.session.clear()
    # 獲取用戶當前所在頁面的 URL，如果沒有則預設回到首頁 '/'
    redirect_url = request.META.get('HTTP_REFERER', '/')
    # 進行重定向
    return redirect(redirect_url)

def delete_post(request, articleid=None):
    article_obj = Article.objects.get(id=articleid)
    article_obj.delete()
    # 獲取用戶當前所在頁面的 URL，如果沒有則預設回到首頁 '/'
    redirect_url = request.META.get('HTTP_REFERER', '/')
    # 進行重定向
    return redirect(redirect_url)

def edit_post(request, articleid=None):
    article_obj = Article.objects.get(id=articleid)
    title = article_obj.title
    content = article_obj.content
    id = article_obj.id
    return render(request, 'edit_post.html', {'title':title, 'content':content, 'id':id})

def edit_success(request, articleid=None):
    articleid = request.POST.get('article_id')
    username = request.session.get('name')
    title = request.POST.get('title')
    content = request.POST.get('content')
    date = timezone.now()

    article_obj = Article.objects.get(id=articleid)
    article_obj.username = username
    article_obj.title = title
    article_obj.content = content
    article_obj.datelast = date
    article_obj.save()

    # 添加重定向，將用戶轉到 blog.html 頁面
    return redirect('/blog')

def create_album(request):
    return render(request, 'create_album.html')

def create_album_success(request):
    if request.method =='POST': 
        atitle = request.POST.get('album')
        adesc = request.POST.get('desc')
        album_unit = AlbumModel.objects.create(atitle=atitle, adesc=adesc)
        message = '建立相簿成功'
        return render(request, 'create_album_success.html', locals())
    else:
        message = '請用POST方法連線至此'
        return render(request, 'error_page.html', {'message': message})
    
def album(request, albumid=None):
    name = request.session.get('name')
    if albumid == None:
        albums = AlbumModel.objects.all().order_by('id')  #讀取所有相簿
        photos = []  #每一相簿第1張相片串列
        for album in albums:
            photo = PhotoModel.objects.filter(album__atitle=album.atitle).order_by('id')[:1]  #讀取相片(第一張)
            image = PhotoModel.objects.filter(album__atitle=album.atitle).order_by('id') #讀取相片所有(計算數量用)
            # 將每個相簿以及相關的第一張相片組合成一個字典
            # 若無將 None 加入到 photo 的鍵值中
            photos.append({'album': album, 'photo': photo.first() if photo else None, 'imagelens':image.count()})

        return render(request, 'album.html', locals())
    else:
        album = AlbumModel.objects.get(id=albumid)
        title = album.atitle
        desc = album.adesc
        desc = linebreaksbr(desc) # 使用linebreaksbr將資料欄位中的換行改成html中的<br>
        images = album.photomodel_set.all()
        # 將 QuerySet 包裝進 Paginator，每頁顯示 16 筆資料（可根據需求調整）
        paginator = Paginator(images, 16)
        # 取得當前頁數（預設為第一頁）
        page = request.GET.get('page', 1)
        # 取得該頁的留言資料
        images = paginator.get_page(page)
        return render(request, 'album_detail.html', locals())
    
def album_edit(request, albumid=None):
    album = AlbumModel.objects.get(id=albumid)
    id = albumid
    atitle = album.atitle
    adesc = album.adesc
    return render(request, 'album_edit.html', locals())

def album_edit_success(request, albumid=None):
    albumid = request.POST.get('albumid')
    title = request.POST.get('album')
    desc = request.POST.get('desc')

    album_obj = AlbumModel.objects.get(id=albumid)
    album_obj.atitle = title
    album_obj.adesc = desc
    album_obj.save()
    return render(request, 'album_edit_success.html', locals())
    
def create_photo(request, albumid=None):
    album = AlbumModel.objects.get(id=albumid)
    title = album.atitle
    id = album.id
    form = ImageUploadForm(request.POST, request.FILES)
    if form.is_valid():
        image_instance = form.save(commit=False)
        image_instance.album = album
        desc = request.POST.get('desc')
        image_unit = PhotoModel.objects.create(album=album, image=image_instance.image, imagedesc=desc)
        image_unit.save()
        albumid = album.id
    return render(request, 'create_photo.html', locals())

def album_delete(request, albumid=None):
    album = AlbumModel.objects.get(id=albumid)
    album.delete()
    message = '刪除相簿成功'
    return render(request, 'album_delete.html')

def photo_delete(request, photoid=None):
    photo = PhotoModel.objects.get(id=photoid)
    photo.delete()
    # 獲取用戶當前所在頁面的 URL，如果沒有則預設回到首頁 '/'
    redirect_url = request.META.get('HTTP_REFERER', '/')
    # 進行重定向
    return redirect(redirect_url)

def photo_edit(request, photoid=None):
    photo = PhotoModel.objects.get(id=photoid)
    desc = photo.imagedesc
    id = photo.id
    return render(request, 'photo_edit.html', locals())

def photo_edit_success(request, photoid=None):
    photoid = request.POST.get('photo_id')
    photo = PhotoModel.objects.get(id=photoid)
    newdesc = request.POST.get('desc')
    photo.imagedesc = newdesc
    photo.save()
    message = '修改相片描述成功'
    albumid = photo.album.id # 取得此 image 對應至Albummodel資料表的 album 的 id
    return render(request, 'photo_edit_success.html', locals())

def board(request):
    obj = User.objects.get(username='rain')
    id = obj.id
    profile_obj = Profile.objects.get(id=id)
    nickname = profile_obj.nickname
    board_obj = BoardModel.objects.all().order_by('-id')
    # 將 QuerySet 包裝進 Paginator，每頁顯示 3 條留言（可根據需求調整）
    paginator = Paginator(board_obj, 3)
    # 取得當前頁數（預設為第一頁）
    page = request.GET.get('page', 1)
    # 取得該頁的留言資料
    messagedata = paginator.get_page(page)
    # 使用了 paginator 將留言物件包裝成分頁 就不用再對 board_obj 進行迭代
    # 此時的 messagedata 本身就是迭代物件
    # messagedata = []
    # for i in board_obj:
    #     id = i.id
    #     message = linebreaksbr(i.message) # 使用linebreaksbr將資料欄位中的換行改成html中的<br>
    #     useremail = i.useremail
    #     useruser = i.useruser
    #     date = i.date
    #     messagedata.append({'id': id, 'message': message, 'useremail': useremail, 'useruser': useruser, 'date': date})

    return render(request, 'board.html', locals())

def post_message(request):
    return render(request, 'post_message.html')

def post_message_success(request):
    useruser = request.session.get('name', '遊客')

    if useruser == '遊客':
        message = request.POST.get("boardmessage")
        date = timezone.now()
        useremail = ''

    else:
        message = request.POST.get("boardmessage")
        date = timezone.now()
        user_obj = User.objects.get(username=useruser)
        useremail = user_obj.email

    board_unit = BoardModel.objects.create(message=message, date=date, useruser=useruser, useremail=useremail)
    board_unit.save()

    return render(request, 'post_message_success.html', locals())
    
def delete_message(request, boardid=None):
    board_obj = BoardModel.objects.get(id=boardid)
    board_obj.delete()
    # 獲取用戶當前所在頁面的 URL，如果沒有則預設回到首頁 '/'
    redirect_url = request.META.get('HTTP_REFERER', '/')
    # 進行重定向
    return redirect(redirect_url)

def guest(request):
    # 清除用戶的 session 資料
    request.session.clear()
    # 進行重定向
    return redirect('/user_profile')


















def v(request):
    return render(request, 'show.html', locals())
   
def test(request, articleid=None):
    article_obj = Article.objects.get(id=articleid)

    username = 'rain'
    title = 'HEllo   11123'
    content = 'helloo11111111111'
    date = timezone.now()

    article_obj.username = username
    article_obj.title = title
    article_obj.content = content
    article_obj.date = date
    article_obj.save()

    return redirect('/blog')

def a(request):
    i = 1
    return HttpResponse(i)