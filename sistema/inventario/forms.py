from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.forms import Form
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from phonenumber_field.formfields import PhoneNumberField
from django.core.validators import RegexValidator

import json



class DateInput(forms.DateInput):
    input_type = "date"

from phonenumber_field.formfields import PhoneNumberField
class ClientForm(forms.Form):
    mobile = PhoneNumberField()




    


# forms.py
class ProductoFormulario(forms.ModelForm):
    precioventa = forms.DecimalField(
        min_value=0,
        label='Precio Venta',
        widget=forms.NumberInput(attrs={'placeholder': 'Precio Venta', 'id': 'precio', 'class': 'form-control'}),
    )
    preciocompra = forms.DecimalField(
        min_value=0,
        label='Precio Compra',
        widget=forms.NumberInput(attrs={'placeholder': 'Precio Compra', 'id': 'precio', 'class': 'form-control'}),
    )
    image = forms.ImageField(
        label='Imagen',
        required=False,  # Permite que el campo sea opcional al editar
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Producto
        fields = ['category', 'descripcion', 'preciocompra', 'precioventa', 'image']
        labels = {
            'descripcion': 'Nombre',
        }
        widgets = {
            'descripcion': forms.TextInput(attrs={'placeholder': 'Nombre del producto', 'id': 'descripcion', 'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control', 'id': 'category'}),
        }


# views.py



class ClienteFormulario(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['cedula','nombre','apellido','direccion','nacimiento','telefono','correo']
        labels = {
        'cedula': 'Cedula del cliente',
        'nombre': 'Nombre del cliente',
        'apellido': 'Apellido del cliente',
        'direccion': 'Direccion del cliente',
        'nacimiento': 'Fecha de nacimiento del cliente',
        'telefono': 'Numero telefonico del cliente',
        'correo': 'Correo electronico del cliente',
        }
        widgets = {
        'cedula': forms.TextInput(attrs={'placeholder': 'Inserte la cedula de identidad del cliente',
        'id':'cedula','class':'form-control'} ),
        'nombre': forms.TextInput(attrs={'placeholder': 'Inserte el primer o primeros nombres del cliente',
        'id':'nombre','class':'form-control'}),
        'apellido': forms.TextInput(attrs={'class':'form-control','id':'apellido','placeholder':'El apellido del cliente'}),
        'direccion': forms.TextInput(attrs={'class':'form-control','id':'direccion','placeholder':'Direccion del cliente'}), 
        'nacimiento':forms.DateInput(format=('%d-%m-%Y'),attrs={'id':'hasta','class':'form-control','type':'date'} ),
        'telefono':forms.TextInput(attrs={'id':'telefono','class':'form-control',
        'placeholder':'El telefono del cliente'} ),
        'correo':forms.TextInput(attrs={'placeholder': 'Correo del cliente',
        'id':'correo','class':'form-control'} )
        }


class ProveedorFormulario(forms.ModelForm):


    class Meta:
        model = Proveedor
        fields = ['rut','nombre','direccion','telefono','correo']
        labels = {
        'rut': 'Rut del proveedor',
        'nombre': 'Nombre del proveedor',
        'direccion': 'Direccion del proveedor',
        'telefono': 'Numero telefonico del proveedor',
        'correo': 'Correo electronico del proveedor',
        }
        widgets = {
        'rut': forms.TextInput(attrs={'placeholder': 'Inserte rut del proveedor',
        'id':'rut','class':'form-control'} ),
        'nombre': forms.TextInput(attrs={'placeholder': 'Inserte el primer o primeros nombres del proveedor',
        'id':'nombre','class':'form-control'}),
        'direccion': forms.TextInput(attrs={'class':'form-control','id':'direccion','placeholder':'Direccion del proveedor'}), 
        'telefono':forms.TextInput(attrs={'id':'telefono','class':'form-control',
        'placeholder':'El telefono del proveedor'} ),
        'correo':forms.TextInput(attrs={'placeholder': 'Correo del proveedor',
        'id':'correo','class':'form-control'} )
        } 
class OperadorForm(ModelForm):
    class Meta:
        model=Operador
        fields='__all__'
        exclude=['admin','gender','mobile','address']



class CategoryForm(forms.ModelForm):
    class Meta:
        model=Category
        fields='__all__'




class PedidoFormulario(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['producto', 'proveedor', 'cantidad']

    def clean_cantidad(self):
        cantidad = self.cleaned_data['cantidad']
        if cantidad <= 0:
            raise forms.ValidationError("La cantidad debe ser mayor que 0.")
        return cantidad








       


class HodForm(ModelForm):
    class Meta:
        model=AdminHOD
        fields='__all__'
        exclude=['admin','gender','mobile','address']




        
