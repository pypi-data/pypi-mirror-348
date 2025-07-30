import requests


def get_items(api_key, group_id, collection_key):
    """
    Obtém os itens da coleção Zotero.

    Args:
        api_key (str): Chave da API Zotero.
        group_id (str): ID do grupo Zotero.
        collection_key (str): Chave da coleção Zotero.

    Returns:
        list: Lista de itens JSON da coleção.
    """
    items = []
    start = 0
    while True:
        url = f"https://api.zotero.org/groups/{group_id}/collections/{collection_key}/items"
        headers = {"Zotero-API-Key": api_key}
        params = {"limit": 100, "start": start}
        resp = requests.get(url, headers=headers, params=params)
        if resp.status_code != 200:
            break
        batch = resp.json()
        if not batch:
            break
        items.extend(batch)
        start += 100
    return items


def update_item(api_key, group_id, item_key, issn, qualis):
    """
    Atualiza o ISSN e a classificação Qualis de um item no Zotero.

    Args:
        api_key (str): Chave da API Zotero.
        group_id (str): ID do grupo Zotero.
        item_key (str): Chave do item Zotero.
        issn (str): ISSN para atualizar.
        qualis (str): Estrato Qualis para atualizar.

    Returns:
        bool: True se a atualização foi bem-sucedida, False caso contrário.

    Prints mensagens informativas sobre as atualizações realizadas.
    """
    url = f"https://api.zotero.org/groups/{group_id}/items/{item_key}"
    headers = {"Zotero-API-Key": api_key, "Content-Type": "application/json"}
    item_data = requests.get(url, headers=headers).json()

    updated = False
    if issn and item_data['data'].get('ISSN') != issn:
        item_data['data']['ISSN'] = issn
        updated = True
    if qualis and item_data['data'].get('extra') != qualis:
        item_data['data']['extra'] = qualis
        updated = True

    if updated:
        put = requests.put(url, headers=headers, json=item_data)
        return put.status_code == 200
    return False
