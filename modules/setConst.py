#-*- coding: utf-8 -*-
#
# Orfeopy, Sistema de gestion documental basado en python 
# Site: https://github.com/orfeopy/ 
# desarrollado por aurigadl@gmail.com
#
# Copyright (c) 2011 correlibre.org 
#
# License Code: GPL, General Public License v. 2.0
# License Content: Creative Commons Attribution 3.0 
#
# Also visit: orfeogpl.org
#             or Groups: http://groups.google.com/group/orfeopy 
#                http://groups.google.com/group/orfeopy-usuarios  
#
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>

import datetime

from gluon.tools        import Auth    
from gluon.tools        import Mail
from gluon.tools        import Recaptcha

from gluon.html         import *
from gluon.http         import *
from gluon.validators   import *
from gluon.sqlhtml      import *
from gluon.sql          import *
from xmlConv            import *

class setConst(object):
    ''' Asigna las variables del archivo
        suministrado al sistema. '''

    def __init__(self, file, globals, response):
        ''' Inicio de variables globales
            que pertenecen al framework'''
        self.file       = file   
        self.globals    = globals 
        self.response   = response
        dicTmp          = self.getConfigvar() 
        self.config     = dicTmp.config_var
        self.init_web()

    def setConfile(self, file):
        self.file  = file   
        
    def getConfigvar(self):
        ''' Retorna el diccionario con los valores
            del archivo de configuracion xml en un
            diccionario'''
        datos = ConvertXmlToDict(self.file)
        return datos

    def connect_to_db(self):
        ''' Coneccion a la base  de  datos '''
        self.db = DAL(self.config.DB_CONNECT_URI)
        return self.db

    def init_mail(self):
        ''' Configuracion del corrreo electronico
            necesario para enviar correos en el registro
            de usuarios'''
        mail                 = Mail() # mailer
        mail.settings.server = self.config.MAIL_SERVER or 'smtp.gmail.com:587' # your SMTP server
        mail.settings.sender = self.config.MAIL_SERVER # your email
        mail.settings.login  = self.config.MAIL_LOGIN  # your credentials or None
        self.mail            = mail
        return mail

    def init_web(self):
        ''' Configuracion de variables que personalizan la 
            pagina como titulo, palabras claves etc.'''

        response = self.response
        config   = self.config

        response.title            = config.CONF_TITLE
        response.subtitle         = config.CONF_SUBTITLE
        response.keywords         = config.CONF_KEYWORDS 
        response.description      = config.CONF_DESCRIPTION 
        response.meta.author      = config.CONF_AUTHOR 
        response.meta.description = config.CONF_DESCRIPTION 
        response.meta.keywords    = config.CONF_KEYWORDS 
        response.meta.generator   = config.CONF_GENERATOR 
        response.meta.copyright   = config.CONF_COPYRIGHT 
        response.confMenu         = config.CONF_MENU 

class myAuth(Auth):
    ''' Heredamos de auth para personalizar
        los mensajes, variables de configuracion
        y crear metodos para plugins'''

    def __init__(self, file, globals, db, mail):
        ''' Inicio de variables globales
            que pertenecen al framework'''
            
        Auth.__init__(self, globals, db)
        datos           = ConvertXmlToDict(file)
        self.config     = datos.config_var
        self.globals    = globals
        self.db   		= db
        self.mail 		= mail
        self.setMessa()
		
    def initAuth(self):
        ''' Configuracion de las tablas y parametros de usuario
            registro y validacion de cuentas '''
        db      = self.db
        globals = self.globals
        request = globals.request
        T       = globals.T 

        #8.1.4 Customizing Auth page 350
        self.settings.hmac_key  = self.config.AUTH_HMAC_KEY # before define_tables()
        self.settings.formstyle = 'divs' #format of form

        if self.config.AUTH_REGIS_METHOD in ['Disabled']:
            self.settings.actions_disabled.append('register') #disable register
        #Recaptcha (pag349)
        if self.config.AUTH_REGIS_METHOD  in ['Recaptcha']:
            self.settings.captcha = Recaptcha(request, self.config.AUTH_RECAP_PUBLKEY, self.config.AUTH_RECAP_PRIVKEY)    
        
        db.define_table(
            self.settings.table_user_name,
            Field('first_name', length=128, default=''),
            Field('last_name', length=128, default=''),
            Field('email', length=128, default='', unique=True),
            Field('password', 'password', length=512,
                  readable=False, label='Password'),
            Field('registration_key', length=512,
                  writable=False, readable=False, default=''),
            Field('reset_password_key', length=512,
                  writable=False, readable=False, default=''),
            Field('registration_id', length=512,
                  writable=False, readable=False, default=''),
            Field('created_on', 'datetime', default=datetime.datetime.today(),
                      writable=False,readable=False),                
            Field('site_language', length=128,writable=False, readable=False, 
                  default='', label=T('Language')))
        
        custom_auth_table                     = db[self.settings.table_user_name] # get the custom_auth_table
        custom_auth_table.first_name.requires = IS_NOT_EMPTY(error_message = self.messages.is_empty)
        custom_auth_table.last_name.requires  = IS_NOT_EMPTY(error_message = self.messages.is_empty)
        custom_auth_table.password.requires   = [CRYPT(key = self.settings.hmac_key)]
        custom_auth_table.email.requires = [
          IS_EMAIL(error_message = self.messages.invalid_email),
          IS_NOT_IN_DB(db, custom_auth_table.email)]
        
        self.settings.table_user = custom_auth_table

        self.define_tables()         # creates all needed tables
        self.settings.mailer = self.mail  # for user email verification
        
        if self.config.AUTH_REGIS_METHOD in ['None','Recaptcha','Approval']:
            self.settings.registration_requires_verification = False
        else:
            self.settings.registration_requires_verification = True
        
        if self.config.AUTH_REGIS_METHOD in ['Approval']:
            self.settings.registration_requires_approval = True
        else:
            self.settings.registration_requires_approval = False
        
        self.settings.reset_password_requires_verification = True
            
        self.messages.verify_email = 'Click on the link http://'+request.env.http_host+\
            URL(r=request,c='default',f='user',args=['verify_email'])+\
            '/%(key)s to verify your email'
        self.messages.reset_password = 'Click on the link http://'+request.env.http_host+\
            URL(r=request,c='default',f='user',args=['reset_password'])+\
            '/%(key)s to reset your password'
    
    def setMessa(self):
        ''' Configuracion de los mensajes suministrados al
            usuario para autenticacion'''
        globals = self.globals
        T       = globals.T
        self.messages.logged_in                 = T("Logged in")
        self.messages.email_sent                = T("Email sent")
        self.messages.email_verified            = T("Email verified")
        self.messages.logged_out                = T("Logged out")
        self.messages.registration_successful   = T("Registration successful")
        self.messages.invalid_email             = T("Invalid email")
        self.messages.invalid_login             = T("Invalid login")
        self.messages.verify_email_subject      = T("Password verify")
        self.messages.username_sent             = T("Your username was emailed to you")
        self.messages.new_password_sent         = T("A new password was emailed to you")
        self.messages.password_changed          = T("Password changed")
        self.messages.retrieve_username         = str(T("Your username is"))+": %(username)s"
        self.messages.retrieve_username_subject = "Username retrieve"
        self.messages.retrieve_password         = str(T("Your password is"))+": %(password)s"
        self.messages.retrieve_password_subject = T("Password retrieve")
        self.messages.profile_updated           = T("Profile updated")

    def relacionUsuaplug(self, plug_name, user_id=None):
        ''' Valida la existencia entre un usuario 
            y un plugin '''
        db            = self.db
        self.plugName = plug_name
        memb          = db.auth_membership.group_id
        r             = False 

        if not user_id and self.user: 
            user_id = self.user.id 

        # list1 grupos a los cuales el usuario pertenece
        query1 = db.auth_membership.user_id == user_id 
        list1  = db(query1).select(memb, distinct=True)
        grupUs = [int(p.group_id) for p in list1] 

        # id del plugin suministrado
        query2 = db.plug_plugins.plug_nombre == plug_name 
        idPlug = db(query2).select(db.plug_plugins.id)
        plugid = idPlug[0].id

        # list2 id del plugin suministrado
        query3 = db.auth_modules.plug_plugins_id == plugid
        list2  = db(query3).select(db.auth_modules.auth_group_id)
        grupMo = [int(p.auth_group_id)  for p in list2] 

        for grup in grupMo:
            if grup in grupUs:
                r = True 
                break

        log = self.messages.has_membership_log 

        if log: 
            self.log_event(log % dict(user_id=user_id, 
                                group_id=group_id, check=r)) 
        return r 

    def relausuaSubplug(self, plug_name, pref, user_id=None):
        ''' Retorna datos existentes entre un usuario 
            y un subplugin 
            plug_name: Nombre del plugin a evaluar
            plug_pref: Permiso a consultar del plugin
            user_id: Usuario registrado que se evalua'''

        db            = self.db
        memb          = db.subp_plugins.subp_dato 
        memn          = db.subp_plugins.subp_nombre 

        if not user_id and self.user: 
            user_id = self.user.id 

        # grupos a los cuales el usuario pertenece
        qur1 = db.auth_membership.user_id  == user_id 
        qur2 = db.auth_membership.group_id == db.auth_modules.auth_group_id 
        qur4 = db.plug_plugins.plug_nombre == plug_name 
        qur5 = db.plug_plugins.id == db.auth_modules.plug_plugins_id 
        qur6 = db.subp_plugins.plug_plugins_id == db.auth_modules.plug_plugins_id 
        qur7 = db.subp_plugins.subp_pref == pref
        qur8 = db.auth_submodules.subp_plugins_id == db.subp_plugins.id
        qur9 = db.auth_submodules.auth_group_id == db.auth_membership.group_id

        list1  = db(qur1 & qur2 & qur4 & qur5 & qur6 & qur7 & qur8 & qur9).select(memb,memn,distinct=True)
        grupUs = list1.as_list()

        return grupUs
