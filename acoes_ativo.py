from entrada import ler_int, ler_nao_vazio, ler_opcional, ler_tipo_ativo
from modelos import Ativo, Inventario


def cadastrar_ativo(inventario: Inventario) -> None:
    print("\ncadastrar ativo")
    id_ = ler_int("id do ativo: ")
    nome = ler_nao_vazio("nome/hostname: ")
    responsavel = ler_nao_vazio("responsavel: ")
    setor = ler_nao_vazio("setor/localizacao: ")
    tipo = ler_tipo_ativo()
    descricao = input("descricao (opcional): ").strip()

    ativo = Ativo(
        id=id_,
        nome=nome,
        responsavel=responsavel,
        setor=setor,
        tipo=tipo,
        descricao=descricao,
    )
    inventario.adicionar(ativo)  # lanca ValueError se o id ja existir
    print(f"  ativo '{nome}' cadastrado com id {id_}.")


def buscar_ativo_interativo(inventario: Inventario) -> Ativo | None:
    print("  buscar por:")
    print("    1 - id")
    print("    2 - nome/hostname")
    opcao = ler_int("  opcao: ", minimo=1, maximo=2)
    if opcao == 1:
        id_ = ler_int("  id: ")
        return inventario.buscar_por_id(id_)
    nome = ler_nao_vazio("  nome/hostname: ")
    return inventario.buscar_por_nome(nome)


def imprimir_ativo(ativo: Ativo) -> None:
    print(f"  id..........: {ativo.id}")
    print(f"  nome........: {ativo.nome}")
    print(f"  responsavel.: {ativo.responsavel}")
    print(f"  setor.......: {ativo.setor}")
    print(f"  tipo........: {ativo.tipo.rotulo()}")
    if ativo.descricao:
        print(f"  descricao...: {ativo.descricao}")


def consultar_ativo(inventario: Inventario) -> None:
    print("\nconsultar ativo")
    ativo = buscar_ativo_interativo(inventario)
    if ativo is None:
        print("  ! ativo nao encontrado")
        return
    imprimir_ativo(ativo)


def atualizar_ativo(inventario: Inventario) -> None:
    print("\natualizar ativo")
    ativo = buscar_ativo_interativo(inventario)
    if ativo is None:
        print("  ! ativo nao encontrado")
        return

    # o nome nao entra aqui de proposito: ele e a chave do indice por_nome
    # em Inventario, e o requisito de atualizacao (R5) nao pede pra mudar o
    # nome/hostname, so responsavel, setor, tipo ou descricao.
    print("  deixe em branco pra manter o valor atual")
    ativo.responsavel = ler_opcional(f"  responsavel [{ativo.responsavel}]: ", ativo.responsavel)
    ativo.setor = ler_opcional(f"  setor [{ativo.setor}]: ", ativo.setor)
    ativo.descricao = ler_opcional(f"  descricao [{ativo.descricao}]: ", ativo.descricao)

    trocar_tipo = input(f"  trocar tipo (atual: {ativo.tipo.rotulo()})? (s/n): ").strip().lower()
    if trocar_tipo == "s":
        ativo.tipo = ler_tipo_ativo()

    print("  ativo atualizado.")


def excluir_ativo(inventario: Inventario) -> None:
    print("\nexcluir ativo")
    id_ = ler_int("  id do ativo a excluir: ")
    ativo = inventario.remover(id_)
    if ativo is None:
        print("  ! ativo nao encontrado")
        return
    qtd_vulns = len(ativo.vulnerabilidades)
    print(f"  ativo '{ativo.nome}' removido (junto com {qtd_vulns} vulnerabilidade(s)).")