from django import forms

class ContactUsForm(forms.Form):
    email = forms.EmailField()
    name = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)

    widgets = {
        'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Your email"}),
        'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Your name"}),
        'message': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Your message"}),
    }
