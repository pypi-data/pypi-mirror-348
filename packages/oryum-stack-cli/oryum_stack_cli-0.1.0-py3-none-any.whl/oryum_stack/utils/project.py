import os

def is_oryum_project():
    """Verifica se o diretório atual contém uma estrutura Oryum."""
    return os.path.exists("oryum.json") or os.path.exists("oryum_stack")

def get_project_root():
    """Retorna o caminho absoluto da raiz do projeto."""
    return os.getcwd()
