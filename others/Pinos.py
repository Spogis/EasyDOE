import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm

# Definindo os parâmetros das distribuições normais
media_furo, dp_furo = 50.0, 1.0
media_pino, dp_pino = 40.0, 1.0


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

fig, ax = plt.subplots(figsize=(10, 6))
fig.patch.set_facecolor('#00FF00')
ax.set_facecolor('#00FF00')

ax = sns.histplot(data=dados1, bins=30, kde=False, stat='density', color='#ff1493',
                  label=f'Furos - Média {media_furo}, Desvio Padrão {dp_furo}')
sns.kdeplot(data=dados1, color='crimson', ax=ax)

ax = sns.histplot(data=dados2, bins=30, kde=False, stat='density', color='#ff0000',
                  label=f'Pinos - Média {media_pino}, Desvio Padrão {dp_pino}')
sns.kdeplot(data=dados2, color='crimson', ax=ax)

ax.set_title(f'Probabilidade do pino não entrar no furo: {probabilidade:.2f}%', color='#ffffff', fontsize=20)
ax.set_xlabel('Diâmetro', color='#ffffff', fontsize='large')
ax.set_ylabel('Frequência', color='#ffffff', fontsize='large')
ax.tick_params(axis='x', colors='#ffffff', labelsize='large')
ax.tick_params(axis='y', colors='#ffffff', labelsize='large')

ax.legend(facecolor='#00FF00')
legend = ax.legend(fontsize='large', loc='upper right'
                   , facecolor='#000000')
for text in legend.get_texts():
    text.set_color('#ffffff')

for spine in ax.spines.values():
    spine.set_edgecolor('#ffffff')

plt.show()



