## --------------------------------------------------------
## Automacao de processos no REDMINE
## by Feliciano Junior
## Gerar os registros para lança no REDMINE do usuario
## para ser lidos pelo gera_lancamentos_redmine.py
## ------------------------------------------------------
"""
    Gerar os registros para lança no REDMINE do usuario
    para ser lidos pelo gera_lancamentos_redmine.py
"""
import os
import json
from dotenv import load_dotenv
from datetime import datetime, timedelta, date
from FeriadoBrasil import *
load_dotenv()

#parametros de entrada
if os.getenv("PARM_DATA") == "NONE":
    data=date.today() #data para iniciar a sequencia
else:    
    data=datetime.strptime(os.getenv("PARM_DATA"), "%Y/%m/%d").date() #data para iniciar a sequencia
##variaveis
#sem = date.today().weekday()
sem = data.weekday()
tarefas= {"tarefas": []}
comentario=""
#   
atividade=os.getenv("PARM_ATIVIDADE")
uf =os.getenv("PARM_UF")
cidade=os.getenv("PARM_CIDADE")
senha=os.getenv("PARM_SENHA")
usuario=os.getenv("PARM_USUARIO")
gestor=os.getenv("PARM_GESTOR")
projeto=os.getenv("PARM_PROJETO")
tarefa=os.getenv("PARM_TAREFA")
horas=os.getenv("PARM_HORAS")
#
ferias=[os.getenv("PARM_INICIO_FERIAS"), 
        os.getenv("PARM_FIM_FERIAS")
        ] #informe o intervalo de ferias programadas em .env


fer = FeriadoBrasil(data,
                    uf,
                    cidade
                    )


    
def ativa_ferias(data, ferias):
    data_atual = data
    inicio = datetime.strptime(ferias[0], "%Y-%m-%d").date()
    fim = datetime.strptime(ferias[1], "%Y-%m-%d").date()

    return inicio <= data_atual <= fim 
    

def GuardaTarefas():
        tarefas["tarefas"].append(  
        {
        "Data": datetime.strftime(data, "%d/%m/%Y"),
        "Usuário": usuario,
        "Gestor": gestor,
        "Projeto": projeto,
        "Atividade": atividade,
        "Tarefa": tarefa,
        "Comentário": comentario,
        "Horas": horas
        }
        )
##preenche para uma faixa de dias
for i in range(int(os.getenv("PARM_FAIXA_DIAS"))):
    if ativa_ferias(data, ferias):
        comentario="Ausência Temporária - Férias Programadas"
        tarefa='35054 - FY Non_Worked Hours'
        atividade='Day-Off'
        GuardaTarefas()
    
    if ativa_ferias(data, ferias)==False:
         if sem < 5:    
                fer.data_feriado = data
                comentario='PDSM - Incidentes do TMS - Tratamento de Correção, Liberação, Duvidas de Usuário, Consultas ao Mastersaf, Consultas ao SOLIS.'
                tarefa='35053 - Sustentação - Hora trabalhada'
                atividade='Tarefa'   

                if fer.FeriadoNacional() == True:
                    comentario= f'Ferido Nacional: {fer.comentario}'
                    tarefa =fer.tarefa #'35054'  
                    atividade =fer.atividade #'Day-Off' 

                if fer.feriadoEstadual() == True:
                    comentario= f'Ferido Estadual: {fer.comentario}'
                    tarefa=fer.tarefa #'35054'  
                    atividade =fer.atividade #'Day-Off' 
                
                if fer.feriadoMunicipal() == True:
                    comentario= f'Ferido Municipal: {fer.comentario}'
                    tarefa=fer.tarefa #'35054'  
                    atividade =fer.atividade #'Day-Off'

                GuardaTarefas()    
                
    #GuardaTarefas()
    data = data + timedelta(days=1)
    sem = data.weekday()  
        
##laco de gravacao do arquivo json  
with open('dados.json','w',encoding="utf-8") as file:
           json.dump(tarefas, file,indent=4)
