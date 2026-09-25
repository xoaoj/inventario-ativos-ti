from entrada import ler_int
from modelos import Inventario

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


def em_desenvolvimento(_inventario: Inventario) -> None:
    print("  (WIP - ainda to fazendo)")

ACOES = {codigo: em_desenvolvimento for codigo in OPCOES if codigo != 0}

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
        except (ValueError, KeyError) as erro:
            print(f"  ! Erro: {erro}")


if __name__ == "__main__":
    main()