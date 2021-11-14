def hash(SumaASCII: int, timestamp: int) -> int:
    return SumaASCII % timestamp


# codigo; block_number; from_address; to_address; value; block_timestamp
def cargar_programa(ruta: str) -> list:
    res = []
    cadena = ''
    suma = 0
    bloque = -1
    with open(ruta) as f:
        f.readline()

        for linea in f:
            lista = linea.strip().split(',')
            bloque = int(lista[1])
            if bloque + 1 == len(res):
                res[bloque]['cantidad_transacciones'] += 1
                res[bloque][transaccion] = {
                    'codigo_transaccion': lista[0],
                    'remitente': lista[2],
                    'destinatario': lista[3],
                    'valor': lista[4],
                    'operacion': 'contrato' if lista[3] == '' else 'transferencia'
                }
                for valor in res[len(res) - 1][transaccion].values():
                    cadena += valor
                transaccion += 1
            else:
                if bloque >= 1:
                    cadena += str(res[bloque - 1]['numero_bloque']) + \
                        str(res[bloque - 1]['hash_anterior'])
                    for caracter in cadena:
                        suma += ord(caracter)

                    res[bloque -
                        1]['hash'] = hash(suma, res[bloque - 1]['timestamp'])
                    cadena = ''
                    suma = 0
                transaccion = 0
                res.append({'numero_bloque': bloque,
                           'cantidad_transacciones': 1,
                            transaccion: {
                                'codigo_transaccion': lista[0],
                                'remitente': lista[2],
                                'destinatario': lista[3],
                                'valor': lista[4],
                                'operacion': 'contrato' if lista[3] == '' else 'transferencia'
                            },
                            'timestamp': int(lista[5]),
                            'abierto': True if lista[5] == '' else False
                            })
                res[bloque]['hash_anterior'] = res[bloque -
                                                   1].get('hash') if len(res) > 1 else None
                for valor in res[len(res) - 1][transaccion].values():
                    cadena += valor
                transaccion += 1

        cadena += str(res[bloque]['numero_bloque']) + \
            str(res[bloque]['hash_anterior'])
        for caracter in cadena:
            suma += ord(caracter)
        res[bloque]['hash'] = hash(suma, res[bloque]['timestamp'])

        return res


def agregar_transaccion(blockchain: list, transaccion: dict):
    if blockchain[len(blockchain) - 1]['abierto']:
        blockchain[len(blockchain) - 1][blockchain[len(blockchain) - 1]
                                        ['cantidad_transacciones']] = transaccion
        blockchain[len(blockchain) - 1]['cantidad_transacciones'] += 1
    else:
        blockchain.append({
            'numero_bloque': len(blockchain),
            'cantidad_transacciones': 1,
            'abierto': True,
            'hash_anterior': blockchain[len(blockchain) - 1]['hash'],
            0: transaccion
        })
    return blockchain
