from sklearn.preprocessing import MinMaxScaler
import numpy as np

# Dados de exemplo
data = np.array([[1], [2], [3], [4], [5]])

# Instanciando o MinMaxScaler com o intervalo desejado. Por exemplo, [5, 10].
scaler = MinMaxScaler(feature_range=(5, 10))

# Ajustando o scaler aos dados e transformando-os
scaled_data = scaler.fit_transform(data)

print("Dados originais:", data.reshape(-1))
print("Dados reescalonados:", scaled_data.reshape(-1))
