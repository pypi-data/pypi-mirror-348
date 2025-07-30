import logging, jsonpickle
from http import HTTPMethod
from fmconsult.utils.url import UrlUtil
from getrak.api import GetrakApi

class Localizacoes(GetrakApi):

  def get(self, id_veiculo=None, id_modulo=None):
    logging.info('get vehicles locations...')
    
    params = { }

    if not(id_veiculo is None):
      params['id'] = id_veiculo
    
    if not(id_modulo is None):
      params['modulo'] = id_modulo

    res = self.call_request(
      http_method=HTTPMethod.GET, 
      request_url=UrlUtil().make_url(self.base_url, ['v0.1','localizacoes']), 
      params=params
    )
    
    res = jsonpickle.decode(res)
    
    return res['veiculos']