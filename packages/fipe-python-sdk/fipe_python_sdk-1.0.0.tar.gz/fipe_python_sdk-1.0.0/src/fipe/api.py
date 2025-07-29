import os
from fmconsult.http.api import ApiBase

class FipeApi(ApiBase):
    
    def __init__(self):
        try:
            self.base_url = 'https://veiculos.fipe.org.br/api/veiculos'
            self.headers = {}
        except:
            raise
    
    def create_payload(self, codigoTabelaReferencia=None, codigotTipoVeiculo=None, codigoMarca=None, codigoModelo=None, anoModelo=None):
        payload = {}

        if not(codigoTabelaReferencia is None):
            payload['codigoTabelaReferencia'] = int(codigoTabelaReferencia)

        if not(codigotTipoVeiculo is None):
            payload['codigoTipoVeiculo'] = int(codigotTipoVeiculo)

        if not(codigoMarca is None):
            payload['codigoMarca'] = int(codigoMarca)
        
        if not(codigoModelo is None):
            payload['codigoModelo'] = int(codigoModelo)
        
        if not(anoModelo is None):
            payload['ano'] = str(anoModelo)
            split = anoModelo.split('-')
            payload['anoModelo'] = int(split[0])
            payload['codigoTipoCombustivel'] = int(split[1])
            payload['tipoConsulta'] = str('tradicional')

        return payload