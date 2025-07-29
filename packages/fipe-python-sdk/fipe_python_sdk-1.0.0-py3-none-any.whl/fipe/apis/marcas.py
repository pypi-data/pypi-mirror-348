import logging, jsonpickle
from http import HTTPMethod
from fmconsult.utils.url import UrlUtil
from fipe.api import FipeApi

class Marcas(FipeApi):

    def __init__(self):
        super().__init__()
        self.endpoint_url = UrlUtil().make_url(self.base_url, ['ConsultarMarcas'])

    def get_marcas(self, codigoTabelaReferencia, codigoTipoVeiculo):
        try:
            logging.info('listing FIPE Brands...')
            res = self.call_request(
                http_method=HTTPMethod.POST,
                request_url=self.endpoint_url,
                payload=self.create_payload(codigoTabelaReferencia, codigoTipoVeiculo)
            )
            return jsonpickle.decode(res)
        except:
            raise