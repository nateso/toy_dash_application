import copy

from dash import Dash, html, dcc

# define some general styles
overall_background_color = '#161d2f'
base_color = '#1d283c'
side_panel_color = '#f5f7f7'

base_style = {
    'vertical-align': 'top',
    'margin': '0px auto',
    'border-radius': '0px',
    'width': '95%',
    'display': 'block',
    'text-align': 'center',
}

within_tab_style = {
    'width': '95%',
    'margin': '10px auto',
    'padding-left': '10px',
    'padding-right': '10px',
    'display': 'flex',
    'align-items': 'center',
    'background-color': side_panel_color,
}

outer_tab_style = {
    'width': '95%',
    'margin': '0px auto',
    'text-align': 'center',
    'border-radius': '0px 0px 5px 5px',
    'box-shadow': '0px 0px 10px 0px rgba(0,0,0,0.1)',
    'margin-bottom': '10px',
    'background-color': side_panel_color,
}

selected_tab_style = {
    'background-color': side_panel_color,
}

# basic_tab_style = {
#     'background-color': '#f9f9f9',
#     'color': overall_background_color
# }


warning_div = html.Div(
    children=[
        html.Div(
            children=[
                html.H4("Warning", style={'color': 'white'}),
                html.H6(
                    "This is an exemplary toy dashboard. The Data is fictional and does not represent any real-world scenario.",
                    style={'color': 'white',
                           'padding-bottom': '5px'}
                ),
            ],
            style={'vertical-align': 'top',
                   'padding-top': '10px',
                   'margin': '0px auto'}
        )
    ],
    style={
        'width': '95%',
        'margin': '5px auto',
        'display': 'block',
        'text-align': 'center',
        'background-color': 'darkred',
        'border-radius': '5px',
    }
)


def show_placeholder(base_style):
    aux = html.Div(
        children=[
            html.Div(
                children=[
                    html.H5("No project selected"),
                    html.H6("Please select a project on the map to obtain more information on the projects")
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
        style={'flex': '1', 'padding': '10px', 'text-align': 'left', 'line-height': '1.25'}
    )
    style = {
        'width': '90%',
        'margin': '20px auto',
        'display': 'flex',
        'align-items': 'center',
        'background-color': '#f9f9f9',
        'border-radius': '5px',
        'box-shadow': '0px 0px 10px 0px rgba(0,0,0,0.2)'
    }

    if reverse:
        style['margin-left'] = 'auto'
        style['margin-right'] = '20px'
        return html.Div(children=[text, image], style=style)
    else:
        style['margin-left'] = '20px'
        style['margin-right'] = 'auto'
        return html.Div(children=[image, text], style=style)


# --------------------------------- Entry Layout -----------------------------------------------------------------------
entry_layout = html.Div([
    dcc.ConfirmDialogProvider(
        children=html.Button('Enter', id='enter-btn'),
        id='confirm-enter',
        message='Are you sure you want to enter?',
    ),
    html.Div(id='output-container-button')
])

# project name etc
project_title = html.Div(
    children=[
        html.Div(
            children=[
                html.H3('Mapping for Transparency')
            ],
            style={
                'border-bottom': '1px solid darkslategray',
                'padding': '20px 0px 0px 0px',
                'margin-left': '10px',
                'margin-right': '10px'
            }
        ),
        html.Div(
            children=[
                html.P('A project by the Data Economy Team at GIZ')
            ],
            style={
                'padding': '10px 0px 0px 0px',
                'margin-left': '20px',
                'margin-right': '20px'
            }
        )
    ]
)

# -------------------------------- Dropdown menus --------------------------------------------------------------------------

basic_dd_style = {
    'padding': '10px 20px 0px 20px',
    'text-align': 'left',
    'line-height': '1'
}

country_dropdown = html.Div(
    children=[
        html.Div("Select a country", style={'padding': '3px'}),
        # add the dropdown menu
        dcc.Dropdown(
            options=[
                {'label': 'All countries', 'value': 'all'},
                {'label': 'Cambodia', 'value': 'KHM'},
            ],
            value='KHM',
            id='country_dropdown'
        )
    ],
    style=basic_dd_style
)

project_dropdown = html.Div(
    children=[
        html.Div("Select a project topic", style={'padding': '3px'}),
        # add the dropdown menu
        dcc.Dropdown(
            options=[
                {'label': 'All', 'value': 'all'},
                {'label': 'Education', 'value': 'education'},
                {'label': 'Infrastructure', 'value': 'infrastructure'},
            ],
            value='infrastructure',
            id='topic_dropdown',
            multi=True
        )
    ],
    style=basic_dd_style
)

poverty_dropdown = html.Div(
    children=[
        html.Div("Select a poverty indicator", style={'padding': '3px'}),
        # add the dropdown menu
        dcc.Dropdown(
            options=[
                {'label': 'Multidimensional poverty index', 'value': 'mpi_region'},
                {'label': 'Multidimensional poverty headcount ratio', 'value': 'hr_poor'}
            ],
            value='',
            id='poverty_dropdown'
        )
    ],
    style=basic_dd_style
)

# --------------------------------- Side Panel --------------------------------------------------------------------------
basic_side_div_style = {
    'padding': '20px'
}

side_panel = html.Div(
    children=[
        project_title,
        country_dropdown,
        project_dropdown,
        poverty_dropdown
    ],
    style={'width': '20%',
           'min-height': '100vh',
           'text-align': 'center',
           'position': 'fixed',
           'top': '0',
           'left': '0',
           'overflow-y': 'auto',
           'background-color': side_panel_color,
           'shadow': '10px 0px 10px 0px rgba(0,0,0,0.1)'}
)

footer = html.Div(
    id='footer',
    children=[
        html.H6(
            'This is a toy dashboard. The Data is fictional and does not represent any real-world scenario.'
        )
    ],
    style={
        'text-align': 'center',
        'position': 'relative',
        'background-color': side_panel_color,
        'padding': '10px',
        'bottom': '0',
        'width': '80%',
        'margin-left': '20%',
    }
)

content = (
    html.Div(
        children=[
            # add warning at the top
            warning_div,

            # add the map
            html.Div(
                children=[
                    dcc.Graph(id='the_map', figure={}, style={'height': '50vh'})
                ],
                style={
                    'vertical-align': 'top',
                    'margin': '10px auto',
                    'height': '50vh',
                    'width': '95%',
                    'shadow': '0px 0px 10px 0px rgba(0,0,0,0.2)'
                }
            ),

            # add tabs to the dashboard, enabling the selection between stories and before and after images
            html.Div(
                id='tabs',
                children=[],
                style=outer_tab_style
            ),
        ],
        style={
            'display': 'flex',
            'flex-direction': 'column',
            'width': '80%',
            'min-height': 'calc(100vh - 50px)',
            'margin-left': '20%',
            'overflow-y': 'auto'
        }
    )
)

main_panel = html.Div(
    children=[
        content,
        footer
    ],
)

base_layout = html.Div(
    children=[
        side_panel,
        main_panel
    ],
    style={'display': 'flex', 'flex-direction': 'column', 'justify-content': 'space-between'}
)
# --------------------------------- TABS -------------------------------------------------------------------------------

empty_tabs = dcc.Tabs(
    value='tab_0',
    children=[
        dcc.Tab(value='tab_0',
                label='Project description',
                children=[show_placeholder(base_style)],
                selected_style=selected_tab_style),
        dcc.Tab(label='Before-After story',
                children=[show_placeholder(base_style)],
                selected_style=selected_tab_style),
        dcc.Tab(label='Testimonials',
                children=[show_placeholder(base_style)],
                selected_style=selected_tab_style),
        dcc.Tab(label='Project Progress',
                children=[show_placeholder(base_style)],
                selected_style=selected_tab_style)
    ]
)

filled_tabs = dcc.Tabs(
    value='tab_0',
    children=[
        dcc.Tab(
            value='tab_0',
            label='Project description',
            children=[
                html.Div(
                    children=[
                        html.Img(id='project_img',
                                 style={
                                     'height': '200px',
                                     'width': 'auto',
                                     'padding': '0px 0px 0px 0px',
                                     'vertical-align': 'top'
                                 }),
                        html.Div(id='project_text',
                                 children=[],
                                 style={
                                     'flex': '1',
                                     'padding': '10px',
                                     'text-align': 'left',
                                     'line-height': '1.25'
                                 }
                                 )
                    ],
                    style=within_tab_style
                )
            ],
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
                                html.H2(f"Before", style={'textAlign': 'center', 'margin-top': '10px'}),
                                html.Img(id='before_img',
                                         style={'height': 'auto', 'width': '70%', 'padding': '5px',
                                                'margin': '0px auto'}),
                            ],
                            style={'width': '48%', 'display': 'inline-block', 'vertical-align': 'top',
                                   'text-align': 'center'}
                        ),
                        html.Div(
                            id='second_block',
                            children=[
                                html.H2(f"After", style={'textAlign': 'center', 'margin-top': '10px'}),
                                html.Img(id='after_img',
                                         style={'height': 'auto', 'width': '70%', 'padding': '5px'}),
                            ],
                            style={'width': '48%', 'display': 'inline-block', 'vertical-align': 'top',
                                   'text-align': 'center'}
                        ),
                        html.Div(id='before_after_text', children=[],
                                 style={'padding': '20px'})
                    ],
                    style={
                        'vertical-align': 'top',
                        'width': '95%',
                        'margin': '0px auto',
                        'margin-bottom': '20px',
                        'text-align': 'left',
                        'text-height': '1.25'
                    }
                )
            ],
            selected_style=selected_tab_style
        ),
        dcc.Tab(label='Testimonials',
                children=[
                    html.Div([
                        generate_testimonial_box(image_id='testimonial_img_1', text_id='testimonial_text_1'),
                        generate_testimonial_box(image_id='testimonial_img_2', text_id='testimonial_text_2',
                                                 reverse=True),
                        generate_testimonial_box(image_id='testimonial_img_3', text_id='testimonial_text_3')
                    ])
                ],
                selected_style=selected_tab_style
                ),
        dcc.Tab(
            label='Project Progress',
            children=[
                html.Div(
                    children=[
                        dcc.Graph(id='progress_fig', figure={}, style={'height': '300px'}),
                        html.Div(
                            children=[
                                html.Div("Select a progress indicator",
                                         style={'padding': '3px', 'left': '10px', 'right': '10px'}),
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
                                   'width': '300px'}
                        )
                    ],
                    style={'position': 'relative',
                           'padding': '10px 10px 10px 10px',
                           'border-radius': '0px 0px 0px 0px'}
                )
            ],
            selected_style=selected_tab_style
        )
    ]
)
