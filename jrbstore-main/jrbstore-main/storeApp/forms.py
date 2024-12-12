from django import forms
from storeApp.models import Producto, Categoria, Registro, Tarjeta
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class CustomSetPasswordForm(SetPasswordForm):
    error_messages = {
        **SetPasswordForm.error_messages,
        'password_too_similar': _("Tu contraseña no puede ser demasiado similar a tu otra información personal."),
        'password_too_common': _("Tu contraseña no puede ser una contraseña comúnmente utilizada."),
        'password_entirely_numeric': _("Tu contraseña no puede ser completamente numérica."),
        'password_mismatch': _("Introduce la misma contraseña que antes para verificación."),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs.update({
            'class': 'inputoe',
            'placeholder': 'Ingresa tu nueva contraseña'
        })
        self.fields['new_password2'].widget.attrs.update({
            'class': 'inputoe',
            'placeholder': 'Confirma tu nueva contraseña'
        })

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'
        widgets = {
            'codigoBarra': forms.NumberInput(attrs={'class': 'inputoe'}),
            'nombre': forms.TextInput(attrs={'class': 'inputoe'}),
            'categoria': forms.Select(attrs={'class': 'inputoe'}),
            'precio': forms.NumberInput(attrs={'class': 'inputoe'}),
            'stock': forms.NumberInput(attrs={'class': 'inputoe'}),
            'descripcion': forms.Textarea(attrs={'class': 'inputoe', 'rows': 3}),
            'foto': forms.FileInput(attrs={'class': 'inputoe'}),
            'plataformas': forms.CheckboxSelectMultiple(attrs={'class': 'inputoe'})  # Selección múltiple
        }

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = '__all__'
        widgets = {
            'categoria' : forms.TextInput(attrs={'class':'inputoe'}),
        } 

class RegistroForm(UserCreationForm):
    nombre = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'inputoe'}))
    
    class Meta:
        model = User
        fields = ('username', 'nombre', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'inputoe'}),
            'email': forms.EmailInput(attrs={'class': 'inputoe'}),
            'password1': forms.PasswordInput(attrs={'class': 'inputoe'}),
            'password2': forms.PasswordInput(attrs={'class': 'inputoe'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'inputoe'})
        self.fields['password2'].widget.attrs.update({'class': 'inputoe'})

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        username = self.cleaned_data.get("username")

        if password2 and username and username in password2:
            raise ValidationError("La contraseña no puede ser similar al nombre de usuario.")

        return password2
    
class TarjetaForm(forms.ModelForm):
    class Meta:
        model = Tarjeta
        fields = '__all__'
        widgets = {
            'codigoBarra': forms.NumberInput(attrs={'class': 'inputoe'}),
            'nombre': forms.TextInput(attrs={'class': 'inputoe'}),
            'categoria': forms.Select(attrs={'class': 'inputoe'}),
            'precio': forms.NumberInput(attrs={'class': 'inputoe'}),
            'stock': forms.NumberInput(attrs={'class': 'inputoe'}),
            'descripcion': forms.Textarea(attrs={'class': 'inputoe', 'rows': 3}),
            'foto': forms.FileInput(attrs={'class': 'inputoe'}),
        }
 