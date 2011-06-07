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

from datetime           import date
from gluon.tools        import Auth    
from gluon.sql          import *
from gluon.validators   import *

class modRadicar(object):
    ''' Registro de documentos y asignacion de 
        consecutivo temporal y oficial.
        Creacion de listado geografico y 
        de directorio de usuarios'''

    def __init__(self, globals, db, confVar):
        self.globals = globals 
        self.db      = db 
        self.config  = confVar
        self.initRadi()

    def initRadi(self):
        ''' Configuracion de las tablas y parametros
            de los radicados, usuario, ubicación'''

        db      = self.db
        globals = self.globals
        T       = globals.T 

        widgetCascading = globals.local_import('plugin_radicar/widgetCascading')
        #Definicion de tabla para ubicacion geografica

        #Tabla de Continente
        db.define_table('sgd_cont_continente',
            Field('cont_nombre'), format = '%(cont_nombre)s')

        db_c = db.sgd_cont_continente.cont_nombre

        # Restriccion de la tabla continente
        db_c.writable = False
        db_c.required = True
        db_c.notnull  = True
        db_c.requires = IS_NOT_EMPTY()
        db_c.label    = T('Continente')

        #Tabla de pais
        db.define_table('sgd_pais',
            Field('pais_nombre'),
            Field('sgd_cont_continente', 
                    db.sgd_cont_continente), format='%(pais_nombre)s')

        dbp_a = db.sgd_pais.pais_nombre
        dbp_c = db.sgd_pais.sgd_cont_continente

        # Restriccion de la tabla pais 
        dbp_a.writable = False
        dbp_a.required = True
        dbp_a.unique   = True
        dbp_a.notnull  = True
        dbp_a.label    = T('pais')
        dbp_a.requires = IS_NOT_EMPTY()
        dbp_c.writable = False
        dbp_c.required = True
        dbp_c.notnull  = True

        #Tabla de departamento 
        db.define_table('sgd_depa_departamento',
            Field('depa_nombre'),
            Field('sgd_pais', db.sgd_pais)
                    , format='%(depa_nombre)s')
            
        dbd_n = db.sgd_depa_departamento.depa_nombre
        dbd_p = db.sgd_depa_departamento.sgd_pais

        # Restriccion de la departamento 
        dbd_n.writable       = False
        dbd_n.required       = True
        dbd_n.unique         = True
        dbd_n.notnull        = True
        dbd_n.requires       = IS_NOT_EMPTY()

        dbd_p.writable       = False
        dbd_p.required       = True
        dbd_p.notnull        = True

        #Tabla de municipio
        db.define_table('sgd_muni_municipio',
            Field('muni_nombre'),
            Field('sgd_depa_departamento',db.sgd_depa_departamento)
                  , format='%(muni_nombre)s')


        dbm_n = db.sgd_muni_municipio.muni_nombre        
        dbm_d = db.sgd_muni_municipio.sgd_depa_departamento

        #Restriccion de municipio 
        dbm_n.writable = False
        dbm_n.required = True
        dbm_n.unique   = True
        dbm_n.notnull  = True
        dbm_n.requires = IS_NOT_EMPTY()

        dbm_d.writable = False
        dbm_d.required = True
        dbm_d.notnull  = True

        #Tabla de directorio
        db.define_table('sgd_dire_directorio',
            Field('dire_nombre'),
            Field('dire_identificacion'),
            Field('sgd_muni_municipio',db.sgd_muni_municipio),
            Field('dire_direccion'),
            Field('dire_telefono', 'integer'),
            Field('dire_email'),
            Field('dire_descripcion'),
            Field('dire_tipo', 'boolean'), format='%(dire_nombre)s')
 
        #Restriccion de directorio
        dbdir_n = db.sgd_dire_directorio.dire_nombre
        dbdir_i = db.sgd_dire_directorio.dire_identificacion
        dbdir_m = db.sgd_dire_directorio.sgd_muni_municipio
        dbdir_d = db.sgd_dire_directorio.dire_direccion
        dbdir_t = db.sgd_dire_directorio.dire_telefono
        dbdir_e = db.sgd_dire_directorio.dire_email
        dbdir_d = db.sgd_dire_directorio.dire_descripcion
        dbdir_t = db.sgd_dire_directorio.dire_tipo
        
        dbdir_n.label    = T('Nombre')
        dbdir_n.notnull  = True
        dbdir_n.required = True
        dbdir_n.requires = [IS_NOT_EMPTY(),IS_UPPER()]
        
        dbdir_i.label    = T("No identificación")
        dbdir_i.requires = IS_ALPHANUMERIC()
        
        dbdir_m.notnull  = True
        dbdir_m.label    = T('Ubicación')

        dbdir_d.label    = T('Dirección')
        dbdir_d.notnull  = True
        dbdir_d.required = True
        dbdir_d.requires = [IS_NOT_EMPTY()]

        dbdir_t.label    = T('Telefono')
        dbdir_t.notnull  = True
        dbdir_t.required = True
        dbdir_t.requires = [IS_NOT_EMPTY(), IS_LENGTH(minsize = 6)]

        dbdir_e.label    = T('E-mail')
        dbdir_e.requires = IS_EMAIL()

        dbdir_d.label    = T('Descripción')
        dbdir_d.requires = IS_LENGTH(maxsize = 30)

        dbdir_t.default  = 0
        dbdir_t.label    = T('Empresa')

        #Tabla para generar radicación
        db.define_table('sgd_radi_radicado',
            Field('radi_radicado','integer'),
            Field('auth_user_radicador', db.auth_user),
            Field('auth_user_actual', db.auth_user),
            Field('radi_fechaCreado', 'datetime'),
            Field('radi_fechaRadicado', 'datetime'),
            Field('radi_activo','boolean'),
            Field('radi_tipo','integer'),
            Field('sgd_dire_directorio',db.sgd_dire_directorio))

        #Restriccion de radicado 
        dbr_rd = db.sgd_radi_radicado.radi_radicado
        dbr_us = db.sgd_radi_radicado.auth_user_radicador
        dbr_ua = db.sgd_radi_radicado.auth_user_actual
        dbr_fc = db.sgd_radi_radicado.radi_fechaCreado
        dbr_fr = db.sgd_radi_radicado.radi_fechaRadicado
        dbr_ra = db.sgd_radi_radicado.radi_activo
        dbr_rt = db.sgd_radi_radicado.radi_tipo
        dbr_di = db.sgd_radi_radicado.sgd_dire_directorio  

        dbr_rd.unique   = True
        dbr_rd.ritable  = False
        dbr_rd.readable = False

        dbr_us.writable = False
        dbr_us.eadable  = False
        dbr_us.equired  = True

        dbr_ua.required = True

        dbr_fc.ritable  = False
        dbr_fc.eadable  = False

        dbr_fr.writable = False
        dbr_fr.eadable  = False

        dbr_ra.default = True
        dbr_ra.ritable = False
        dbr_ra.eadable = False

        dbr_rt.writable = False
        dbr_rt.eadable  = False

        dbr_di.label    = T('Remitente')

        #Tabla para historico radicado
        db.define_table('sgd_radh_radihist',
            Field('sgd_radi_radicado',db.sgd_radi_radicado),
            Field('radh_fecha', 'datetime'))

    #Generar numero de radicado
    def numRadi(object):
        ano_actu = date.today().year
        rows     = db(db.sgd_radi_radicado).select(db.sgd_radi_radicado.id)
        last_row = rows.last()
        form.vars.radi_radicado = str(ano_actu) + str(int(last_row) + 1)

    #Restriccion de historico radicado 
    def radiFormat(object):
        pass
