import copy

from dash import Dash, html, dcc

base_style = {'vertical-align': 'top',
             'background-color': 'beige',
             'margin': '10px auto',
             'border-radius': '10px',
             'box-shadow': '0px 0px 10px 0px rgba(0,0,0,0.1)',
             'width': '90%',
             'display': 'block',
             'text-align': 'center',
             'color': 'darkslategray'}


def show_warning(base_style):
    style = copy.deepcopy(base_style)
    style['background-color'] = 'darkred'
    style['color'] = 'white'
    aux = html.Div(
        children=[
            html.Div(
                children=[
                    html.H1("Warning"),
                    html.H3("This is an exemplary toy dashboard. The Data is fictional and does not represent any real-world scenario."),
                ],
                style={'vertical-align': 'top', 'padding': '10px'}
            )
        ],
        style = style
    )
    return aux



def show_placeholder(base_style):
    aux = html.Div(
        children=[
            html.Div(
                children=[
                    html.H2("No project selected"),
                    html.H3("Please select a project on the map to obtain more information on the projects")
                ],
                style={'vertical-align': 'top', 'padding': '10px'}
            )
        ],
        style=base_style
    )
    return aux


def generate_testimonial_box(image_id, text_id, reverse=False):
    image = html.Img(
        id=image_id,
        style={'height': '100px', 'width': 'auto', 'padding': '5px'}
    )
    text = html.Div(
        children=[html.Div(id=text_id, children=[])],
        style={'flex': '1', 'padding': '10px'}
    )
    style = {
        'width': '90%',
        'margin': '10px auto',
        'display': 'flex',
        'align-items': 'center',
        'background-color': 'lightblue',
        'border-radius': '10px',
        'box-shadow': '0px 0px 10px 0px rgba(0,0,0,0.1)'
    }

    if reverse:
        style['margin-left'] = 'auto'
        style['margin-right'] = '10px'
        return html.Div(children=[text, image], style=style)
    else:
        style['margin-left'] = '10px'
        style['margin-right'] = 'auto'
        return html.Div(children=[image, text], style=style)


base_layout = html.Div(
    children=[
        show_warning(base_style),
        html.Div([
            html.Div(
                children=[dcc.Graph(id='the_map', figure={}, style={'height': '60vh'})],
                style={'width': '100%', 'height': '60vh', 'vertical-align': 'top'}
            ),
            html.Div([
                html.Div("Select a poverty indicator to be displayed on the map",
                         style={'padding': '3px'}),
                dcc.Dropdown(
                    options=[
                        {'label': 'No indicator', 'value': 'no_indicator'},
                        {'label': 'Multidimensional poverty index', 'value': 'mpi_region'},
                        {'label': 'Multidimensional poverty headcount ratio', 'value': 'hr_poor'}
                    ],
                    value='no_indicator',
                    id='poverty_indicator'
                )],
                style={'position': 'absolute', 'top': '10px', 'left': '10px', 'zIndex': '1000',
                       'background-color': 'rgba(255, 255, 255, 0.9)', 'padding': '20px', 'border-radius': '10px'}
            )
        ], style={'position': 'relative'}),

        # add tabs to the dashboard, enabling the selection between stories and before and after images
        html.Div(
            id='tabs',
            children=[]
        )
    ]
)

empty_tabs = dcc.Tabs(
    value='',
    children=[
        dcc.Tab(label='Project description',
                children=[show_placeholder(base_style)]),
        dcc.Tab(label='Before-After story',
                children=[show_placeholder(base_style)]),
        dcc.Tab(label='Testimonials',
                children=[show_placeholder(base_style)]),
        dcc.Tab(label='Project Progress',
                children=[show_placeholder(base_style)])
    ]
)

filled_tabs = dcc.Tabs([
    dcc.Tab(
        label='Project description',
        children=[
            html.Div(
                id='tab_0',
                children=[
                    html.Img(id='project_img',
                             style={'height': '200px', 'width': 'auto', 'padding': '5px'}),
                    html.Div(id='project_text',
                             children=[],
                             style={'flex': '1', 'padding': '10px'}),
                ],
                style={
                    'width': '90%',
                    'margin': '10px auto',
                    'display': 'flex',
                    'align-items': 'center',
                    'background-color': 'lightblue',
                    'border-radius': '10px',
                    'box-shadow': '0px 0px 10px 0px rgba(0,0,0,0.1)'
                }
            )
        ]
    ),
    dcc.Tab(
        label='Before-After story',
        children=[
            html.Div(
                id='big_block',
                children=[
                    html.Div(
                        id='first_block',
                        children=[
                            html.H2(f"Before", style={'textAlign': 'center'}),
                            html.Img(id='before_img',
                                     style={'height': '300px', 'width': 'auto', 'padding': '5px',
                                            'margin': '0px auto'}),
                        ],
                        style={'width': '48%', 'display': 'inline-block', 'vertical-align': 'top',
                               'text-align': 'center'}
                    ),
                    html.Div(
                        id='second_block',
                        children=[
                            html.H2(f"After", style={'textAlign': 'center'}),
                            html.Img(id='after_img',
                                     style={'height': '300px', 'width': 'auto', 'padding': '5px'}),
                        ],
                        style={'width': '48%', 'display': 'inline-block', 'vertical-align': 'top',
                               'text-align': 'center'}
                    ),
                    html.Div(id='before_after_text', children=[],
                             style={'padding': '20px'})
                ],
                style={'vertical-align': 'top',
                       'width': '90%',
                       'margin': '0px auto',
                       'margin-bottom': '20px',
                       'box-shadow': '0px 0px 3px rgba(0,0,0,0.1)',
                       'border-radius': '0px 0px 10px 10px',
                       'background-color': 'beige'}
            )
        ]
    ),
    dcc.Tab(label='Testimonials', children=[
        html.Div([
            generate_testimonial_box(image_id='testimonial_img_1', text_id='testimonial_text_1'),
            generate_testimonial_box(image_id='testimonial_img_2', text_id='testimonial_text_2', reverse=True),
            generate_testimonial_box(image_id='testimonial_img_3', text_id='testimonial_text_3')
        ])
    ]),
    dcc.Tab(label='Project Progress', children=[
        html.Div([
            dcc.Graph(id='progress_fig', figure={}),
            html.Div([
                html.Div("Select a progress indicator",
                         style={'padding': '3px', 'left': '10px', 'right': '10px'}),
                dcc.Dropdown(
                    id='dropdown_options',
                    options=[],
                    value='disbursement',
                )
            ],
                style={'position': 'absolute', 'top': '40px', 'left': '70px', 'zIndex': '1000',
                       'background-color': 'rgba(255, 255, 255, 0.9)',
                       'padding': '10px', 'border-radius': '10px',
                       'width': '300px'}
            )
        ],
            style={'position': 'relative', 'padding': '0px 10px 0px 10px',
                   'border-radius': '0px 0px 10px 10px',
                   'box-shadow': '0px 0px 10px rgba(0,0,0,0.1)'}
        ),
    ]),
])
