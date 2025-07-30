# oryum_stack/config/settings.py

_config = {
    "verbose": False
}

def set(key, value):
    _config[key] = value

def get(key, default=None):
    return _config.get(key, default)

def load_from_file(path):
    try:
        with open(path, "r") as f:
            exec(f.read(), globals())
    except Exception as e:
        print(f"Erro ao carregar configuração: {e}")
