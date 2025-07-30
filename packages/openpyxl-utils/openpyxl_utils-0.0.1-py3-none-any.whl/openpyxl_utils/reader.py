from src.openpyxl_utils.utils import iniciar_planilha, descobrir_linha_vazia_planilha, is_merged, List


def pegar_dados_intervalo_planilha(conteudo, intervalo: str, ultima_linha: bool = False) -> List[list]:
    """
    Retorna os valores presentes no intervalo informado.
    Os valores são retornados dentro de uma lista.
    A lista retornada contém listas para cada linha do intervalo informado.
    Ex: [['Pessoa1', 46, 2500, 'Jogador', '987654321'], ['Pessoa2', 22, 8000, 'Streamer', '768948302']]
    :param conteudo: Arquivo da planilha excel, podendo ser um path ou o arquivo em bytes.
    :param intervalo: Intervalo da planilha.
    :param ultima_linha: Define se deverá ser pego até a ultima linha do intervalo informado.
    :return: Retorna uma lista contendo os valores.
    """
    if ultima_linha:
        intervalo: str = intervalo + descobrir_linha_vazia_planilha(conteudo, intervalo[0])

    planilha = iniciar_planilha(conteudo)
    aba_ativa = planilha.active

    try:
        valores: list = []
        valores_linha: list = []

        merged_ranges = aba_ativa.merged_cells.ranges  # -> Coleta todas as faixas de células mescladas na aba ativa da planilha.
        """
            merged_ranges = aba_ativa.merged_cells.ranges
            Explicação: 
                aba_ativa.merged_cells - Retorna um objeto que contém todas as faixas de células mescladas na planilha.
                ranges - Fornece uma lista de todas as faixas mescladas. Cada faixa é representada como um objeto CellRange.
        """

        # Adicionei os if's para impedir que dados vazios sejam obtidos.
        for celula in aba_ativa[intervalo]:
            contador_coluna_vazia: int = 0  # -> Contador de colunas vazias.
            for elemento in celula:
                if elemento.value is not None:
                    valores_linha.append(elemento.value)
                else:
                    if is_merged(elemento, merged_ranges):
                        pass
                    else:
                        if contador_coluna_vazia < 1:  # Permite até 1 coluna vazia.
                            contador_coluna_vazia += 1
                        else:
                            break  # -> Talvez eu possa tirar esse else e deixar ele pegar uma linha onde um elemento seja None.
            if len(valores_linha) > 0:
                valores.append(valores_linha.copy())
                valores_linha.clear()
            # else:
            # break  # -> Para a procura se achar algum registro vazio.
    except Exception as e:
        print(f"[ERRO] pegar_dados_intervalo_planilha: {e}")
        return []
    else:
        planilha.close()
        return valores
