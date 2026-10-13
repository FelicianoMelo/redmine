import json
import os
import pyautogui
from openpyxl import load_workbook
from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.user_credential import UserCredential
from dotenv import load_dotenv
import time

# Carregar variáveis de ambiente
load_dotenv()

# Configurações do SharePoint
SHAREPOINT_SITE_URL = os.getenv('SHAREPOINT_SITE_URL')
SHAREPOINT_USER = os.getenv('SHAREPOINT_USER')
SHAREPOINT_PASSWORD = os.getenv('SHAREPOINT_PASSWORD')
SHAREPOINT_TARGET_FOLDER = os.getenv('SHAREPOINT_TARGET_FOLDER', 'Shared Documents')

# Caminhos dos arquivos
BASE_DIR = '/Users/famj/projetos/redmine'
EXCEL_FILE = os.path.join(BASE_DIR, os.getenv('BASE_FILE_XLSX'))
JSON_FILE = os.path.join(BASE_DIR, 'dados.json')


def read_json_data(filepath):
    """Lê os dados do arquivo JSON."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def update_excel(excel_path, data):
    """Atualiza a planilha local com os dados do JSON usando openpyxl."""
    print(f"Atualizando planilha local: {excel_path}")
    wb = load_workbook(excel_path)
    ws = wb.active
    
    # Exemplo simples: procurando pelo ID na coluna A e atualizando B (status) e C (observação)
    # Ajuste o mapeamento das colunas conforme a estrutura real da sua planilha
    for entry in data:
        entry_id = entry.get("id")
        for row in range(2, ws.max_row + 1):
            if ws.cell(row=row, column=1).value == entry_id:
                ws.cell(row=row, column=2).value = entry.get("status")
                ws.cell(row=row, column=3).value = entry.get("observacao")
                break
                
    wb.save(excel_path)
    print("Planilha local atualizada com sucesso.")

def upload_to_sharepoint_api(local_path, file_name):
    """Faz o upload do arquivo para o SharePoint via API (Recomendado)."""
    print(f"Autenticando no SharePoint: {SHAREPOINT_SITE_URL}")
    ctx = ClientContext(SHAREPOINT_SITE_URL).with_credentials(UserCredential(SHAREPOINT_USER, SHAREPOINT_PASSWORD))
    
    target_folder = ctx.web.get_folder_by_server_relative_url(SHAREPOINT_TARGET_FOLDER)
    
    print(f"Fazendo upload para a pasta SharePoint: {SHAREPOINT_TARGET_FOLDER}")
    with open(local_path, 'rb') as content_file:
        file_content = content_file.read()
        target_folder.upload_file(file_name, file_content).execute_query()
        
    print(f"Upload do arquivo '{file_name}' concluído com sucesso via API!")

def upload_with_pyautogui():
    """
    Exemplo de automação visual caso não seja possível usar a API (Ex: MFA obrigatório sem App Password).
    Abre o navegador, acessa o sharepoint e simula interação.
    """
    print("Iniciando automação com PyAutoGUI (método visual)...")
    # Este é um esboço: o PyAutoGUI precisa de posições exatas na tela
    print("Você teria 5 segundos para focar a tela do navegador na pasta do SharePoint...")
    time.sleep(5)
    
    # Exemplo: Clicar no botão 'Upload' no centro da tela e depois em 'File'
    # pyautogui.click(x=800, y=300) 
    # time.sleep(1)
    # pyautogui.typewrite('DEVs_Redmine_2026.xlsx')
    # pyautogui.press('enter')
    
    print("Ações do PyAutoGUI concluídas (modo demonstração).")


def main():
    if not os.path.exists(JSON_FILE):
        print(f"Erro: Arquivo {JSON_FILE} não encontrado.")
        return
        
    if not os.path.exists(EXCEL_FILE):
        print(f"Erro: Arquivo {EXCEL_FILE} não encontrado.")
        return
        
    # 1. Ler os dados do JSON
    dados = read_json_data(JSON_FILE)
    
    # 2. Atualizar a planilha local
    update_excel(EXCEL_FILE, dados)
    
    # 3. Atualizar no SharePoint
    # Recomendamos a API, mas caso prefira o PyAutoGUI, basta comentar o bloco do try/except
    # e descomentar a chamada da função upload_with_pyautogui()
    try:
        upload_to_sharepoint_api(EXCEL_FILE, os.path.basename(EXCEL_FILE))
    except Exception as e:
        print(f"Falha ao usar a API do SharePoint: {e}")
        print("Para utilizar o pyautogui, ajuste a função upload_with_pyautogui() com as coordenadas corretas da sua tela.")
        # upload_with_pyautogui()

if __name__ == '__main__':
    main()
