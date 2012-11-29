import requests
import json
import logging

# Se crea un log para mostrar la salida
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger = logging.getLogger('database.backup')
logger.setLevel(logging.INFO)
logger.addHandler(ch)

# Url desde la cual se consumiran los servicios
url = 'http://localhost:8881/products'

# get sin parametros a la url
logger.info("Obteniendo info de %s"%url)
try:
    r = requests.get(url)
    if r.status_code == 200:
        logger.info("Info obtenida satisfactoriamente")
    else:
        logger.error("Error en la transaccion: %s"%r.reason)
except Exception as e:
    logger.error("Error grave en la transaccion: %s"%e)

# get con un id especifico
logger.info("Obteniendo el id 4 %s"%url)
try:
    r = requests.get(url, data={'id':4})
    if r.status_code == 200:
        logger.info("Info obtenida satisfactoriamente")
    else:
        logger.error("Error en la transaccion: %s"%r.reason)
        logger.info("  Contenido %s"%r.content)
except Exception as e:
    logger.error("Error grave en la transaccion: %s"%e)

# prueba de put
logger.info("Agregando nuevo producto ")
try:
    r = requests.put(url, data = {'name':'Perolito barato', 'code':'CODIGOPEROLITO', 'price':123})
    if r.status_code == 200:
        logger.info("Procesado satisfactoriamente")
        logger.info("  Contenido %s"%r.content)
    else:
        logger.error("Error en la transaccion: %s"%r.reason)
except Exception as e:
    logger.error("Error grave en la transaccion: %s"%e)
    
# prueba de put
logger.info("Editanto el producto")
try:
    r = requests.post(url, data = {'name':'Perolito Barato', 'code':'CODPERO123'})
    if r.status_code == 200:
        logger.info("Procesado satisfactoriamente")
        logger.info("  Contenido %s"%r.content)
    else:
        logger.error("Error en la transaccion: %s"%r.reason)
except Exception as e:
    logger.error("Error grave en la transaccion: %s"%e)
