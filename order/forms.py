# -*- coding: utf-8 -*-

from django import forms

class OrderFormFirst(forms.Form) :
    sender_name = forms.CharField(label="이름", max_length=45, required=True)
    sender_phone_1 = forms.IntegerField(label="전화번호(시작)", max_value=1000, required=True)
    sender_phone_2 = forms.IntegerField(label="전화번호(중앙)", max_value=1000, required=True)
    sender_phone_3 = forms.IntegerField(label="전화번호(끝)", max_value=1000, required=True)
    doll_count = forms.ChoiceField(label="다섯걱정이 세트", choices=map((lambda x:(x, x)), range(0, 11)))
    phonedoll_count = forms.ChoiceField(label="두 걱정이 핸드폰줄", choices=map((lambda x:(x, x)), range(0, 11)))
    content = forms.CharField(widget=forms.Textarea, label="걱정거리")

    def clean_sender_phone(self):
        if 'sender_phone1' in self.cleaned_data and 'sender_phone2' in self.cleaned_data and 'sender_phone3' in self.cleaned_data:
            sender_phone_1 = self.cleaned_data['sender_phone_1']
            sender_phone_2 = self.cleaned_data['sender_phone_2']
            sender_phone_3 = self.cleaned_data['sender_phone_3']

            if sender_phone_1 == '' or sender_phone_2 == '' or sender_phone_3 == '' :
                forms.ValidationError('전화번호를 입력해주세요.')
                
            return sender_phone_1 + sender_phone_2 + sender_phone_3
        
        raise forms.ValidationError('전화번호가 올바르지 않습니다.')
