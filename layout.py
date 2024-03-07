import copy

from dash import Dash, html, dcc

# define some general styles
overall_background_color = '#161d2f'
base_color = '#1d283c'

base_style = {
    'vertical-align': 'top',
    'background-color': base_color,
    'margin': '0px auto',
    'border-radius': '0px',
    'width': '95%',
    'display': 'block',
    'text-align': 'center',
    'color': 'white'
}

within_tab_style={
    'width': '95%',
    'margin': '10px auto',
    'padding-left': '10px',
    'padding-right': '10px',
    'display': 'flex',
    'align-items': 'center',
    'background-color': base_color
}

outer_tab_style={
    'width': '95%',
    'margin': '0px auto',
    'display': 'block',
    'text-align': 'center',
    'background-color': base_color,
    'color': 'white',
    'border-radius': '0px 0px 5px 5px',
    'box-shadow': '0px 0px 10px 0px rgba(0,0,0,0.1)',
    'margin-bottom':'10px'
}

selected_tab_style = {
    'background-color': base_color,
    'color': 'white'
}

basic_tab_style = {
    'background-color': '#f9f9f9',
    'color': overall_background_color
}

def show_warning():
    aux = html.Div(
        children=[
            html.Div(
                children=[
                    html.H1("Warning"),
                    html.H3(
                        "This is an exemplary toy dashboard. The Data is fictional and does not represent any real-world scenario."),
                ],
                style={'vertical-align': 'top', 'padding': '10px', 'margin': '20px auto'}
            )
        ],
        style={
            'width': '95%',
            'margin': '10px auto',
            'display': 'block',
            'text-align': 'center',
            'background-color': 'darkred',
            'color': 'white',
            'border-radius': '5px',
        }
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
        'background-color': overall_background_color,
        'border-radius': '5px',
        'box-shadow': '0px 0px 10px 0px rgba(0,0,0,0.1)'
    }

    if reverse:
        style['margin-left'] = 'auto'
        style['margin-right'] = '20px'
        return html.Div(children=[text, image], style=style)
    else:
        style['margin-left'] = '20px'
        style['margin-right'] = 'auto'
        return html.Div(children=[image, text], style=style)


def create_poverty_indicator_dropdown():
    aux = html.Div(
        children=[
            html.Div("Select a poverty indicator to be displayed on the map", style={'padding': '3px'}),
            # add the dropdown menu
            dcc.Dropdown(
                options=[
                    {'label': 'No indicator', 'value': 'no_indicator'},
                    {'label': 'Multidimensional poverty index', 'value': 'mpi_region'},
                    {'label': 'Multidimensional poverty headcount ratio', 'value': 'hr_poor'}
                ],
                value='no_indicator',
                id='poverty_indicator'
            )
        ],
        style={'position': 'absolute', 'top': '10px', 'left': '10px', 'zIndex': '1000',
               'background-color': 'rgba(255, 255, 255, 0.9)', 'padding': '20px',
               'border-radius': '10px'}
    )
    return aux

# --------------------------------- Entry Layout -----------------------------------------------------------------------
entry_layout = html.Div([
    dcc.ConfirmDialogProvider(
        children=html.Button('Enter', id='enter-btn'),
        id='confirm-enter',
        message='Are you sure you want to enter?',
    ),
    html.Div(id='output-container-button'),
])
# -------------------------------- BASE LAYOUT --------------------------------------------------------------------------
base_layout = (
    html.Div(
        children=[
            # add warning at the top
            show_warning(),

            # add the map
            html.Div(
                children=[
                    # add the map
                    html.Div(
                        children=[dcc.Graph(id='the_map', figure={})],
                    ),
                    # add the poverty dropdown menu
                    create_poverty_indicator_dropdown()
                ],
                style={'position': 'relative',
                       'vertical-align': 'top',
                       'text-align': 'center',
                       'margin': '5px auto',
                       'display': 'block',
                       'height': '50vh',
                       'width':'95%'}
            ),

            # add tabs to the dashboard, enabling the selection between stories and before and after images
            html.Div(
                id='tabs',
                children=[],
                style=outer_tab_style
            ),

            # add the footer
            html.Div(
                id='footer',
                children=[
                    html.P('This is toy dashboard. The Data is fictional and does not represent any real-world scenario.')
                ],
                style={'width': '100%',
                       'background-color': base_color,
                       'color': 'white',
                       'text-align': 'center',
                       'position': 'absolute',
                       'bottom': '0'}
            )
        ],
        style={'width': '100%',
               'min-height': '100vh',
               'background-color': overall_background_color,
               'position': 'relative',
               'font-family': 'Arial, sans-serif',
               'padding-bottom': '50px',
               'padding-top': '1px'}
    )
)

# --------------------------------- TABS -------------------------------------------------------------------------------

empty_tabs = dcc.Tabs(
    value='',
    children=[
        dcc.Tab(label='Project description',
                children=[show_placeholder(base_style)],
                style=basic_tab_style,
                selected_style=selected_tab_style),
        dcc.Tab(label='Before-After story',
                children=[show_placeholder(base_style)],
                style=basic_tab_style,
                selected_style=selected_tab_style),
        dcc.Tab(label='Testimonials',
                children=[show_placeholder(base_style)],
                style=basic_tab_style,
                selected_style=selected_tab_style),
        dcc.Tab(label='Project Progress',
                children=[show_placeholder(base_style)],
                style=basic_tab_style,
                selected_style=selected_tab_style)
    ]
)

filled_tabs = dcc.Tabs(
    value='tab_0',
    children=[
        dcc.Tab(
            id='tab_0',
            label='Project description',
            children=[
                html.Div(
                    children=[
                        html.Img(id='project_img',
                                 style={'height': '200px', 'width': 'auto', 'padding': '5px'}),
                        html.Div(id='project_text',
                                 children=[],
                                 style={'flex': '1', 'padding': '10px'}),
                    ],
                    style=within_tab_style
                )
            ],
            style=basic_tab_style,
            selected_style=selected_tab_style
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
                           'width': '95%',
                           'margin': '0px auto',
                           'margin-bottom': '20px',
                           'background-color': base_color}
                )
            ],
            style=basic_tab_style,
            selected_style=selected_tab_style
        ),
        dcc.Tab(label='Testimonials',
                children=[
                    html.Div([
                        generate_testimonial_box(image_id='testimonial_img_1', text_id='testimonial_text_1'),
                        generate_testimonial_box(image_id='testimonial_img_2', text_id='testimonial_text_2', reverse=True),
                        generate_testimonial_box(image_id='testimonial_img_3', text_id='testimonial_text_3')
                    ])
                ],
                style=basic_tab_style,
                selected_style=selected_tab_style
        ),
        dcc.Tab(
            label='Project Progress',
            children=[
                html.Div(
                    children=[
                        dcc.Graph(id='progress_fig', figure={}),
                        html.Div(
                            children=[
                                html.Div("Select a progress indicator", style={'padding': '3px', 'left': '10px', 'right': '10px'}),
                                # add the dropdown menu
                                dcc.Dropdown(
                                    id='dropdown_options',
                                    options=[],
                                    value='disbursement',
                                )
                            ],
                            style={'position': 'absolute',
                                   'top': '70px',
                                   'left': '100px',
                                   'zIndex': '1000',
                                   'background-color': 'rgba(255, 255, 255, 0.8)',
                                   'color': overall_background_color,
                                   'padding': '10px',
                                   'border-radius': '5px',
                                   'width': '250px'}
                        )
                    ],
                    style={'position': 'relative',
                           'padding': '10px 10px 10px 10px',
                           'border-radius': '0px 0px 0px 0px'}
                )
            ],
            style=basic_tab_style,
            selected_style=selected_tab_style
        )
    ]
)
