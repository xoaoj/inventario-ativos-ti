from acoes_ativo import buscar_ativo_interativo
from entrada import ler_vulnerabilidade
from modelos import Inventario


def cadastrar_vulnerabilidade(inventario: Inventario) -> None:
    print("\n▸ Cadastrar vulnerabilidade")
    ativo = buscar_ativo_interativo(inventario)
    if ativo is None:
        print("  ✗ Ativo não encontrado.")
        return

    vuln = ler_vulnerabilidade()
    ativo.vulnerabilidades.append(vuln)
    print(f"  ✓ Vulnerabilidade cadastrada no ativo '{ativo.nome}'.")


def ver_vulnerabilidades(inventario: Inventario) -> None:
    print("\n▸ Ver vulnerabilidades")
    ativo = buscar_ativo_interativo(inventario)
    if ativo is None:
        print("  ✗ Ativo não encontrado.")
        return

    if not ativo.vulnerabilidades:
        print(f"  ℹ O ativo '{ativo.nome}' está sem vulnerabilidades registradas.")
        return

    print(f"  Vulnerabilidades do ativo '{ativo.nome}':")
    for indice, vuln in enumerate(ativo.vulnerabilidades, start=1):
        print(f"    {indice}. {vuln.descricao}")
        print(f"       Categoria..: {vuln.categoria}")
        print(f"       Severidade.: {vuln.severidade.rotulo()}")
        print(f"       Status.....: {vuln.status.rotulo()}")