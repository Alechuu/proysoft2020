#from app.models.permiso import Permiso
#from app.models.user import User

def usuarioTienePermiso(unUsuario, unPermiso):
    tienePermiso = False
    for unRol in unUsuario.roles:        
        if unRol.permisos.count(unPermiso) > 0:
            tienePermiso = True
    return tienePermiso

def get_permisos(unUsuario):
    #Retorno una lista con los nombres de los permisos del usuario
    lista_permisos = set()
    for unRol in unUsuario.roles:
        for unPermiso in unRol.permisos:
            lista_permisos.add(unPermiso.nombre)
    return lista_permisos
