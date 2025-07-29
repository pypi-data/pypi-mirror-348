import logging, jsonpickle
from http import HTTPMethod
from fmconsult.utils.url import UrlUtil
from fipe.api import FipeApi

class Modelos(FipeApi):

    def __init__(self):
        super().__init__()
        self.endpoint_url = UrlUtil().make_url(self.base_url, ['ConsultarModelos'])

    def get_modelos_by_marca(self, codigoTabelaReferencia, codigoTipoVeiculo, codigoMarca):
        try:
            logging.info(f'listing FIPE Models by Brand {str(codigoMarca)}...')
            res = self.call_request(
                http_method=HTTPMethod.POST,
                request_url=self.endpoint_url,
                payload=self.create_payload(codigoTabelaReferencia, codigoTipoVeiculo, codigoMarca)
            )
            return jsonpickle.decode(res)
        except:
            raise