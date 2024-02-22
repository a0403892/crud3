# forms.py
from django import forms
from .models import PhotoModel
from .models import Profile

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = PhotoModel
        fields = ['image']
        labels = {
            'image': '請選擇您要上傳的圖片',
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profilepic']
        labels = {
            'profilepic': '請選擇您要上傳的圖片',
        }