#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
from tweetllaves import *
import tweepy
import mechanize
import cookielib
from BeautifulSoup import BeautifulSoup
import sys
import model

from sqlalchemy import orm

from sqlalchemy import create_engine

def SesionDB(basededatos):
    #Crear un engine y crear todas las tablas necesarias
    engine = create_engine('sqlite:///%s' %basededatos, echo=False)
    model.metadata.bind = engine
    model.metadata.create_all()

    sm = orm.sessionmaker(bind=engine, autoflush=True, autocommit=False,expire_on_commit=True)
    session = orm.scoped_session(sm)
    return model,session

def InsertarDB(usuarios):
    model,session = SesionDB("cmdtweetpy.db")

    for usuario in usuarios:
        cuenta = model.Cuentas()
        cuenta.usuario = usuario["usuario"]
        cuenta.access_key = usuario["tokenkey"]
        cuenta.access_secret = usuario["tokensecret"]
        cuenta.estatus = True
        cuenta.clave = usuario["clave"]
        session.add(cuenta)
        session.flush()
        session.commit()




#Creacion del token de forma manual
def PrimerAcceso():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth_url = auth.get_authorization_url()
    print 'Please authorize: ' + auth_url
    verifier = raw_input('PIN: ').strip()
    auth.get_access_token(verifier)
    print "ACCESS_KEY = '%s'" % auth.access_token.key
    print "ACCESS_SECRET = '%s'" % auth.access_token.secret

#Creacion del token de forma automatica
def Autenticacion(usuario):
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth_url = auth.get_authorization_url()
    br = mechanize.Browser()
    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)
    br.set_handle_robots(False)
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
    br.addheaders = [('User-agent','Mozilla/5.0 (X11; U; Linux i686; es-VE; rv:1.9.0.1)Gecko/2008071615 Debian/6.0 Firefox/9')]
    r = br.open(auth_url)
    br.select_form(nr=0)
    br.form['session[username_or_email]'] = usuario[0]
    br.form['session[password]'] = usuario[1]
    br.submit()
    html = br.response().read()
    soup = BeautifulSoup(html)
    for row in soup("code"):
        codigo = str(row.string)
    try:
        auth.get_access_token(codigo)
        return (auth.access_token.key,auth.access_token.secret)
    except NameError:
        return None
    except tweepy.error.TweepError:
        return None

def ExtraerCSV(archivocsv):
    cuentas = []
    with open(archivocsv,'r') as csvfile:
        spamreader = csv.reader(csvfile,delimiter=',', quotechar='"')
        for row in spamreader:
            tokens = Autenticacion((row[0],row[1]))
            if tokens <> None:
                usuario = {"usuario": row[0],"clave":row[1],"tokenkey":tokens[0],"tokensecret":tokens[1]}
            else:
                usuario = {"usuario": row[0],"clave":row[1],"tokenkey":"","tokensecret":""}
            cuentas.append(usuario)
        return cuentas

def ExtraerDatos(archivocsv):
    cuentas = []
    with open(archivocsv,'r') as csvfile:
        spamreader = csv.reader(csvfile,delimiter=',', quotechar='"')
        for row in spamreader:
            usuario = {"usuario": row[0],"clave":row[1],"tokenkey":row[2],"tokensecret":row[3]}
            cuentas.append(usuario)
        return cuentas

def AgregarCuentasCSV(archivocsvfinal,cuentas):
    with open(archivocsvfinal,'wb') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
        total = len(cuentas)
        for i in range(len(cuentas)):
            try:
                spamwriter.writerow([cuentas[i]["usuario"],cuentas[i]["clave"],cuentas[i]["tokenkey"],cuentas[i]["tokensecret"]])
            except KeyboardInterrupt:
                sys.exit()

def AutenticacionCuentasCSV(archivocsv,archivocsvfinal):

    cuentas =ExtraerCSV(archivocsv)
    AgregarCuentasCSV(archivocsvfinal,cuentas)



def AutenticacionCuentasDB(archivocsv):
    cuentas = ExtraerDatos(archivocsv)
    InsertarDB(cuentas)


if __name__ == '__main__':
    #CuentasCSV()
    #PrimerAcceso()
    #Cuentas()
    AutenticacionCuentasCSV("twiter2.csv","usuarios2.csv")
    AutenticacionCuentasDB("usuarios2.csv")


