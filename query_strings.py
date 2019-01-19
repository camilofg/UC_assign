class QueryStrings:
    dictionary_query = {
        "update_solicitud_cto": 'UPDATE SOLICITUDES SET "Circuito" = '
                                'REGEXP_REPLACE(LTRIM(RTRIM("Circuito")), ‘/’, ‘’);',
        "update_tramos_cto": 'UPDATE TRAMOS T2 SET "CTO_COD" = TC."alias" '
                             'FROM (( SELECT S."Circuito", T."IdElemento", C."alias" '
                             'FROM TRAMOS T INNER JOIN SOLICITUDES S ON T."IdSolicitud" = S."IdSolicitud" '
                             'INNER JOIN CIRCUITOS C ON S."Circuito" = C."linea" )) AS TC '
                             'WHERE T2."IdElemento" = TC."IdElemento"; '
                             ''
                             'UPDATE TRAMOS T2 SET "CTO_COD" = TC."alias" '
                             'FROM(( SELECT S."Circuito", T."IdElemento", C."alias" FROM TRAMOS T '
                             'INNER JOIN SOLICITUDES S ON T."IdSolicitud" = S."IdSolicitud" '
                             'INNER JOIN CIRCUITOS C ON C."linea" = S."Circuito" '
                              'AS TC WHERE T2."IdElemento" = TC."IdElemento" '
    }

    def __init__(self):
        self.dictionary_query = {
            "update_solicitud_cto": 'UPDATE SOLICITUDES SET "Circuito" = '
                                    'REGEXP_REPLACE(LTRIM(RTRIM("Circuito")), ‘/’, ‘’);',
            "update_tramos_cto": 'UPDATE TRAMOS T2 SET "CTO_COD" = TC."alias" '
                                 'FROM (( SELECT S."Circuito", T."IdElemento", C."alias"--* '
                                 'FROM TRAMOS T INNER JOIN SOLICITUDES S ON T."IdSolicitud" = S."IdSolicitud" '
                                 'INNER JOIN CIRCUITOS C ON S."Circuito" = C."linea" )) AS TC '
                                 'WHERE T2."IdElemento" = TC."IdElemento"; '
                                 ''
                                 'UPDATE TRAMOS T2 SET "CTO_COD" = TC."alias" '
                                 'FROM(( SELECT S."Circuito", T."IdElemento", C."alias" FROM TRAMOS T '
                                 'INNER JOIN SOLICITUDES S ON T."IdSolicitud" = S."IdSolicitud" '
                                 'INNER JOIN CIRCUITOS C ON C."linea" = S."Circuito"--LIKE '%'|| S."Circuito"|| '%' )) '
                                 'AS TC WHERE T2."IdElemento" = TC."IdElemento" '
        }