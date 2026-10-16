from datetime import datetime, timedelta, date

ferias=['2026-05-11', '2026-06-09']
        
#data=date.today() 
data=datetime.strptime('2026-05-11', "%Y-%m-%d").date() #data para iniciar a sequencia

print(data)

def ativa_ferias(data, ferias):
    data_atual = data
    inicio = datetime.strptime(ferias[0], "%Y-%m-%d").date()
    fim = datetime.strptime(ferias[1], "%Y-%m-%d").date()

    return inicio <= data_atual <= fim 

if ativa_ferias(data, ferias):
        comentario="Ausência Temporária - Férias Programadas"
        tarefa='35054 - FY Non_Worked Hours'
        atividade='Day-Off'
        print(atividade)
print(ativa_ferias(data, ferias))
print(data, "Está de férias" if ativa_ferias(data, ferias) else "Não está de férias")