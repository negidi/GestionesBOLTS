from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.phonenumber import PhoneNumber

from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.core.cache import cache 
from django.db.models import BooleanField, ExpressionWrapper, Q
from django.db.models.functions import Now
from django.contrib.auth.models import AbstractUser
from django.db import models

from django.contrib.auth.models import AbstractUser



class CustomUser(AbstractUser):
    user_type_data = ((1, "AdminHOD"), (2, "Operador"))
    user_type = models.CharField(default=1, choices=user_type_data, max_length=10)

    # Agrega otros campos personalizados que necesites para tu usuario








class AdminHOD(models.Model):
    gender_category=(
        ('Male','Male'),
        ('Female','Female'),
    )
    admin = models.OneToOneField(CustomUser,null=True, on_delete = models.CASCADE)
    emp_no= models.CharField(max_length=100,null=True,blank=True)
    gender=models.CharField(max_length=100,null=True,choices=gender_category)
    mobile=models.CharField(max_length=10,null=True,blank=True)
    address=models.CharField(max_length=300,null=True,blank=True)
    profile_pic=models.ImageField(default="admin.png",null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    date_employed=models.DateTimeField(auto_now_add=True, auto_now=False)
    objects = models.Manager()
    def __str__(self):
        return str(self.admin)
    

    

class Operador(models.Model):
    gender_category=(
        ('Masculino','Masculino'),
        ('Femenino','Femenino'),
    )
    admin = models.OneToOneField(CustomUser,null=True, on_delete = models.CASCADE)
    emp_no=models.CharField(max_length=100,null=True,blank=True)
    age= models.IntegerField(default='0', blank=True, null=True)
    gender=models.CharField(max_length=100,null=True,choices=gender_category)
    mobile=models.CharField(max_length=10,null=True,blank=True)
    address=models.CharField(max_length=300,null=True,blank=True)
    profile_pic=models.ImageField(default="doctor.png",null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    def __str__(self):
        return str(self.admin)


class Category(models.Model):
    nombre = models.CharField(max_length=50, blank=False, null=True)
    
    def __str__(self):
        return str(self.nombre)
	

    



#operador 



   
# clase cliente
class Cliente(models.Model):
    #id
    cedula = models.CharField(max_length=12, unique=True)
    nombre = models.CharField(max_length=40)
    apellido = models.CharField(max_length=40)
    direccion = models.CharField(max_length=200)
    nacimiento = models.DateField()
    telefono = models.CharField(max_length=20)
    correo = models.CharField(max_length=100)
    def __str__(self):
        return f'{self.nombre} - {self.cedula}'


    @classmethod
    def numeroRegistrados(self):
        return int(self.objects.all().count() )

    @classmethod
    def cedulasRegistradas(self):
        objetos = self.objects.all().order_by('nombre')
        arreglo = []
        for indice,objeto in enumerate(objetos):
            arreglo.append([])
            arreglo[indice].append(objeto.cedula)
            nombre_cliente = objeto.nombre + " " + objeto.apellido
            arreglo[indice].append("%s. C.I: %s" % (nombre_cliente,self.formatearCedula(objeto.cedula)) )
 
        return arreglo   



#operador



class Producto(models.Model):
    #id
    category = models.ForeignKey(Category,null=True,on_delete=models.CASCADE,blank=True)
    descripcion = models.CharField(max_length=40)
    image = models.ImageField(null=True, blank=True)
    preciocompra = models.DecimalField(max_digits=9,decimal_places=2) 
    precioventa = models.DecimalField(max_digits=9,decimal_places=2)
    stock= models.IntegerField(null=True)
    #tiene_iva = models.BooleanField(null=True)

    def __str__(self):
        return str(self.descripcion)
    @classmethod
    def productosRegistrados(self):
        objetos = self.objects.all().order_by('descripcion')
        return objetos




#------------------------------------------PROVEEDOR-----------------------------------
class Proveedor(models.Model):
    #id
    rut = models.CharField(max_length=12, unique=True)
    nombre = models.CharField(max_length=40)
    apellido = models.CharField(max_length=40)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20)
    correo = models.CharField(max_length=100)
    def __str__(self):
        return f'{self.nombre} - {self.rut}'

    @classmethod
    def cedulasRegistradas(self):
        objetos = self.objects.all().order_by('nombre')
        arreglo = []
        for indice,objeto in enumerate(objetos):
            arreglo.append([])
            arreglo[indice].append(objeto.rut)
            nombre_proveedor = objeto.nombre 
            arreglo[indice].append("%s. C.I: %s" % (nombre_proveedor,self.formatearRut(objeto.rut)) )
 
        return arreglo 

    @staticmethod
    def formatearCedula(rut):
        return format(int(rut), ',d')  


from django.db import models

class Pedido(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_total = models.DecimalField(max_digits=9, decimal_places=2)
    recibido = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Calcula el precio total antes de guardar el pedido
        self.precio_total = self.producto.preciocompra * self.cantidad
        super(Pedido, self).save(*args, **kwargs)




#-------------------------------------FACTURA---------------------------------------------








@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:
            AdminHOD.objects.create(admin=instance)
        if instance.user_type == 2:
            Operador.objects.create(admin=instance,address="")
     
     
       
       
       

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.adminhod.save()
    if instance.user_type == 2:
        instance.operador.save()



   



 