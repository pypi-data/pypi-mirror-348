import requests

doi_cache = {}
titulo_cache = {}


def buscar_issn(titulo, doi=None):
    """
    Busca o(s) ISSN de um artigo com base no título e/ou DOI usando a API OpenAlex.

    Args:
        title (str): Título do artigo.
        doi (str): DOI do artigo.

    Returns:
        list[str]: Lista de ISSNs encontrados (sem hífen).
    """
    base_url = "https://api.openalex.org/works"
    if doi and doi in doi_cache:
        return [doi_cache[doi]]
    if titulo and titulo in titulo_cache:
        return [titulo_cache[titulo]]

    try:
        if doi:
            url = f"{base_url}/https://doi.org/{doi}"
            r = requests.get(url)
            data = r.json()
        else:
            r = requests.get(base_url, params={"search": titulo, "per_page": 1})
            data = r.json()['results'][0] if r.json().get('results') else {}

        source = data.get("primary_location", {}).get("source", {})
        issns = source.get("issn", [])
        issn_l = source.get("issn_l")
        all_issns = ([issn_l] if issn_l else []) + [i for i in issns if i != issn_l]

        if all_issns:
            if doi: doi_cache[doi] = all_issns[0]
            if titulo: titulo_cache[titulo] = all_issns[0]
            return all_issns
    except Exception:
        pass
    return []
