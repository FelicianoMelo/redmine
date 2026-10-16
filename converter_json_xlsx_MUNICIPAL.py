import json
import pandas as pd

# Ler JSON
with open('Feriados-MUNICIPAL.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Converter para DataFrame
df = pd.DataFrame(data)

# Salvar no Excel
df.to_excel('Feriados_MUNICIPAL.xlsx', index=False)
