import pyDOE2

# Gerar um LHS com uma única variável
n_vars = 1  # Número de variáveis
n_samples = 10  # Número de amostras desejadas

# Gerar o LHS
lhs_sample= pyDOE2.lhs(n_vars, samples=n_samples, criterion='correlation')

# Mostrar o resultado
print(lhs_sample)