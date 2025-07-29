from jellyfish import jaro_winkler, levenshtein_distance
from unicodedata import normalize
from string import punctuation
from functools import lru_cache


def remover_acentos(frase: str):
    """
    Remove acentos da frase parametro
    :param frase: parametros a remover acentos
    :return:
    """
    return normalize("NFKD", frase).encode("ASCII", "ignore").decode("ASCII")


@lru_cache(maxsize=4096)
def carregar_punctuation_dict():
    """
    Usada para carregar pontuacoes
    :return:
    """
    return {key: " " for key in punctuation}


def normalizar(frase: str, sort: bool = True):
    """
    Remove acentos/acentuacao, ordena as palavras e limpa espaços extras
    :param frase: frase a ser normalizada
    :param sort: true se as palavras devem ser ordenadas
    :return:
    """
    if frase:
        # remover acentos
        frase = remover_acentos(frase.lower())
        # remover acentuacao
        frase = frase.translate(str.maketrans(carregar_punctuation_dict()))
        # ordenar palavras
        if sort:
            frase = "".join(sorted(frase.split()))
        # limpar espaços extras
        frase = frase.strip()
    return frase


def comparador(org: str, dest: str, return_value: bool = False, porcentagem: int = 0.95):
    """
    Compara duas strings (org e dest) usando os algoritmos de Jaro–Winkler e distância Levenshtein
    :param org: string ser comparada
    :param dest: outra string ser comparada
    :param return_value: indica se o valor calculado deve ser retornado para uso posterior
    :param porcentagem: porcentagem usada na comparacao com o valor calculado (caso o valor nao precise ser retornado)
    :return:
    """
    jws: float = 0.0
    lvd: float = 0.0
    calc: float = 0.0

    if org and dest:
        jws = jaro_winkler(org, dest)
        lvd = abs(1 - (levenshtein_distance(org, dest) / 100))
        calc = round(((jws * 0.9) + (lvd * 0.1)), 2)
    if return_value:
        return calc
    return calc > porcentagem


def comparar_e_obter_mais_semelhante(org: str, dests: list, porcentagem: int = 0.95, sort : bool = True):
    """
    Compara uma string (org) com uma lista de strings (dests), retornando a mais semelhante
    de acordo com a porcentagem informada (porcentagem)
    :param org: string ser comparada
    :param dests: lista de strings a ser comparada
    :param porcentagem: porcentagem minima de igualdade entre as strings a ser considerada
    :param sort: true se as palavras devem ser ordenadas
    :return:
    """
    nome_retorno = None
    old_calc = 0
    for idx, aut in enumerate(dests):
        calc = comparador(normalizar(org, sort), normalizar(aut, sort), True)
        if calc > porcentagem and calc > old_calc:
            old_calc = calc
            nome_retorno = aut

    return nome_retorno