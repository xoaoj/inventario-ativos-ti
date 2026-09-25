from modelos import Severidade, StatusVulnerabilidade, TipoAtivo


def ler_nao_vazio(mensagem: str) -> str:
    while True:
        texto = input(mensagem).strip()
        if texto:
            return texto
        print("n pode deixar vazio")


def ler_opcional(mensagem: str, atual: str) -> str:
    texto = input(mensagem).strip()
    return texto if texto else atual


def ler_int(mensagem: str, minimo: int | None = None, maximo: int | None = None) -> int:
    while True:
        texto = input(mensagem).strip()
        try:
            valor = int(texto)
        except ValueError:
            print("digite um numero inteiro")
            continue
        if minimo is not None and valor < minimo or maximo is not None and valor > maximo:
            print(f"digite um numero entre {minimo} e {maximo}.")
            continue
        return valor


def ler_tipo_ativo() -> TipoAtivo:
    print("tipo de ativo")
    for tipo in TipoAtivo:
        print(f"    {tipo.value} - {tipo.rotulo()}")
    while True:
        codigo = ler_int("cod do ativo")
        try:
            return TipoAtivo.por_codigo(codigo)
        except ValueError:
            print("cod de tipo nao existe")


def ler_severidade() -> Severidade:
    # severidade nao precisa de codigo inteiro proprio (isso e' exigido so
    # pra tipo de ativo, no R2); aqui a posicao na lista basta pra escolher.
    opcoes = list(Severidade)
    print("  severidade")
    for i, sev in enumerate(opcoes, start=1):
        print(f"    {i} - {sev.rotulo()}")
    escolha = ler_int("  escolha: ", minimo=1, maximo=len(opcoes))
    return opcoes[escolha - 1]


def ler_status_vulnerabilidade() -> StatusVulnerabilidade:
    opcoes = list(StatusVulnerabilidade)
    print("  status de tratamento")
    for i, status in enumerate(opcoes, start=1):
        print(f"    {i} - {status.rotulo()}")
    escolha = ler_int("  escolha: ", minimo=1, maximo=len(opcoes))
    return opcoes[escolha - 1]