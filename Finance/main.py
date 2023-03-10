import pandas as pd
import datetime
import yfinance as yf
from matplotlib import pyplot as plt
import mplcyberpunk
import win32com.client as win32

codigos_de_negociacao = ["^BVSP", "BRL=X"]  

hoje = datetime.datetime.now()
um_ano_atras = hoje - datetime.timedelta(days = 365)

dados_mercado = yf.download(codigos_de_negociacao, um_ano_atras, hoje)

dados_mercado = dados_mercado.resample("1D").last()

dados_fechamento = dados_mercado['Adj Close']

dados_fechamento.columns = ['dolar', 'ibovespa']

dados_fechamento

#dados_fechamento = dados_fechamento.dropna()

dados_anuais = dados_fechamento.resample("Y").last()

dados_mensais = dados_fechamento.resample("M").last()

dados_anuais

dados_mensais

#print(dados_fechamento)
#print(dados_anuais)
#print(dados_mensais)

retorno_anual = dados_anuais.pct_change().dropna()
retorno_mensal = dados_mensais.pct_change().dropna()
retorno_diario = dados_fechamento.pct_change().dropna()

retorno_diario

#print(retorno_anual)
#print(retorno_mensal)
#print(retorno_diario)

retorno_diario_dolar = retorno_diario.iloc[-1, 0]
retorno_diario_ibov = retorno_diario.iloc[-1, 1]

retorno_mensal_dolar = retorno_mensal.iloc[-1, 0]
retorno_mensal_ibov = retorno_mensal.iloc[-1, 1]

retorno_anual_dolar = retorno_anual.iloc[-1, 0]
retorno_anual_ibov = retorno_anual.iloc[-1, 1]

retorno_diario_dolar = round((retorno_diario_dolar * 100), 2)
retorno_diario_ibov = round((retorno_diario_ibov * 100), 2)

retorno_mensal_dolar = round((retorno_mensal_dolar * 100), 2)
retorno_mensal_ibov = round((retorno_mensal_ibov * 100), 2) 

retorno_anual_dolar = round((retorno_anual_dolar * 100), 2)
retorno_anual_ibov = round((retorno_anual_ibov * 100), 2)

#print(retorno_anual_dolar)
#print(retorno_anual_ibov)

#print(retorno_mensal_dolar)
#print(retorno_mensal_ibov)

#print(retorno_diario_dolar)
#print(retorno_diario_ibov)

plt.style.use("cyberpunk")

dados_fechamento.plot(y = "ibovespa", use_index = True, legend = False, )

plt.title("Ibovespa")

plt.savefig('ibovespa.png', dpi = 300)

plt.show()

plt.style.use("cyberpunk")

dados_fechamento.plot(y = "dolar", use_index = True, legend = False)

plt.title("Dolar")

plt.savefig('dolar.png', dpi = 300)

plt.show()

outlook = win32.Dispatch("outlook.application")

email = outlook.CreateItem(0)

email.To = "vanderlaus@hotmail.com"
email.Subject = "Relat??rio Di??rio"
email.Body = f'''Prezado diretor, segue o relat??rio di??rio:

Bolsa:

No ano o Ibovespa est?? tendo uma rentabilidade de {retorno_anual_ibov}%, 
enquanto no m??s a rentabilidade ?? de {retorno_mensal_ibov}%.

No ??ltimo dia ??til, o fechamento do Ibovespa foi de {retorno_diario_ibov}%.

D??lar:

No ano o D??lar est?? tendo uma rentabilidade de {retorno_anual_dolar}%, 
enquanto no m??s a rentabilidade ?? de {retorno_mensal_dolar}%.

No ??ltimo dia ??til, o fechamento do D??lar foi de {retorno_diario_dolar}%.


Abs,

O melhor estagi??rio do mundo

'''

anexo_ibovespa = r'C:\Users\Vander\Documents\PythonWolrd\Finance\ibovespa.png'
anexo_dolar = r'C:\Users\Vander\Documents\PythonWolrd\Finance\dolar.png'

email.Attachments.Add(anexo_ibovespa)
email.Attachments.Add(anexo_dolar)

email.Send()
