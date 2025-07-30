import yaml
from pathlib import Path


def load_config(path="config.yaml"):
    """
    Carrega configurações do arquivo YAML.

    Args:
        path (str): Caminho para o arquivo YAML de configuração.

    Returns:
        dict: Dicionário com as configurações carregadas.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Arquivo de configuração '{path}' não encontrado.")
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)
