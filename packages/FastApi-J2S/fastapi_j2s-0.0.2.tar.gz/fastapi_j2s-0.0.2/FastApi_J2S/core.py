import inspect, uvicorn, os
class Processing:
	def __init__(kimin, **parameter):
		kimin.parameter = parameter
		kimin.base_dir = kimin.Base_Dir()
		if 'loader' in kimin.parameter:
			kimin.loader = kimin.parameter['loader']
			ext = kimin.loader.Load('ext')
			kimin.loader.Load('colorama').init()
			kimin.config = ext(loader=kimin.parameter['loader']).ReadFile(path=kimin.parameter['config_path'], tipe='json', mode='r')['data']
		else:
			raise FileNotFoundError(f"Ada Yang Error Dengan Parameter 'loader'")
	
	def Base_Dir(kimin):
		stack = inspect.stack()
		for frame_info in stack:
			# Menghindari frame dari modul ini sendiri
			if frame_info.filename != __file__:
				# Mendapatkan path dari file yang memanggil fungsi ini
				caller_file = frame_info.filename
				# Mendapatkan base path dari file pemanggil
				caller_base_path = os.path.dirname(os.path.abspath(caller_file))
				return caller_base_path
		return None
	
	def Run_Server(kimin):
		modul = kimin.loader.Load('server')
		x = modul(config=kimin.parameter['config_path'], loader=kimin.loader, base_dir=kimin.base_dir)
		server = x.Server()
		x.Routes(server)
		if 'ssl' in kimin.config['server'] and 'cert' in kimin.config['server']['ssl'] and 'key' in kimin.config['server']['ssl'] and kimin.config['server']['ssl']['cert'] and kimin.config['server']['ssl']['key']:
			uvicorn.run(server, host=kimin.config['server']['host'], port=kimin.config['server']['port'], ssl_keyfile=kimin.config['server']['ssl']['key'], ssl_certfile=kimin.config['server']['ssl']['cert'])
		else:
			uvicorn.run(server, host=kimin.config['server']['host'], port=kimin.config['server']['port'])