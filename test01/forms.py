from django import forms
from .models import *

class TicketForm(forms.Form):
    SUBJECT_CHOICES = (
        ('پیشنهاد', 'پیشنهاد'),
        ('گزارش', 'گزارش'),
        ('انتقاد', 'انتقاد'),
    )
    subject = forms.ChoiceField(choices=SUBJECT_CHOICES)
    full_name = forms.CharField(label='نام و نام خانوادگی', max_length=255)
    message = forms.CharField(widget=forms.Textarea, label='پیغام', required=True)
    email = forms.EmailField(label='ایمیل')
    phone = forms.CharField(label='شماره تلفن', max_length=11)

    def clean(self):
        # def clean_phone():  {# نوع دیگر نوشتن اعتبار سنجی #}
        #     cd = cleaned_data['phone']
        cleaned_data = super(TicketForm, self).clean()
        phone = cleaned_data.get('phone')
        email = cleaned_data.get('email')
        if phone:
            if not phone.isdigit():
                msg = "شماره موبایل معتبر نیست !"
                self.add_error('phone', msg)
            if 1 < phone.count() > 11:
                msg = "تعداد حروف مناسب نیست !"
                self.add_error('phone', msg)
        if email:
            if not '@gmail.com' in email:
                msg = "ایمیل شما معتبر نیست !"
                self.add_error('email', msg)
        return cleaned_data