from modelos import TipoAtivo


def ler_nao_vazio(mensagem: str) -> str:
    while True:
        texto = input(mensagem).strip()
        if texto:
            return texto
        print("n pode deixar vazio")


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