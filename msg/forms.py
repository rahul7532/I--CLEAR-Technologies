from django import forms


class UserForm(forms.Form):
    fn = forms.CharField(widget=forms.TextInput)
    ln = forms.CharField(widget=forms.TextInput)
    age = forms.IntegerField()
    username = forms.EmailField(widget=forms.TextInput)
    password = forms.CharField(widget=forms.PasswordInput)
    cnf_password = forms.CharField(widget=forms.PasswordInput)


class LoginForm(forms.Form):
    username = forms.EmailField(widget=forms.TextInput)
    password = forms.CharField(widget=forms.PasswordInput)
