import tornado.web
from tornado.options import (define, options)
from utils import (json_handler, copyListDicts)
import psycopg2
import psycopg2.extras
import json

class ProductHandler(tornado.web.RequestHandler):
    """
    Clase para el manejo de productos, es la unica que tiene implementada 
    todos los metodos rest para las pruebas, el resto de las clases 
    se hacen de manera similar, para evitar exceso de documentacion unicamente
    se implementan _todos_ los metodos aca
    """
    @property
    def cursor(self):
        """
        Se usa un unico cursor instanciado cuando se crea la aplicacion
        """
        return self.application.cur

    def _get_products(self, product_ids = None):
        """
        Este metodo retorna una lista de productos segun el valor de product_ids
        no es necesartio hacerlo siempre de esta manera, pero la idea es ilustrar 
        que se pueden ejecutar metodos externos al get o a cualquier otro
        de los metodos rest
        """
        if product_ids:
            self.cursor.execute("SELECT * FROM products WHERE id IN (%s)", (product_ids, ))
        else:
            self.cursor.execute("SELECT * FROM products")
        res = copyListDicts( self.cursor.fetchall())
        ret = {}
        
        """
        Como lo indica la convencion REST las referencias a otros objetos debe ser enviada
        como una propiedad, aunque en este caso es una referencia al mismo objeto, sin embargo
        es lo recomendado para no verse en la oblicacion de construirlo del lado del cliente.
        La propiedad self.request.host se usa para obtener la url a la que se realizo la peticion
        en caso de que exista un proxy o cualquier intermedio
        """
        for r in res:
            r.update({'ref' : 'http://%s/products/%s'%(self.request.host, r.get('id'))})
        ret.update({'products':res})
        return  ret

    def get(self, product_id):
        if product_id:
            res = self._get_products(product_id)
        else:
            res = self._get_products()
        """
        La funcion dumps de la libreria json serializa un diccionario python 
        """
        self.set_header("Content-Type", "application/json")
        self.write(json.dumps(res))
        self.finish()

    def post(self, p):
        name = self.get_argument('name', '')
        quantity = self.get_argument('quantity', 0)
        code = self.get_argument('code')
        price = self.get_argument('price', 0)
        product_id = self.get_argument('id')
        fields = self.request.arguments.keys() 
        fo
        if product_id:
            self.cursor.execute("""UPDATE products 
                                    SET name = %s, 
                                    quantity = %s, 
                                    code = %s, 
                                    price = %s
                                    WHERE id = %s""",
                                (name, quantity, code, price, product_id))
        
        res = {'status' : {'id' : 'OK', 'message' : ''}}
        self.set_header("Content-Type", "application/json")
        self.write(json.dumps(res))
        self.finish()
        
    def delete(self, p):
            # self.cursor.execute("""INSERT INTO products (name, quantity, code, price) 
                                    # VALUES (%s, %s, %s, %s)""",
                                # (name, quantity, code, price))
        print p
        
    def put(self, p):
        print p
