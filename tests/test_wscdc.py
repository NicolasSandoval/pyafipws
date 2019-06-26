# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 3, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTIBILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.

"""Pruebas para el servicio web Constatación de Comprobantes de AFIP"""

__author__ = "Mariano Reingart <reingart@gmail.com>"
__copyright__ = "Copyright (C) 2013-2019 Mariano Reingart"
__license__ = "GPL 3.0"


import unittest
import sys

from pyafipws.wscdc import WSCDC
from pyafipws.wsaa import WSAA


WSDL = "https://wswhomo.afip.gov.ar/WSCDC/service.asmx?WSDL"
CUIT = 20267565393
CERT = "home/reingart/pyafipws/reingart.crt"
PRIVATEKEY = "home/reingart/pyafipws/reingart.key"
CACERT = "home/reingart/pyafipws/afip_root_desa_ca.crt"
CACHE = "home/reingart/pyafipws/cache"

# Autenticación:
ta = WSAA().Autenticar("wscdc", "reingart.crt", "reingart.key")
print(ta)


class TestWSCDC(unittest.TestCase):

    def setUp(self):
        sys.argv.append("--trace")                  # TODO: use logging
        self.wscdc = wscdc = WSCDC()
        wscdc.LanzarExcepciones = True
        wscdc.SetTicketAcceso(ta)
        wscdc.Conectar(CACHE, WSDL)
        wscdc.Cuit = CUIT

    def test_dummy(self):
        wscdc = self.wscdc
        print(wscdc.client.help('ComprobanteDummy'))
        wscdc.Dummy()
        print("AppServerStatus", wscdc.AppServerStatus)
        print("DbServerStatus", wscdc.DbServerStatus)
        print("AuthServerStatus", wscdc.AuthServerStatus)
        self.assertEqual(wscdc.AppServerStatus, 'OK')
        self.assertEqual(wscdc.DbServerStatus, 'OK')
        self.assertEqual(wscdc.AuthServerStatus, 'OK')

    def test_constatar_comprobante(self):
        """Prueba de Constatación de Comprobantes."""
        wscdc = self.wscdc
        cbte_modo = "CAE"
        cuit_emisor = "20267565393"
        pto_vta = 4002
        cbte_tipo = 1
        cbte_nro = 109
        cbte_fch = "20131227"
        imp_total = "121.0"
        cod_autorizacion = "63523178385550"
        doc_tipo_receptor = 80
        doc_nro_receptor = "30628789661"
        ok = wscdc.ConstatarComprobante(cbte_modo, cuit_emisor, pto_vta, cbte_tipo,
                                        cbte_nro, cbte_fch, imp_total, cod_autorizacion,
                                        doc_tipo_receptor, doc_nro_receptor)
        self.assertTrue(ok)
        self.assertEqual(wscdc.Resultado, "R")  # Rechazado
        self.assertEqual(wscdc.Obs,
                         "100: El N° de CAI/CAE/CAEA consultado no existe en las bases del organismo.")
        self.assertEqual(wscdc.PuntoVenta, pto_vta)
        self.assertEqual(wscdc.CbteNro, cbte_nro)
        self.assertEqual(wscdc.ImpTotal, imp_total)
        self.assertEqual(wscdc.CAE, cod_autorizacion)
        self.assertEqual(wscdc.EmisionTipo, "CAE")

    def test_escribir_archivo(self):
        pass

    def test_leer_archivo(self):
        pass

    def test_consultas(self):
        wscdc = self.wscdc
        self.assertIsInstance(wscdc.ConsultarModalidadComprobantes(), list)
        self.assertIsInstance(wscdc.ConsultarTipoComprobantes(), list)
        self.assertIsInstance(wscdc.ConsultarTipoDocumentos(), list)
        self.assertIsInstance(wscdc.ConsultarTipoOpcionales(), list)


if __name__ == '__main__':
    unittest.main()
