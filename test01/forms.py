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
    message = forms.CharField(widget=forms.Textarea(attrs={'class':'form_control'}), label='پیغام', required=True)
    email = forms.EmailField(label= 'ایمیل', widget=forms.EmailInput(attrs={'class': 'form-control'}))
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

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'letter']
    def clean(self):
        cleaned_data = super(CommentForm, self).clean()
        name = cleaned_data.get('name')
        letter = cleaned_data.get('letter')
        if name.isdigit():
            msg = "به نظرم اگه از عدد استفاده نکنی بهتره"
            self.add_error('name', msg)
        if letter.count() < 5:
            msg = "حالا هداری کامنت میزاری یکم مطالب بیشتر بزار"
            self.add_error('letter', msg)
        return cleaned_data

class CreatePostForm(forms.Form):
    title = forms.CharField(label='عنوان', max_length=255)
    description = forms.CharField(label='متن پست', widget=forms.Textarea(attrs={'class':'form_control'}))
    reading_time = forms.IntegerField(label='زمان مطالعه')

    def clean(self):
        cleaned_data = super(CreatePostForm, self).clean()
        title = cleaned_data.get('title')
        reading_time = cleaned_data.get('reading_time')
        if not type(reading_time) == int:
            msg = "زمان مطالعه باید عدد باشد !"
            self.add_error('reading_time', msg)
        if reading_time < 0:
            msg = "چرا زمان مطالعه رو منفی میزنی !"
        if len(title) < 2:
            msg = "تعداد کاراکتر عنوان کم است !"
            self.add_error('title', msg)
        if len(title) > 40:
            msg = "تعداد کاراکتر عنوان زیاد است !"
        return cleaned_data