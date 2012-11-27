import tornado.web
from tornado.options import (define, options)
from utils import (json_handler, copyListDicts)
import psycopg2
import psycopg2.extras
import json
import logging
import base
gen_log = logging.getLogger("tornado.general")

class ProductHandler(base.BaseHandler):
    def _get_products(self, product_ids = None):
        if product_ids:
            self.cursor.execute("SELECT * FROM products WHERE id IN (%s)", (product_ids, ))
        else:
            self.cursor.execute("SELECT * FROM products")
        res = copyListDicts( self.cursor.fetchall())
        ret = {}
        for r in res:
            r.update({'ref' : 'http://%s/products?id=%s'%(self.request.host, r.get('id'))})
        ret.update({'products':res})
        return  ret

    def get(self, p):
        product_id = self.get_argument('id', False)
        try:
            if product_id:
                res = self._get_products(product_id)
            else:
                res = self._get_products()
            res.update({'status':{'id' : 'OK', 'message' : ''}})
            self._send_response(res)
        except e:
            res.update({'status':{'id' : 'ERROR', 'message' : 'Hubo un error, no se pudo realizar la consulta'}})
            gen_log.error("Error consultando", exc_info=True)
            
    def post(self, p):
        name = self.get_argument('name', '')
        quantity = self.get_argument('quantity', 0)
        code = self.get_argument('code')
        price = self.get_argument('price', 0)
        product_id = self.get_argument('id', False)
        fields = self.request.arguments.keys() 
        res = {'status' : {'id' : 'OK', 'message' : ''}}
        if len(fields) > 1 and product_id:
            sql = "UPDATE products SET"
            values = []
            for field in fields:
                if field != 'id':
                    sql += " " + field + " = %s, "
                    values.append(self.get_argument(field))
            sql = sql[:-2] + " WHERE id = %s"
            values.append(product_id)
            try:
                self.cursor.execute(sql, values)
            except Exception as e:
                res.update({'status':{'id' : 'ERROR', 'message' : 'Hubo un error, no se pudo actualziar el registro'}})
                gen_log.error("Error actualizando el registro", exc_info=True)
        else:
            if not product_id:
                res.update({'status':{'id' : 'ERROR', 'message' : 'El campo id es obligatorio'}})
            else:
                res.update({'status':{'id' : 'ERROR', 'message' : 'Nada que actualizar'}})
        self._send_response(res)
        
    def delete(self, p):
        fields = self.request.arguments.keys() 
        product_id = self.get_argument('id', False)
        if not fields:
            params = self.request.body.split('&')
            for p in params:
                if 'id' in p:
                    product = p.split('=')
                    product_id = product[1]
                
        res = {'status' : {'id' : 'OK', 'message' : ''}}
        if product_id:
            try:
                self.cursor.execute("""DELETE FROM products 
                                      WHERE id = %s""",
                                        (product_id,))
            except Exception as e:
                res.update({'status':{'id' : 'ERROR', 'message' : 'Hubo un error, no se pudo eliminar el registro'}})
                gen_log.error("Error eliminando el registro", exc_info=True)
        else:
            res.update({'status':{'id' : 'ERROR', 'message' : 'Hubo un error, en id es obligatorio'}})
        self._send_response(res)        
        
    def put(self, p):
        obligatorios = ['name', 'code']
        name = self.get_argument('name', '')
        quantity = self.get_argument('quantity', 0)
        code = self.get_argument('code')
        price = self.get_argument('price', 0)
        fields = self.request.arguments.keys()
        f = []
        for field in obligatorios:
            if not field in fields:
                f.append(field)
        res = {'status' : {'id' : 'OK', 'message' : ''}}
        if not f:
            try:
                self.cursor.execute("""INSERT INTO products (name, quantity, code, price) 
                                      VALUES (%s, %s, %s, %s)""",
                                        (name, quantity, code, price))
            except Exception as e:
                res.update({'status':{'id' : 'ERROR', 'message' : 'Hubo un error, no se pudo crear el registro'}})
                gen_log.error("Error agregando el registro", exc_info=True)
        else:
                res.update({'status':{'id' : 'ERROR', 'message' : 'No se pudo crear registro, faltan campos obligatorios %s'%str(f)}})
            
        self._send_response(res)
