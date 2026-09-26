import sys

from acoes_ativo import atualizar_ativo, cadastrar_ativo, consultar_ativo, excluir_ativo
from acoes_vulnerabilidade import cadastrar_vulnerabilidade, ver_vulnerabilidades
from entrada import ler_int
from persistencia import carregar, salvar

LARGURA_MENU = 42

OPCOES = {
    1: "Cadastrar ativo",
    2: "Consultar ativo",
    3: "Atualizar ativo",
    4: "Excluir ativo",
    5: "Cadastrar vulnerabilidade",
    6: "Ver vulnerabilidades",
    0: "Sair",
}


def mostrar_menu() -> None:
    print("\n" + "═" * LARGURA_MENU)
    print("  INVENTÁRIO DE ATIVOS DE TI".center(LARGURA_MENU))
    print("═" * LARGURA_MENU)
    for codigo, texto in OPCOES.items():
        print(f"  [{codigo}] {texto}")
    print("─" * LARGURA_MENU)


ACOES = {
    1: cadastrar_ativo,
    2: consultar_ativo,
    3: atualizar_ativo,
    4: excluir_ativo,
    5: cadastrar_vulnerabilidade,
    6: ver_vulnerabilidades,
}


def main() -> None:
    inventario = carregar()
    print(f"→ {len(inventario.ativos)} ativo(s) carregado(s) da base.")
    while True:
        mostrar_menu()
        opcao = ler_int("Escolha uma opção", minimo=0, maximo=max(OPCOES))
        if opcao == 0:
            print("\n→ Até logo!")
            break
        acao = ACOES.get(opcao)
        if acao is None:
            print("  ✗ Opção inválida, tente novamente.")
            continue
        try:
            acao(inventario)
            salvar(inventario)
        except (ValueError, KeyError) as erro:
            print(f"  ✗ Erro: {erro}")


if __name__ == "__main__":
    # forca UTF-8 na saida: o terminal padrao do Windows (cp1252/850) nao
    # imprime os simbolos do menu (═ ─ → ✗ ✓) e derruba o programa sem isso.
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()