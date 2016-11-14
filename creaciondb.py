#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Nombre: creaciondb.py
Descripción: Crea la base de datos con las tablas que se usarán para la
aplicación cmdtweetpy.
Versión: 0.1
Autor: Ernesto Nadir Crespo Avila
Correo: ernesto@crespo.org.ve
Licencia: GPLv3
Copyright: Ernesto Nadir Crespo Avila <ernesto@crespo.org.ve>
"""
from elixir import metadata, Entity, Field
from elixir import Unicode, UnicodeText
from elixir import *
import string

#Se asocia el metadato con la base de datos sqlite
metadata.bind = "sqlite:///cmdtweetpy.db"
#Se activa el echo de los resultados de los comandos.
metadata.bind.echo = False

class Cuentas(Entity):
    usuario = Field(String(100),unique=True)
    clave = Field(String(20))
    access_key = Field(String(100),unique=True)
    access_secret = Field(String(100),unique=True)
    estatus = Field(Boolean)

    #Devuelve la informacion de los contactos
    def __repr__(self):
        return '<Usuarios- usuario: "%s", clave: "%s", access key: "%s",access secret>' % (self.usuario,self.clave,self.access_key,self.access_secret)



class Mensajes(Entity):
    mensaje = Field(String(144))
    etiqueta = Field(String(20))
    tipoMensaje = Field(String(2))
    fechaenv = Field(DateTime)

    def __repr__(self):
        return '<Mensaje: "%s", etiqueta: "%s", tipo: %s'  %(self.mensajesaje,self.etiquetqueta,self.tipoMenoMensaje)

class Bitacora(Entity):
    usuario = Field(String(100))
    tweet = Field(String(144))
    mensaje = Field(String(200))
    fechaHoraMensaje = Field(DateTime,default = datetime.now)

    def __repr_(self):
        return 'Bitacora:  usuario: %s,tweet: %s, mensaje: %s, fecha: %s' %(self.usuari,self.tweet,self.mensaje,self.fechaHoraMensaje)


if __name__ == "__main__":
    #Se importa create_all, setup_all y session de elixir.
    from elixir import create_all, setup_all, session
    #Se crea las clases segun los modelos.
    setup_all()
    #Se crea las tablas en la base de datos segun los modelos definidos
    create_all()
