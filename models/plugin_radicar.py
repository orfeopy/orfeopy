#Registramos el modulo en el diccionario siguiente
pluginRadicar = {}
pluginRadicar['plug_nombre']        = "plugin_radicar"#Este nombre debe ser igual al  del archivo
pluginRadicar['plug_autor']         = "aurigadl@gmail.com"
pluginRadicar['plug_icono']         = "radicar" #Debe existir en /miplugin/static/img/xxx.png 40x40px
pluginRadicar['plug_enlace']        = "www.correlibre.org" #Podemos encontrar mas info sobre el modulo 
pluginRadicar['plug_prevPlugins']   = '' #Plugins previos, se escriben separados por comas. 
pluginRadicar['plug_version']       = '0.001' 
pluginRadicar['plug_tip']           = "Radicar" #Mensaje que sale al seleccionarlo en el menu
pluginRadicar['plug_descripcion']   = "Generar nuevos registros de documentos"

#Registramos el plugin
plugin_modulo.insertPlugin(pluginRadicar)

#Registramos el submodulo en el diccionario siguiente
pluginSubRadi = {}
pluginSubRadi['subp_pref']        = 'trad'
pluginSubRadi['subp_nombre']      = 'Entrada'
pluginSubRadi['subp_descripcion'] = 'Generar radicados de entrada'
pluginSubRadi['subp_dato' ]       = 01

#Registramos el submodulo
plugin_modulo.insertSubPlugin(pluginSubRadi)

pluginSubRadi['subp_pref']        = 'trad'
pluginSubRadi['subp_nombre']      = 'Salida'
pluginSubRadi['subp_descripcion'] = 'Generar radicados de salida'
pluginSubRadi['subp_dato']        = 02

#Registramos el submodulo
plugin_modulo.insertSubPlugin(pluginSubRadi)

perm =  auth.relausuaSubplug(pluginRadicar['plug_nombre'], pluginSubRadi['subp_pref'])
