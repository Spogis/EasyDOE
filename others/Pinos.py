import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm

# Definindo os parâmetros das distribuições normais
media_furo, dp_furo = 100.0, 5.0
media_pino, dp_pino = 40.0, 4.0


def probabilidade_pino_nao_entrar(media_furo, dp_furo, media_pino, dp_pino):
    diferenca_medias = media_furo - media_pino
    dp_combinada = (dp_furo ** 2 + dp_pino ** 2) ** 0.5
    probabilidade_entrar = 1 - norm.cdf(0, loc=diferenca_medias, scale=dp_combinada)
    return (1-probabilidade_entrar) * 100

# Gerando dados para as distribuições normais
dados1 = np.random.normal(media_furo, dp_furo, 10000)
dados2 = np.random.normal(media_pino, dp_pino, 10000)
diferenca = dados1-dados2

df = pd.DataFrame({'Furo': dados1, 'Pino': dados2, 'Diferença': diferenca})
caminho_arquivo = '../datasets/PinosEFuros.xlsx'
df.to_excel(caminho_arquivo, index=False)

probabilidade = probabilidade_pino_nao_entrar(media_furo, dp_furo, media_pino, dp_pino)

# Plotando as distribuições
plt.figure(figsize=(10, 6))
sns.histplot(dados1, bins=30, kde=True, color='blue', label='Furos - Média ' + str(media_furo) + ', Desvio Padrão ' + str(dp_furo))
sns.histplot(dados2, bins=30, kde=True, color='red', label='Pinos - Média ' + str(media_pino) + ', Desvio Padrão ' + str(dp_pino))
plt.title('Distribuição Normal para Dois Casos')
plt.xlabel('Valor')
plt.ylabel('Frequência')
plt.legend()

# Ajusta o layout para criar espaço adicional abaixo do gráfico
plt.subplots_adjust(bottom=0.2)
plt.figtext(0.5, 0.05, s=f'Probabilidade do pino não entrar no furo: {probabilidade:.2f}%', fontsize=12, color='green', ha='center',
            bbox={'facecolor': 'white', 'alpha': 0.2})

plt.show()

