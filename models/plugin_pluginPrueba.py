#Registramos el modulo en el diccionario siguiente
pluginPrueba = {}
pluginPrueba['plug_nombre']        = "plugin_pluginPrueba"#Este nombre debe ser igual al  del archivo
pluginPrueba['plug_autor']         = "aurigadl@gmail.com"
pluginPrueba['plug_icono']         = "logoA" #Debe existir en /miplugin/static/img/xxx.png 40x40px
pluginPrueba['plug_enlace']        = "www.correlibre.org" #Podemos encontrar mas info sobre el modulo 
pluginPrueba['plug_prevPlugins']   = '' #Plugins previos, se escriben separados por comas. 
pluginPrueba['plug_version']       = '0.001' 
pluginPrueba['plug_tip']           = "plugin de prueba" #Mensaje que sale al seleccionarlo en el menu
pluginPrueba['plug_descripcion']   = "permite ver como se  configuran \
                                los modulos y los parametros para que \
                                en la aplicacion se puedan integrar \
                                sin alterar la  estructura"

plugin_modulo.insertPlugin(pluginPrueba)
