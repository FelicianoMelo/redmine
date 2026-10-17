# Projeto de Automação: Redmine, Gestão de Feriados e Integração Excel/SharePoint

Este repositório contém uma solução completa de automação desenvolvida em **Python** voltada para a gestão de apontamentos de horas no **Redmine**, validação automática de calendário (feriados nacionais, estaduais, municipais e períodos de férias), geração e conversão de bases de dados e sincronização automatizada com planilhas locais (Microsoft Excel) e repositórios em nuvem no **Microsoft SharePoint**.

---

## 🎯 Visão Geral e Funcionalidades

O projeto é estruturado em módulos independentes e integrados que atendem às seguintes etapas do fluxo de trabalho:

1. **Geração Automatizada de Apontamentos (`criar_lancamentos_redmine.py`)**:
   - Projeta uma sequência de dias úteis a partir dos parâmetros configurados no `.env`.
   - Ignora automaticamente finais de semana (sábados e domingos).
   - Valida intervalos de férias programadas (`PARM_INICIO_FERIAS` e `PARM_FIM_FERIAS`), atribuindo o status `Day-Off` e tarefa correspondente.
   - Detecta automaticamente feriados (Nacionais, Estaduais e Municipais) de acordo com a localidade configurada (`UF` e `Cidade`), atribuindo o apontamento como feriado / `Day-Off`.
   - Gera o arquivo consolidado `dados.json` pronto para processamento.

2. **Motor de Feriados no Brasil (`FeriadoBrasil.py`)**:
   - Classe especializada na verificação de datas festivas e feriados oficiais em três esferas:
     - **Nacional**: Consulta à base `Feriados-NACIONAL.json`.
     - **Estadual**: Consulta à base `Feriados-ESTADUAL.json` filtrando pela UF.
     - **Municipal**: Consulta à base `Feriados-MUNICIPAL.json` filtrando por UF e Município.
   - Fornece o comentário descritivo do feriado e parametriza a tarefa e atividade correspondentes.

3. **Mesclagem de Apontamentos Customizados do Usuário (`mesclar_arquivo_usuario_redmine.py`)**:
   - Lê os lançamentos pontuais e customizados do usuário a partir de `login_usuario.json` (ou `<login>.json`, ex: `fajunior1.json`).
   - Valida e normaliza as datas, inserindo-as no intervalo cronológico exato em `dados.json`.
   - Preenche automaticamente campos faltantes (como `Usuário`, `Gestor`, etc.) com base no histórico de `dados.json` ou nas variáveis do `.env`.
   - Substitui ou complementa as tarefas dos respectivos dias mantendo a lista ordenada por data.

4. **Conversão de Bases de Feriados (`converter_json_xlsx_*.py`)**:
   - Scripts utilitários que utilizam a biblioteca **Pandas** e **openpyxl** para converter os catálogos de feriados em JSON para planilhas formatadas em Excel (`.xlsx`):
     - `converter_json_xlsx_NACIONAL.py` ➔ `Feriados_NACIONAL.xlsx`
     - `converter_json_xlsx_ESTADUAL.py` ➔ `Feriados_ESTADUAL.xlsx`
     - `converter_json_xlsx_MUNICIPAL.py` ➔ `Feriados_MUNICIPAL.xlsx`

5. **Atualização da Planilha Local e Sincronização em Nuvem (`main.py`)**:
   - **Manipulação Local**: Lê as entradas de dados e atualiza a planilha de controle (`DEVs_Redmine_2026.xlsx`) utilizando `openpyxl`.
   - **Sincronização SharePoint (API REST)**: Conecta-se de forma segura ao Microsoft SharePoint via biblioteca `Office365-REST-Python-Client` e sobrescreve a versão em nuvem com a versão atualizada.
   - **RPA / Fallback Visual (`pyautogui`)**: Mecanismo alternativo de automação via interface gráfica para superar restrições de MFA (Multi-Factor Authentication) ou bloqueios de rede corporativos.

---

## 🛠️ Tecnologias, Pacotes e Bibliotecas

Abaixo estão listadas as bibliotecas e ferramentas utilizadas no projeto:

### Bibliotecas de Terceiros

| Pacote | Versão Mínima / Instalada | Finalidade |
| :--- | :--- | :--- |
| **[pandas](https://pandas.pydata.org/)** | `>=2.3.3` | Manipulação e transformação de dados tabulares; conversão de grandes bases JSON de feriados para formato Excel (`.xlsx`). |
| **[openpyxl](https://openpyxl.readthedocs.io/)** | `>=3.1.5` | Leitura, edição e gravação direta em planilhas Microsoft Excel (`.xlsx`), servindo também como engine de gravação para o Pandas. |
| **[python-dotenv](https://pypi.org/project/python-dotenv/)** | `>=1.2.1` | Gerenciamento seguro de variáveis de ambiente e configurações sensíveis através do arquivo `.env`. |
| **[Office365-REST-Python-Client](https://github.com/vgrem/Office365-REST-Python-Client)** | `>=3.2.0` | Autenticação e integração via API REST com o ecossistema Microsoft SharePoint para upload automático de arquivos. |
| **[PyAutoGUI](https://pyautogui.readthedocs.io/)** | `>=0.9.54` | Automação de Interface Gráfica (RPA) para simulação de cliques e digitação no navegador em caso de contingência. |

### Gerenciamento de Dependências e Build

- **[uv](https://docs.astral.sh/uv/)**: Gerenciador moderno, extremamente rápido de pacotes e ambientes virtuais Python, integrado via `pyproject.toml` e `uv.lock`.
- **pip / requirements.txt**: Suporte mantido para instalação padrão no ecossistema Python tradicional.

### Módulos Nativos do Python (Built-in)

- **`datetime` (`date`, `datetime`, `timedelta`)**: Operações com calendários, cálculo de intervalos de datas, dias úteis (`weekday`) e formatação (`strftime`, `strptime`).
- **`json`**: Serialização e desserialização de arquivos e estruturas de dados de apontamentos e feriados.
- **`os`**: Manipulação de caminhos de arquivos e leitura de variáveis de ambiente do sistema operacional.
- **`time`**: Controle de intervalos e pausas durante rotinas de execução automatizada.

---

## 📁 Estrutura de Arquivos do Projeto

```text
redmine/
├── .env.exemplo                     # Modelo de variáveis de ambiente e parâmetros
├── .gitignore                       # Regras de exclusão do controle de versão
├── pyproject.toml                   # Configuração do projeto e dependências (uv/PEP 621)
├── uv.lock                          # Travamento exato de versões gerenciado pelo uv
├── requirements.txt                 # Dependências do projeto para instalação via pip
├── README.md                        # Documentação completa do projeto
│
├── FeriadoBrasil.py                 # Módulo de consulta e classificação de feriados
├── Feriados-NACIONAL.json           # Base de dados de feriados nacionais
├── Feriados-ESTADUAL.json           # Base de dados de feriados estaduais
├── Feriados-MUNICIPAL.json          # Base de dados de feriados municipais
│
├── converter_json_xlsx_NACIONAL.py  # Conversor JSON -> XLSX de feriados nacionais
├── converter_json_xlsx_ESTADUAL.py  # Conversor JSON -> XLSX de feriados estaduais
├── converter_json_xlsx_MUNICIPAL.py # Conversor JSON -> XLSX de feriados municipais
│
├── criar_lancamentos_redmine.py     # Gerador de apontamentos diários do Redmine
├── dados.json                       # Arquivo gerado com a lista de tarefas/apontamentos
├── mesclar_arquivo_usuario_redmine.py # Mesclador de lançamentos customizados do usuário no dados.json
├── login_usuario.json               # Apontamentos específicos do usuário (customizados)
├── fajunior1.json                   # Exemplo de arquivo de apontamentos do usuário
│
├── main.py                          # Atualização do Excel local e upload para o SharePoint
└── DEVs_Redmine_2026.xlsx           # Planilha de controle local de acompanhamento
```

---

## ⚙️ Pré-requisitos e Instalação

Certifique-se de possuir o **Python 3.9+** (ou superior) instalado.

Você pode instalar as dependências de duas formas:

### Opção 1: Usando `uv` (Recomendado)

O projeto inclui arquivos de configuração do `uv` (`pyproject.toml` e `uv.lock`):

```bash
# Sincroniza o ambiente e instala as dependências
uv sync
```

### Opção 2: Usando `pip`

Você também pode utilizar o gerenciador padrão do Python com o ambiente virtual ativo:

```bash
# Cria e ativa o ambiente virtual (opcional se já possuir um)
python3 -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# Instala as dependências listadas no requirements.txt
pip install -r requirements.txt
```

---

## 🔐 Configuração do Arquivo `.env`

Crie uma cópia do arquivo `.env.exemplo` nomeando-a como `.env` na raiz do projeto:

```bash
cp .env.exemplo .env
```

Preencha os parâmetros conforme o seu contexto de trabalho:

### 1. Parâmetros do Redmine e Apontamento Diário

```env
# Credenciais e Identificação do Usuário
PARM_LOGIN=seu_login
PARM_SENHA=sua_senha
PARM_USUARIO=Seu Nome Completo
PARM_GESTOR=Nome do Gestor Responsável

# Localidade para Validação de Feriados
PARM_UF=SP
PARM_CIDADE=Sao Paulo

# Configuração Padrão do Apontamento
PARM_PROJETO=TMS
PARM_TAREFA=35053 - Sustentação - Hora trabalhada
PARM_ATIVIDADE=Tarefa
PARM_HORAS=8

# Faixa de Projeção de Datas
PARM_DATA=NONE               # Use NONE para iniciar a partir de hoje ou YYYY/MM/DD
PARM_FAIXA_DIAS=30           # Quantidade de dias para gerar os apontamentos

# Período de Férias Programadas (apontado automaticamente como Day-Off)
PARM_INICIO_FERIAS=2026-05-11
PARM_FIM_FERIAS=2026-06-09
```

### 2. Parâmetros de Integração SharePoint (se aplicável)

Caso utilize a rotina de sincronização em nuvem presente no `main.py`:

```env
SHAREPOINT_SITE_URL=https://sua-empresa.sharepoint.com/sites/SeuSite
SHAREPOINT_USER=seu_email@empresa.com.br
SHAREPOINT_PASSWORD=sua_senha_aqui
SHAREPOINT_TARGET_FOLDER=Documentos Compartilhados/Caminho/Da/Sua/Pasta
BASE_FILE_XLSX=DEVs_Redmine_2026.xlsx
```

> ⚠️ **Atenção:** O arquivo `.env` contém credenciais e dados pessoais. Ele está incluído no `.gitignore` e **nunca** deve ser commitado para repositórios remotos.

---

## 🚀 Como Executar

### 1. Gerar os Lançamentos do Redmine (`dados.json`)

Para calcular os dias úteis, detectar feriados e férias programadas e gerar o arquivo base `dados.json`:

```bash
python criar_lancamentos_redmine.py
```
*(Ou com uv: `uv run python criar_lancamentos_redmine.py`)*

### 2. Mesclar Apontamentos Customizados do Usuário (Opcional / Conforme Demanda)

Para mesclar apontamentos pontuais e customizados do usuário (`login_usuario.json` ou `fajunior1.json`) preenchendo dados ausentes e ordenando no intervalo correto de `dados.json`:

```bash
# Executa procurando login_usuario.json ou <login>.json automaticamente:
python mesclar_arquivo_usuario_redmine.py

# Ou informando um arquivo específico:
python mesclar_arquivo_usuario_redmine.py fajunior1.json
```
*(Ou com uv: `uv run python mesclar_arquivo_usuario_redmine.py`)*

### 3. Atualizar a Planilha e Sincronizar com o SharePoint

Para ler o `dados.json` consolidado, atualizar a planilha `DEVs_Redmine_2026.xlsx` e enviar para o SharePoint:

```bash
python main.py
```
*(Ou com uv: `uv run python main.py`)*

### 4. Converter Bases de Feriados para Excel (Opcional)

Se desejar exportar as bases de feriados de JSON para arquivos `.xlsx`:

```bash
python converter_json_xlsx_NACIONAL.py
python converter_json_xlsx_ESTADUAL.py
python converter_json_xlsx_MUNICIPAL.py
```

---

## 📌 Notas de Desenvolvimento e Customizações

- **Mapeamento de Colunas (Excel)**: No arquivo `main.py`, dentro da função `update_excel()`, o código localiza a linha pelo ID e atualiza as colunas de status e observações. Ajuste os índices (`column=1`, `column=2`, etc.) conforme o cabeçalho real da sua planilha corporativa.
- **Modo de Upload (API vs. RPA)**: Por padrão, o envio é realizado via API REST do SharePoint. Caso a autenticação seja barrada por políticas de MFA corporativas sem App Password, habilite a função `upload_with_pyautogui()` comentando a chamada da API no `main.py`.
- **Bases de Feriados**: As bases JSON (`Feriados-NACIONAL.json`, `Feriados-ESTADUAL.json`, `Feriados-MUNICIPAL.json`) contêm a relação de datas com codificações e registros históricos/futuros para identificação precisa.
