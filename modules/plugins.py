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

from gluon.tools        import Auth    
from gluon.sql          import *
from gluon.html         import *
from gluon.validators   import *
from xmlConv            import *

class plugins(object):
    ''' Registra los plugin instalados
        y permite que el administrador
        relacione los plugins con los grupos '''

    def __init__(self, globals, db):
        ''' Creamos las tablas si estas no existen '''
        self.db			= db
        self.globals    = globals 

    def regisPlugins(self):
        ''' Registramos las tablas de modulo que permitiran 
            agrupar los plugins con los grupos y asignar de 
            esta manera permisos sobre las acciones '''

        db      = self.db
        globals = self.globals
        T       = globals.T 
        request = globals.request
        response= globals.response

        #Define tabla del plugins
        db.define_table('plug_plugins',
            Field('plug_nombre'   	, label=T('Nombre')),
            Field('plug_descripcion', label=T('Descripcion')),
            Field('plug_fecha'      , 'datetime', default=request.now),
            Field('plug_autor'      , label=T('Autor')),
            Field('plug_tip'        , label=T('Tip')),
            Field('plug_icono'      , label=T('Icono'), notnull=True),
            Field('plug_enlace'     , label=T('PaginaWeb')),
            Field('plug_prevPlugins', 'list:string', label=T('Plugins requeridos')),
            Field('plug_tab'        , label=T('Tab')),
            Field('plug_version'    , label=T('Version')))


        # response.confMenu viene de setConst.py
        menu = response.confMenu.split(',')
        dbp   = db.plug_plugins

        # Restriccion de la tabla plugins
        dbp.plug_nombre.requires    = IS_NOT_IN_DB(db, dbp.plug_nombre)
        dbp.plug_nombre.writable    = False
        dbp.plug_nombre.readable    = False
        dbp.plug_nombre.notnull     = True
        dbp.plug_descripcion.length = 500
        dbp.plug_fecha.writable     = False
        dbp.plug_fecha.readable     = False
        dbp.plug_autor.length       = 200
        dbp.plug_tip.default        = 'Esto aparece en el menu'
        dbp.plug_tip.length         = 100
        dbp.plug_icono.requires     = IS_NOT_IN_DB(db, dbp.plug_icono)
        dbp.plug_icono.length       = 100
        dbp.plug_enlace.length      = 300
        dbp.plug_tab.requires       = IS_IN_SET(menu, zero= T('Selecciona uno'))
        dbp.plug_tab.default        = 'Acciones' 

        #Define tabla relacion plugin y grupo
        db.define_table('auth_modules',
            Field('plug_plugins_id', 'integer' , db.plug_plugins.id),
            Field('auth_group_id'  , 'integer' , db.auth_group.id))

        #Restricciones de la tabla modules
        db.auth_modules.auth_group_id.requires = IS_IN_DB(db, 'auth_group.id',
                '%(role)s', zero=T('Selecciona uno'))

        db.auth_modules.plug_plugins_id.requires = IS_IN_DB(db, 'plug_plugins.id',
                '%(plug_nombre)s', zero=T('Selecciona uno'))
                

        #Define tabla sub_plugins
        db.define_table('subp_plugins',
            Field('plug_plugins_id' , 'integer' , db.plug_plugins.id),
            Field('subp_pref'   	, label=T('prefijo')),
            Field('subp_nombre'   	, label=T('Nombre')),
            Field('subp_descripcion', label=T('Descripcion')),
            Field('subp_dato'       , label=T('Variable')),
            )

        dbs = db.subp_plugins 

        # Restriccion de la tabla sub_plugins
        dbs.subp_nombre.requires        = IS_NOT_IN_DB(db, 'subp_plugins.subp_pref'
                                            ,'subp_plugins.subp_nombre'
                                            ,'subp_plugins.subp_dato')
        dbs.subp_nombre.writable        = False
        dbs.plug_plugins_id.requires    = IS_IN_DB(db, 'plug_plugins.id',
                '%(role)s', zero=T('Selecciona uno'))
        dbs.subp_pref.required        = True
        dbs.subp_nombre.required      = True
        dbs.subp_descripcion.required = True
        dbs.subp_dato.required        = True
        dbs.plug_plugins_id.required  = True

        #Define tabla relacion sub_plugin y grupo
        db.define_table('auth_submodules',
            Field('subp_plugins_id', 'integer' , db.subp_plugins.id),
            Field('auth_group_id'  , 'integer' , db.auth_group.id))

        #Restricciones de la tabla submodules
        db.auth_submodules.auth_group_id.requires = IS_IN_DB(db, 'auth_group.id',
                '%(role)s', zero=T('Selecciona uno'))

        db.auth_submodules.subp_plugins_id.requires = IS_IN_DB(db, 'subp_plugins.id',
                '%(subp_nombre)s', zero=T('Selecciona uno'))

        self.db = db

    def insertPlugin(self, registro):
        ''' Creamos el resgistro del plugin
            en la tabla plug_plugins validando
            los campos suministrados en el 
            archivo de registro'''
            
        db  = self.db
        reg = registro
        dbp = db.plug_plugins

        row = db(dbp.plug_nombre == reg["plug_nombre"]).select(dbp.id).first()
        
        if not row:
            dbp.insert( plug_nombre      = reg['plug_nombre'],
                        plug_descripcion = reg['plug_descripcion'],
                        plug_autor       = reg['plug_autor'],
                        plug_tip         = reg['plug_tip'],
                        plug_icono       = reg['plug_icono'],
                        plug_enlace      = reg['plug_enlace'],
                        plug_prevPlugins = reg['plug_prevPlugins'],
                        plug_version     = reg['plug_version']
                      )
            row = db(dbp.plug_nombre == reg["plug_nombre"]).select(dbp.id).first()
        self.plugid = row

    def getidPlugin(self):
        return self.plugid         

    def insertSubPlugin(self, registro):
        ''' Creamos el resgistro del subplugin
            en la tabla subp_plugins validando
            los campos suministrados en el 
            archivo de registro'''
            
        db  = self.db
        reg = registro
        dbp = db.subp_plugins

        qu1 = dbp.subp_pref == reg['subp_pref']
        qu2 = dbp.subp_dato == reg['subp_dato']
        qu3 = dbp.plug_plugins_id ==  self.plugid

        row = db(qu1 & qu2 & qu3).select(dbp.id).first()

        if not row:
            dbp.insert( 
                        plug_plugins_id  = self.plugid,  
                        subp_pref        = reg['subp_pref'],
                        subp_nombre      = reg['subp_nombre'],
                        subp_descripcion = reg['subp_descripcion'],
                        subp_dato        = reg['subp_dato']
                      )
        

    def previosPlugins(self):
        pass
        
    def setConfigvar(self, file):
        ''' Genera el diccionario con los valores
            del archivo de configuracion xml en un
            diccionario'''
        datos = ConvertXmlToDict(file)
        self.config_var = datos.config_var

    def getConfigvar(self):
        ''' Retorna con los valores
            del archivo de configuracion xml en un
            diccionario'''
        return self.config_var

class navegacion(object):
    ''' Elementos necesarios para crear los tabs
        los elementos que estos los componen como los
        enlaces y las solicitudes ajax'''

    def __init__(self, db, user_id):
        self.db = db
        self.user = user_id
        self.lisM = self.listMenu() 

    def listMenu(self):
        ''' Retorna lista  de diccionarios con los plugins clasificados
            por tabs que existen'''

        db      = self.db
        user_id = self.user

        cons1 = (db.auth_membership.user_id == user_id)
        cons2 = (db.auth_modules.auth_group_id == db.auth_membership.group_id)
        cons3 = (db.plug_plugins.id  == db.auth_modules.plug_plugins_id)
        cons4 = (db.plug_plugins.plug_tab != None)

        rows  = db(cons1 & cons2 & cons3 & cons4).select(db.plug_plugins.ALL, orderby=db.plug_plugins.plug_tab,  distinct=True)
        list1 = rows.as_list()
        return list1

    def getlistMenu(self):
        """ Retorna lista con enlaces para mostrar el
            menu de navegacion"""
        return self.lisM

    def enlaTabs(self):
        """ Retorna lista con  los tabs que de los  plugins
            a los cuales el usuario pretenece"""
        tabs = self.lisM 
        return list(set([t['plug_tab']for t in tabs]))

