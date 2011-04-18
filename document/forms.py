# -*- coding: utf-8 -*-

from django import forms

class WriteForm(forms.Form) :
    tx_article_title = forms.CharField(label="제목", max_length=255, required=True)
    tx_content = forms.CharField(label="내용", required=True)
    tx_article_category = forms.CharField(label="카테고리", required=True)
    is_secret = forms.BooleanField(required=False)
    tags = forms.CharField(label='태그', required=False)
    is_notice = forms.BooleanField(required=False)


class GuestBookForm(forms.Form) :
    tx_content = forms.CharField(label="내용", required=True)
    is_secret = forms.BooleanField(required=False)

class WriteCommentForm(forms.Form) :
    content = forms.CharField(label="내용", required=True)
    is_secret = forms.BooleanField(required=False)

class GuestWriteForm(forms.Form) :
    tx_content = forms.CharField(label="내용", required=True)
    is_secret = forms.BooleanField(required=False)

class GuestWriteCommentForm(forms.Form) :
    content = forms.CharField(widget=forms.Textarea, label="내용", required=True)
    is_secret = forms.BooleanField(required=False)
