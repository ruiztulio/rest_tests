import tornado.web
from tornado.options import (define, options)
from utils import (json_handler, copyListDicts)
import psycopg2
import psycopg2.extras
import json

class ProductHandler(tornado.web.RequestHandler):

    @property
    def cursor(self):
        """
        Se usa un unico cursor instanciado cuando se crea la aplicacion
        """
        return self.application.cur

    def _get_products(self, product_ids = None):
        if product_ids:
            self.cursor.execute("SELECT * FROM products WHERE id IN (%s)", (product_ids, ))
        else:
            self.cursor.execute("SELECT * FROM products")
        res = copyListDicts( self.cursor.fetchall())
        ret = {}
        
        for r in res:
            r.update({'ref' : 'http://%s/products/%s'%(self.request.host, r.get('id'))})
        ret.update({'products':res})
        return  ret

    def _send_response(self, res):
        self.set_header("Content-Type", "application/json")
        self.write(json.dumps(res))
        self.finish()

    def get(self, product_id):
        if product_id:
            res = self._get_products(product_id)
        else:
            res = self._get_products()
        self._send_response(res)

    def post(self, p):
        name = self.get_argument('name', '')
        quantity = self.get_argument('quantity', 0)
        code = self.get_argument('code')
        price = self.get_argument('price', 0)
        product_id = self.get_argument('id')
        fields = self.request.arguments.keys() 

        res = {'status' : {'id' : 'OK', 'message' : ''}}
        if product_id:
            try:
                self.cursor.execute("""UPDATE products 
                                        SET name = %s, 
                                        quantity = %s, 
                                        code = %s, 
                                        price = %s
                                        WHERE id = %s""",
                                    (name, quantity, code, price, product_id))
            except Exception as e:
                res = {'status' : {'id' : 'ERROR', 'message' : e}}
        self._send_response(res)

    def delete(self, p):
            # self.cursor.execute("""INSERT INTO products (name, quantity, code, price) 
                                    # VALUES (%s, %s, %s, %s)""",
                                # (name, quantity, code, price))
        print p
        
    def put(self, p):
            # self.cursor.execute("""INSERT INTO products (name, quantity, code, price) 
                                    # VALUES (%s, %s, %s, %s)""",
                                # (name, quantity, code, price))
        print p
