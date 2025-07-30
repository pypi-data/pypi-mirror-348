from .core import processar
from .config import load_config


def main():
    config = load_config()
    # Passa o dicionário desempacotado nos argumentos nomeados
    processar(
        zotero_api_key=config['zotero_api_key'],
        zotero_group_id=config['zotero_group_id'],
        collection_key=config['collection_key'],
        qualis_csv_path=config['qualis_csv_path']
    )


if __name__ == "__main__":
    main()
