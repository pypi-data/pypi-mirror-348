import pandas as pd

estrato_ordem = {
    'A1': 1, 'A2': 2, 'A3': 3, 'A4': 4,
    'B1': 5, 'B2': 6, 'B3': 7, 'B4': 8, 'C': 9
}


def carregar_base_qualis(caminho_csv):
    """
    Carrega a base Qualis do arquivo CSV.

    Args:
        caminho_csv (str): Caminho para o arquivo CSV da base Qualis.

    Returns:
        tuple:
            dict: Mapeamento ISSN -> estrato Qualis
            dict: Mapeamento nome da revista (minúsculo) -> estrato Qualis
    """
    df = pd.read_csv(caminho_csv, sep=';', header=None, dtype=str, names=['ISSN', 'Nome', 'Área', 'Qualis'])
    df['ISSN'] = df['ISSN'].str.replace('-', '', regex=False).str.strip()
    dict_issn = dict(zip(df['ISSN'], df['Qualis']))

    dict_nome = {}
    for _, row in df.iterrows():
        nome = row['Nome'].strip().lower()
        estrato = row['Qualis'].strip().upper()
        if nome in dict_nome:
            if estrato_ordem.get(estrato, 99) < estrato_ordem.get(dict_nome[nome], 99):
                dict_nome[nome] = estrato
        else:
            dict_nome[nome] = estrato

    return dict_issn, dict_nome
