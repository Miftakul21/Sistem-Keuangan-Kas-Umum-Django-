from secrets import choice
from django import forms
# from django.contrib.auth.forms import UserCreationForm
from .models import User, Buku


class AddUserForm(forms.ModelForm):
    first_name = forms.CharField(
        required=True, 
        widget = forms.widgets.TextInput(
            attrs = {
                'class': 'form-control',
                'placeholder': 'Nama awal'
            }
        )
    )

    last_name = forms.CharField(
        required = True,
        widget = forms.widgets.TextInput(
            attrs = {
                'class': 'form-control',
                'placeholder': 'Nama akhir'
            }
        )
    )

    email = forms.CharField(
        required = True, 
        widget = forms.widgets.TextInput(
            attrs = {
                'class': 'form-control',
                'placeholder': 'Email',
            }
        ) 
    )

    mobile = forms.CharField(
        required = True,
        widget = forms.widgets.TextInput(
            attrs = {
                'class': 'form-control',
                'placeholder': 'Nomor telepon'
            } 
        )
    )

    role = forms.ChoiceField(
        required=True,
        choices = [('admin', 'Admin'), ('user', 'User')],
        widget = forms.Select(
            attrs = {
                'class': 'form-control'
            }
        )
    )

    password = forms.CharField(
        required = True,
        widget = forms.PasswordInput(
            attrs = {
                'class': 'form-control',
                'placeholder': 'Password'
            }
        )
    )

    class Meta: 
        model = User
        fields = ['first_name', 'last_name', 'email', 'mobile', 'role',]


class UpdateUserForm(forms.ModelForm):
        first_name = forms.CharField(
            required=True, 
            widget = forms.widgets.TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Nama awal'
                }
            )
        )

        last_name = forms.CharField(
            required = True,
            widget = forms.widgets.TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Nama akhir'
                }
            )
        )

        email = forms.CharField(
            required = True, 
            widget = forms.widgets.TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Email',
                }
            ) 
        )

        mobile = forms.CharField(
            required = True,
            widget = forms.widgets.TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Nomor telepon'
                } 
            )
        )

        role = forms.ChoiceField(
            required=True,
            choices = [('admin', 'Admin'), ('user', 'User')],
            widget = forms.Select(
                attrs = {
                    'class': 'form-control'
                }
            )
        )

        class Meta: 
            model = User
            fields = ['first_name', 'last_name', 'email', 'mobile', 'role']


class LoginForm(forms.Form):
    email = forms.CharField(
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control form-control-user',
                'placeholder': 'Masukkan email',
                'name': 'email',
            }
        )
    )

    password = forms.CharField(
        widget = forms.PasswordInput(
            attrs = {
                'class': 'form-control form-control-user',
                'placeholder': 'Maskkan password',
                'name': 'password'
            }
        )
    )

class RegisterForm(forms.Form):
    first_name = forms.CharField(
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control form-control-user',
                'placeholder': 'Nama awal',
                'name': 'first_name',
            }
        )
    )

    last_name = forms.CharField(
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control form-control-user',
                'placeholder': 'Nama akhir',
                'name': 'first_last',
            }
        )
    )

    email = forms.CharField(
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control form-control-user',
                'placeholder': 'Email',
                'name': 'email',
            }
        )
    )

    password1 = forms.CharField(
        widget = forms.PasswordInput(
            attrs = {
                'class': 'form-control form-control-user',
                'placeholder': 'Password',
                'name': 'password'
            }
        )
    )

    password2 = forms.CharField(
        widget = forms.PasswordInput(
            attrs = {
                'class': 'form-control form-control-user',
                'placeholder': 'Confirm password',
                'name': 'confirm_password'
            }
        )
    )

    class Meta: 
        model = User
        fields = ('last_name', 'first_name', 'email', 'password1', 'password2') 


class AddBook(forms.ModelForm):
    keterangan_kas = forms.CharField(
        required=True,
        widget = forms.Textarea(
            attrs = {
                'class': 'form-control',
                'placeholder': 'Keterangan kas',
                'name': 'keterangan_kas'
            }
        )
    )

    saldo = forms.IntegerField(
        required=False,
        widget = forms.NumberInput(
            attrs = {
                'class': 'form-control',
                'min': '0',
                'name': 'saldo'
            }
        )
    )

    debet = forms.IntegerField(
        required=False,
        widget = forms.NumberInput(
            attrs = {
                'class': 'form-control',
                'min': '0',
                'name': 'debet'
            }
        )
    )

    tanggal = forms.DateField(
        widget = forms.DateInput(
            attrs = {
                'class': 'form-control',
                'name': 'tanggal',
                'type': 'date'
            }
        )
    )

    class Meta:
        model = Buku
        fields = ('keterangan_kas', 'saldo', 'debet', 'tanggal')

        
