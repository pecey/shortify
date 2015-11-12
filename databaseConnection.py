import redis

def connect(server="127.0.0.1", port=6379, db=0, password=None):
	connection = {}
	connection['Status'] = None
	connection['Data'] = None
	try:
		connectionString = redis.StrictRedis(host=server, port=port, db=db, password=password, charset="utf-8")
		connection['Status'] = True
		connection['Data'] = connectionString
	except:
		connection['Status'] = False
		connection['Data'] = "There was an error in connecting to the Redis server."
	finally:
		return connection

def insert(connectionString, key, value):
	response = {}
	response['Status'] = None
	response['Data'] = None
	if connectionString.exists(key):
		response['Status'] = False
		response['Data'] = "Key is already set."
	else:
		connectionString.set(key,value)
		response['Status'] = True
		response['Data'] = "Data inserted."
	return response

def query(connectionString, key):
	response = {}
	response['Status'] = None
	response['Data'] = None
	if connectionString.exists(key):
		response['Status'] = True
		response['Data'] = connectionString.get(key)
	else:
		response['status'] = False
		response['Data'] = "Key not set."
	return response