import os

import pandas as pd
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash

import dash_bio


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

DATAPATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

# Load dataset into a DataFrame
df = pd.read_csv(os.path.join(DATAPATH, 'data.csv'))

n_chr = 23  # number of chromosome pairs in humans
assert 'CHR' in df.columns
assert df['CHR'].max() == n_chr

# Trim down the data
DATASET = df.groupby('CHR').apply(lambda u: u.head(50))
DATASET = DATASET.droplevel('CHR').reset_index(drop=True)

# Feed the data to a function which creates a Manhattan Plot figure
fig = dash_bio.ManhattanPlot(DATASET)


def description():
    return 'Display genomic studies results sorted out by chromosome with ' \
           'this Manhattan plot.\
    Perfect to visualize genome-wide association studies (GWAS).'


def header_colors():
    return {
        'bg_color': '#0D76BF',
        'font_color': '#fff',
        'light_logo': True
    }


def layout():
    return html.Div(
        id='forna-body',
        className='app-body',
        children=[
            html.Div(
                id='forna-control-tabs',
                className='control-tabs',
                children=[
                    dcc.Tabs(id='forna-tabs', value='what-is', children=[
                        dcc.Tab(
                            label='About',
                            value='what-is',
                            children=html.Div(className='control-tab', children=[
                                html.H4(className='what-is', children='What is FornaContainer?'),
                                dcc.Markdown('''
                                FornaContainer is a force-directed graph that is
                                used to represent the secondary structure of nucleic
                                acids (i.e., DNA and RNA).

                                In the "Add New" tab, you can enter a sequence
                                by specifying the nucleotide sequence and the
                                dot-bracket representation of the secondary
                                structure.

                                In the "Sequences" tab, you can select which
                                sequences will be displayed, as well as obtain
                                information about the sequences that you have
                                already created.

                                In the "Colors" tab, you can choose to color each
                                nucleotide according to its base, the structural
                                feature to which it belongs, or its position in
                                the sequence; you can also specify a custom color
                                scheme.

                                The example RNA molecule shown has ID
                                [PDB_01019](http://www.rnasoft.ca/strand/show_results.php?molecule_ID=PDB_01019)
                                 on the [RNA Strand](http://www.rnasoft.ca/strand/) database.
                                ''')
                            ])
                        ),

                        dcc.Tab(
                            label='Add New',
                            value='add-sequence',
                            children=html.Div(className='control-tab', children=[
                                html.Div(
                                    title='Enter a dot-bracket string and a nucleotide sequence.',
                                    className='app-controls-block',
                                    children=[
                                        html.Div(className='fullwidth-app-controls-name',
                                                 children='Sequence'),
                                        html.Div(
                                            className='app-controls-desc',
                                            children='Specify the nucleotide sequence as a string.'
                                        ),
                                        dcc.Input(
                                            id='forna-sequence',
                                            placeholder=initial_sequences['PDB_01019']['sequence']
                                        ),

                                        html.Br(),
                                        html.Br(),

                                        html.Div(className='fullwidth-app-controls-name',
                                                 children='Structure'),
                                        html.Div(
                                            className='app-controls-desc',
                                            children='Specify the RNA secondary structure '
                                            'with a dot-bracket string.'
                                        ),
                                        dcc.Input(
                                            id='forna-structure',
                                            placeholder=initial_sequences['PDB_01019']['structure']
                                        ),

                                    ]
                                ),
                                html.Div(
                                    title='Change some boolean properties.',
                                    className='app-controls-block',
                                    children=[
                                        html.Div(className='app-controls-name',
                                                 children='Apply force'),
                                        daq.BooleanSwitch(
                                            id='forna-apply-force',
                                            on=True,
                                            color='#85002D'
                                        ),
                                        html.Div(
                                            className='app-controls-desc',
                                            children='Indicate whether the force-directed layout ' +
                                            'will be applied to this molecule.'
                                        ),
                                        html.Br(),
                                        html.Div(className='app-controls-name',
                                                 children='Circularize external'),
                                        daq.BooleanSwitch(
                                            id='forna-circularize-external',
                                            on=True,
                                            color='#85002D'
                                        ),
                                        html.Div(
                                            className='app-controls-desc',
                                            children='Indicate whether the external loops ' +
                                            'should be forced to be arranged in a circle.'
                                        ),
                                        html.Br(),
                                        html.Div(className='app-controls-name',
                                                 children='Avoid others'),
                                        daq.BooleanSwitch(
                                            id='forna-avoid-others',
                                            on=True,
                                            color='#85002D'
                                        ),
                                        html.Div(
                                            className='app-controls-desc',
                                            children='Indicate whether this molecule should ' +
                                            '"avoid" being close to other molecules.'
                                        ),
                                        html.Br(),
                                        html.Div(className='app-controls-name',
                                                 children='Label interval'),
                                        dcc.Slider(
                                            id='forna-label-interval',
                                            min=1,
                                            max=10,
                                            value=5,
                                            marks={i+1: str(i+1) for i in range(10)}
                                        ),
                                        html.Div(
                                            className='app-controls-desc',
                                            children='Indicate how often nucleotides are ' +
                                            'labelled with their number.'
                                        )

                                    ]
                                ),

                                html.Div(
                                    className='app-controls-block',
                                    children=[
                                        html.Div(className='fullwidth-app-controls-name',
                                                 children='ID'),
                                        html.Div(
                                            className='app-controls-desc',
                                            children='Specify a unique ID for this sequence.'
                                        ),
                                        dcc.Input(id='forna-id', placeholder='PDB_01019')
                                    ]
                                ),

                                html.Hr(),

                                html.Div(id='forna-error-message'),
                                html.Button(id='forna-submit-sequence', children='Submit sequence'),
                            ])
                        ),
                        dcc.Tab(
                            label='Sequences',
                            value='show-sequences',
                            children=html.Div(className='control-tab', children=[
                                html.Div(
                                    className='app-controls-block',
                                    children=[
                                        html.Div(
                                            className='fullwidth-app-controls-name',
                                            children='Sequences to display'
                                        ),
                                        html.Div(
                                            className='app-controls-desc',
                                            children='Choose the sequences to display by ID.'
                                        ),
                                        html.Br(),
                                        dcc.Dropdown(
                                            id='forna-sequences-display',
                                            multi=True,
                                            clearable=True,
                                            value=['PDB_01019']
                                        )
                                    ]
                                ),
                                html.Hr(),
                                html.Div(
                                    className='app-controls-block',
                                    children=[
                                        html.Div(
                                            className='app-controls-block',
                                            children=[
                                                html.Div(
                                                    className='fullwidth-app-controls-name',
                                                    children='Sequence information by ID'
                                                ),
                                                html.Div(
                                                    className='app-controls-desc',
                                                    children='Search for a sequence by ID ' +
                                                    'to get more information.'
                                                ),
                                                html.Br(),
                                                dcc.Dropdown(
                                                    id='forna-sequences-info-search',
                                                    clearable=True
                                                ),
                                                html.Br(),
                                                html.Div(id='forna-sequence-info')
                                            ]
                                        )
                                    ]
                                )
                            ])
                        ),
                        dcc.Tab(
                            label='Colors',
                            value='colors',
                            children=html.Div(className='control-tab', children=[
                                html.Div(
                                    className='app-controls-name',
                                    children='Color scheme'
                                ),
                                dcc.Dropdown(
                                    id='forna-color-scheme',
                                    options=[
                                        {'label': color_scheme,
                                         'value': color_scheme}
                                        for color_scheme in [
                                            'sequence', 'structure', 'positions', 'custom'
                                        ]
                                    ],
                                    value='sequence',
                                    clearable=False
                                ),
                                html.Div(
                                    className='app-controls-desc',
                                    id='forna-color-scheme-desc',
                                    children='Choose the color scheme to use.'
                                ),
                                html.Div(
                                    id='forna-custom-colorscheme',
                                    className='app-controls-block',
                                    children=[
                                        html.Hr(),
                                        html.Div(
                                            className='app-controls-name',
                                            children='Molecule name'
                                        ),
                                        dcc.Dropdown(
                                            id='forna-custom-colors-molecule'
                                        ),
                                        html.Div(
                                            className='app-controls-desc',
                                            children='Select the sequence to which the custom ' +
                                            'color scheme will be applied. If none is selected, ' +
                                            'the color scheme will be applied to all molecules.'
                                        ),
                                        html.Br(),
                                        html.Div(
                                            className='app-controls-name',
                                            children='Coloring range'
                                        ),
                                        daq.ColorPicker(
                                            id='forna-color-low',
                                            label='Low',
                                            labelPosition='top',
                                            value={'hex': '#BE0000'}
                                        ),
                                        daq.ColorPicker(
                                            id='forna-color-high',
                                            label='High',
                                            labelPosition='top',
                                            value={'hex': '#336AFF'}
                                        ),
                                        html.Div(
                                            className='fullwidth-app-controls-name',
                                            children='Coloring domain'
                                        ),
                                        html.Div(
                                            className='app-controls-desc',
                                            children='Specify a minimum and maximum value ' +
                                            'which will be used to calculate intermediate ' +
                                            'colors for nucleotides that have a numerical ' +
                                            'value specified below.'
                                        ),
                                        html.Br(),
                                        dcc.Input(
                                            id='forna-color-domain-low',
                                            type='number',
                                            value=1
                                        ),
                                        dcc.Input(
                                            id='forna-color-domain-high',
                                            type='number',
                                            value=100
                                        ),
                                        html.Br(),
                                        html.Br(),
                                        html.Div(
                                            className='fullwidth-app-controls-name',
                                            children='Colors map'
                                        ),
                                        html.Div(
                                            className='app-controls-desc',
                                            children='Specify the colors for each ' +
                                            'nucleotide by entering the position of ' +
                                            'the nucleotide into the left input box, ' +
                                            'and either a) a string representation ' +
                                            'of a color or b) a number within the ' +
                                            'range specified above. Then, press the ' +
                                            '"Submit" button,'
                                        ),
                                        html.Br(),
                                        dcc.Input(
                                            id='forna-color-map-nucleotide',
                                            type='number',
                                            min=1,
                                            placeholder=1
                                        ),
                                        dcc.Input(
                                            id='forna-color-map-color',
                                            placeholder='green'
                                        ),
                                        html.Br(),
                                        html.Br(),
                                        html.Button(
                                            id='forna-submit-custom-colors',
                                            children='Submit'
                                        )
                                    ]
                                )
                            ])
                        )
                    ])
                ]),
            html.Div(id='forna-container', children=[
                dash_bio.FornaContainer(
                    id='forna',
                    height=500,
                    width=500
                )
            ]),

            dcc.Store(id='forna-sequences', data=initial_sequences),
            dcc.Store(id='forna-custom-colors')
        ]
    )


def callbacks(_app):
    @_app.callback(
        Output('mhp-graph', 'figure'),
        [
            Input('mhp-slider-genome', 'value'),
            Input('mhp-slider-indic', 'value'),
        ]
    )
    def update_graph(slider_genome, slider_indic):
        """update the data sets upon change the genomewideline value"""
        return dash_bio.ManhattanPlot(
            DATASET,
            genomewideline_value=float(slider_genome),
            suggestiveline_value=float(slider_indic),
        )




if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
