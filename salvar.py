import pandas as pd

resultados = [
    # COLE AQUI OS DADOS PARCIAIS DO RESULTADOS (se você tiver)
]

# Salva o que estiver em "resultados"
df_resultados = pd.DataFrame(resultados)
df_resultados.to_excel("resultados_pid_parcial.xlsx", index=False)
print("✅ Resultados parciais salvos em 'resultados_pid_parcial.xlsx'.")