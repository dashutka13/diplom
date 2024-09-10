from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from users.models import User


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name not in ('is_published', 'usable_password'):
                field.widget.attrs['class'] = 'form-control'


class UserRegisterForm(StyleFormMixin, UserCreationForm):

    class Meta:
        model = User
        fields = ('first_name', 'gender', 'email', 'password1', 'password2',)


class UserForm(StyleFormMixin, UserChangeForm):
    class Meta:
        model = User
        fields = ('first_name', 'gender', 'email', 'password', 'avatar', )

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #
    #     self.fields['password'].widget = forms.HiddenInput()
