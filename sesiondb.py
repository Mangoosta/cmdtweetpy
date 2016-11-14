#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime

#Se importa schema y tupes de sqlalchemy

from sqlalchemy import schema, types



#Se instancia la clase MetaData.

metadata = schema.MetaData()



#Se crea la función now que devuelve la hora actual.

def now():

    return datetime.datetime.now()

cuentas_tabla = schema.Table('cuentas',metadata,
    schema.Column('id',types.Integer,primary_key=True),
    schema.Column('usuario',types.String(100),nullable=False),
    schema.Column('clave',types.String(20),nullable=False),
    schema.Column('access_key',types.String(100),nullable=False),
    schema.Column('access_secret',types.String(100),nullable=False),
    schema.Column('estatus',types.Boolean)
)

mensajes_tabla = schema.Table('mensajes',metadata,
    schema.Column('id',types.Integer,primary_key=True),
    schema.Column('mensaje',types.String(144),nullable=False),
    schema.Column('etiqueta',types.String(20),nullable=False),
    schema.Column('tipoMensaje',types.String(2),nullable=False),
    schema.Column('fechaenv',types.DateTime,nullable=False)
)

bitacora_tabla = schema.Table('bitacora',metadata,
    schema.Column('id',types.Integer,primary_key=True),
    schema.Column('usuario_id',types.Integer,nullable=False),
    schema.Column('tweet_id',types.Integer,nullable=False),
    schema.Column('mensaje',types.String(200),nullable=False),
    schema.Column('fechaHoraMensaje',types.DateTime,nullable=False),
)

class Cuentas(object): pass
class Mensajes(object): pass
class Bitacora(object): pass

orm.mapper(Cuentas,cuentas_tabla)
orm.mapper(Mensajes,mensajes_tabla)
orm.mapper(Bitacora,bitacora_tabla)


