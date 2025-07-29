import importlib, ast, json, os, inspect, datetime, time
from types import ModuleType
from typing import Any, Dict

class Wrap:
	def __init__(kimin, modul_path:str, debug:bool = False):
		if not os.path.exists(modul_path):
			raise FileNotFoundError(f"File Konfigurasi Modul Tidak Ditemukan : {modul_path}")
		kimin.debug = debug
		kimin.base_path = kimin._get_caller_dir()
		kimin.config = kimin._Load_Config(modul_path)
		kimin.modul: Dict[str, Any] = {}
		kimin._loader = set()
	
	def _get_caller_dir(kimin):
		# Ambil file script utama yang memanggil Modul_Wrapper
		s = time.process_time()
		frame = inspect.stack()[2]
		caller_file = frame.filename
		hasil = os.path.dirname(os.path.abspath(caller_file))
		if kimin.debug:
			print("="*50)
			print(f"[#] Caller File : {caller_file}")
			print(f"[#] Frame Detail: {frame}")
			print(f"[#] Current Dir : {hasil}")
			e = time.process_time()
			print(f"[#] Process Time: {e - s} sec")
			print("="*50)
		return hasil
	
	def _Validator(kimin, data: Dict[str, Any]) -> None:
		folder = data.get('folder', '')
		if not isinstance(folder, str):
			raise TypeError(f"Field 'folder' harus berupa string : {data}")
		
		path_file = data.get('file', [])
		if not isinstance(path_file, list):
			raise TypeError(f"Field 'file' harus berupa list : {data}")
		
		if any(not isinstance(i, str) for i in path_file):
			raise TypeError(f"Setiap item dalam 'file' harus berupa string : {data}")
		
		module_name = data.get('module', '')
		if not isinstance(module_name, str):
			raise TypeError(f"Field 'module' harus berupa string : {data}")
		
		object_name = data.get('function_name', '')
		if not isinstance(object_name, str):
			raise TypeError(f"Field 'function_name' harus berupa string : {data}")
		alias = data.get('alias', '')
		if not isinstance(alias, str):
			raise TypeError(f"Field 'alias' harus berupa string : {data}")
	
	def _Load_Config(kimin, path: str) -> Dict[str, Dict[str, Any]]:
		try:
			with open(path, 'r', encoding="UTF-8") as dataku:
				data = json.load(dataku)
				if 'modul' not in data:
					raise ValueError("Konfigurasi Modul tidak Mengandung kunci 'modul'")
				hasil = {}
				for i in data['modul']:
					kimin._Validator(i)
					
					folder = i.get('folder', '').strip('.')
					path_file = i.get('file', [])
					module_name = i.get('module')
					object_name = i.get('function_name', '')
					alias = i.get('alias')
					if not alias or alias == "":
						alias = object_name or module_name
					# print(alias)
					import_path = ".".join(filter(None, [folder] + path_file))
					
					is_stdlib = (folder.strip() == "" and len(path_file) == 0)
					if not is_stdlib:
						source_path = os.path.join(kimin.base_path, *([folder.replace('.', os.sep)]+ path_file)) + ".py"
						if not os.path.isfile(source_path):
							raise FileNotFoundError(f"File Modul tidak ditemukan di path : {source_path}")
					
					hasil[alias] = {"import_path":import_path, "object":object_name, "alias":alias, "module":module_name}
				return hasil
		except json.JSONDecodeError as e:
			raise ValueError(f"File JSON Tidak Valid : {e}")
	
	def Path_Function(kimin, config, *args, **kwargs):
		path = f"{config['import_path']}"
		class_name = config['object'] if not config['module'] == "" and not path == "" else config['module']
		if path == "":
			if not config['object'] == "":
				modul = importlib.import_module(class_name)
				modul = getattr(modul, config['object'])
			else:
				modul = __import__(class_name)
		else:
			modul = importlib.import_module(path)
			if not class_name == "":
				if not config['module'] == "":
					modul = getattr(modul, config['module'])
				else:
					modul = getattr(modul, class_name)
		return modul
	
	def _ImportModul(kimin, alias:str) -> Any:
		s = time.process_time()
		if alias not in kimin.config:
			raise KeyError(f"Alias '{alias}' tidak ditemukan di Konfigurasi")
		item = kimin.config[alias]
		import_path = item['import_path']
		object_name = item['object']
		modul = kimin.Path_Function(item)
		kimin.modul[alias] = modul
		kimin._loader.add(alias)
		if kimin.debug:
			target = f"{import_path}.{object_name}" if not import_path  == "" else object_name
			e = time.process_time()
			print(f"[+] Lazy loaded : {target} as '{alias}' -> {e - s} sec")
		return modul
	
	def Load(kimin, alias:str) -> Any:
		if alias in kimin.modul:
			return kimin.modul[alias]
		return kimin._ImportModul(alias)
	
	def ShowModul(kimin) -> Dict[str, Any]:
		return dict(kimin.modul)
		
	def ShowAlias(kimin) -> Dict[str, Any]:
		return {alias: item['import_path'] if not item['import_path'] == "" else item['object'] for alias, item in kimin.config.items()}
	
	def Reload(kimin, alias: str) -> Any:
		if alias in kimin.modul:
			del kimin.modul[alias]
			kimin._loader.discard(alias)
		return kimin._ImportModul(alias)
	
	