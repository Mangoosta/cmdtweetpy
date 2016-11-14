#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tweetllaves import *
from string import find
from time import sleep
#Se importa twython y de time a  sleep

from twython import Twython
import twython

from parser_config import config
import csv
import random
from string import find
from time import sleep
import logging
import logging.handlers
#import urllib2

#from pudb import set_trace; set_trace()

import model

from sqlalchemy import orm

from sqlalchemy import create_engine



class Tweetmsg:

    def __init__(self,archivolog,configuracioncfg,basededatos):
        self.__client_args = {'headers': {'User-Agent': 'cmdtweetpy'},
            'proxies': {'http': '127.0.0.1:9050'},
            'timeout': 300}
        self.__logger = logging.getLogger('cmdtweetpy')
        self.__logger.setLevel(logging.DEBUG)
        self.__handler = logging.handlers.RotatingFileHandler(filename='%s' %archivolog, mode='a')
        self.__formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',datefmt='%y-%m-%d %H:%M:%S')
        self.__handler.setFormatter(self.__formatter)
        self.__logger.addHandler(self.__handler)

        self.__configuracion = config(configuracioncfg)
        self.__tiempo = float(self.__configuracion.ShowValueItem("tiempo","retardo"))
        self.__basededatos = basededatos


    def __Sesion(self):
        #Crear un engine y crear todas las tablas necesarias
        engine = create_engine('sqlite:///%s' %self.__basededatos, echo=False)
        model.metadata.bind = engine
        model.metadata.create_all()
        sm = orm.sessionmaker(bind=engine, autoflush=True, autocommit=False,expire_on_commit=True)
        session = orm.scoped_session(sm)
        return model,session




    def ConsultaCuentasDB(self):
        self.__usuarios = []
        model, session = self.__Sesion()
        consulta = session.query(model.Cuentas).all()
        for lista in consulta:
            usuario = { 'usuario': lista.usuario,
                'clave': lista.clave,
                'estatus': lista.estatus,
                'tokenkey':lista.access_key,
                'tokensecret':lista.access_secret
                }
            self.__usuarios.append(usuario)

    def __Logs(self,mensaje,nivel):
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

    def __LogsDB(self,mensaje,nivel):
        pass


    def __UsuariosCSV(self,archivocsv):
        self.__usuarios = []
        with open(archivocsv, 'r') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in spamreader:
                usuario = {"usuario": row[0],
                    "clave":row[1],
                    "tokenkey":"%s" %row[2],
                    "tokensecret":"%s" %row[3]}
                self.__usuarios.append(usuario)



    def __CapturarMensajes(self,mensajescnf):
        self.__archivomsg = config(mensajescnf)
        listado = self.__archivomsg.ShowItemSection("mensajes")
        self.__mensajes = []
        for mensaje  in listado:
            self.__mensajes.append(mensaje[1])
        self.__total_mensajes = len(self.__mensajes)



    def EnviarTweet(self,usuario,mensaje,tipolog):
        cuenta = usuario["usuario"]
        clave = usuario["clave"]
        ACCESS_KEY = usuario["tokenkey"]
        ACCESS_SECRET = usuario["tokensecret"]
        if len(mensaje) == 14:
            msgtrunk = mensaje
        elif len(mensaje) > 14:
            msgtrunk = mensaje[:11] + "..."
        else:
            msgtrunk = mensaje

        try:
            api = Twython(CONSUMER_KEY,
                CONSUMER_SECRET,
                ACCESS_KEY,
                ACCESS_SECRET,
                client_args = self.__client_args)

            api.update_status(status=mensaje)
            estado = "Mensaje %s  de %s, enviado" %(msgtrunk,cuenta)
            nivelerror = "info"
        except twython.exceptions.TwythonAuthError:
            estado =  "Error de autenticacion||| mensaje: %s |||cuenta: %s" %(msgtrunk,cuenta)
            nivelerror = "error"
        except twython.exceptions.TwythonError:
            estado = "Cuenta Suspendida ||| cuenta: %s" %cuenta
            nivelerror = "error"
        self.__Logs(estado,nivelerror)


    def EnvioMasivo(self,usuarioscsv,lstmensajes):
        tipolog = "log"
        self.__UsuariosCSV(usuarioscsv)
        self.__CapturarMensajes(lstmensajes)
        for msg in self.__mensajes:
            for cuenta in self.__usuarios:
                if cuenta["tokenkey"] == "":
                    continue
                self.EnviarTweet(cuenta,msg,tipolog)
            sleep(float(5.0))


    def EnvioMasivoDB(self,lstmensajes):
        tipolog = "db"
        self.__ConsultaCuentasDB()
        self.__CapturarMensajes(lstmensajes))
        for msg in self.__mensajes:
            for cuenta in self.__usuarios:
                if (cuenta["tokenkey"] == "") or (cuenta["tokensecret"] == ""):
                    continue
                elif cuenta["estatus"] == False:
                    continue
                self.EnviarTweet(cuenta,msg,tipodatos)
                sleep(float(5.0))





if __name__ == '__main__':
    mensajes = Tweetmsg("cmdtweetpy.log","cmdtweetpy.cfg","cmdtweetpy.db")
    #mensajes.EnvioMasivo("usuarios.csv","mensajes.cfg")

    #mensajes.ConsultaCuentasDB()

    #usuario = {'tokensecret': '2qrii2QJ9MiEdkeHNkTCCOI66oMqb4EXWNgcx1kpfu8X7',
    #'tokenkey': '2182681938-THu7onCsGsprYCpjtkv4PqCB0oZyLDavyIDQdyJ',
    #'clave': '19191818Dp',
    #'usuario': 'p.daniela45@yahoo.com'}
    #mensaje = "1,2,3 probando #TROPA"

    #mensajes.EnviarTweet(usuario,mensaje)
