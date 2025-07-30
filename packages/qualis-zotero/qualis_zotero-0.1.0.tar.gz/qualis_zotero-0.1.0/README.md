# qualis-zotero

Ferramenta para automatizar a verificação e classificação de artigos do Zotero com base na tabela Qualis CAPES, utilizando também a API do OpenAlex.
## Antes de começar, você precisará de alguns requisitos:

Python: O código foi escrito em Python. Você precisa ter o Python instalado em sua máquina. A versão recomendada é a Python 3.x.

Pacotes Python: O código usa algumas bibliotecas externas que precisam ser instaladas. Use pip para instalar os pacotes necessários.

`pip install requests fuzzywuzzy pandas rapidfuzz`

Conta Zotero: Certifique-se de ter uma conta no Zotero. Você pode criar uma conta em https://www.zotero.org/.

API Key Zotero: Você precisará gerar uma chave de API do Zotero, que será usada para autenticar suas requisições.

### Passo 1: Obter a API Key do Zotero

- Acesse sua conta no [Zotero](https://www.zotero.org/).

- Vá para Configurações de [API](https://www.zotero.org/settings/keys0).

- Crie uma nova chave de API.

- Copie a chave (token) de API gerada. Você usará essa chave para autenticar suas requisições para a API do Zotero.
    - OBS: Guarde o UserID da API, você pode precisar 

### Passo 2: Obter o ID do Grupo e da Coleção
- Se você estiver utilizando uma biblioteca de grupo no Zotero, precisará do ID do grupo e da chave da coleção para acessar os itens do grupo.

- ID do Grupo: Vá até a página do seu grupo no Zotero. O ID do grupo geralmente aparece na URL do grupo. Exemplo: `https://www.zotero.org/groups/GROUPID/my_group`, onde GROUPID é o ID do grupo.

- Chave da Coleção: Ao acessar a coleção, procure o ID único da coleção na URL, por exemplo: `https://www.zotero.org/groups/GROUPID/nome-do-grupo/collections/KEY_COLLECTION`, onde KEY_COLLECTION é a chave da coleção. Copie e cole somente a URLabaixo no navegador para encontrar a KEY_COLLECTION da coleção desejada:
```markdown
https://www.zotero.org/groups/GROUPID/nome-do-grupo/collections
```
    - Outras informações `https://api.zotero.org/users/USER_ID/groups?key=API_KEY`, onde USER_ID é o user id do API e API_KEY é a chave

## Funcionamento

- Conecta com Zotero via API para obter artigos de uma coleção de grupo.
- Busca o ISSN via DOI ou título usando a API do OpenAlex.
- Atribui o estrato Qualis com base em base CSV fornecida.
- Atualiza os campos `ISSN` e `extra` nos itens Zotero.
- Usa Fuzzy Matching como fallback quando o ISSN não está presente na base Qualis.

## Instalação local

Clone o repositório e instale localmente:

```bash
git clone https://github.com/wvanucci/Qualis-Zotero/tree/main/qualis-zotero.git
cd qualis-zotero
pip install .
