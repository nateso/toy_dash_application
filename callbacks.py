import numpy as np
import pandas as pd
from dash import html
import plotly.express as px
from PIL import Image
import io
import base64

import warnings
warnings.simplefilter("ignore", category=FutureWarning)

# define some general styles
overall_background_color = '#f5f7f7'
base_color = '#f5f7f7'


# Define the callback function to deal with the map
def display_poverty(value, project_df, khm_01):
    hover_template = (
        "<b>%{customdata[1]}</b><br>"
        "Town: %{customdata[2]}<br>"
        "Funding: %{customdata[3]}<br>"
        "Start Date: %{customdata[4]}<br>"
        "End Date: %{customdata[5]}<extra></extra>"
    )

    hover_template_choropleth = (
        "<b>%{customdata[0]}</b><br>"
        "MPI: %{customdata[1]}<br>"
        "MPI HR: %{customdata[2]}%<extra></extra>"
    )

    map_style = 'carto-positron'

    scatter_fig = px.scatter_mapbox(
            data_frame=project_df,
            lat='lat',
            lon='lon',
            hover_name='name',
            hover_data=['project_id', 'name', 'location', 'funding_format', 'start', 'end'],
            custom_data=['project_id'],
            center={'lat': 12, 'lon': 105},
            zoom=5,
            mapbox_style=map_style
        )
    scatter_fig.update_traces(
        hovertemplate=hover_template,
        hoverlabel=dict(
            bgcolor=base_color,
            font=dict(color='darkslategray')
        ),
        marker=dict(
            color='red',
            size=10
        )
    )

    if value != 'no_indicator':
        fig = px.choropleth_mapbox(
            khm_01,
            geojson=khm_01['geometry'],
            locations=khm_01.index,
            color=value,
            mapbox_style=map_style,
            opacity=.3,
            center={'lat': 12, 'lon': 105},
            zoom=5,
            labels={
                'mpi_region': 'MPI',
                'hr_poor': '% Poor',
            },
            hover_data=['subnational_region', 'mpi_region', 'hr_poor', 'GID_0'],
            color_continuous_scale='Viridis'
        )
        fig.update_traces(
            hovertemplate=hover_template_choropleth
        )
        fig.add_trace(scatter_fig.data[0])
    else:
        fig = scatter_fig

    fig.update_layout(
        clickmode = 'event+select',
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        paper_bgcolor=base_color,
        plot_bgcolor=base_color,
        font={'color': 'darkslategray'},
        legend=dict(
            bgcolor=base_color,
            font={'color':'darkslategray'}
        )
    )
    return fig


# define a callback function to update the layout of the tabs once a point is clicked
def update_tab_layout(clickData, empty_tabs, filled_tabs):
    if clickData:
        customdata = clickData['points'][0]['customdata']
        if 'KHM' not in customdata:
            return filled_tabs
        else:
            return empty_tabs
    else:
        return empty_tabs

def plot_static_image(image_data):
    height, width, _ = image_data.shape
    fig = px.imshow(image_data)
    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        xaxis=dict(visible=False),
        yaxis=dict(visible=False)
    )
    return fig


def get_img_src(image_data):
    pil_img = Image.fromarray(image_data)
    buff = io.BytesIO()
    pil_img.save(buff, format="PNG")
    encoded = base64.b64encode(buff.getvalue()).decode("utf-8")
    return f"data:image/png;base64,{encoded}"


# callback function to populate the testimonial tab
def get_testimonials(clickData, testimonial_dict, image_data):

    clicked_point_id = clickData['points'][0]['customdata'][0]

    # get the testimonial data
    out = []
    # loop over all testimonials
    for i in range(1,4):
        # get the testimonial data
        testimonial_id = f'{clicked_point_id}_testimonial_0{i}'
        # first the image, then the text
        out.append(get_img_src(image_data[testimonial_id]))
        out.append(testimonial_dict[testimonial_id])

    # return tuple
    return tuple(out)


# Second callback function to deal with the interactive points

def display_click_data(clickData, project_df, description_dict, before_after_dict, image_data, indicator_df):
    # get the clicked point id
    clicked_point_id = clickData['points'][0]['customdata'][0]

    # get the project name
    clicked_name = str(project_df.name[project_df.project_id == clicked_point_id].reset_index(drop=True)[0])

    # get the project description
    proj_des = description_dict[clicked_point_id]
    project_text = html.Div([
        html.H3(f"{clicked_name}"),
        html.P(proj_des)
    ])

    # get the before after text
    before_after = before_after_dict[clicked_point_id]
    before_after_text = before_after

    #------ get the images -------------
    # get the proj img
    proj_img = get_img_src(image_data[clicked_point_id])

    # get the before image
    before_id = clicked_point_id + '_before'
    before_img = get_img_src(image_data[before_id])

    # get the after image
    after_id = clicked_point_id + '_after'
    after_img = get_img_src(image_data[after_id])

    # get the labels of the dropdown options
    indicator_1_name = indicator_df.indicator_name_1[indicator_df.project_id == clicked_point_id].values[0]
    indicator_2_name = indicator_df.indicator_name_2[indicator_df.project_id == clicked_point_id].values[0]

    ##### add the different dropdown options
    dropdown_options = [
        {'label': 'Disbursements', 'value': 'disbursement'},
        {'label': indicator_1_name, 'value': "indicator_1"},
        {'label': indicator_2_name, 'value': "indicator_2"}
    ]

    return proj_img, project_text, before_img, after_img, before_after_text, dropdown_options


# Third callback function to generate the plot on project progress
def update_progress_figure(value, clickData, indicator_df):

    clicked_point_id = clickData['points'][0]['customdata'][0]

    # get the project data, the disbursement data and the indicator data
    indicator_data = indicator_df[indicator_df.project_id == clicked_point_id].reset_index(drop=True)
    indicator_data['Total'] = indicator_data[value].cumsum(axis=0)

    indicator_data['Date'] = pd.to_datetime(indicator_data['ts'])

    # get the indicator goal (in a dirty way)
    indicator_goal = list(indicator_data['Total'])[-1]

    # get the y label
    ind_1_lab = indicator_data.indicator_name_1.values[0]
    ind_2_lab = indicator_data.indicator_name_2.values[0]

    # define the y lab
    if '1' in value:
        y_lab = ind_1_lab
    elif '2' in value:
        y_lab = ind_2_lab
    else:
        y_lab = 'Disbursements'

    x_lab = 'Date'

    fig = px.line(indicator_data, 'Date', 'Total', hover_data = ['Total'])
    fig.data[0].update(mode='markers+lines')
    fig.add_hline(y=indicator_goal, line_dash="dash", line_color="green", annotation_text=f"Project Goal",
                  annotation_position="top right")

    fig.update_xaxes(title_text=x_lab)
    fig.update_yaxes(title_text=y_lab)
    fig.update_layout(
        margin={"r": 30, "t": 30, "l":30, "b": 30},
        paper_bgcolor=overall_background_color,
        plot_bgcolor=overall_background_color,
        font=dict(color="darkslategray"),
        hovermode="x unified"
    )
    return fig
