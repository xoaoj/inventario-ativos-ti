from acoes_ativo import atualizar_ativo, cadastrar_ativo, consultar_ativo, excluir_ativo
from acoes_vulnerabilidade import cadastrar_vulnerabilidade, ver_vulnerabilidades
from entrada import ler_int
from persistencia import carregar, salvar

OPCOES = {
    1: "cadastrar",
    2: "consultar",
    3: "atualizar",
    4: "excluir",
    5: "cadastrar vulnerabilidade",
    6: "ver vulnerabilidades",
    0: "sair",
}


def mostrar_menu() -> None:
    print("\ninventario")
    for codigo, texto in OPCOES.items():
        print(f"  {codigo} - {texto}")


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
    print(f"{len(inventario.ativos)} ativo(s) carregado(s) da base.")
    while True:
        mostrar_menu()
        opcao = ler_int("escolha a opção: ", minimo=0, maximo=max(OPCOES))
        if opcao == 0:
            print("vc escolheu sair! encerrando...")
            break
        acao = ACOES.get(opcao)
        if acao is None:
            print("! n tem essa opção")
            continue
        try:
            acao(inventario)
            salvar(inventario)
        except (ValueError, KeyError) as erro:
            print(f"  ! Erro: {erro}")


if __name__ == "__main__":
    main()