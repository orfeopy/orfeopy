# coding: utf8
from datetime import date
ano_actu = date.today().year


@auth.requires_login()
def my_form_radicado(form):
    rows = db(db.sgd_radi_radicado).select(db.sgd_radi_radicado.id)
    last_row = rows.last()
    form.vars.radi_radicado = str(ano_actu) + str(int(last_row) + 1)


@auth.requires_login()
def radicar():
    '''form = crud.create(db.sgd_radi_radicado, next=URL('index'),
           onvalidation=my_form_radicado,
           message=T("Se creo el nuevo radicado"))'''
    return dict()
