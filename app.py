from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State

# import additional packages
import pandas as pd
import pickle

# load the app modules
import data
from layout import base_layout, empty_tabs, filled_tabs
from callbacks import display_poverty, display_click_data, update_progress_figure, get_testimonials, update_tab_layout

# ------------------------------- Define the global variables ----------------------------------------------------------
# define the global data path
data_pth = "Data/"

#----------------- Load external data ----------------------------------------------------------------------------------
# define the data paths
cntry_code = 'KHM' # cambodia country code
pvty_pth = f'{data_pth}/wealth_data/subnational_mpi.csv'
geo_pth = f'{data_pth}/geo_boundaries/gadm41_KHM_1.json'

project_pth = f'{data_pth}/cambodia_projects.csv'
indicator_pth = f'{data_pth}/indicators.csv'
testimonials_pth = f'{data_pth}/testimonials.csv'
img_pth = pth = f'{data_pth}/image_data.pkl'

# load the data
pvty_data = data.import_geo_poverty_data(pvty_pth,geo_pth,cntry_code)

# load the project data
project_df = data.import_project_data(project_pth)

# load the testimonial data
testimonial_df = pd.read_csv(testimonials_pth)
testimonial_dict = dict(zip(testimonial_df.testimonial_id, testimonial_df.testimonial))

# load the image data
with(open(img_pth, 'rb')) as f:
    image_data = pickle.load(f)

# load the indicator data
indicator_df = data.import_indicator_df(indicator_pth)

# ------------------------------- Initialise the dashboard -------------------------------------------------------------

# initialise the app
app = Dash(__name__, suppress_callback_exceptions=True)

# define the base layout
app.layout = base_layout

# ------------------------------- Define the callbacks -----------------------------------------------------------------
# poverty map callback
app.callback(
    Output('the_map', 'figure'),
    Input('poverty_indicator', 'value'),
)(lambda value: display_poverty(value, project_df, pvty_data))

# ToDO: change the layout of the map points as soon as the user clicks on it

# change the layout of the page as soon as the user clicks on a point
app.callback(
    Output('tabs', 'children'),
    Input('the_map', 'clickData')
)(lambda clickData: update_tab_layout(clickData, empty_tabs, filled_tabs))


# callback for the testimonial tab
app.callback(
    [
        Output('testimonial_img_1', 'src'),
        Output('testimonial_text_1', 'children'),
        Output('testimonial_img_2', 'src'),
        Output('testimonial_text_2', 'children'),
        Output('testimonial_img_3', 'src'),
        Output('testimonial_text_3', 'children')
    ],
    Input('the_map', 'clickData')
)(lambda clickData: get_testimonials(clickData, testimonial_dict, image_data))


app.callback(
    [
        Output('project_img', 'src'),
        Output('project_text', 'children'),
        Output('before_img', 'src'),
        Output('after_img', 'src'),
        Output('before_after_text', 'children'),
        Output('dropdown_options', 'options')
    ],
    Input('the_map', 'clickData')
)(lambda clickData: display_click_data(clickData, project_df, image_data, indicator_df))

app.callback(
    Output('progress_fig', 'figure'),
    [
        Input('dropdown_options', 'value'),
        Input('the_map', 'clickData')
    ]
)(lambda value, clickData: update_progress_figure(value, clickData, indicator_df))

# ------------------------- run the dashboard ---------------------------------------------------------------------------
if __name__ == '__main__':
    #app.run_server(host="0.0.0.0")
    app.run_server(debug = True)
