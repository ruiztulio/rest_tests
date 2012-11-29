class Product():
    def _build_restrict(self, restrictions):
        res = u""
        params = []
        for r in restrictions:
            res += u" AND " + r[0] + r[1] + " %s "
            values.append(r[2])
        if res:
            return (res[4:], params)
        return (res, params)
        
    def select(self, restrictions = None):
        r = self._build_restrict(restrictions)
        sql = "SELECT * FROM products"
        if r[0]:
            sql += " WHERE "+r[0]
        self.cursor.execute(sql, r[1])
        res = copyListDicts( self.cursor.fetchall())
        
    
