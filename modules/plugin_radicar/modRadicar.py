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

class modRadicar(object):
    ''' Registro de documentos y asignacion de 
        consecutivo temporal y oficial.
        Creacion de listado geografico y 
        de directorio de usuarios'''

    def __init__(self, globals, db, confVar):
        self.globals = globals 
        self.db      = db 
        self.config  = confVar

    def initRadi(self):
        ''' Configuracion de las tablas y parametros
            de los radicados, usuario, ubicación'''

        db      = self.db
        globals = self.globals
        T       = globals.T 

        widgetCascading = local_import('plugin_directorio/widgetCascading')
        #Definicion de tabla para ubicacion geografica

        #Tabla de Continente
        db.define_table('sgd_cont_continente',
            Field('cont_nombre'),format = '%(cont_nombre)s')

        dbc = db.sgd_cont_continente.cont_nombre

        # Restriccion de la tabla continente
        dbc.writable = False
        dbc.required = True
        dbc.notnull  = True
        dbc.requires = IS_NOT_EMPTY()
        dbc.label    = T('Continente')

        #Tabla de pais
        db.define_table('sgd_pais',
            Field('pais_nombre'),
            Field('sgd_cont_continente', 
                    db.sgd_cont_continente), format='%(pais_nombre)s')

        dbpa = db.sgd_pa_pais.nombre
        dbpc = db.sgd_pa_pais.continente

        # Restriccion de la tabla pais 
        dbpa.writable = False
        dbpa.required = True
        dbpa.unique   = True
        dbpa.notnull  = True
        dbpa.label    = label=T('pais'))
        dbpa.requires = IS_NOT_EMPTY()
        dbpc.writable = False
        dbpc.required = True
        dbpc.notnull  = True

        #Tabla de departamento 
        db.define_table('sgd_depa_departamento',
            Field('depa_nombre'),
            Field('sgd_pais', db.sgd_pa_pais), format='%(depa_nombre)s')
            
        dbdn = db.sgd_depa_departamento.depa_nombre
        dbdp = db.sgd_depa_departamento.sgd_pais

        dbdn.writable       = False
        dbdn.required       = True
        dbdn.unique         = True
        dbdn.notnull        = True
        dbdn.requires       = IS_NOT_EMPTY()

        dbdp.writable       = False
        dbdp.required       = True
        dbdp.notnull        = True

        #Tabla de municipio
        db.define_table('sgd_muni_municipio',
            Field('muni_nombre',writable=False, required=True, unique=True, notnull=True, requires=IS_NOT_EMPTY()),
            Field('sgd_depa_departamento',db.sgd_pa_depa_departamento, writable=False, required=True, notnull=True), format='%(muni_nombre)s')

        #Tabla de directorio
        db.define_table('sgd_dire_directorio',
            Field('dire_nombre', 'string', label="Nombre",notnull=True,required=True, requires=[IS_NOT_EMPTY(),IS_UPPER()]),
            Field('dire_identificacion','string', label="No identificación",requires=IS_ALPHANUMERIC()),
            Field('sgd_muni_municipio',db.sgd_pa_muni_municipio, notnull=True, label="Ubicación"),
            Field('dire_direccion','string',label="Dirección", notnull=True, required=True, requires=[IS_NOT_EMPTY()]),
            Field('dire_telefono','integer', label="Telefono", notnull=True, required=True, requires=[IS_NOT_EMPTY(),IS_LENGTH(minsize=6)]),
            Field('dire_email', label="E-mail", requires=IS_EMAIL()),
            Field('dire_Descripcion', 'string',label="Descripción", requires=IS_LENGTH(maxsize=30)),
            Field('dire_tipo', 'boolean',default=0, label="Empresa"), format='%(dire_nombre)s')

        #Tabla para generar radicación
        db.define_table('sgd_radi_radicado',
            Field('radi_radicado','integer', unique=True,writable=False, readable=False),
            Field('auth_user_radicador', db.auth_user, default=auth.user_id,writable=False, readable=False  ,required=True),
            Field('auth_user_actual', db.auth_user, required=True),
            Field('radi_fechaCreado', 'datetime', default=request.now, writable=False, readable=False),
            Field('radi_fechaRadicado', 'datetime', writable=False, readable=False),
            Field('radi_activo','boolean',default=True, writable=False, readable=False),
            Field('radi_tipo','integer', writable=False, readable=False),
            Field('dire_id',db.sgd_di_dire_directorio,label='Remitente'))
