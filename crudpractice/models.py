from django.db import models
from django.utils.timezone import now
from django.core.validators import RegexValidator

# 建立user資料表
class User(models.Model):
    alphanumeric_validator = RegexValidator(
        regex='^[a-zA-Z0-9]*$',
        message='只能包含英文和數字。',
    )
    username = models.CharField(
        max_length=20,
        null=False,
        validators=[alphanumeric_validator],
    )
    username = models.CharField(max_length=20, null=False)
    email = models.EmailField(max_length=100, null=False)
    password = models.CharField(max_length=20, null=False)
    confirm_password = models.CharField(max_length=20, null=False)

    def __str__(self):
        return self.username
    
class Profile(models.Model):
    GENDER_CHOICES = [
        ('男', '男'),
        ('女', '女'),
        ('不顯示', '不顯示'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profilepic = models.ImageField(upload_to='profilepic/')
    nickname = models.CharField(max_length=20, null=False)
    age = models.IntegerField(null=False)
    gender = models.CharField(max_length=5, choices=GENDER_CHOICES, null=False)
    likes = models.CharField(max_length=20, null=False)
    dislikes = models.CharField(max_length=20, null=False)
    aboutme = models.TextField(max_length=255, null=False)

    def __str__(self):
        return self.nickname

class Article(models.Model):
    username = models.CharField(max_length=20, null=False)
    title = models.CharField(max_length=40, null=False)
    content = models.TextField(max_length=2000, null=False)
    datestart = models.DateTimeField()
    datelast = models.DateTimeField(default=now())

    def __str__(self):
        return self.title
    
class AlbumModel(models.Model):
    atitle = models.CharField(max_length=100, null=False)
    adesc = models.TextField(blank=True, default='')
    def __str__(self):
        return self.atitle
    
class PhotoModel(models.Model):
    album = models.ForeignKey(AlbumModel, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')
    imagedesc = models.CharField(max_length=20, default='', blank=True)
    
    def __str__(self):
        return f"{self.id} - {self.album.atitle} - {self.image.url}"
    
class BoardModel(models.Model):
    message = models.TextField(max_length=2000, null=False)
    date = models.DateTimeField()
    useruser = models.CharField(max_length=20)
    useremail = models.EmailField(max_length=100, default='', blank=True)
    def __str__(self):
        return f"{self.id} - {self.message} - {self.useruser}"