import tornado.web
from tornado.options import (define, options)
from utils import (json_handler, copyListDicts, generate_insert)
import psycopg2
import psycopg2.extras
import json
import logging
import base

gen_log = logging.getLogger("tornado.general")

class ProductHandler(base.BaseHandler):
    SUPPORTED_METHODS = ("GET","POST","DELETE","PUT")
    @tornado.web.asynchronous
    def get(self, p):
        self._get_callback()

    def _get_callback(self):
        field_id = self.get_argument('id', False)
        try:
            if field_id:
                self.cursor.execute("SELECT code, id, name, price, quantity FROM products WHERE id = %s", (field_id, ))
            else:
                self.cursor.execute("SELECT code, id, name, price, quantity FROM products")
            res = copyListDicts( self.cursor.fetchall() )
            for r in res:
                r.update({'ref' : 'http://%s/products?id=%s'%(self.request.host, r.get('id'))})
            res = {'products':res, 'status':{'id' : 'OK', 'message' : ''}}
        except Exception as e:
            res = {'status':{'id' : 'ERROR', 'message' : 'Hubo un error, no se pudo realizar la consulta'}}
            gen_log.error("Error consultando", exc_info=True)
        self._send_response(res)
    
    
    @tornado.web.asynchronous
    def post(self, p):
        self._post_callback()

    def _post_callback(self):
        obligatorios = ["code","name","price","quantity"]
        fields = self.request.arguments.keys()
        f = []
        for field in obligatorios:
            if not field in fields:
                f.append(field)
        res = {'status' : {'id' : 'OK', 'message' : ''}}
        if not f:
            try:
                sql = generate_insert('products', fields)
                values = [self.get_argument(f) for f in fields]
                self.cursor.execute(sql,values)                                        
            except Exception as e:
                res.update({'status':{'id' : 'ERROR', 'message' : 'Hubo un error, no se pudo crear el registro'}})
                gen_log.error("Error agregando el registro", exc_info=True)
        else:
                res.update({'status':{'id' : 'ERROR', 'message' : 'No se pudo crear registro, faltan campos obligatorios %s'%str(f)}})
            
        self._send_response(res)

    
    @tornado.web.asynchronous
    def delete(self, p):
        self._delete_callback()

    def _delete_callback(self):
        fields = self.request.arguments.keys() 
        field_id = self.get_argument('id', False)
        if not fields:
            params = self.request.body.split('&')
            for p in params:
                if 'id' in p:
                    product = p.split('=')
                    field_id = product[1]
                
        res = {'status' : {'id' : 'OK', 'message' : ''}}
        if field_id:
            try:
                self.cursor.execute("DELETE FROM products WHERE id = %s",
                                        (field_id,))
            except Exception as e:
                res.update({'status':{'id' : 'ERROR', 'message' : 'Hubo un error, no se pudo eliminar el registro'}})
                gen_log.error("Error eliminando el registro", exc_info=True)
        else:
            res.update({'status':{'id' : 'ERROR', 'message' : 'Hubo un error, en id es obligatorio'}})
        self._send_response(res)            
    
    @tornado.web.asynchronous
    def put(self, p):
        self._put_callback()

    def _put_callback(self):
        field_id = self.get_argument('id', False)
       
        fields = self.request.arguments.keys() 
        res = {'status' : {'id' : 'OK', 'message' : ''}}
        if len(fields) > 1 and field_id:
            sql = "UPDATE products SET"
            values = []
            for field in fields:
                if field != 'id':
                    sql += " " + field + " = %s, "
                    values.append(self.get_argument(field))
            sql = sql[:-2] + " WHERE id = %s"
            values.append(field_id)
            try:
                self.cursor.execute(sql, values)
            except Exception as e:
                res.update({'status':{'id' : 'ERROR', 'message' : 'Hubo un error, no se pudo actualziar el registro'}})
                gen_log.error("Error actualizando el registro", exc_info=True)
        else:
            if not field_id:
                res.update({'status':{'id' : 'ERROR', 'message' : 'El campo id es obligatorio'}})
            else:
                res.update({'status':{'id' : 'ERROR', 'message' : 'Nada que actualizar'}})
        self._send_response(res)
