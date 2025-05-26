from Models.model import Cotizaciones
def usuario_registrado( obj_user:Cotizaciones):
    mensaje_registrar = ""
    if(obj_user.nombrecliente_cotizacion== "" ):
        mensaje_registrar = "El nombre no puede estar vacio"
        return mensaje_registrar
    if(obj_user.correocliente_cotizacion== "" ):
        mensaje_registrar = "El correo no puede estar vacio"
        return mensaje_registrar
    if(obj_user.tservicio_cotizacion== "" ):
        mensaje_registrar = "El servicio no puede estar vacio"
        return mensaje_registrar
    return "usuario creado exitosamente"