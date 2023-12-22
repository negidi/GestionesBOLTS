from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.forms import  UserCreationForm
from .decorators import *
from django.contrib.auth.decorators import login_required

from .forms import *
from .models import *


@login_required
def clerkHome(request):
   

    context={
       
    }
    return render(request,'operador_templates/clerk_home.html',context)



@login_required
def receptionistProfile(request):
    customuser = CustomUser.objects.get(id=request.user.id)
    staff = Operador.objects.get(admin=customuser.id)

    form=OperadorForm()
    if request.method == "POST":
       

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        address = request.POST.get('address')
        phone_number=request.POST.get('phone_number')

      
        customuser = CustomUser.objects.get(id=request.user.id)
        customuser.first_name = first_name
        customuser.last_name = last_name
        customuser.save()

        staff = Operador.objects.get(admin=customuser.id)
        form=OperadorForm(request.POST,request.FILES,instance=staff)

        staff.address = address
        staff.phone_number=phone_number
        staff.save()
        if form.is_valid():
            form.save()
        

    context={
        "form":form,
        "staff":staff,
        'user':customuser
    }
      

    return render(request,'operador_templates/clerk_profile.html',context)


    


    
@login_required
def crearCliente(request):
    form=ClienteFormulario(request.POST, request.FILES)
    try:
        if request.method == "POST":
            if form.is_valid():
            
                cedula = form.cleaned_data['cedula']
                nombre = form.cleaned_data['nombre']
                apellido = form.cleaned_data['apellido']
                direccion = form.cleaned_data['direccion']
                nacimiento = form.cleaned_data['nacimiento']
                telefono = form.cleaned_data['telefono']
                correo = form.cleaned_data['correo']
            
        
                cliente = Cliente(
                    cedula=cedula, nombre=nombre, apellido=apellido,
                    direccion=direccion, nacimiento=nacimiento,
                    telefono=telefono, correo=correo
                )
                cliente.save()
                form = ClienteFormulario()

                messages.success(request, f'Cliente "{cliente.nombre}" agregado exitosamente.')
                request.session['clienteProcesado'] = 'agregado'
                return redirect('crear_cliente')
            
    except:
        
        messages.error(request, f'Error al agregar cliente: {str(e)}')
        return redirect('crear_cliente')
    contexto = {'form': form, 'modo': request.session.get('clienteProcesado')}
       
    return render(request, 'operador_templates/crearCliente.html', contexto)

@login_required
def listClientes(request):
    clientes = Cliente.objects.all()  # Obtener todos los clientes por defecto

    # Procesar el formulario de búsqueda si se envió
    if request.method == 'GET':
        search_query = request.GET.get('search_query', '')
        if search_query:
            # Aplicar filtros a la consulta para buscar por nombre, apellido, etc.
            clientes = clientes.filter(
                nombre__icontains=search_query
            )  # Puedes agregar más filtros según tus necesidades

    context = {'clientes': clientes}
    return render(request, 'operador_templates/listClientes.html', context)







       

