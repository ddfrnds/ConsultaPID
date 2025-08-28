import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Carrega os dados do Excel
df = pd.read_excel("Contatos.xlsx")

# Inicializa o navegador
driver = webdriver.Chrome()
driver.get("https://portaldousuario.reparacaobaciariodoce.com/consulta-de-condicao-para-ingresso-do-pid/")

# Aguarda o usuário resolver o reCAPTCHA manualmente
input("🔵 Resolva o reCAPTCHA no navegador e pressione Enter para continuar...")

# Cria a lista onde os resultados serão armazenados
resultados = []

# Cria o WebDriverWait fora do loop
wait = WebDriverWait(driver, 20)

# Loop principal de consulta
for index, row in df.iterrows():
    cpf_cnpj = str(row['CPF/CNPJ']).strip().replace('.', '').replace('-', '').replace('/', '')

    try:
        # Espera o campo de CPF/CNPJ estar visível
        campo_cpf = wait.until(EC.visibility_of_element_located((By.ID, "inputCPF")))
        campo_cpf.clear()
        campo_cpf.send_keys(cpf_cnpj)
        campo_cpf.send_keys(Keys.RETURN)

        # Espera o resultado aparecer com "APTO" ou "NÃO APTO"
        resultado_element = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//span[contains(text(), "APTO") or contains(text(), "NÃO APTO")]')
            )
        )

        resultado_texto = resultado_element.text.strip().upper()

        if "NÃO APTO" in resultado_texto:
            status = "Não apto"
        elif "APTO" in resultado_texto:
            status = "Apto"
        else:
            status = f"Resultado desconhecido: {resultado_texto}"

        resultados.append({'CPF/CNPJ': cpf_cnpj, 'Resultado': status})

    except Exception as e:
        print(f"❌ Erro ao clicar em Nova consulta para CPF/CNPJ {cpf_cnpj}: {e}")
        resultados.append({'CPF/CNPJ': cpf_cnpj, 'Resultado': f"Erro: {str(e)}"})

    # Clicar manualmente no botão "Nova consulta"
    input(f"🟡 Clique manualmente em 'Nova consulta' para continuar com o próximo CPF/CNPJ. Pressione Enter quando estiver pronto...")

# Salva os resultados em Excel
df_resultados = pd.DataFrame(resultados)
df_resultados.to_excel("resultados_pid.xlsx", index=False)
print("✅ Consulta finalizada. Resultados salvos em 'resultados_pid.xlsx'.")