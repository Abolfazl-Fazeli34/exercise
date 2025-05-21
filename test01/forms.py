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
        if len(letter) < 5:
            msg = "حالا هداری کامنت میزاری یکم مطالب بیشتر بزار"
            self.add_error('letter', msg)
        return cleaned_data

class PostSearchForm(forms.Form):
    query = forms.CharField(label='جستجو', max_length=255)


class CreatePostForm(forms.ModelForm):
    image1 = forms.ImageField(label='image1', required=False)
    image2 = forms.ImageField(label='image2', required=False)
    class Meta:
        model = Post
        fields = ['title', 'description', 'reading_time']
    def clean(self):
        cleaned_data = super(CreatePostForm, self).clean()
        reading_time = cleaned_data['reading_time']
        if not type(reading_time) == int:
            msg = "نوع زمان باید عدد باشد !"
            self.add_error('reading_time', msg)
        return cleaned_data

