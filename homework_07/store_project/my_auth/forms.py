from django.contrib.auth.forms import UserCreationForm
from .models import StoreUser
from django import forms
from django.utils.translation import gettext_lazy as _

class StoreUserCreateForm(UserCreationForm):
    class Meta:
        model = StoreUser
        fields = ('username', 'email', 'password1', 'password2')     
        labels = {
            'username': 'Имя пользователя:',
            'email': 'Электронная почта:',
            'password1': 'Пароль:',
            'password2': 'Подтверждение пароля:',
            
        }
        

    def __init__(self, *args, **kwargs):
        super(StoreUserCreateForm, self).__init__(*args, **kwargs)
        # Убираем текст помощи
        for field in self.fields.values():
            field.help_text = None
        
        # Переопределяем метки для полей password1 и password2
        self.fields['password1'].label = 'Пароль:'
        self.fields['password2'].label = 'Подтверждение пароля:'
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError("Это поле обязательно для заполнения.")
        # Дополнительная проверка на валидность email
        if not forms.EmailField().clean(email):
            raise forms.ValidationError("Введите корректный адрес электронной почты.")
        return email
    

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if not password1:
            raise forms.ValidationError("Это поле обязательно для заполнения.")
        return password1

    def clean_password2(self):
        password2 = self.cleaned_data.get('password2')
        if not password2:
            raise forms.ValidationError("Это поле обязательно для заполнения.")
        return password2
