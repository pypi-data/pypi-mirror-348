import logging, os, jsonpickle
from http import HTTPMethod
from fmconsult.http.api import ApiBase
from fmconsult.utils.url import UrlUtil

class GetrakApi(ApiBase):

	def __init__(self):
		try:
			self.api_auth_code 	= os.environ['getrak.api.auth_code']
			self.api_login 		= os.environ['getrak.api.login']
			self.api_password 	= os.environ['getrak.api.password']
			self.api_grant_type = os.environ['getrak.api.grant_type']

			self.base_url = 'https://api.getrak.com'
			self.headers = {
				'Authorization': f'Basic {self.api_auth_code}'
			}

			self.__login()
		except:
			raise
	
	def __login(self):
		try:
			logging.info('api authentication...')
			res = self.call_request(
				http_method=HTTPMethod.POST, 
				request_url=UrlUtil().make_url(self.base_url, ['newkoauth','oauth','token']), 
				params={
					'username': self.api_login, 
					'password': self.api_password,
					'grant_type': self.api_grant_type
				}
			)
			res = jsonpickle.decode(res)
			if not('error' in res):
				self.token_type = res['token_type']
				self.access_token = res['access_token']
				self.headers = {
					'Authorization': f'{self.token_type} {self.access_token}'
				}
			else:
				raise Exception(res['error_description'])
		except:
			raise