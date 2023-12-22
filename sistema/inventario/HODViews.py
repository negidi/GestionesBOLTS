from inventario.operadorViews import receptionistProfile
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.forms import  UserCreationForm
from .decorators import *
from django.contrib.auth.decorators import login_required
from django.utils import timezone, dateformat
from django.core.exceptions import ValidationError
from datetime import datetime
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import datetime 


from .forms import *
from .models import *


def adminDashboard(request):
    
    producto_total=Producto.objects.all().count()
   


    today = datetime.today()

     


    context={

        "producto_total":producto_total

    }
    return render(request,'hod_templates/admin_dashboard.html',context)



  

@login_required
def crearOperador(request):
    
    if request.method == "POST":
           
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
           
        try:
            user = CustomUser.objects.create_user(username=username, email=email,password=password, first_name=first_name, last_name=last_name,user_type=2)
            user.operador.address = address
            user.operador.mobile = mobile

            user.save()
            messages.success(request, "¡Personal agregado con éxito!")
            return redirect('add_operador')
        except:
            messages.error(request, "¡No se pudo agregar personal!")
            return redirect('add_operador')

    context = {
        "title":"Agregar Operador"

    }
    

    return render(request,'hod_templates/add_operador.html',context)

def manageOperador(request):
    staffs = Operador.objects.all()

    context = {
        "staffs": staffs,
        "title":"Operador Details"

    }

    return render(request,'hod_templates/manage_operador.html',context)

from django.http import JsonResponse

def aCliente(request):
    if request.method == 'POST':
        form = ClienteFormulario(request.POST)
        if form.is_valid():
            cliente = form.save()
            messages.success(request, f'Cliente "{cliente.nombre}" agregado exitosamente.')
            return redirect('listar_clientes')
        else:
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'errors': errors})
    else:
        form = ClienteFormulario()

    contexto = {'form': form, 'modo': request.session.get('clienteProcesado')}
    return render(request, 'hod_templates/modal_cliente.html', contexto)



#cliente

def agregarCliente(request):
    if request.method == 'POST':
        form = ClienteFormulario(request.POST)
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
            return redirect('agregar_Cliente')
    else:
        form = ClienteFormulario()

    
    contexto = {'form': form, 'modo': request.session.get('clienteProcesado')}
    return render(request, 'hod_templates/agregarCliente.html', contexto)

def listarClientes(request):
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
    return render(request, 'hod_templates/listarClientes.html', context)




def EditarCliente(request, p):
    cliente = Cliente.objects.get(id=p)

    if request.method == 'POST':
        form = ClienteFormulario(request.POST, instance=cliente)

        if form.is_valid():
            cliente = form.save()
            messages.success(request, 'cliente actualizada exitosamente.')
            return redirect('editarCliente', p=cliente.id)
    else:
        form = ClienteFormulario(instance=cliente)

    contexto = {'form': form, 'modo': request.session.get('clienteProcesado'), 'editar': True}

    return render(request, 'hod_templates/agregarCliente.html', contexto)




def EliminarCliente(request, p):
    cliente=Cliente.objects.get(id=p)
    if request.method == 'POST':
        cliente.delete()
        messages.success(request, f'Cliente "{cliente.nombre}" eliminado exitosamente.')
        return redirect('listar_clientes')  # Redirige a la lista de clientes u otra página después de eliminar.

    contexto = {'cliente': cliente}
    return render(request, 'hod_templates/sure_delete.html', contexto)

# proveedor

def agregarProveedor(request):
    if request.method == 'POST':
        form = ProveedorFormulario(request.POST)
        if form.is_valid():
            rut = form.cleaned_data['rut']
            nombre = form.cleaned_data['nombre']
            direccion = form.cleaned_data['direccion']
            telefono = form.cleaned_data['telefono']
            correo = form.cleaned_data['correo']

            proveedor = Proveedor(
                rut=rut, nombre=nombre,
                direccion=direccion,
                telefono=telefono, correo=correo

            )
            proveedor.save()
            form = ClienteFormulario()

            messages.success(request, f'Proveedor "{proveedor.nombre}" agregado exitosamente.')
            request.session['proveedorProcesado'] = 'agregado'
            return redirect('agregar_Proveedor')
    else:
        form = ProveedorFormulario()

    
    contexto = {'form': form, 'modo': request.session.get('ProveedorProcesado')}
    return render(request, 'hod_templates/agregarProveedor.html', contexto)


def listarProveedor(request):
    proveedor = Proveedor.objects.all()  # Obtener todos los clientes por defecto

    # Procesar el formulario de búsqueda si se envió
    if request.method == 'GET':
        search_query = request.GET.get('search_query', '')
        if search_query:
            # Aplicar filtros a la consulta para buscar por nombre, apellido, etc.
            proveedor = proveedor.filter(
                nombre__icontains=search_query
            )  # Puedes agregar más filtros según tus necesidades

    context = {'proveedor': proveedor}
    return render(request, 'hod_templates/listarProveedor.html', context)


def EditarProveedor(request, p):
    proveedor = Proveedor.objects.get(id=p)

    if request.method == 'POST':
        form = ProveedorFormulario(request.POST, instance=proveedor)

        if form.is_valid():
            proveedor = form.save()
            messages.success(request, 'proveedor actualizada exitosamente.')
            return redirect('editarProveedor', p=proveedor.id)
    else:
        form = ProveedorFormulario(instance=proveedor)

    contexto = {'form': form, 'modo': request.session.get('proveedorProcesado'), 'editar': True}

    return render(request, 'hod_templates/agregarProveedor.html', contexto)




def EliminarProveedor(request, p):
    proveedor=Proveedor.objects.get(id=p)
    if request.method == 'POST':
        proveedor.delete()
        messages.success(request, f'Proveedor "{proveedor.nombre}" eliminado exitosamente.')
        return redirect('listar_proveedor')  # Redirige a la lista de clientes u otra página después de eliminar.

    contexto = {'proveedor': proveedor}
    return render(request, 'hod_templates/sure_delete.html', contexto)










def AgregarProducto(request):
    if request.method == 'POST':
        form = ProductoFormulario(request.POST, request.FILES)  # Asegúrate de usar request.FILES
        if form.is_valid():
            descripcion = form.cleaned_data['descripcion']
            preciocompra = form.cleaned_data['preciocompra']
            precioventa = form.cleaned_data['precioventa']
            category = form.cleaned_data['category']
            
            stock = 0  # No olvides configurar el stock según tus necesidades

            # Si el formulario es válido, puedes guardar el producto
            prod = Producto(category=category, descripcion=descripcion, preciocompra=preciocompra, precioventa=precioventa, stock=stock, image=request.FILES['image'])
            prod.save()

            messages.success(request, f'{descripcion} se agregó correctamente con ID {prod.id}')
            request.session['productoProcesado'] = 'agregado'
            return redirect('agregar_producto')

    else:
        form = ProductoFormulario()

    contexto = {'form': form, 'modo': request.session.get('productoProcesado')}
    return render(request, 'hod_templates/agregarProducto.html', contexto)






def ListarProducto(request):
    producto = Producto.objects.all()  # Obtener todos los clientes por defecto

    # Procesar el formulario de búsqueda si se envió
    if request.method == 'GET':
        search_query = request.GET.get('search_query', '')
        if search_query:
            # Aplicar filtros a la consulta para buscar por nombre, apellido, etc.
            producto =producto.filter(
                nombre__icontains=search_query
            )  

    context = {'tabla': producto}
    return render(request, 'hod_templates/listar_herramientas.html', context)

from django.shortcuts import render, redirect
from .models import Producto
from .forms import ProductoFormulario

def EditarProducto(request, p):
    producto = Producto.objects.get(id=p)

    if request.method == 'POST':
        form = ProductoFormulario(request.POST, request.FILES, instance=producto)

        if form.is_valid():
            producto = form.save()
            messages.success(request, 'Producto actualizada exitosamente.')
            return redirect('editarProducto', p=producto.id)
    else:
        form = ProductoFormulario(instance=producto)

    contexto = {'form': form, 'modo': request.session.get('productoProcesado'), 'editar': True}

    return render(request, 'hod_templates/agregarProducto.html', contexto)




def EliminarProducto(request,pk):
    try:
    
        producto=Producto.objects.get(id=pk)
        if request.method == 'POST':
        
            producto.delete()
            messages.success(request, "Producto eliminado")
                
            return redirect('listar_herramientas')

    except:
        messages.error(request, "Producto ya eliminado")
        return redirect('listar_herramientas')
    

    return render(request,'hod_templates/sure_delete.html')



def realizarPedido(request):
    if request.method == 'POST':
        form = PedidoFormulario(request.POST)
        if form.is_valid():
            form.save()  # Esto guarda el pedido en la base de datos
            # No es necesario realizar acciones adicionales aquí
            
    else:
        form = PedidoFormulario()

    contexto = {'form': form}
    return render(request, 'hod_templates/agregarPedido.html', contexto)

def listarPedido(request):
    if request.method == 'POST':
        pedido_id = request.POST.get('pedido_id')
        if pedido_id:
            pedido = Pedido.objects.get(id=pedido_id)

            if not pedido.recibido:
                # Marca el pedido como recibido
                pedido.recibido = True
                pedido.save()

                # Actualiza el stock en el modelo Producto
                producto = pedido.producto
                producto.stock += pedido.cantidad
                producto.save()

    # Obtén la lista de pedidos
    pedidos = Pedido.objects.all()
    contexto = {'pedidos': pedidos}
    return render(request, 'hod_templates/listarPedido.html', contexto)




from django.urls import reverse

# Resto del código

def recibirPedido(request, pedido_id):
    pedido = Pedido.objects.get(id=pedido_id)

    if not pedido.recibido:
        producto = pedido.producto
        producto.stock += pedido.cantidad
        producto.save()

        pedido.recibido = True
        pedido.save()

    return redirect('listar_pedido') 

    


def emitirFactura(request):
  
   return render(request,'hod_templates/emitirFactura.html') 


def verReportes(request):
      
   return render(request,'hod_templates/verReportes.html') 



def addCategory(request):
    try:
        form=CategoryForm(request.POST or None)

        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(request, "Categoría añadida ¡Con éxito!")

                return redirect('add_category')
    except:
        messages.error(request, "Categoría ¡No añadido! Inténtalo de nuevo")

        return redirect('add_category')

    
    context={
        "form":form,
        "title":"Agregar una nueva categoria"
    }
    return render(request,'hod_templates/add_category.html',context)



    


    

       

    




def hodProfile(request):
    customuser=CustomUser.objects.get(id=request.user.id)
    staff=AdminHOD.objects.get(admin=customuser.id)


    form=HodForm()
    if request.method == 'POST':
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
       
        address = request.POST.get('address')
        mobile = request.POST.get('mobile')

        customuser=CustomUser.objects.get(id=request.user.id)
        customuser.first_name=first_name
        customuser.last_name=last_name
        customuser.save()

        staff=AdminHOD.objects.get(admin=customuser.id)
        form =HodForm(request.POST,request.FILES,instance=staff)
        staff.address = address
       
        staff.mobile=mobile
        staff.save()

        if form.is_valid():
            form.save()

    context={
        "form":form,
        "staff":staff,
        "user":customuser
    }

    return render(request,'hod_templates/hod_profile.html',context)

    


   

def editarOperador(request,operador_id):
    operador=Operador.objects.get(admin=operador_id)
    if request.method == "POST":
        username = request.POST.get('username')
        last_name=request.POST.get('last_name')
        first_name=request.POST.get('first_name')
        address=request.POST.get('address')
        mobile=request.POST.get('mobile')
        gender=request.POST.get('gender')
        email=request.POST.get('email')
    
        try:
            user=CustomUser.objects.get(id=operador_id)
            user.email=email
            user.username=username
            user.first_name=first_name
            user.last_name=last_name
            user.save()

            operador =Operador.objects.get(admin=operador_id)
            operador.address=address
            operador.mobile=mobile
            operador.gender=gender
            operador.save()

            messages.success(request,'Receptionist Updated Succefully')
        except:
            messages.success(request,'An Error Was Encounterd Receptionist Not Updated')


        
    context={
        "staff":operador,
        "title":"Editar Operador"


    }
    return render(request,'hod_templates/editarOperador.html',context)


def editAdmin(request):
    customuser=CustomUser.objects.get(id=request.user.id)
    staff=AdminHOD.objects.get(admin=customuser.id)


    form=HodForm()
    if request.method == 'POST':
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
       
        address = request.POST.get('address')
        mobile = request.POST.get('mobile')

        customuser=CustomUser.objects.get(id=request.user.id)
        customuser.first_name=first_name
        customuser.last_name=last_name
        customuser.save()

        staff=AdminHOD.objects.get(admin=customuser.id)
        form =HodForm(request.POST,request.FILES,instance=staff)
        staff.address = address
       
        staff.mobile=mobile
        staff.save()

        if form.is_valid():
            form.save()

    context={
        "form":form,
        "staff":staff,
        "user":customuser
    }

    return render(request,'hod_templates/edit-profile.html',context)










