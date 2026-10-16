## --------------------------------------------------------
## Automacao de processos no REDMINE
## by Feliciano Junior
## classe feriados no Brasil. sejam
## no Estados, Municipios e Nacinal. 
## --------------------------------------------------------
import json
from datetime import datetime, timedelta, date
class FeriadoBrasil:
    comentario = ''
    tarefa='35054 - FY Non_Worked Hours'  
    atividade='Day-Off'
 
    def __init__(self, data, UF, cidade):
        self.data_feriado =  data.strftime("%d/%m/%Y")
        self.UF_feriado = UF
        self.cidade = cidade


    def FeriadoNacional(self):
            #print(self.data_feriado,self.UF_feriado,self.cidade)     
            with open("Feriados-NACIONAL.json",'r',encoding='windows-1252') as meu_json:
                dados = json.load(meu_json)           
            # para cada item do arquivo json
            for i in dados:
                if self.data_feriado.strftime("%d/%m/%Y") == i['Data']:
                  self.comentario = i['Feriado']
                  return True
            return  False 

    def feriadoEstadual(self):
            #print(self.data_feriado,self.UF_feriado,self.cidade)   
            with open('Feriados-ESTADUAL.json','r',encoding='windows-1252') as meu_json:
                dados = json.load(meu_json)
            # para cada item do arquivo json
            for i in dados:
                if self.data_feriado.strftime("%d/%m/%Y") == i['Data'] and self.UF_feriado == i['UF']:
                  self.comentario = i['Resumo']
                  return True
            return  False 
                            
    def feriadoMunicipal(self):
            #print(self.data_feriado,self.UF_feriado,self.cidade)   
            with open('Feriados-MUNICIPAL.json', 'r',encoding='latin1') as meu_json:
                dados = json.load(meu_json)             
            # para cada item do arquivo json
            for i in dados:  
                #print(self.data_feriado,i['Data'])           
                if self.data_feriado.strftime("%d/%m/%Y") == i['Data']  and self.UF_feriado == i['UF'] and self.cidade==i['Cidade']:
                  self.comentario = i['Resumo']
                  return True
            return  False 
    

        