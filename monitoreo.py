#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Se define el token de la aplicacion
CONSUMER_KEY = 'n1yP3qQNhzL668BHaNuHw'
CONSUMER_SECRET = 'BVQC7eATM79NxkmRlbZtciDKxlYVb7CoOgdzwizpHE'
#Se define el acceso al usuario
ACCESS_KEY = '35950442-mJBAUbLqKAp5j6SUtXT3Gx11N1bYArAf0JLbHdnOo'
ACCESS_SECRET = '5OYojQjDCmscb6lgQgPImvEIOB9OM1r87SyGeZys'

#Se importa twython y de time a  sleep
from twython import Twython
from time import sleep
from twython import TwythonStreamer
PITIYAN = [
            135953666 , # napoleonbravo
            47491330 , # hcapriles
            77054564 , # leonardo_padron
            144164028 , # Pr1meroJusticia
            76947892 , # cmrondon
            204033649 , # hramosallup
            ]

PITIMEDIOS = [
            76931020 , # Unoticias
            44145131 , # noticierovv
            17485551,  # globovision
            17485118, # Venevision
            14071538, # Noticias24
            124172948, # la patilla
            ]

PATRIO = [
            108196938 , # LaHojillaenTV
            12493262 , # lubrio
            110023872 , # RevoHCF
            335309790 , # IzquierdaActiva
            416740182 , # Vhzg15
            1304948641 , # ForoBolivariano
            1317722024 , # ForoPatriota
            140446030 , # vertale80
            114880615 , # anat5
            140235272 , # temasdebates
            1035994254 , # RedSocialista_
            109071331 , # twizquierda
            149289053 , # frankcandanga69
            146159034 , # opErnesto
            1252764865 , # nicolasmaduro
            1197438062 , # Sibci
            342363193 , # VillegasPoljakE
            118864905 , # vtvcanal8
            108604055 , # nicmerevans
            553873038 , # difundelaverdad
            1450211138, # mandingavtv
            ]

#users = PITIYAN + PITIMEDIOS
users = PATRIO

class MyStreamer(TwythonStreamer):
    def on_success(self, data):
        if 'text' in data:
            #print data
            print data['text'].encode('utf-8')
        # Want to disconnect after the first result?
        # self.disconnect()

    def on_error(self, status_code, data):
        print status_code, data
try:
    # Requires Authentication as of Twitter API v1.1
    stream = MyStreamer(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET)
    #stream.statuses.filter(track='python')
    stream.statuses.filter(track=None, follow=users)
except KeyboardInterrupt:
    print(u"Fin de la aplicación")
