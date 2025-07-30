# -*- coding: utf-8 -*-
import json
from mongoengine import *
from mongoengine.fields import DateTimeField, EmbeddedDocumentField, FloatField, IntField, StringField, ListField
from fmconsult.database.models.base import CustomBaseDocument
from .dataexplained import DataExplained

class Vehicle(CustomBaseDocument):
	meta = {'collection': 'vehicles'}

	ano = StringField()
	anomodelo = StringField()
	apelido = StringField()
	apn = StringField()
	celmodulo = StringField()
	chassi = StringField()
	cliente_celular = StringField()
	cliente_id = IntField()
	cliente_nome = StringField()
	cliente_telefone = StringField()
	color = StringField()
	contato = StringField()
	cor = StringField()
	data = DateTimeField()
	dataServidor = EmbeddedDocumentField(DataExplained)
	datastatus = EmbeddedDocumentField(DataExplained)
	equipamento = StringField()
	fix = IntField()
	hodometro = IntField()
	horimetro = IntField()
	ico_veiculo = ListField(StringField())
	icone = StringField()
	id_veiculo = IntField(unique=True)
	lat = FloatField()
	latencia = FloatField()
	lig = IntField()
	lng = FloatField()
	lon = FloatField()
	marca = StringField()
	modelo = StringField()
	modulo = StringField()
	num_chip = StringField()
	operadora = StringField()
	placa = StringField()
	status_online = IntField()
	subcliente_id = IntField()
	subcliente_nome = StringField()
	telcontato = StringField()
	tipo = StringField()
	vel = IntField()
	velocidade = IntField()
 
	def to_dict(self):
		json_string = {
			"id_veiculo": self.id_veiculo,
			"ano": self.ano,
			"anomodelo": self.anomodelo,
			"apelido": self.apelido,
			"apn": self.apn,
			"celmodulo": self.celmodulo,
			"chassi": self.chassi,
			"cliente_celular": self.cliente_celular,
			"cliente_id": self.cliente_id,
			"cliente_nome": self.cliente_nome,
			"cliente_telefone": self.cliente_telefone,
			"color": self.color,
			"contato": self.contato,
			"cor": self.cor,
			"data": self.data.isoformat(),
			"dataServidor": self.dataServidor.to_mongo(),
			"datastatus": self.datastatus.to_mongo(),
			"equipamento": self.equipamento,
			"fix": self.fix,
			"hodometro": self.hodometro,
			"horimetro": self.horimetro,
			"ico_veiculo": self.ico_veiculo,
			"icone": self.icone,
			"lat": self.lat,
			"latencia": self.latencia,
			"lig": self.lig,
			"lng": self.lng,
			"lon": self.lon,
			"marca": self.marca,
			"modelo": self.modelo,
			"modulo": self.modulo,
			"num_chip": self.num_chip,
			"operadora": self.operadora,
			"placa": self.placa,
			"status_online": self.status_online,
			"subcliente_id": self.subcliente_id,
			"subcliente_nome": self.subcliente_nome,
			"telcontato": self.telcontato,
			"tipo": self.tipo,
			"vel": self.vel,
			"velocidade": self.velocidade,
			"created_at": self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
			"updated_at": self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if not(self.updated_at is None) else None
		}
	
		return json.dumps(json_string, default=str)