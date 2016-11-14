#!/usr/bin/env python
# -*- coding: utf-8 -*-


import csv
import model

from sqlalchemy import orm

from sqlalchemy import create_engine

from datetime import datetime


class Usuarios:

    def __init__(self,basededatos):
        self.__basededatos = basededatos

    def __SesionDB(self):
        engine = create_engine('sqlite:///%s' %self.__basededatos, echo=False)
        model.metadata.bind = engine
        model.metadata.create_all()
        sm = orm.sessionmaker(bind=engine, autoflush=True, autocommit=False,expire_on_commit=True)
        session = orm.scoped_session(sm)
        return model,session

    def Consultar(self):
        usuarios = []
        model,session = self.__SesionDB()
        consulta = session.query(model.Cuentas).all()
        for lista in consulta:
            usuario = {'usuario':lista.usuario,
                'clave':lista.clave,
                'access_key': lista.access_key,
                'access_secret': lista.access_secret,
                'estatus': lista.estatus
                }
            usuarios.append(usuario)
        return usuarios

    def InsertarVarios(self,usuarios):
        model,session = self.__SesionDB()

        for i in range(len(usuarios)):
            usuario = model.Cuentas()
            usuario.usuario = usuarios[i]["usuario"]
            usuario.clave = usuarios[i]["clave"]
            usuario.estatus = usuarios[i]["estatus"]
            usuario.access_key = usuarios[i]["access_key"]
            usuario.access_secret = usuarios[i]["access_secret"]
            session.add(usuario)
            session.flush()
            session.commit()

    def Insertar(self,usuario):
        model,session = self.__SesionDB()
        cuenta = model.Cuentas()
        cuenta.usuario = usuario["usuario"]
        cuenta.clave = usuario["clave"]
        cuenta.estatus = usuario["estatus"]
        cuenta.access_key = usuario["access_key"]
        cuenta.access_secret = usuario["access_secret"]
        session.add(cuenta)
        session.flush()
        session.commit()




if __name__ == "__main__":
    usuarios = Usuarios("cmdtweetpy.db")
    usuario = {'access_key': u'2209373551-puGPazl55RY6NQsyWoNf5YBVII6o8Mt9OrrxxzJ',
    'access_secret': u'qckoZstYMh6gMG8gzNJwkDX7qajX8wy2ffBCn364Ynpmt',
    'clave': u'Merida2013',
    'estatus': False,
    'usuario': u'rafaelrojas888'}

    usuarios.Insertar(usuario)

    lista = usuarios.Consultar()
    for usuario in lista:
        print usuario
