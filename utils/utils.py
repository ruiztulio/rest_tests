from decimal import Decimal

def json_handler(obj):
    """
    This function handles the datetime and Decimal objects so
    there is no problem with json serialization
    """
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    if isinstance(obj, Decimal):
        return float(obj)
    return obj

def copyListDicts(lines):
    res = []
    for line in lines:
        d = {}
        for l in line.keys():
            d.update({l : line[l]})
        res.append(d.copy())
    return res
