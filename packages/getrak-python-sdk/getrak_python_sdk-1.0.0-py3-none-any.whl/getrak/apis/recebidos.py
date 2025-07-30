import logging, jsonpickle
from http import HTTPMethod
from fmconsult.utils.url import UrlUtil
from getrak.api import GetrakApi

class Recebidos(GetrakApi):

  def get(self, id_veiculo, data_inicio, data_fim):
    logging.info(f'get vehicle {id_veiculo} records from {data_inicio} to {data_fim}...')
    res = self.call_request(
      http_method=HTTPMethod.GET, 
      request_url=UrlUtil().make_url(self.base_url, ['v0.1','recebidos', id_veiculo, data_inicio, data_fim])
    )    
    return jsonpickle.decode(res)