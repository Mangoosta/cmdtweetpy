#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import model

from sqlalchemy import orm

from sqlalchemy import create_engine

from datetime import datetime




class Mensajes:

    def __init__(self,basededatos):
        self.__basededatos = basededatos

    def __SesionDB(self):
        engine = create_engine('sqlite:///%s' %self.__basededatos, echo=False)
        model.metadata.bind = engine
        model.metadata.create_all()
        sm = orm.sessionmaker(bind=engine, autoflush=True, autocommit=False,expire_on_commit=True)
        session = orm.scoped_session(sm)
        return model,session

    def Insertar(self,mensajes):
        model,session = self.__SesionDB()
        for i in range(len(mensajes)):
            mensaje = model.Mensajes()
            mensaje.mensaje = mensajes[i]["mensaje"]
            mensaje.etiqueta = mensajes[i]["etiqueta"]
            mensaje.fechaenv = datetime.now()
            mensaje.tipoMensaje ="N"
            session.add(mensaje)
            session.flush()
            session.commit()

    def Consultar(self):
        mensajes = []
        model,session = self.__SesionDB()
        consulta = session.query(model.Mensajes).all()
        for lista in consulta:
            mensaje = {'mensaje':lista.mensaje,
                'etiqueta':lista.etiqueta,
                'tipoMensaje': lista.tipoMensaje,
                'fechaenv': lista.fechaenv
                }
            mensajes.append(mensaje)
        return mensajes

if __name__ == "__main__":

    from parser_config import config
    from string import find
    archivocfn = config("mensajes.cfg")
    listado = archivocfn.ShowItemSection("mensajes")
    mensajes = []
    for mensaje in listado:
        posinicial = find(mensaje[1],"#")
        posfinal = find(mensaje[1][posinicial:]," ") +1
        etiqueta = mensaje[1][posinicial:posinicial+posfinal]
        texto = mensaje[1]
        linea = {"mensaje":texto,"etiqueta": etiqueta}
        mensajes.append(linea)
    Mensaje = Mensajes("cmdtweetpy.db")
    Mensaje.Insertar(mensajes)

    resultado = Mensaje.Consultar()
    print resultado



