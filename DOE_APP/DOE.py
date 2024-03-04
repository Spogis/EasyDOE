import pandas as pd
import numpy as np
import pyDOE2 as pyDOE
from scipy.stats.distributions import norm

def estimate_std(max, min, trust_level):
    prop_trust_level = float(trust_level)
    z_critical = norm.ppf((1 + prop_trust_level) / 2)
    amplitude = max - min
    std = amplitude / (2 * z_critical)
    return std


def estimate_min_max(mean, std, trust_level):
    prop_trust_level = float(trust_level)
    z_critical = norm.ppf((1 + prop_trust_level) / 2)
    margin_error = z_critical * std

    min = mean - margin_error
    max = mean + margin_error
    return min, max


def UpdateNaNValues(filename):
    df = pd.read_excel(filename)
    for index, row in df.iterrows():
        if pd.isna(row['Min']):
            df.at[index, 'Min'], _ = estimate_min_max(row['Mean'], row['Standard Deviation'], float(row['Trust Level']))
        if pd.isna(row['Max']):
            _, df.at[index, 'Max'] = estimate_min_max(row['Mean'], row['Standard Deviation'], float(row['Trust Level']))

        if pd.isna(row['Mean']):
            df.at[index, 'Mean'] = np.mean([row['Max'], row['Min']])
        if pd.isna(row['Standard Deviation']):
            df.at[index, 'Standard Deviation'] = estimate_std(row['Max'], row['Min'], float(row['Trust Level']))

    df.to_excel('NewInputVariables.xlsx', index=False)

def LatinHypercube(NumberOfSimulations):
    df = pd.read_excel('NewInputVariables.xlsx')
    InputVariables = df['Variable Name']
    Variable_Mean = df['Mean']
    Variable_Standard_deviation = df['Standard Deviation']

    NumberOfInputVariables = len(InputVariables)
    design = pyDOE.lhs(NumberOfInputVariables, samples=NumberOfSimulations, criterion='center')
    for i in range(NumberOfInputVariables):
        design[:, i] = norm(loc=Variable_Mean[i], scale=Variable_Standard_deviation[i]).ppf(design[:, i])

    # Criar o DataFrame
    df_simulations = pd.DataFrame({'Simulation': range(1, NumberOfSimulations + 1)})
    for j in range(NumberOfInputVariables):
        df_simulations[InputVariables[j]] = design[:, j]

    df_simulations.set_index('Simulation', inplace=True)
    df_simulations.to_excel('datasets/DOE_LHC.xlsx')


def FullFactorial():
    df = pd.read_excel('NewInputVariables.xlsx')
    num_vars = len(df)
    # Gera o design full-factorial
    full_fact_design = pyDOE.ff2n(num_vars)

    # Converte os níveis codificados para os valores reais das variáveis
    def convert_to_real_values(coded_values, min_values, max_values):
        real_values = np.zeros(coded_values.shape)
        for i in range(coded_values.shape[1]):
            real_values[:, i] = coded_values[:, i] * (max_values[i] - min_values[i]) / 2 + (max_values[i] + min_values[i]) / 2
        return real_values

    # Aplica a conversão
    real_values_doe = convert_to_real_values(full_fact_design, df['Min'].values, df['Max'].values)

    # Cria um DataFrame para exportação
    doe_df = pd.DataFrame(real_values_doe, columns=df['Variable Name'])
    doe_df.reset_index(inplace=True)
    doe_df['index'] += 1
    doe_df.rename(columns={'index': 'Simulation'}, inplace=True)
    column_order = ['Simulation'] + list(df['Variable Name'])
    doe_df = doe_df[column_order]

    # Salva o DOE em um arquivo Excel
    doe_df.set_index('Simulation', inplace=True)
    doe_df.to_excel('datasets/DOE_Full_Factorial.xlsx')


def Run_DOE(filename, NumberOfSimulations):
    UpdateNaNValues(filename)
    LatinHypercube(NumberOfSimulations)
    FullFactorial()