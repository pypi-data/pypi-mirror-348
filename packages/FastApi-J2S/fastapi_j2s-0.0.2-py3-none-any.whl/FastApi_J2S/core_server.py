import importlib

class Set_Server:
	def __init__(kimin, config, loader, base_dir):
		kimin.loader = loader
		kimin.config = loader.Load('ext')(loader=loader).ReadFile(path=config, tipe='json', mode='r')['data']
		kimin.base_dir= base_dir
		kimin.use_routes = []
	
	def Check_Func(kimin, modul, function):
		return hasattr(modul, function)
	
	def Prepare(kimin):
		if kimin.modul['ext'](modul=kimin.modul).CekFile(f"{kimin.config['routes']['modul_name'].replace('.', '/')}.py")['data']:
			kimin.modul['Gen'](log=kimin.config['system'].get('builder_log', False), modul=kimin.modul, modul_path=kimin.config['routes']['modul_name'], class_name=kimin.config['routes']['class_name']).generate(func=kimin.config['routes'], mode='new')
		
		for route in kimin.config['route']:
			if route not in ['modul_name', 'class_name']:
				function = kimin.config['routes'][route]['function']
				modul = importlib.import_module(f"{kimin.config['routes']['modul_name']}")
				modul = getattr(modul, kimin.config['routes']['class_name'])(modul=kimin.modul)
				if not kimin.Check_Func(modul, function):
					kimin.modul['Gen'](log=kimin.config['system'].get('builder_log', False), modul=kimin.modul, modul_path=kimin.config['routes']['modul_name'], class_name=kimin.config['routes']['class_name']).generate(func=kimin.config['routes'][route], kunci=route)
		# sin = kimin.modul['Gen'](log=kimin.config['system'].get('builder_log', False), modul=kimin.modul)
	
	def Routes(kimin, server):
		for route in kimin.config['routes']:
			if route not in ['modul_name', 'class_name']:
				if kimin.config['routes'][route] not in kimin.use_routes:
					modul = importlib.import_module(f"{kimin.config['routes']['modul_name']}")
					if kimin.config['system'].get('import_config', False):
						modul = getattr(modul, kimin.config['routes']['class_name'])(loader=kimin.loader, cfg=kimin.config, server=server)
					else:
						modul = getattr(modul, kimin.config['routes']['class_name'])(loader=kimin.loader)
					function = kimin.config['routes'][route]['function']
					url = kimin.config['routes'][route]['url']
					methods= [i.lower() for i in kimin.config['routes'][route]['methods']]
					
					if 'get' in methods:
						server.get(url)(getattr(modul, function))
					if 'post' in methods:
						server.post(url)(getattr(modul, function))
					if 'delete' in methods:
						server.delete(url)(getattr(modul, function))
					if 'head' in methods:
						server.head(url)(getattr(modul, function))
					
					kimin.use_routes.append(kimin.config['routes'][route])
	
	def Server(kimin):
		"""Menyiapkan aplikasi FastAPI dan konfigurasi server"""
		# Mengatur file statis
		# kimin.app.mount("/static", StaticFiles(directory=f"{kimin.base_dir}/{kimin.config['server']['static_path']}"),
					   # name="static")

		# if kimin.config['server'].get('debug', False):
			# kimin.app.debug = True
		fi = kimin.loader.Load('FI')
		template = kimin.loader.Load('template')
		static = kimin.loader.Load('static')
		server = fi()
		server.mount("/static", static(directory=f"{kimin.base_dir}/{kimin.config['server']['static_path']}"), name="static")
		template(directory=f"{kimin.base_dir}/{kimin.config['server']['template_path']}")
		return server