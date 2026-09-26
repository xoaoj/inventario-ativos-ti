import csv
from pathlib import Path

from modelos import Ativo, Inventario, Severidade, StatusVulnerabilidade, TipoAtivo, Vulnerabilidade

PASTA_DADOS = Path("dados")
ARQ_ATIVOS = PASTA_DADOS / "ativos.txt"
ARQ_VULNS = PASTA_DADOS / "vulnerabilidades.txt"

CAMPOS_ATIVO = ["id", "nome", "responsavel", "setor", "tipo", "descricao"]
CAMPOS_VULN = ["ativo_id", "descricao", "categoria", "severidade", "status"]


def _abrir_escrita(caminho: Path):
    return open(caminho, "w", newline="", encoding="utf-8")


def salvar(inventario: Inventario) -> None:
    PASTA_DADOS.mkdir(exist_ok=True)

    with _abrir_escrita(ARQ_ATIVOS) as arq:
        escritor = csv.DictWriter(arq, fieldnames=CAMPOS_ATIVO, delimiter=";")
        escritor.writeheader()
        for ativo in inventario.ativos.values():
            escritor.writerow({
                "id": ativo.id,
                "nome": ativo.nome,
                "responsavel": ativo.responsavel,
                "setor": ativo.setor,
                "tipo": ativo.tipo.value,
                "descricao": ativo.descricao,
            })

    with _abrir_escrita(ARQ_VULNS) as arq:
        escritor = csv.DictWriter(arq, fieldnames=CAMPOS_VULN, delimiter=";")
        escritor.writeheader()
        for ativo in inventario.ativos.values():
            for vuln in ativo.vulnerabilidades:
                escritor.writerow({
                    "ativo_id": ativo.id,
                    "descricao": vuln.descricao,
                    "categoria": vuln.categoria,
                    "severidade": vuln.severidade.value,
                    "status": vuln.status.value,
                })


def carregar() -> Inventario:
    inventario = Inventario()

    if ARQ_ATIVOS.exists():
        with open(ARQ_ATIVOS, newline="", encoding="utf-8") as arq:
            for linha in csv.DictReader(arq, delimiter=";"):
                try:
                    ativo = Ativo(
                        id=int(linha["id"]),
                        nome=linha["nome"],
                        responsavel=linha["responsavel"],
                        setor=linha["setor"],
                        tipo=TipoAtivo.por_codigo(int(linha["tipo"])),
                        descricao=linha.get("descricao") or "",
                    )
                    inventario.adicionar(ativo)
                except (ValueError, KeyError) as erro:
                    print(f"  ✗ Linha ignorada em {ARQ_ATIVOS.name}: {linha} ({erro})")

    if ARQ_VULNS.exists():
        with open(ARQ_VULNS, newline="", encoding="utf-8") as arq:
            for linha in csv.DictReader(arq, delimiter=";"):
                try:
                    ativo = inventario.buscar_por_id(int(linha["ativo_id"]))
                except ValueError:
                    ativo = None
                if ativo is None:
                    print(f"  ✗ Vulnerabilidade sem ativo correspondente ignorada: {linha}")
                    continue
                try:
                    vuln = Vulnerabilidade(
                        descricao=linha["descricao"],
                        categoria=linha["categoria"],
                        severidade=Severidade(linha["severidade"]),
                        status=StatusVulnerabilidade(linha["status"]),
                    )
                    ativo.vulnerabilidades.append(vuln)
                except (ValueError, KeyError) as erro:
                    print(f"  ✗ Linha ignorada em {ARQ_VULNS.name}: {linha} ({erro})")

    return inventario