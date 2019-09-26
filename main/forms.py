from django import forms


class PayForm(forms.Form):
    fullname = forms.CharField(label='Full name', widget=forms.TextInput(attrs={'placeholder': 'Full name', 'autofocus': True}))
    email = forms.EmailField(label='Real email', widget=forms.TextInput(attrs={'placeholder': 'my.email@mail.com'}))
    period = forms.CharField(label='Select a plan:', widget=forms.Select(choices=(('1', '1 month - $4.99'), ('3', '3 months - $12.99'), ('6', '6 months - $19.99'), ('12', '1 year - $24.99, -60% discount!'), ('0', 'FOREVER - $499.99')), attrs={'class': 'form-control'}))



class ContactUsForm(forms.Form):
    email = forms.EmailField()
    name = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)

    widgets = {
        'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Your email"}),
        'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Your name"}),
        'message': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Your message"}),
    }
