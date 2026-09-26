from acoes_ativo import buscar_ativo_interativo
from entrada import ler_vulnerabilidade
from modelos import Inventario


def cadastrar_vulnerabilidade(inventario: Inventario) -> None:
    print("\ncadastrar vulnerabilidade")
    ativo = buscar_ativo_interativo(inventario)
    if ativo is None:
        print("  ! ativo nao encontrado")
        return

    vuln = ler_vulnerabilidade()
    ativo.vulnerabilidades.append(vuln)
    print(f"  vulnerabilidade cadastrada no ativo '{ativo.nome}'.")


def ver_vulnerabilidades(inventario: Inventario) -> None:
    print("\nver vulnerabilidades")
    ativo = buscar_ativo_interativo(inventario)
    if ativo is None:
        print("  ! ativo nao encontrado")
        return

    if not ativo.vulnerabilidades:
        print(f"  o ativo '{ativo.nome}' esta sem vulnerabilidades registradas.")
        return

    print(f"  vulnerabilidades do ativo '{ativo.nome}':")
    for indice, vuln in enumerate(ativo.vulnerabilidades, start=1):
        print(f"    {indice}. {vuln.descricao}")
        print(f"       categoria..: {vuln.categoria}")
        print(f"       severidade.: {vuln.severidade.rotulo()}")
        print(f"       status.....: {vuln.status.rotulo()}")