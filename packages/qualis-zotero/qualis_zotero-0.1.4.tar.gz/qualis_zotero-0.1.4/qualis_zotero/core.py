from .zotero import get_items, update_item
from .qualis import carregar_base_qualis
from .openalex import buscar_issn
from thefuzz import process, fuzz
from tqdm import tqdm


def processar(zotero_api_key, zotero_group_id, collection_key, qualis_csv_path,**kwargs):
    """
    Processa os itens de uma coleção do Zotero, atualizando o campo ISSN (se necessário) e atribuindo a classificação Qualis com base em uma base de dados CSV.

    A função realiza as seguintes etapas:
    1. Busca os itens da coleção especificada no grupo Zotero.
    2. Verifica se o campo ISSN está presente. Caso não esteja, tenta obtê-lo via API do OpenAlex.
    3. Com o ISSN, consulta a base Qualis para obter o estrato da publicação.
    4. Se o ISSN não estiver na base, realiza uma correspondência fuzzy com o nome da revista.
    5. Atualiza os dados no Zotero com o ISSN e a classificação Qualis, quando aplicável.
    6. Exibe um resumo da execução, incluindo número de correspondências via OpenAlex e Fuzzy Matching.

    :param zotero_api_key: Chave de API do Zotero com permissões de leitura/escrita.
    :type zotero_api_key: str
    :param zotero_group_id: ID do grupo Zotero onde os itens estão armazenados.
    :type zotero_group_id: str
    :param collection_key: Chave da coleção Zotero a ser processada.
    :type collection_key: str
    :param qualis_csv_path: Caminho para o arquivo CSV contendo os dados do Qualis (com colunas 'ISSN', 'Estrato' e 'Publicação').
    :type qualis_csv_path: str

    :return: Nenhum valor é retornado. Os dados são atualizados diretamente no Zotero, e um relatório é impresso no console.
    :rtype: None
    """

    qualis_dict_issn, qualis_dict_nome = carregar_base_qualis(qualis_csv_path)
    items = get_items(zotero_api_key, zotero_group_id, collection_key)
    fuzzy_matches = []
    count_openalex = count_fuzzy = 0

    for item in tqdm(items, desc="Processando artigos"):
        data = item.get("data", {})
        if data.get('itemType') != 'journalArticle':
            continue
        titulo = data.get("title", "")
        doi = data.get("DOI", "")
        issn = data.get("ISSN", "").replace("-", "").strip()
        pub = data.get("publicationTitle", "").strip().lower()
        item_key = data.get("key")

        if issn not in qualis_dict_issn:
            novos = buscar_issn(titulo, doi)
            for n in novos:
                if n.replace("-", "").strip() in qualis_dict_issn:
                    issn = n.replace("-", "").strip()
                    count_openalex += 1
                    break
            else:
                if novos:
                    issn = novos[0].replace("-", "").strip()

        nota = qualis_dict_issn.get(issn)
        if not nota and pub:
            match = process.extractOne(pub, qualis_dict_nome.keys(), scorer=fuzz.WRatio)
            if match and match[1] >= 80:
                nota = qualis_dict_nome[match[0]]
                count_fuzzy += 1
                fuzzy_matches.append({
                    'titulo': titulo,
                    'pub_zotero': pub,
                    'match_qualis': match[0],
                    'score': match[1],
                    'qualis': nota
                })

        if nota:
            update_item(zotero_api_key, zotero_group_id, item_key, issn, nota)

    print("\nResumo da execução:")
    print(f"Artigos com ISSN via OpenAlex: {count_openalex}")
    print(f"Artigos com Fuzzy Matching: {count_fuzzy}")
    if fuzzy_matches:
        print("\nDetalhes dos artigos que usaram Fuzzy Matching:")
        for match in fuzzy_matches:
            print(f"- {match['titulo']}")
            print(f"  Revista no Zotero: {match['pub_zotero']}")
            print(f"  Match Qualis: {match['match_qualis']} (score: {match['score']})")
            print(f"  Estrato atribuído: {match['qualis']}\n")


from .config import load_config


def processar_com_config(path="config.yaml"):
    config = load_config(path)
    processar(
        zotero_api_key=config["zotero_api_key"],
        zotero_group_id=config["zotero_group_id"],
        collection_key=config["collection_key"],
        qualis_csv_path=config["qualis_csv_path"]
    )
