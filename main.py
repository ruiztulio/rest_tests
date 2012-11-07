import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import os.path
import sys
from tornado.options import (define, options)
sys.path.append('./utils')
from utils import (json_handler, copyListDicts)
import psycopg2
import psycopg2.extras
import json

define("title", default="Pagina de prueba", help="Page title", type=str)
define("company_name", default="La compania", help="Company name", type=str)
define("port", default=8888, help="run on the given port", type=int)

"""
La configuraion se puede definir de esta manera de modo que este disponible desde
todo el contexto de tornado o simplemente leerla de archivos de configuracion
en caso de que sea compartida por varias aplicaciones
"""
define("pg_user", default="testrest", help="User for database", type=str)
define("pg_pass", default="123", help="User password for database", type=str)
define("pg_host", default="localhost", help="Database server", type=str)
define("pg_dbname", default="rest_sales", help="Database server", type=str)
define("pg_port", default=5432, help="Database server", type=int)

common={
    'title':options.title,
    'company_name':options.company_name,
}

class Application(tornado.web.Application):
    def __init__(self):
        """
        Los manejadores de urls, se pueden usar colocando urls fijas
        en caso de que no se necesiten pasar parametros. En dicho caso quedan:
            (r"/products", ProductHandler),
            
        Para obtener las ventas se hace de manera diferente solo como demostracion,
        ninguna de las dos maneras mostradas a continicacion es especialmente buena
        mas alla de la aplicacion que se les quiera dar, por ejemplo:
            (r"/products/(\d*)", ProductHandler),
        Se usa en caso de que se desee que la url sea del tipo:
            http://servidor/products/123
        En otro caso se puede usar:
            (r"/sales([^/]*)", SaleHandler),
        Si se desea ser mas generico en su uso, permitiendo hacer llamados del tipo:
            http://servidor/sales?fecha_inicio=2012/1/23&fecha_fin=2012/04/12
        El tercer caso se define la url como:
            (r"/product/([^/]+)", ProductHandler2),
        Para tener mas flexibilidad y poder ejecutar urls del tipo
            http://servidor/product/metodo?param1=valor&paramn=valorn
        
        El ProductHandler2 se creo con la intencion de demostrar el uso de
        este tipo de url y no tiene ninguna funcionalidad 
        """
        handlers = [
            (r"/", MainHandler),
            (r"/products/(\d*)", ProductHandler),
            (r"/addproduct", AddProductHandler),
            (r"/sales([^/]*)", SaleHandler),
            (r"/clients/(\d*)", ClientHandler),
            (r"/detail/(\d*)", DetailHandler),
            (r"/product/([^/]+)", ProductHandler2),
        ]
        settings = dict(
            cookie_secret="43oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
            login_url="/auth/login",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=False,
            autoescape="xhtml_escape",
        )
        tornado.web.Application.__init__(self, handlers, **settings)
        self.conn = psycopg2.connect("host=%s dbname=%s password=%s user=%s port=%s"%
                            (options.pg_host, options.pg_dbname, options.pg_pass, options.pg_user, options.pg_port))
        self.conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

class AddProductHandler(tornado.web.RequestHandler):
    @property
    def cursor(self):
        """
        Se usa un unico cursor instanciado cuando se crea la aplicacion
        """
        return self.application.cur

    def get(self):
        self.render("formprod.html", common = common)

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
        name = self.get_argument('name')
        quantity = self.get_argument('quantity')
        code = self.get_argument('code')
        price = self.get_argument('price')
        product_id =self.get_argument('product_id', '')
        if product_id:
            self.cursor.execute("""UPDATE products 
                                    SET name = %s, 
                                    quantity = %s, 
                                    code = %, 
                                    price = %
                                    WHERE id = %s""",
                                (name, quantity, code, price, product_id))
        else:
            self.cursor.execute("""INSERT INTO products (name, quantity, code, price) 
                                    VALUES (%s, %s, %s, %s)""",
                                (name, quantity, code, price))

class ProductHandler2(tornado.web.RequestHandler):
    def get(self, action):
        """
        Definimos un diccionario de arreglos en el que tenemos el nombre del
        metodo como indice y un arreglo con los parametros obligatorios,
        de modo tal que podamos verificar si se pasaron todos los parametros segun el metodo 
        """
        actions = {'delete' : ['id'],
                    'query' : ['start', 'end'],}
        """
        Se verifica si el metodo que se solicita existe en el diccionario,
        en caso negativo 404, pero si se consigue validamos que los parametros
        sean los correctos segun la solicitud
        """
        if self.request.arguments.has_key(action):
            for arg in self.request.arguments:
                if not arg in actions.get(action):
                    raise tornado.web.HTTPError(405)
        else:
            raise tornado.web.HTTPError(404)
        print self.request.arguments

class SaleHandler(tornado.web.RequestHandler):
    """
    Esta clase se encarga de manejar las ventas y a diferencia de las demas
    esta modificada con el decorador @tornado.web.asynchronous con la intecion
    de hacer que el llamado al metodo get sea asincrono, ya que esto es
    lo recomendado en caso de que algun metodo del handler consuma mucho tiempo
    """
    @property
    def cursor(self):
        return self.application.cur

    def _get_sales(self):
        sql = """SELECT sales.*, clients.name client_name 
                FROM sales JOIN clients 
                ON sales.client_id = clients.id"""
        if self.fecha_inicio or self.fecha_fin:
            sql += " WHERE "
            if self.fecha_inicio:
                sql = self.cursor.mogrify(sql + " sale_date >= %s ", (self.fecha_inicio, ))
            if self.fecha_inicio and self.fecha_fin:
                sql += " AND " 
            if self.fecha_fin:
                sql = self.cursor.mogrify(sql + " sale_date <= %s ", (self.fecha_fin, ))
        self.cursor.execute(sql)
        res = copyListDicts( self.cursor.fetchall())
        ret = {}
        for r in res:
            r.update({'client_id_ref' : 'http://%s/clients/%s'%(self.request.host, r.get('client_id'))})
            r.update({'detail_ref' : 'http://%s/detail/%s'%(self.request.host, r.get('id'))})
        """
        siempre es conveniente retornar la respuesta como un elemento del diccionario,
        esto es en caso de que se auiera agregar informacion adicional como un paginador
        informacion de sesion, paginadores, etc
        """
        ret.update({'sales':res})
        return  ret

    def _sales_callback(self):
        """
        Este metodo se ejecuta en background y cuando termina de procesar notifica
        al handler y este envia la respuesta al cliente
        """
        res = self._get_sales()
        """
        Se indica que la respuesta sera de tipo json
        """
        self.set_header("Content-Type", "application/json")
        """
        El json_handler es para los elementos no serializables de python como date, 
        datetime o Decimal, que son los unicos que se manejan en este caso, 
        sin embargo se pueden agregar a conveniencia
        """
        self.write(json.dumps(res, default=json_handler))
        """
        La llamada de finish es importante para evitar que la solicitud quede 
        abierta del lado de navegador web
        """
        self.finish()

    @tornado.web.asynchronous
    def get(self, *args, **kwargs):
        """
        Este metodo se ejecuta de manera asincrona, es importante notar que no posee return
        ni la llamada al metodo finish para finalizar la llamada, esto es para que se "encole"
        y cuando termine con la ejecucion se llame el medoto definido como callback
        
        El metodo get_argument se usa para obtener el valor de un parametro
        que se le envie a la solicitud, el segundo parmatro en el llamado a la funcion
        es el valor por defecto que tendra en caso de no estar presente
        """
        
        # Se puede hacer la consulta por rango de fecha
        self.fecha_inicio = self.get_argument('fecha_inicio', '')
        self.fecha_fin = self.get_argument('fecha_fin', '')
        self._sales_callback()

class DetailHandler(tornado.web.RequestHandler):
    """
    Esta clase maneja el detalle de la factura, trae los productos que
    estan asociados a la compra
    """
    @property
    def cursor(self):
        return self.application.cur

    def _detail_sales(self, sale_id):
        self.cursor.execute("""SELECT sales_lines.*, products.name product_name, products.price price 
                                FROM sales_lines JOIN products 
                                ON sales_lines.product_id = products.id 
                                WHERE sale_id = %s""", (sale_id, ))
        res = copyListDicts( self.cursor.fetchall())
        ret = {}
        for r in res:
            r.update({'product_id_ref' : 'http://%s/products/%s'%(self.request.host, r.get('product_id'))})
        ret.update({'detail':res})
        return  ret

    def _detail_callback(self, sale_id):
        res = self._detail_sales(sale_id)
        self.set_header("Content-Type", "application/json")
        self.write(json.dumps(res, default=json_handler))
        self.finish()

    @tornado.web.asynchronous
    def get(self, sale_id):
        self._detail_callback(sale_id)

class ClientHandler(tornado.web.RequestHandler):

    @property
    def cursor(self):
        return self.application.cur

    def _get_clients(self, client_ids = None):
        if client_ids:
            self.cursor.execute("SELECT * FROM clients WHERE id IN (%s)", (client_ids, ))
        else:
            self.cursor.execute("SELECT * FROM clients")
        res = copyListDicts( self.cursor.fetchall())
        ret = {}
        for r in res:
            r.update({'ref' : 'http://%s/clients/%s'%(self.request.host, r.get('id'))})
        ret.update({'clients':res})
        return  ret

    def get(self, client_id):
        if client_id:
            res = self._get_clients(client_id)
        else:
            res = self._get_clients()
        self.set_header("Content-Type", "application/json")
        self.write(json.dumps(res))
        self.finish()

class MainHandler(tornado.web.RequestHandler):
    """
    En caso de que se desee servir paginas estaticas o plantillas creadas
    para la aplicacion se ejecuta el metodo render y se le indica que plantilla
    es la que va a renderizar y enviar al servidor
    """
    def get(self):
        self.render("index.html", common = common)

def main():
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

# Se ejecuta la funcion main
if __name__ == "__main__":
    main()
