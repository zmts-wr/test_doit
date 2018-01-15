from django import forms


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()


class SignUpForm(forms.Form):
    username = forms.EmailField()
    password = forms.CharField()
    repassword = forms.CharField()

    def clean(self):
        password = self.cleaned_data.get('password')
        repassword = self.cleaned_data.get('repassword')

        if password != repassword:
            raise forms.ValidationError('Password retyped incorrectly')


class AnswerForm(forms.Form):
    question_id = forms.IntegerField()
    answer = forms.IntegerField()