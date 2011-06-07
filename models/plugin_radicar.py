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


################################
#### configuracion   ###########
################################

# Las constantes las tenemos almacenadas en el 
# archivo /private/plugin_radicar/config.xml y permitiran realizar
# cambios desde la administracion.

# Cargamos los datos del archivo de configuracion
# del modulo la carpeta debe tener __ini__.py
file1    = 'plugin_radicar/modRadicar'
file2    = 'private/plugin_radicar'

impclass = local_import(file1, True)
clasRad  = impclass.modRadicar(globals2, db, confVar)

xmlFile  = 'config.xml'
path     = os.path.join(request.folder,file2,xmlFile)

conf.setConfile(path)
confplug = conf.getConfigvar()
xmlc     = confplug['config_var']
xmlp     = xmlc['plug_subplugin']

#Registramos el plugin
plugin_modulo.insertPlugin(xmlc)

#Registramos submodulos
if len(xmlp) >  0:
    for xm in xmlp:
        #Registramos el modulo
        plugin_modulo.insertSubPlugin(xm)

    perm =  auth.relausuaSubplug(xmlc['plug_nombre'], xm['subp_pref'])
