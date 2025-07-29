import logging, jsonpickle
from http import HTTPMethod
from fmconsult.utils.url import UrlUtil
from fipe.api import FipeApi

class ValorParametros(FipeApi):

    def __init__(self):
        super().__init__()
        self.endpoint_url = UrlUtil().make_url(self.base_url, ['ConsultarValorComTodosParametros'])

    def get_valor_by_parametros(self, codigoTabelaReferencia, codigoTipoVeiculo, codigoMarca, codigoModelo, anoModelo):
        try:
            logging.info(f'get Valor by parameters...')
            res = self.call_request(
                http_method=HTTPMethod.POST,
                request_url=self.endpoint_url,
                payload=self.create_payload(codigoTabelaReferencia, codigoTipoVeiculo, codigoMarca, codigoModelo, anoModelo)
            )
            return jsonpickle.decode(res)
        except:
            raise