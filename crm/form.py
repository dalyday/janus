from django import forms
from django.forms import ModelForm
from django.forms import fields
from django.forms import widgets

class LoginFrom(forms.Form):
    username = fields.CharField(
        label='用户名',
        required=True,
        min_length=3,
        error_messages={
            'required':'用户名不能为空',
            'min_length':'用户名字过短',
        },
        widget=widgets.TextInput(attrs={'class':'form-control'})
    )
    password = fields.CharField(
        label='密码',
        required=True,
        min_length=3,
        error_messages={
            'required':'密码不能为空',
            'min_length':'密码过短',
        },
        widget=widgets.TextInput(attrs={'class': 'form-control'})
    )

