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
# archivo /private/config.xml y permitiran realizar
# cambios desde la administracion.

import os
import copy
from   gluon.storage import *


globals2   = Storage(copy.copy(globals()))

constan    = local_import('setConst', True)
plugin     = local_import('plugins', True)
xmlFile    = 'config.xml'

path       = os.path.join(request.folder,'private',xmlFile)
conf       = constan.setConst(path, globals2, response)
confVar    = conf.getConfigvar() 

db         = conf.connect_to_db()
mail       = conf.init_mail()

auth       = constan.myAuth(path, globals2, db, mail)
db         = auth.initAuth()

plugin_modulo = plugin.plugins(globals2, db)
db            = plugin_modulo.regisPlugins()
