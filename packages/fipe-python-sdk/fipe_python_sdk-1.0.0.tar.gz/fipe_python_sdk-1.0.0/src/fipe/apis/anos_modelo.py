import logging, jsonpickle
from http import HTTPMethod
from fmconsult.utils.url import UrlUtil
from fipe.api import FipeApi

class AnosModelo(FipeApi):

    def __init__(self):
        super().__init__()
        self.endpoint_url = UrlUtil().make_url(self.base_url, ['ConsultarAnoModelo'])

    def get_anos_by_modelo(self, codigoTabelaReferencia, codigoTipoVeiculo, codigoMarca, codigoModelo):
        try:
            logging.info(f'listing FIPE Years by Model {str(codigoModelo)}...')
            res = self.call_request(
                http_method=HTTPMethod.POST,
                request_url=self.endpoint_url,
                payload=self.create_payload(codigoTabelaReferencia, codigoTipoVeiculo, codigoMarca, codigoModelo)
            )
            return jsonpickle.decode(res)
        except:
            raise