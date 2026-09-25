from acoes_ativo import buscar_ativo_interativo
from entrada import ler_nao_vazio, ler_severidade, ler_status_vulnerabilidade
from modelos import Inventario, Vulnerabilidade


def cadastrar_vulnerabilidade(inventario: Inventario) -> None:
    print("\ncadastrar vulnerabilidade")
    ativo = buscar_ativo_interativo(inventario)
    if ativo is None:
        print("  ! ativo nao encontrado")
        return

    descricao = ler_nao_vazio("  descricao da vulnerabilidade: ")
    categoria = ler_nao_vazio("  categoria (ex.: falha de configuracao, senha fraca): ")
    severidade = ler_severidade()
    status = ler_status_vulnerabilidade()

    vuln = Vulnerabilidade(descricao=descricao, categoria=categoria, severidade=severidade, status=status)
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