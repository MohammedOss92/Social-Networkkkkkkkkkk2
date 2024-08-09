from django import forms
from django.core.exceptions import ValidationError
from .models import User

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'profile_pic', 'cover']

    def __init__(self, *args, **kwargs):
        # تأكد من تمرير المستخدم الحالي كـ instance للنموذج
        self.current_user = kwargs.get('instance')
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.fields['profile_pic'].required = False
        self.fields['cover'].required = False
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        

    def clean_username(self):
        username = self.cleaned_data.get('username')
        # إذا لم يتم تغيير اسم المستخدم، يتم قبوله مباشرة
        if self.current_user and username == self.current_user.username:
            return username
        # تحقق مما إذا كان اسم المستخدم موجود لدى مستخدم آخر
        if User.objects.filter(username=username).exists():
            raise ValidationError("اسم المستخدم هذا موجود بالفعل. يرجى اختيار اسم آخر.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.current_user.pk).exists():
            raise ValidationError("البريد الإلكتروني مستخدم بالفعل.")
        return email
    

def save(self, commit=True):
        instance = super(EditProfileForm, self).save(commit=False)
        if commit:
            # حفظ الحقل profile_pic فقط إذا تم رفع صورة جديدة
            if 'profile_pic' in self.files:
                instance.profile_pic = self.files['profile_pic']
            # حفظ الحقل cover فقط إذا تم رفع صورة جديدة
            if 'cover' in self.files:
                instance.cover = self.files['cover']
            instance.save()
        return instance