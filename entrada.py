from modelos import Severidade, StatusVulnerabilidade, TipoAtivo, Vulnerabilidade


def ler_nao_vazio(mensagem: str) -> str:
    while True:
        texto = input(f"  {mensagem}: ").strip()
        if texto:
            return texto
        print("  ✗ Esse campo não pode ficar em branco.")


def ler_opcional(mensagem: str, atual: str) -> str:
    texto = input(f"  {mensagem} [{atual or '—'}]: ").strip()
    return texto if texto else atual


def ler_int(mensagem: str, minimo: int | None = None, maximo: int | None = None) -> int:
    while True:
        texto = input(f"  {mensagem}: ").strip()
        try:
            valor = int(texto)
        except ValueError:
            print("  ✗ Digite um número inteiro válido.")
            continue
        if minimo is not None and valor < minimo or maximo is not None and valor > maximo:
            print(f"  ✗ Digite um número entre {minimo} e {maximo}.")
            continue
        return valor


def confirmar(mensagem: str) -> bool:
    resposta = input(f"  {mensagem} (s/n): ").strip().lower()
    return resposta == "s"


def ler_tipo_ativo() -> TipoAtivo:
    print("  Tipo de ativo:")
    for tipo in TipoAtivo:
        print(f"    [{tipo.value}] {tipo.rotulo()}")
    while True:
        codigo = ler_int("Código do tipo")
        try:
            return TipoAtivo.por_codigo(codigo)
        except ValueError:
            print("  ✗ Não existe tipo com esse código.")


def ler_severidade() -> Severidade:
    # severidade nao precisa de codigo inteiro proprio (isso e' exigido so
    # pra tipo de ativo, no R2); aqui a posicao na lista basta pra escolher.
    opcoes = list(Severidade)
    print("  Severidade:")
    for i, sev in enumerate(opcoes, start=1):
        print(f"    [{i}] {sev.rotulo()}")
    escolha = ler_int("Escolha", minimo=1, maximo=len(opcoes))
    return opcoes[escolha - 1]


def ler_status_vulnerabilidade() -> StatusVulnerabilidade:
    opcoes = list(StatusVulnerabilidade)
    print("  Status de tratamento:")
    for i, status in enumerate(opcoes, start=1):
        print(f"    [{i}] {status.rotulo()}")
    escolha = ler_int("Escolha", minimo=1, maximo=len(opcoes))
    return opcoes[escolha - 1]


def ler_vulnerabilidade() -> Vulnerabilidade:
    descricao = ler_nao_vazio("Descrição da vulnerabilidade")
    categoria = ler_nao_vazio("Categoria (ex.: falha de configuração, senha fraca)")
    severidade = ler_severidade()
    status = ler_status_vulnerabilidade()
    return Vulnerabilidade(descricao=descricao, categoria=categoria, severidade=severidade, status=status)