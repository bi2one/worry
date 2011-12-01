# -*- coding: utf-8 -*-

import re
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django import forms

class JoinForm(forms.Form) :
    username = forms.CharField(max_length=30, label="사용자id", required=True)
    password = forms.CharField(max_length=128, label="비밀번호", widget=forms.PasswordInput())
    password_confirm = forms.CharField(max_length=128, label="비밀번호(확인용)", widget=forms.PasswordInput())
    nick_name = forms.CharField(max_length=30, label="닉네임", required=True)
    email = forms.EmailField(label="이메일")

    def clean_password_confirm(self):
        if 'password' in self.cleaned_data:
            password = self.cleaned_data['password']
            password_confirm = self.cleaned_data['password_confirm']
        if password == '':
            forms.ValidationError('필수항목 입니다.')
        if password == password_confirm:
            return password_confirm
        raise forms.ValidationError('비밀번호가 일치하지 않습니다.')

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'^[a-zA-Z][a-zA-Z0-9]*$', username):
            raise forms.ValidationError('사용자 아이디는 알파벳으로 시작하고, 기호가 들어갈 수 없습니다.')
        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError('이미 사용중인 아이디 입니다.')

class FindPasswordForm(forms.Form):
    email = forms.EmailField(label="이메일")

class NewPasswordForm(forms.Form):
    password = forms.CharField(max_length=128, label="비밀번호", widget=forms.PasswordInput())
    password_confirm = forms.CharField(max_length=128, label="비밀번호확인", widget=forms.PasswordInput())
    
    def clean_password_confirm(self):
        if 'password' in self.cleaned_data:
            password = self.cleaned_data['password']
            password_confirm = self.cleaned_data['password_confirm']
        if password == '':
            forms.ValidationError('필수항목 입니다.')
        if password == password_confirm:
            return password_confirm
        raise forms.ValidationError('비밀번호가 일치하지 않습니다.')
