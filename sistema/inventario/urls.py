from django.urls import path
from .import HODViews
from .import views,operadorViews
from django.contrib.auth import views as auth_views


urlpatterns=[
    path('',HODViews.adminDashboard,name='admin_dashboard'),
 
    path('login/',views.loginPage,name='login'),
    path('logout/',views.logoutUser,name='logout'), 
    # path('get_user_details/', views.get_user_details, name="get_user_details"),

    path('admin_user/add_operador/',HODViews.crearOperador,name='add_operador'),
    
    path('admin_user/manage_operador/',HODViews.manageOperador,name='manage_operador'),


    path('admin_user/add_category/',HODViews.addCategory,name='add_category'), 
    
    path('admin_user/agregar_producto/', HODViews.AgregarProducto, name='agregar_producto'),
    path('admin_user/listar_herramienta/',HODViews.ListarProducto, name='listar_herramientas'),
    path('admin_user/editarProducto/<int:p>', HODViews.EditarProducto, name='editarProducto'),
    path('admin_user/eliminarProducto/<int:pk>', HODViews.EliminarProducto, name='eliminarHerramienta'),
    
    path('admin_user/aCliente/', HODViews.aCliente, name='a_Cliente'),
    path('admin_user/agregarCliente/', HODViews.agregarCliente, name='agregar_Cliente'),
    path('listar_clientes/', HODViews.listarClientes, name='listar_clientes'),
    path('admin_user/editarCliente/<int:p>', HODViews.EditarCliente, name='editarCliente'),
    path('admin_user/eliminarCliente/<int:p>', HODViews.EliminarCliente, name='eliminarCliente'),

    path('admin_user/agregarProveedor/', HODViews.agregarProveedor, name='agregar_Proveedor'),

    path('listar_proveedor/', HODViews.listarProveedor, name='listar_proveedor'),
    path('admin_user/editarProveedor/<int:p>', HODViews.EditarProveedor, name='editarProveedor'),
    path('admin_user/eliminarProveedor/<int:p>', HODViews.EliminarProveedor, name='eliminarProveedor'),

    path('admin_user/agregarPedido/', HODViews.realizarPedido, name='agregar_Pedido'),
    path('listar_pedido/', HODViews.listarPedido, name='listar_pedido'),
    path('recibir_pedido/<int:pedido_id>/', HODViews.recibirPedido, name='recibir_pedido'),

     path('recibir_factura/', HODViews.emitirFactura, name='emitir_factura'),
   # path('admin_user/emitirfactura/', HODViews.emitirFactura, name='emitir_factura'),

    path('ver_reportes/', HODViews.verReportes, name='ver_reportes'),

    path('admin_user/hod_profile/',HODViews.hodProfile,name='hod_profile'),

    
    path('admin_user/hod_profile/editAdmin_profile/',HODViews.editAdmin,name='edit-admin'),

    path('admin_user/edit_receptionist/<operador_id>/', HODViews.editarOperador, name="editar_operador"),


   

    #Receptionist
    path('receptionist_profile/',operadorViews.receptionistProfile,name='clerk_profile'),
    path('receptionist_home/',operadorViews.clerkHome,name='clerk_home'),
    
    path('receptionist/crear_form/',operadorViews.crearCliente,name='crear_cliente'),
    
    path('receptionist/list_client/', operadorViews.listClientes, name='list_cliente'),




  
    path('reset_password/',auth_views.PasswordResetView.as_view(template_name="password_reset.html"),name="reset_password"),

    path('reset_password_sent/',auth_views.PasswordResetDoneView
    .as_view(template_name="password_reset_sent.html"),name="password_reset_done"),
    
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView
    .as_view(template_name="password_reset_form.html"),name="password_reset_confirm"),



    

   path('reset_password_complete/',auth_views.PasswordResetCompleteView
    .as_view(template_name="password_reset_done.html"),name="password_reset_complete"),
]
