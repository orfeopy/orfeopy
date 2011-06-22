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

validarMod = auth.relacionUsuaplug(xmlc['plug_nombre'])

@auth.requires(validarMod)
def index():
    form1 = SQLFORM(db.sgd_radi_radicado)
    if form1.accepts(request.vars, session):
        response.flash = 'form accepted'
    elif form1.errors:
        response.flash = 'form has errors'
    else:
        response.flash = T('Formulario de radicacíon')
    return dict(form1=form1)

@auth.requires(validarMod)
def directorio():
    response.files.append(URL('static','plugin_radicar/css/radicar.css'))
    form2 = SQLFORM(db.sgd_dire_directorio)
    if form2.accepts(request.vars, session):
        response.flash = 'form accepted'
    elif form2.errors:
        response.flash = 'form has errors'
    else:
        response.flash = T('Formulario de radicacac&oacute;n')
    return dict(form2=form2)
