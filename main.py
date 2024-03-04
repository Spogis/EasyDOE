import dash
from dash import html, dcc, dash_table
from dash.dependencies import Input, Output, State
import pandas as pd
from dash.dash_table.Format import Format, Scheme
import base64
import io

from DOE_APP.DOE import *

# Inicializa os dados da tabela com as novas colunas e uma linha de exemplo
df = pd.DataFrame({
    'Variable Name': [''],
    'Mean': [''],
    'Standard Deviation': [''],
    'Max': [''],
    'Min': [''],
    'Step (If Variable is Discrete)': [''],
    'Trust Level': [0.95],  # 95% como valor inicial
    'Variable Type': ['Continuous']  # Valor inicial padrão
})

# Definição dos tipos de variáveis para o dropdown
variable_types = ['Continuous', 'Discrete']
trust_level_values = ['0.90', '0.95', '0.99']

# Inicializa o aplicativo Dash
app = dash.Dash(__name__)

# Layout do aplicativo
app.layout = html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Div(['Arraste ou ', html.A('Selecione um Arquivo')]),
        style={
            'width': '100%', 'height': '60px', 'lineHeight': '60px',
            'borderWidth': '1px', 'borderStyle': 'dashed', 'borderRadius': '5px',
            'textAlign': 'center', 'margin': '10px'
        },
        multiple=False  # Permite a seleção de um único arquivo por vez
    ),
    dash_table.DataTable(
        id='table',
        columns=[
            {'id': 'Variable Name', 'name': 'Variable Name', 'editable': True},
            {'id': 'Mean', 'name': 'Mean', 'type': 'numeric', 'editable': True},
            {'id': 'Standard Deviation', 'name': 'Standard Deviation', 'type': 'numeric', 'editable': True},
            {'id': 'Max', 'name': 'Max', 'type': 'numeric', 'editable': True},
            {'id': 'Min', 'name': 'Min', 'type': 'numeric', 'editable': True},
            {'id': 'Step (If Variable is Discrete)', 'name': 'Step (If Variable is Discrete)', 'type': 'numeric', 'editable': True},
            {'id': 'Trust Level', 'name': 'Trust Level', 'presentation': 'dropdown', 'editable': True,
             'format': Format(precision=2, scheme=Scheme.percentage)},
            {'id': 'Variable Type', 'name': 'Variable Type', 'presentation': 'dropdown', 'editable': True}
        ],
        data=df.to_dict('records'),
        editable=True,
        style_data_conditional=[
            {
                'if': {
                    'filter_query': '{Variable Type} = Discrete',  # Se Variable Type for Discrete
                    'column_id': 'Step (If Variable is Discrete)'
                },
                'backgroundColor': '#FAFAFA',
                'border': '1px solid blue'
            },
        ],
        style_cell={
            'minWidth': '150px', 'width': '150px', 'maxWidth': '150px',  # Defina a largura das colunas aqui
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
            'whiteSpace': 'normal'
        },
        style_header={
            'textAlign': 'center'  # Centraliza o texto no cabeçalho também
        },
        row_deletable=True,  # Permite a exclusão de linhas
        dropdown={
            'Variable Type': {
                'options': [
                    {'label': i, 'value': i}
                    for i in variable_types
                ]
            },
            'Trust Level': {
                'options': [
                    {'label': i, 'value': i}
                    for i in trust_level_values
                ]
            },
        },
    ),

    html.Br(),
    html.Button('Adicionar Linha', id='adding-rows-btn', n_clicks=0,
                style={'backgroundColor': 'orange', 'color': 'white', 'fontWeight': 'bold', 'fontSize': '20px', 'marginRight': '10px'}),

    html.Button('Salvar como Excel', id='save-excel-btn', n_clicks=0,
                style={'backgroundColor': 'blue', 'color': 'white', 'fontWeight': 'bold', 'fontSize': '20px', 'marginRight': '10px'}),

    html.Button('Criar DOE', id='create-doe-btn', n_clicks=0,
                style={'backgroundColor': 'green', 'color': 'white', 'fontWeight': 'bold', 'fontSize': '20px', 'marginRight': '10px'}),

])

def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'xlsx' in filename:
            # Assume que o usuário está carregando um arquivo xlsx
            df = pd.read_excel(io.BytesIO(decoded), engine='openpyxl')
            return df.to_dict('records')
    except Exception as e:
        print(e)
        return None

@app.callback(
    Output('table', 'data', allow_duplicate=True),
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename')],
    prevent_initial_call=True
)
def update_output(contents, filename):
    if contents is not None:
        rows = parse_contents(contents, filename)
        if rows is not None:
            return rows
    return dash.no_update


@app.callback(
    Output('table', 'style_data_conditional'),
    [Input('table', 'data')]
)
def update_editability(rows):
    # Verifica se alguma linha tem 'Variable Type' definido como 'Discrete'
    conditions = []
    for i, row in enumerate(rows):
        if row['Variable Type'] == 'Discrete':
            conditions.append({
                'if': {'row_index': i, 'column_id': 'Step (If Variable is Discrete)'},
                'backgroundColor': '#FAFAFA',
                'border': '1px solid blue',
                # Aqui você pode aplicar estilos adicionais se necessário
            })
    return conditions


@app.callback(
    Output('table', 'data', allow_duplicate=True),
    [Input('adding-rows-btn', 'n_clicks')],
    [State('table', 'data')],
    prevent_initial_call=True
)
def add_row(n_clicks, rows):
    if n_clicks > 0:
        rows.append({col: ('' if col not in ['Variable Name', 'Variable Type', 'Trust Level']
                           else '0.95' if col == 'Trust Level'  # Definindo 95% para a coluna 'Trust Level'
                           else variable_types[0] if col == 'Variable Type'
                           else '')
                     for col in df.columns})
    return rows

@app.callback(
    Output('save-excel-btn', 'children'),
    [Input('save-excel-btn', 'n_clicks')],
    [State('table', 'data')],
    prevent_initial_call=True
)
def save_excel(n_clicks, rows):
    if n_clicks > 0:
        df_to_save = pd.DataFrame(rows)
        filepath = 'datasets/DOE_Input.xlsx'
        df_to_save.to_excel(filepath, index=False)
        return 'Dados salvos com sucesso!'
    return 'Salvar como Excel'

@app.callback(
    Output('create-doe-btn', 'children'),
    [Input('create-doe-btn', 'n_clicks')],
    [State('table', 'data')],
    prevent_initial_call=True
)
def create_doe(n_clicks, rows):
    if n_clicks > 0:
        df_to_save = pd.DataFrame(rows)
        filepath = 'datasets/DOE_Input.xlsx'
        df_to_save.to_excel(filepath, index=False)

        filepath = 'datasets/DOE_Input.xlsx'
        NumberOfSimulations = 1000
        Run_DOE(filepath, NumberOfSimulations)
        return 'Tabela DOE Gerada com sucesso!'

    return 'Criar DOE'

if __name__ == '__main__':
    app.run_server(host='127.0.0.2', port=8080, debug=False)

