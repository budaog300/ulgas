from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm

from .models import CustomUser


class AdminContractForm(forms.Form):
    agreement = forms.CharField(required=False, disabled=True, label="Номер договора")
    user = forms.CharField(required=False, disabled=True, label="Логин пользователя")
    email = forms.EmailField(required=False, disabled=True,label="Email пользователя")
    additional_text = forms.CharField(widget=forms.Textarea, required=False, disabled=True, label="Обращение")
    file = forms.FileField(required="", label="Документ")


class ContractForm(forms.Form):
    contract_number = forms.CharField(label="Номер договора", label_suffix="", required=True,
                                      widget=forms.TextInput(attrs={'placeholder': '100'}))
    inn = forms.CharField(label='ИНН', label_suffix="", required=False, max_length=12,
                          widget=forms.TextInput(attrs={'placeholder': '734143626833'}))
    contract_date = forms.DateField(label='Дата заключения договора', label_suffix="", required=False,
                                    widget=(forms.DateInput(attrs={'type': 'date'})))

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data


class CustomPasswordRestForm(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data.get('email')

        if not CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь не найден')
        return email


class AuthenticationForm(forms.Form):
    username = forms.CharField(max_length=100, label_suffix="", label="Логин",
                               widget=(forms.TextInput(attrs={'placeholder': 'Логин или E-mail'})))
    password = forms.CharField(widget=forms.PasswordInput, label_suffix="", label="Пароль")


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True, label_suffix="", label="Email",
        error_messages={'invalid': ''}
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

        for fieldName in ['username', 'email', 'password1', 'password2']:
            self.fields[fieldName].help_text = ''
            self.fields[fieldName].label_suffix = ''

        self.fields['username'].widget.attrs[
            'placeholder'] = 'Иванов Иван Иванович'
        self.fields['email'].widget.attrs[
            'placeholder'] = 'Пожалуйста, введите действующий email'
        self.fields['password1'].widget.attrs[
            'placeholder'] = 'Ваш пароль должен содержать как минимум 8 символов.'
        self.fields['password2'].widget.attrs[
            'placeholder'] = 'Для подтверждения введите, пожалуйста, пароль ещё раз.'
