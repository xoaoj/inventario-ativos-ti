# Inventário de Ativos de TI e Vulnerabilidades

Sistema em Python, via terminal, para cadastrar, consultar, atualizar e excluir ativos de TI
e suas vulnerabilidades, com persistência em arquivos de texto (CSV). Trabalho individual da
disciplina de Cibersegurança (UFU, 2026/2 — Sprints 1 e 2).

## Como clonar e rodar

Pré-requisito: Python 3.10+ (usa `list[Vulnerabilidade]`, `int | None` e `match` de enums da
biblioteca padrão — sem dependências externas).

```bash
git clone https://github.com/xoaoj/inventario-ativos-ti.git
cd inventario-ativos-ti
python inventario.py
```

Não há `requirements.txt` porque o projeto usa só a biblioteca padrão (`csv`, `pathlib`,
`dataclasses`, `enum`).

Ao rodar, o programa cria uma pasta `dados/` (ignorada pelo git) com dois arquivos-texto que
funcionam como base de dados:

- `dados/ativos.txt` — um ativo por linha, campos separados por `;`.
- `dados/vulnerabilidades.txt` — uma vulnerabilidade por linha, referenciando o `ativo_id`.

Eles são recriados a cada `salvar()` (depois de cada ação bem-sucedida no menu) e recarregados
automaticamente na próxima execução.

## Menu

```
1 - cadastrar            cadastra um ativo (com opção de já cadastrar vulnerabilidades iniciais)
2 - consultar             busca por id ou nome/hostname
3 - atualizar             responsável, setor, tipo, descrição
4 - excluir                remove o ativo e suas vulnerabilidades
5 - cadastrar vulnerabilidade   adiciona vulnerabilidade a um ativo já existente
6 - ver vulnerabilidades   lista as vulnerabilidades de um ativo
0 - sair
```

## Estrutura do código

| Arquivo | Responsabilidade |
|---|---|
| `modelos.py` | Enums (`TipoAtivo`, `Severidade`, `StatusVulnerabilidade`), dataclasses (`Ativo`, `Vulnerabilidade`) e a classe `Inventario` (armazenamento em memória + índices). |
| `entrada.py` | Funções de leitura de input com validação (`ler_int`, `ler_nao_vazio`, `ler_tipo_ativo`, `ler_vulnerabilidade`, etc.). Concentra toda a interação com o terminal que envolve validação/retry. |
| `acoes_ativo.py` | Casos de uso de ativo: cadastrar, consultar, atualizar, excluir, e a busca interativa reutilizada pelos outros módulos. |
| `acoes_vulnerabilidade.py` | Casos de uso de vulnerabilidade: cadastrar avulsa, listar. |
| `persistencia.py` | Leitura/escrita dos arquivos CSV em `dados/`. |
| `inventario.py` | Ponto de entrada: monta o menu, despacha para as ações e trata erros de domínio (`ValueError`, `KeyError`) sem derrubar o programa. |

## Requisitos da avaliação e onde cada um foi atendido

Baseado em `Avaliacao_Sprints_1_e_2_versao_2_0_2026_2` (Tabela 1).

1. **Menu textual com tratamento de erros (10%)** — `inventario.py` mostra o menu e despacha por
   dicionário (`ACOES`); opção inexistente é tratada sem crashar. `entrada.ler_int` rejeita texto
   não-numérico e valores fora do intervalo; `entrada.ler_nao_vazio` rejeita campos vazios.
2. **Enum de tipos de ativo com código inteiro (10%)** — `modelos.TipoAtivo`, 6 categorias
   (notebook, servidor, roteador, software licenciado, aplicação web, banco de dados), cada uma
   com um `int` (`.value`) como código.
3. **Cadastro completo + lista inicial de vulnerabilidades (10%)** — `acoes_ativo.cadastrar_ativo`
   pede id, nome/hostname, responsável, setor/localização, tipo e, opcionalmente, uma lista de
   vulnerabilidades iniciais (loop de "cadastrar outra?"), tudo gravado em `dados/*.txt` via
   `persistencia.salvar`.
4. **Busca por id ou nome (10%)** — `acoes_ativo.buscar_ativo_interativo` + `imprimir_ativo`,
   reaproveitado por consulta, atualização, exclusão e ações de vulnerabilidade.
5. **Atualização (10%)** — `acoes_ativo.atualizar_ativo` permite trocar responsável, setor,
   descrição e tipo, mantendo o valor atual se o campo for deixado em branco.
6. **Exclusão remove vulnerabilidades associadas (10%)** — `acoes_ativo.excluir_ativo` remove o
   ativo de `Inventario.ativos`; como as vulnerabilidades vivem dentro do próprio `Ativo`, elas
   somem junto na próxima gravação (não sobra registro órfão em `vulnerabilidades.txt`).
7. **Cadastro de vulnerabilidade a qualquer momento (10%)** — opção 5 do menu
   (`acoes_vulnerabilidade.cadastrar_vulnerabilidade`), com descrição, categoria, severidade
   (baixa/média/alta/crítica) e status (aberta/em tratamento/corrigida/aceita como risco), via
   `entrada.ler_vulnerabilidade` — a mesma função usada no cadastro inicial do ativo (requisito 3),
   evitando duplicar a lógica de leitura.
8. **Visualização de vulnerabilidades (5%)** — opção 6, `acoes_vulnerabilidade.ver_vulnerabilidades`,
   com mensagem específica quando o ativo não tem nenhuma.
9. **Uso de dicionário para otimizar busca (10%)** — `Inventario` mantém dois `dict`:
   `ativos: dict[int, Ativo]` (busca por id em O(1)) e `por_nome: dict[str, int]` (índice
   hostname → id, também O(1)).
10. **Repositório com mais de 2 branches e merge (15%)** — histórico do repositório tem 3 branches
    de feature (`feature/gravacao`, `feature/crud-ativos`, `feature/vulnerabilidades`) e uma branch
    `refactor/clean-code-r3`, cada uma integrada em `main` via merge/PR.

## Decisões de design

- **CSV com `;` como separador** em vez de um formato próprio: usa `csv.DictWriter`/`DictReader`
  da biblioteca padrão, evita bugs de parsing manual e ainda é "arquivo de texto" como pede o
  enunciado.
- **Vulnerabilidade não tem id próprio**: ela só existe associada a um ativo (`ativo.vulnerabilidades`)
  e é persistida via `ativo_id` em `vulnerabilidades.txt` — não há caso de uso que peça buscar uma
  vulnerabilidade isoladamente.
- **`por_nome` guarda o nome em minúsculo**: busca por hostname fica case-insensitive sem precisar
  normalizar em cada chamada.
- **Erros de domínio (`ValueError`, `KeyError`) são capturados em `inventario.py`**, não dentro de
  cada ação — assim cada função de ação fica livre de try/except repetido e o loop principal nunca
  cai por uma exceção esperada (id duplicado, tipo inválido, etc.).
