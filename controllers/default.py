# -*- coding: utf-8 -*- 
@auth.requires_login()
def index():
    """
    Pantalla inicial de la aplicacion
    """
    menu = plugin.navegacion(db, auth.user_id)
    tab = menu.enlaTabs()
    lisM = menu.getlistMenu()
    response.flash=T("!I see you! ;-)")
    return dict(tabs=tab, lism=lisM)
    
def user():
    """
    Index de la aplicacion
    Pagina mostrada para que el usuario
    se registre o ingrese.
    """
    response.flash=T("!Orfeopy welcome ;-)")
    return dict(form=auth())
