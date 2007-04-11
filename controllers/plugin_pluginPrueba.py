# -*- coding: utf-8 -*- 
validarMod = auth.relacionUsuaplug(pluginPrueba['plug_nombre'])

@auth.requires(validarMod)
def index():
    return dict()
