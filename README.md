# Projeto de Automação: Integração Excel e SharePoint

Este projeto consiste em uma solução de automação desenvolvida em **Python** que tem como objetivo modernizar e agilizar a atualização de planilhas de acompanhamento. A automação faz a leitura estruturada de arquivos de dados, atualiza as informações pertinentes em uma planilha local (Microsoft Excel) e realiza o upload automatizado para um repositório remoto no Microsoft SharePoint.

## 🎯 Objetivo da Automação

1. **Leitura de Dados**: Extrair informações sistêmicas provindas do arquivo `dados.json`.
2. **Manipulação Local**: Localizar os registros correspondentes na planilha `DEVs_Redmine_2026.xlsx` e atualizar suas respectivas células e status usando a biblioteca `openpyxl`.
3. **Sincronização na Nuvem**: Estabelecer comunicação segura com o Microsoft SharePoint e sobrescrever a versão antiga da planilha pela nova versão atualizada.
4. **Fallback Visual**: Integração com a ferramenta `pyautogui` para contornar possíveis cenários onde Políticas de Segurança corporativa (MFA - Multi-Factor Authentication) impeçam a comunicação via API de backend, permitindo uma automação orientada a interface gráfica (RPA).

---

## 🛠️ Tecnologias e Bibliotecas Utilizadas

- **[Python 3.x](https://www.python.org/)**: Linguagem principal da automação.
- **[openpyxl](https://openpyxl.readthedocs.io/)**: Leitura e gravação de arquivos nativos do Excel (`.xlsx`) de forma estruturada.
- **[Office365-REST-Python-Client](https://github.com/vgrem/Office365-REST-Python-Client)**: Biblioteca para integração via API (REST) com o ambiente SharePoint.
- **[PyAutoGUI](https://pyautogui.readthedocs.io/)**: Ferramenta de automação de Interface Gráfica do Usuário (GUI) e simulação de interações (mouse/teclado).
- **[python-dotenv](https://pypi.org/project/python-dotenv/)**: Gerenciamento seguro das variáveis de ambiente e credenciais.

---

## ⚙️ Pré-requisitos e Instalação

1. Certifique-se de que o **Python** está devidamente instalado em sua máquina.
2. Através do terminal, navegue até a raiz do projeto e instale as dependências executando o comando abaixo:

```bash
pip install -r requirements.txt
```

---

## 🔐 Configuração do Ambiente (Credenciais)

Para garantir a segurança das informações sensíveis de sua empresa, as credenciais não devem ser colocadas diretamente no código.

1. Na raiz do projeto, existe um arquivo chamado `.env` (caso não encontre, crie um baseando-se no modelo abaixo).
2. Preencha este arquivo com os parâmetros do ambiente corporativo:

```text
SHAREPOINT_SITE_URL=https://sua-empresa.sharepoint.com/sites/SeuSite
SHAREPOINT_USER=seu_email@empresa.com.br
SHAREPOINT_PASSWORD=sua_senha_aqui
SHAREPOINT_TARGET_FOLDER=Documentos Compartilhados/Caminho/Da/Sua/Pasta
BASE_FILE_XLSX=caminho e nome base arquivo .xlsx
```

> **Atenção:** Nunca realize o *commit* ou compartilhamento do arquivo `.env` para repositórios públicos (GitHub, GitLab, etc.). Mantenha-o exclusivamente na sua máquina local.

---

## 🚀 Como Executar

Após configurar o arquivo `.env` e garantir que os arquivos `DEVs_Redmine_2026.xlsx` e `dados.json` estejam na raiz do projeto (ou no caminho parametrizado), execute o script:

```bash
python main.py
```

### 📌 Notas de Desenvolvimento e Customizações (Solicitações de Ajuste)

Para que a automação se adapte com exatidão ao layout atual da planilha da sua equipe, favor observar e ajustar os seguintes itens no arquivo `main.py`:

- **Mapeamento de Colunas (Excel)**: Na função `update_excel()`, o código busca a correspondência do ID na *Coluna 1* e preenche os resultados nas *Colunas 2 e 3*. Ajuste esses índices (`column=1`, `column=2`, etc.) conforme o cabeçalho real do seu relatório `DEVs_Redmine_2026.xlsx`.
- **Modo de Upload (API vs. RPA)**: O script está pré-configurado para priorizar a robustez, executando o envio via **API (SharePoint REST)**. 
- **PyAutoGUI (Plano de Contingência)**: Caso sua credencial possua travamentos corporativos e a API seja bloqueada com erros de autenticação, você precisará editar a função `main()`. Comente a linha da API e ative a chamada de `upload_with_pyautogui()`. Note que você precisará extrair e configurar as coordenadas exatas da sua tela para garantir que o script saiba onde clicar no navegador.
