#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Nombre: logmodel.py
Descripción: Objeto que facilite el acceso a la creación de logs.
Version: 0.1
Licencia: GPLv3
Autor: Ernesto Crespo
Correo: ecrespo@gmail.com
Copyright: Ernesto Crespo <ecrespo@gmail.com>
"""
import logging
import logging.handlers
from sqlalchemy import orm
from sqlalchemy import create_engine
import model
import sys
from datetime import datetime



class Bitacora:

    def __init__(self,archivolog="",basededatos=""):
        self.__archivolog = archivolog
        self.__basededatos = basededatos
        if self.__archivolog <> "":
            self.__logger = logging.getLogger(archivolog)
            self.__logger.setLevel(logging.DEBUG)
            self.__handler = logging.handlers.RotatingFileHandler(filename='%s' %self.__archivolog, mode='a')
            self.__formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',datefmt='%y-%m-%d %H:%M:%S')
            self.__handler.setFormatter(self.__formatter)
            self.__logger.addHandler(self.__handler)
        elif self.__basededatos <> "":
            pass
        else:
            print("Faltan argumentos")
            sys.exit()

    def __InicioSesionDB(self,basededatos):
        engine = create_engine('sqlite:///%s' %self.__basededatos,echo=False)
        model.metadata.bind = engine
        model.metadata.create_all()
        sm = orm.sessionmaker(bind=engine,autoflush=True,autocommit=False,expire_on_commit=True)
        session = orm.scoped_session(sm)
        return model,session


    def InsertarMensajesDB(self,mensajes):
        model,session = self.__InicioSesionDB(self.__basededatos)
        bitacora = model.Bitacora()
        bitacora.usuario = mensajes["usuario"]
        bitacora.tweet = mensajes["tweet"]
        bitacora.mensaje = mensajes["mensaje"]
        bitacora.fechaHoraMensaje = mensajes["fechaHoraMensaje"]
        session.add(bitacora)
        session.flush()
        session.commit()

    def ConsultarMensajesDB(self,fechayhora):
        mensajes = []
        model, session = self.__InicioSesionDB(self.__basededatos)
        consulta = session.query(model.Mensajes).all()
        for lista in consulta:
            mensaje = { "mensaje": lista.mensaje,
                "etiqueta": lista.etiqueta,
                }
            mensajes.append(mensaje)
        return mensajes

    def Logs(self,mensaje,nivel):
        if nivel == "debug":
            self.__logger.debug('%s' %mensaje)
        elif nivel == "info":
            self.__logger.info('%s' %mensaje)
        elif nivel == "warning":
            self.__logger.warning('%s' %mensaje)
        elif nivel == "error":
            self.__logger.error('%s' %mensaje)
        elif nivel == "critical":
            self.__logger.critical('%s' %mensaje)

if __name__ == "__main__":

    bitacora = Bitacora(basededatos="cmdtweetpy.db")
    mensaje = {'usuario': "seraph1",
        'tweet':"Esta es una prueba",
        'mensaje':u'Error de envío',
        'fechaHoraMensaje': datetime.now(),
        }

    bitacora.InsertarMensajesDB(mensaje)
    #bitacora.Logs("Esta es una prueba","info")