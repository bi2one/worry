# -*- coding: utf-8 -*-

import re
from django import forms
from worry.order.models import Bank

class OrderFormFirst(forms.Form) :
    sender_name = forms.CharField(label="이름", max_length=45, required=True)
    sender_phone_1 = forms.CharField(label="전화번호(시작)", max_length=4, required=True)
    sender_phone_2 = forms.CharField(label="전화번호(중앙)", max_length=4, required=True)
    sender_phone_3 = forms.CharField(label="전화번호(끝)", max_length=4, required=True)
    doll_count = forms.ChoiceField(label="다섯걱정이 세트", choices=map((lambda x:(x, x)), range(0, 11)))
    phonedoll_count = forms.ChoiceField(label="두 걱정이 핸드폰줄", choices=map((lambda x:(x, x)), range(0, 11)))
    content = forms.CharField(widget=forms.Textarea, label="걱정거리", required=False)

    def cleaned_data_phone(self) :
        return str(self.cleaned_data['sender_phone_1']) + "-" + str(self.cleaned_data['sender_phone_2']) + "-" + str(self.cleaned_data['sender_phone_3'])

    def clean_content(self) :
        content = self.cleaned_data['content']
        return content.replace('\n', '<br>')

    # TODO: 걱정이 세트가 둘다 0일 때의 처리. 일단은 보류(4/22 10:21PM)
    # TODO: 전화번호 입력 validation

class OrderFormSecond(forms.Form) :
    sender_name = forms.CharField(label="이름", widget=forms.HiddenInput())
    sender_phone = forms.CharField(label="전화번호", widget=forms.HiddenInput())
    doll_count = forms.CharField(label="걱정인형", widget=forms.HiddenInput())
    phonedoll_count = forms.CharField(label="걱정이핸드폰줄", widget=forms.HiddenInput())
    content = forms.CharField(label="걱정내용", widget=forms.HiddenInput())

    bank_objects = Bank.objects.all()
    bank_name_numbers = map((lambda bank:(bank.id, bank.name + " " + bank.number)),
                            bank_objects)
    
    bank = forms.ChoiceField(widget=forms.RadioSelect,
                            label="입금은행",
                            choices=bank_name_numbers,
                            required=True)
    # 여기서, bank의 라디오 버튼중에 첫번째 것으로 페이지 로딩시 체크 되어 있어야 할지에 관한 이야기.
    payment_name = forms.CharField(label="입금자명", max_length=45, required=True)

    receiver_name = forms.CharField(label="받으실 분", max_length=45, required=True)
    receiver_phone_1 = forms.CharField(label="연락처", max_length=4, required=True)
    receiver_phone_2 = forms.CharField(label="연락처", max_length=4, required=True)
    receiver_phone_3 = forms.CharField(label="연락처", max_length=4, required=True)
    receiver_address_number = forms.CharField(label="배송지 주소", max_length=10, required=True)
    receiver_address = forms.CharField(label="배송지 주소", max_length=127, required=True)
    receiver_detail_address = forms.CharField(label="배송지 주소", max_length=127, required=True)

    send_issue = forms.CharField(widget=forms.Textarea, label="배송시 요청사항", required=False)

    is_gift = forms.BooleanField(required=False, label="선물용")

    def clean_send_issue(self) :
        issue = self.cleaned_data['send_issue']
        return issue.replace('\n', '<br>')
    
    def cleaned_data_receiver_phone(self) :
        return str(self.cleaned_data['receiver_phone_1']) + "-" + str(self.cleaned_data['receiver_phone_2']) + "-" + str(self.cleaned_data['receiver_phone_3'])

class OrderFormModify(forms.Form) :
    doll_count = forms.ChoiceField(label="다섯 걱정이 세트", choices=map((lambda x:(x, x)), range(0, 11)))
    phonedoll_count = forms.ChoiceField(label="두 걱정이 핸드폰줄", choices=map((lambda x:(x, x)), range(0, 11)))
    content = forms.CharField(label="걱정거리", widget=forms.Textarea)

    bank_objects = Bank.objects.all()
    bank_name_numbers = map((lambda bank:(bank.id, bank.name + " " + bank.number)),
                            bank_objects)
    bank = forms.ChoiceField(widget=forms.RadioSelect,
                            label="입금은행",
                            choices=bank_name_numbers,
                            required=True)
    
    payment_name = forms.CharField(label="입금자명", max_length=45, required=True)

    receiver_name = forms.CharField(label="받으실 분", max_length=45, required=True)
    receiver_phone_1 = forms.CharField(label="연락처", max_length=4, required=True)
    receiver_phone_2 = forms.CharField(label="연락처", max_length=4, required=True)
    receiver_phone_3 = forms.CharField(label="연락처", max_length=4, required=True)
    receiver_address_number = forms.CharField(label="배송지 주소", max_length=10, required=True)
    receiver_address = forms.CharField(label="배송지 주소", max_length=127, required=True)
    receiver_detail_address = forms.CharField(label="배송지 주소", max_length=127, required=True)
    is_gift = forms.BooleanField(required=False, label="선물용")

    def cleaned_data_receiver_phone(self) :
        return str(self.cleaned_data['receiver_phone_1']) + "-" + str(self.cleaned_data['receiver_phone_2']) + "-" + str(self.cleaned_data['receiver_phone_3'])

    def clean_content(self) :
        content = self.cleaned_data['content']
        return content.replace('\n', '<br>')

class OrderFormState(forms.Form) :
    invoice_number = forms.CharField(label="송장번호", max_length=127, required=False)
    state = forms.ChoiceField(widget=forms.RadioSelect,
                              label="주문 상태 변경",
                              choices=[("before_payment", "입금전"),
                                       ("create", "탄생중"),
                                       ("send", "배송중"),
                                       ("done", "배송완료"),
                                       ("fail", "배송실패")],
                              required=True)

class InsertDelayForm(forms.Form) :
    month = forms.IntegerField(max_value=12, min_value=0, required=False, label="달")
    day = forms.IntegerField(max_value=31, min_value=0, required=False, label="일")

