## --------------------------------------------------------
## Automacao de processos no REDMINE
## by Feliciano Junior
## Mesclar arquivos de lancamentos do usuario no dados.json
## --------------------------------------------------------
"""
    Script para mesclar registros específicos de um usuário
    (login_usuario.json ou <login>.json) no arquivo central dados.json.
    
    Funcionalidades:
    1. Localiza e lê o arquivo de apontamentos do usuário (ex: login_usuario.json ou fajunior1.json).
    2. Lê o arquivo consolidado dados.json (gerado previamente).
    3. Normaliza e valida os formatos de data (ex: DD/MM/YYYY ou YYYY-MM-DD).
    4. Preenche os dados ausentes no arquivo do usuário (ex: "Usuário", "Gestor", etc.)
       com base nos registros existentes em dados.json ou nas variáveis do .env.
    5. Ajusta o intervalo cronológico inserindo ou atualizando as datas no dados.json
       mantendo a ordenação correta.
    6. Salva o dados.json atualizado e estruturado.
"""

import os
import sys
import json
from datetime import datetime, date
from dotenv import load_dotenv

load_dotenv()


def normalizar_caminho(caminho_relativo):
    """Retorna o caminho absoluto baseado no diretório atual."""
    if os.path.isabs(caminho_relativo):
        return caminho_relativo
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, caminho_relativo)


def ler_json(caminho):
    """
    Lê um arquivo JSON e retorna a lista de tarefas,
    aceitando tanto [ {...}, {...} ] quanto { "tarefas": [ {...} ] }.
    """
    if not os.path.exists(caminho):
        return None

    with open(caminho, "r", encoding="utf-8") as f:
        conteudo = json.load(f)

    if isinstance(conteudo, dict):
        return conteudo.get("tarefas", [])
    elif isinstance(conteudo, list):
        return conteudo
    return []


def salvar_json(caminho, tarefas):
    """Salva a lista de tarefas no formato padrão do projeto."""
    payload = {"tarefas": tarefas}
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=4, ensure_ascii=False)
    print(f"✅ Arquivo salvo com sucesso em: {caminho}")


def parse_data(data_val):
    """Converte diferentes formatos de data para datetime.date."""
    if isinstance(data_val, datetime):
        return data_val.date()
    if isinstance(data_val, date):
        return data_val

    data_str = str(data_val).strip()
    formatos = ["%d/%m/%Y", "%Y-%m-%d", "%Y/%m/%d", "%d-%m-%Y"]
    for fmt in formatos:
        try:
            return datetime.strptime(data_str, fmt).date()
        except ValueError:
            pass

    raise ValueError(f"Formato de data inválido ou não suportado: '{data_str}'")


def formatar_data(dt):
    """Retorna a data formatada no padrão DD/MM/YYYY."""
    return dt.strftime("%d/%m/%Y")


def identificar_arquivo_usuario(caminho_informado=None):
    """
    Identifica dinamicamente o arquivo de tarefas do usuário seguindo a prioridade:
    1. Caminho passado por parâmetro/CLI.
    2. Variável de ambiente PARM_ARQUIVO_USUARIO.
    3. login_usuario.json (se existir).
    4. <PARM_LOGIN>.json (ex: fajunior1.json se existir).
    5. fajunior1.json (se existir na raiz).
    6. Default: login_usuario.json.
    """
    if caminho_informado:
        return normalizar_caminho(caminho_informado)

    caminho_env = os.getenv("PARM_ARQUIVO_USUARIO")
    if caminho_env and os.path.exists(normalizar_caminho(caminho_env)):
        return normalizar_caminho(caminho_env)

    candidatos = [
        "login_usuario.json",
        f"{os.getenv('PARM_LOGIN', '').strip()}.json",
        "fajunior1.json",
    ]

    for cand in candidatos:
        if cand and cand != ".json":
            p = normalizar_caminho(cand)
            if os.path.exists(p):
                return p

    return normalizar_caminho("login_usuario.json")


def obter_dados_padrao(tarefas_base):
    """
    Extrai informações padrão a partir do .env e de registros já existentes em dados.json
    para preencher dados faltantes (como 'Usuário', 'Gestor', etc.).
    """
    defaults = {
        "Usuário": os.getenv("PARM_USUARIO", "").strip(),
        "Gestor": os.getenv("PARM_GESTOR", "").strip(),
        "Projeto": os.getenv("PARM_PROJETO", "TMS").strip(),
        "Atividade": os.getenv("PARM_ATIVIDADE", "Tarefa").strip(),
        "Tarefa": os.getenv("PARM_TAREFA", "35053 - Sustentação - Hora trabalhada").strip(),
        "Comentário": "",
        "Horas": os.getenv("PARM_HORAS", "8").strip() or "8",
    }

    # Se alguma informação estiver vazia no .env, tenta recuperar do histórico do dados.json
    for t in tarefas_base:
        for campo in ["Usuário", "Gestor", "Projeto", "Atividade", "Tarefa"]:
            if not defaults[campo] and t.get(campo):
                defaults[campo] = t.get(campo)

    return defaults


def completar_registro(item_usuario, lookup_por_data, defaults):
    """
    Garante que o registro contenha todas as chaves obrigatórias preenchidas,
    na ordem esperada pelo dados.json.
    """
    dt = parse_data(item_usuario.get("Data"))
    data_formatada = formatar_data(dt)

    # Busca registro correspondente na data para herdar valores se necessário
    registro_base = lookup_por_data.get(dt, {})

    usuario = (
        item_usuario.get("Usuário")
        or registro_base.get("Usuário")
        or defaults["Usuário"]
    )
    gestor = (
        item_usuario.get("Gestor")
        or registro_base.get("Gestor")
        or defaults["Gestor"]
    )
    projeto = (
        item_usuario.get("Projeto")
        or registro_base.get("Projeto")
        or defaults["Projeto"]
    )
    atividade = (
        item_usuario.get("Atividade")
        or registro_base.get("Atividade")
        or defaults["Atividade"]
    )
    tarefa = (
        item_usuario.get("Tarefa")
        or registro_base.get("Tarefa")
        or defaults["Tarefa"]
    )
    comentario = (
        item_usuario.get("Comentário")
        if item_usuario.get("Comentário") is not None
        else registro_base.get("Comentário", defaults["Comentário"])
    )
    horas = str(
        item_usuario.get("Horas")
        if item_usuario.get("Horas") is not None
        else registro_base.get("Horas", defaults["Horas"])
    )

    return {
        "Data": data_formatada,
        "Usuário": usuario,
        "Gestor": gestor,
        "Projeto": projeto,
        "Atividade": atividade,
        "Tarefa": tarefa,
        "Comentário": comentario,
        "Horas": horas,
    }


def mesclar_arquivos(caminho_usuario=None, caminho_dados="dados.json"):
    """
    Executa a mesclagem dos arquivos do usuário e dados.json.
    """
    caminho_usuario_real = identificar_arquivo_usuario(caminho_usuario)
    caminho_dados_real = normalizar_caminho(caminho_dados)

    print("=" * 60)
    print("🔄 INICIANDO PROCESSO DE MESCLAGEM DE APONTAMENTOS")
    print("=" * 60)
    print(f"📄 Arquivo do usuário: {caminho_usuario_real}")
    print(f"📄 Arquivo central:   {caminho_dados_real}")

    # 1. Carregar o arquivo do usuário
    if not os.path.exists(caminho_usuario_real):
        print(f"⚠️  Arquivo '{caminho_usuario_real}' não encontrado.")
        print("💡 Crie o arquivo 'login_usuario.json' ou execute informando o caminho.")
        return False

    tarefas_usuario = ler_json(caminho_usuario_real)
    if not tarefas_usuario:
        print("⚠️  Nenhum apontamento encontrado no arquivo do usuário.")
        return False

    # 2. Carregar o arquivo base dados.json
    tarefas_base = ler_json(caminho_dados_real) or []
    print(f"📊 Registros atuais em dados.json: {len(tarefas_base)}")
    print(f"📊 Registros a mesclar do usuário: {len(tarefas_usuario)}")

    # 3. Mapear defaults e dados base por data
    defaults = obter_dados_padrao(tarefas_base)
    lookup_por_data = {}
    for t in tarefas_base:
        try:
            dt = parse_data(t.get("Data"))
            if dt not in lookup_por_data:
                lookup_por_data[dt] = t
        except Exception:
            pass

    # 4. Agrupar e completar os registros do usuário por data
    registros_usuario_por_data = {}
    for item in tarefas_usuario:
        try:
            dt = parse_data(item.get("Data"))
            item_completado = completar_registro(item, lookup_por_data, defaults)
            if dt not in registros_usuario_por_data:
                registros_usuario_por_data[dt] = []
            registros_usuario_por_data[dt].append(item_completado)
        except Exception as e:
            print(f"⚠️  Erro ao processar item {item}: {e}")

    # 5. Mesclar: substituir os dias existentes ou manter registros que não foram alterados
    novas_tarefas = []
    datas_processadas_usuario = set()

    # Passa pelos itens da base
    for item in tarefas_base:
        try:
            dt = parse_data(item.get("Data"))
        except Exception:
            novas_tarefas.append(item)
            continue

        if dt in registros_usuario_por_data:
            if dt not in datas_processadas_usuario:
                # Substitui os registros desse dia pelos registros customizados do usuário
                novas_tarefas.extend(registros_usuario_por_data[dt])
                datas_processadas_usuario.add(dt)
        else:
            novas_tarefas.append(item)

    # Adiciona datas novas informadas pelo usuário que não estavam na base
    for dt, itens in registros_usuario_por_data.items():
        if dt not in datas_processadas_usuario:
            novas_tarefas.extend(itens)
            datas_processadas_usuario.add(dt)

    # 6. Ordenar cronologicamente para garantir que fiquem no intervalo correto
    novas_tarefas.sort(key=lambda x: parse_data(x.get("Data")))

    # 7. Salvar dados.json atualizado
    salvar_json(caminho_dados_real, novas_tarefas)

    print("\n📋 RESUMO DAS ALTERAÇÕES:")
    print(f"  • Datas atualizadas/adicionadas do usuário: {len(registros_usuario_por_data)}")
    for dt in sorted(registros_usuario_por_data.keys()):
        itens_dt = registros_usuario_por_data[dt]
        total_horas = sum(float(i.get("Horas", 0)) for i in itens_dt)
        print(f"    - {formatar_data(dt)}: {len(itens_dt)} tarefa(s), total de {total_horas:.1f}h")
    print(f"  • Total consolidado final de tarefas: {len(novas_tarefas)}")
    print("=" * 60)
    return True


if __name__ == "__main__":
    arq_usuario = sys.argv[1] if len(sys.argv) > 1 else None
    arq_dados = sys.argv[2] if len(sys.argv) > 2 else "dados.json"
    mesclar_arquivos(arq_usuario, arq_dados)
