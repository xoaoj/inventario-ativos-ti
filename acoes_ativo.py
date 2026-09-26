from entrada import confirmar, ler_int, ler_nao_vazio, ler_opcional, ler_tipo_ativo, ler_vulnerabilidade
from modelos import Ativo, Inventario, Vulnerabilidade


def _ler_vulnerabilidades_iniciais() -> list[Vulnerabilidade]:
    """Pergunta se o usuario quer cadastrar vulnerabilidades ja no cadastro do
    ativo (R3), repetindo ate ele dizer que nao quer mais adicionar."""
    vulnerabilidades: list[Vulnerabilidade] = []
    if not confirmar("Cadastrar vulnerabilidades iniciais agora?"):
        return vulnerabilidades

    while True:
        vulnerabilidades.append(ler_vulnerabilidade())
        if not confirmar("  Cadastrar outra vulnerabilidade?"):
            break
    return vulnerabilidades


def cadastrar_ativo(inventario: Inventario) -> None:
    print("\n▸ Cadastrar ativo")
    id_ = ler_int("Id do ativo")
    nome = ler_nao_vazio("Nome/hostname")
    responsavel = ler_nao_vazio("Responsável")
    setor = ler_nao_vazio("Setor/localização")
    tipo = ler_tipo_ativo()
    descricao = ler_opcional("Descrição (opcional)", "")
    vulnerabilidades = _ler_vulnerabilidades_iniciais()

    ativo = Ativo(
        id=id_,
        nome=nome,
        responsavel=responsavel,
        setor=setor,
        tipo=tipo,
        descricao=descricao,
        vulnerabilidades=vulnerabilidades,
    )
    inventario.adicionar(ativo)  # lanca ValueError se o id ja existir
    print(f"  ✓ Ativo '{nome}' cadastrado (id {id_}, {len(vulnerabilidades)} vulnerabilidade(s) inicial(is)).")


def buscar_ativo_interativo(inventario: Inventario) -> Ativo | None:
    print("  Buscar por:")
    print("    [1] Id")
    print("    [2] Nome/hostname")
    opcao = ler_int("Opção", minimo=1, maximo=2)
    if opcao == 1:
        id_ = ler_int("Id")
        return inventario.buscar_por_id(id_)
    nome = ler_nao_vazio("Nome/hostname")
    return inventario.buscar_por_nome(nome)


def imprimir_ativo(ativo: Ativo) -> None:
    print(f"    Id..........: {ativo.id}")
    print(f"    Nome........: {ativo.nome}")
    print(f"    Responsável.: {ativo.responsavel}")
    print(f"    Setor.......: {ativo.setor}")
    print(f"    Tipo........: {ativo.tipo.rotulo()}")
    if ativo.descricao:
        print(f"    Descrição...: {ativo.descricao}")


def consultar_ativo(inventario: Inventario) -> None:
    print("\n▸ Consultar ativo")
    ativo = buscar_ativo_interativo(inventario)
    if ativo is None:
        print("  ✗ Ativo não encontrado.")
        return
    imprimir_ativo(ativo)


def atualizar_ativo(inventario: Inventario) -> None:
    print("\n▸ Atualizar ativo")
    ativo = buscar_ativo_interativo(inventario)
    if ativo is None:
        print("  ✗ Ativo não encontrado.")
        return

    # o nome nao entra aqui de proposito: ele e a chave do indice por_nome
    # em Inventario, e o requisito de atualizacao (R5) nao pede pra mudar o
    # nome/hostname, so responsavel, setor, tipo ou descricao.
    print("  ℹ Deixe em branco para manter o valor atual.")
    ativo.responsavel = ler_opcional("Responsável", ativo.responsavel)
    ativo.setor = ler_opcional("Setor", ativo.setor)
    ativo.descricao = ler_opcional("Descrição", ativo.descricao)

    if confirmar(f"  Trocar tipo (atual: {ativo.tipo.rotulo()})?"):
        ativo.tipo = ler_tipo_ativo()

    print("  ✓ Ativo atualizado.")


def excluir_ativo(inventario: Inventario) -> None:
    print("\n▸ Excluir ativo")
    id_ = ler_int("Id do ativo a excluir")
    ativo = inventario.remover(id_)
    if ativo is None:
        print("  ✗ Ativo não encontrado.")
        return
    qtd_vulns = len(ativo.vulnerabilidades)
    print(f"  ✓ Ativo '{ativo.nome}' removido (junto com {qtd_vulns} vulnerabilidade(s)).")