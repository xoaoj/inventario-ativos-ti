from dataclasses import dataclass, field
from enum import Enum


class TipoAtivo(Enum):
    NOTEBOOK = 1
    SERVIDOR = 2
    ROTEADOR = 3
    SOFTWARE_LICENCIADO = 4
    APLICACAO_WEB = 5
    BANCO_DE_DADOS = 6

    @classmethod
    def por_codigo(cls, codigo: int) -> "TipoAtivo":
        return cls(codigo)

    def rotulo(self) -> str:
        return self.name.replace("_", " ").capitalize()


class Severidade(Enum):
    BAIXA = "baixa"
    MEDIA = "media"
    ALTA = "alta"
    CRITICA = "critica"

    def rotulo(self) -> str:
        return self.name.capitalize()


class StatusVulnerabilidade(Enum):
    ABERTA = "aberta"
    EM_TRATAMENTO = "em tratamento"
    CORRIGIDA = "corrigida"
    ACEITA_COMO_RISCO = "aceita como risco"

    def rotulo(self) -> str:
        return self.value.capitalize()


@dataclass
class Vulnerabilidade:
    descricao: str
    categoria: str
    severidade: Severidade
    status: StatusVulnerabilidade


@dataclass
class Ativo:
    id: int
    nome: str
    responsavel: str
    setor: str
    tipo: TipoAtivo
    descricao: str = ""
    vulnerabilidades: list[Vulnerabilidade] = field(default_factory=list)


class Inventario:

    def __init__(self):
        self.ativos: dict[int, Ativo] = {}
        self.por_nome: dict[str, int] = {}  # nome/hostname -> id

    def adicionar(self, ativo: Ativo) -> None:
        if ativo.id in self.ativos:
            raise ValueError(f"Já existe um ativo com ID {ativo.id}.")
        self.ativos[ativo.id] = ativo
        self.por_nome[ativo.nome.lower()] = ativo.id

    def buscar_por_id(self, id_: int) -> Ativo | None:
        return self.ativos.get(id_)

    def buscar_por_nome(self, nome: str) -> Ativo | None:
        id_ = self.por_nome.get(nome.lower())
        return self.ativos.get(id_) if id_ is not None else None

    def remover(self, id_: int) -> Ativo | None:
        ativo = self.ativos.pop(id_, None)
        if ativo:
            self.por_nome.pop(ativo.nome.lower(), None)
        return ativo