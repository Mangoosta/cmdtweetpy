#!/usr/bin/env python
# -*- coding: utf-8 -*-


from usuarios import Usuarios
from bitacora import Bitacora
from mensajes import Mensajes

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


class tweets:

    def __init__(self,configuracioncfg):
        self.__archivocfg = configuracioncfg
        self.__configuracion = config(self.__archivocfg)
        self.__tiempo = float(self.__configuracion.ShowValueItem("tiempo","retardo"))
        self.__timeout = float(self.__configuracion.ShowValueItem("tiempo","timeout"))
        self.__basededatos = self.__configuracion.ShowValueItem("basededatos","archivo")
        self.__ip = self.__configuracion.ShowValueItem("proxy","ip")
        self.__puerto = self.__configuracion.ShowValueItem("proxy","puerto")
        self.__app = self.__configuracion.ShowValueItem("aplicacion","nombre")
        self.__client_args = {'headers': {'User-Agent': '%s' %self.__app},
            'proxies': {'http': '%s:%s' %(self.__ip,self.__puerto)},
            'timeout': self.__timeout}
        self.__bitacora = Bitacora(basededatos=self.__basededatos)
        self.__usuarios = Usuarios(basededatos=self.__basededatos)
        self.__mensajes = Mensajes(basededatos=self.__basededatos)

    def __Cuentas(self):
        self.__cuentas = self.__usuarios.Consultar()
        self.__totalCuentas = len(self.__cuentas)

    def __Mensajes(self):
        self.__textos = self.__mensajes.Consultar()
        self.__totalTextos = len(self.__textos)


    def EnviarTweet(self,usuario,mensaje):
        cuenta = usuario["usuario"]
        clave = usuario["clave"]
        ACCESS_KEY = usuario["access_key"]
        ACCESS_SECRET = usuario["access_secret"]
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

            api.update_status(status=msgtrunk)
            estado = {'usuario': "%s" %cuenta,
                'tweet':"%s"  %msgtrunk,
                'mensaje':u'Mensaje enviado',
                'fechaHoraMensaje': datetime.now(),
                }
        except twython.exceptions.TwythonAuthError:
            estado = {'usuario': "%s" %cuenta,
                'tweet':"%s"  %msgtrunk,
                'mensaje':u'Error de autenticación',
                'fechaHoraMensaje': datetime.now(),
                }
        except twython.exceptions.TwythonError:
            estado = {'usuario': "%s" %cuenta,
                'tweet':"%s"  %msgtrunk,
                'mensaje':u'Cuenta suspendida',
                'fechaHoraMensaje': datetime.now(),
                }
        bitacora.InsertarMensajesDB(estado)



    def EnviarTweets(self):
        self.__Cuentas()
        self.__Mensajes()
        for msg in self.__textos:
            for cuenta in self.__cuentas:
                if (cuenta["access_key"] == "") or (cuenta["access_secret"] == ""):
                    continue
                elif cuenta["estatus"] == False:
                    continue
                self.EnviarTweet(cuenta,msg)
                sleep(float(5.0))


if __name__ == "__main__":
    pass
