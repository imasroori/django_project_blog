from django.forms import ModelForm, models


class RegisterForm(ModelForm):
    f_name = models.ChoiceField
