from django import forms
from account.models import User

class ConnexionForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", max_length=30, widget=forms.TextInput(attrs={'type':'username', 'class' : 'form-control', 'name':"username", 'id' : "inputUsername"}))
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput(attrs={'type':"password", 'id':"inputPassword", 'name':"password", 'class':"form-control"}))

class RegisterForm(forms.Form):
    """the form to create an account"""
    user_name = forms.CharField(max_length=100)
    email = forms.EmailField(label="E-mail")
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)
    password_repeat = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)
    robot = forms.BooleanField(required=True)

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        username = cleaned_data.get('user_name')
        email = cleaned_data.get('email')
        pwd = cleaned_data.get('password')
        pwd_2 = cleaned_data.get('password_repeat')
        if pwd != pwd_2:
            raise forms.ValidationError(
                    "les mots de passe ne correspondent pas"
                )
        elif len(pwd) < 8 or pwd.isalnum():
            raise forms.ValidationError(
                    "le mot de passe doit contenir un charactère spécial / au moins 8 charactères"
                )
        else:
            if User.objects.filter(username=username).exists():
                raise forms.ValidationError(u'l\'utilisateur "%s" est déjà utilisé.' % username)
            elif User.objects.filter(email=email).exists():
                raise forms.ValidationError(u'l\'email "%s" est déjà utilisé.' % email)

        return cleaned_data  # N'oublions pas de renvoyer les données si tout est OK

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'name':'username', 'id' : "inputUsername"}))
    email = forms.EmailField(label="E-mail", widget=forms.TextInput(attrs={'name':'email', 'id' : "inputEmail"}))

    def __init__(self, *args, **kwargs):
        # Get 'initial' argument if any
        initial_arguments = kwargs.get('initial', None)
        updated_initial = {}
        if initial_arguments:
                # We have initial arguments, fetch 'user' placeholder variable if any
                user = initial_arguments.get('user',None)
                # Now update the form's initial values if user
                if user:
                    updated_initial['username'] = getattr(user, 'username', None)
                    updated_initial['email'] = getattr(user, 'email', None)
        
        # Finally update the kwargs initial reference
        kwargs.update(initial=updated_initial)
        super(UserUpdateForm, self).__init__(*args, **kwargs)



    class Meta:
        model = User
        fields = ("username", "email")
