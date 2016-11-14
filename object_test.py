import model
from sqlalchemy import orm
from sqlalchemy import create_engine
from twython import Twython
from time import sleep
import twython

# Create an engine and create all the tables we need
engine = create_engine('sqlite:///cmdtweetpy.db', echo=True)
model.metadata.bind = engine
model.metadata.create_all()

# Set up the session
sm = orm.sessionmaker(bind=engine, autoflush=True, autocommit=False,
            expire_on_commit=True)
session = orm.scoped_session(sm)
CONSUMER_KEY = 'n1yP3qQNhzL668BHaNuHw'
CONSUMER_SECRET = 'BVQC7eATM79NxkmRlbZtciDKxlYVb7CoOgdzwizpHE'
client_args = {'headers': {'User-Agent': 'cmdtweetpy'},'proxies': {'http': '127.0.0.1:9150'},'timeout': 300}

archivo = open("listadotwitter.txt","w")
listado = []
consulta = session.query(model.Cuentas).all()
for lista in consulta:
    usuario = lista.usuario
    clave = lista.clave
    ACCESS_KEY = lista.access_key
    ACCESS_SECRET = lista.access_secret
    print "Conectando usuario: %s" %usuario
    try:
        api = Twython(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET,client_args = client_args)
        api.update_status(status="Reactivando la tropa con #NicolasMaduro")
        print "cuenta de usuario %s esta activa" %usuario
        linea = "%s,activado\n" %usuario
    except twython.exceptions.TwythonAuthError:
        linea = "%s,desactivado\n" %usuario
        print "Cuenta de usuario %s ha sido desactivada" %usuario
    listado.append(linea)
    sleep(5)
archivo.writelines(listado)
archivo.close()





