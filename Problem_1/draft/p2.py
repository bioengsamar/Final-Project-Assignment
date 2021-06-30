# from __future__ import division
from plotly.offline import iplot
import plotly.express as px
import plotly.graph_objects as go
# init_notebook_mode()1
from bubbly.bubbly import bubbleplot, add_slider_steps, make_grid, set_layout, get_trace
import re
from datetime import datetime
import pandas as pd
import numpy as np

date_pattern = re.compile(r"\d{1,2}/\d{1,2}/\d{2}")
def reformat_dates(col_name: str) -> str:
    try:
        return date_pattern.sub(datetime.strptime(col_name, "%m/%d/%y").strftime("%d/%m/%Y"), col_name, count=1)
    except ValueError:
        return col_name

confirmed_cases_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data" \
                      "/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
deaths_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data" \
             "/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
recovered_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data" \
             "/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"

renamed_columns_map = {
    "Country/Region": "country",
    "Province/State": "location",
    "Lat": "latitude",
    "Long": "longitude"
}

cols_to_drop = ["location", "latitude", "longitude"]

confirmed_cases_df = (
    pd.read_csv(confirmed_cases_url)
    .rename(columns=renamed_columns_map)
    .rename(columns=reformat_dates)
    .drop(columns=cols_to_drop)
)

deaths_df = (
    pd.read_csv(deaths_url)
    .rename(columns=renamed_columns_map)
    .rename(columns=reformat_dates)
    .drop(columns=cols_to_drop)
)

recovered_df = (
    pd.read_csv(recovered_url)
    .rename(columns=renamed_columns_map)
    .rename(columns=reformat_dates)
    .drop(columns=cols_to_drop)
)

geo_data_df = confirmed_cases_df[["country"]].drop_duplicates()
country_codes_df = (
    pd.read_csv(
        "country_code_mapping.csv",
        usecols=["country", "alpha-3_code"],
        index_col="country")
)
geo_data_df = geo_data_df.join(country_codes_df, how="left", on="country").set_index("country")
geo_data_df[(pd.isnull(geo_data_df["alpha-3_code"])) & (~geo_data_df.index.isin(
    ["Diamond Princess", "MS Zaandam", "West Bank and Gaza"]
))]

dates_list = (
    confirmed_cases_df.filter(regex=r"(\d{2}/\d{2}/\d{4})", axis=1)
    .columns
    .to_list()
)

cases_by_date = {}
for date in dates_list:
    confirmed_cases_day_df = (
        confirmed_cases_df
        .filter(like=date, axis=1)
        .rename(columns=lambda col: "confirmed_cases")
    )
    deaths_day_df = deaths_df.filter(like=date, axis=1).rename(columns=lambda col: "deaths")
    recovered_day_df = recovered_df.filter(like=date, axis=1).rename(columns=lambda col: "recovered")
    cases_df = confirmed_cases_day_df.join(deaths_day_df).join(recovered_day_df).set_index(confirmed_cases_df["country"])

    date_df = (
        geo_data_df.join(cases_df)
        .groupby("country")
        .agg({"confirmed_cases": "sum", "deaths": "sum", "recovered": "sum", "alpha-3_code": "first"})
    )
    date_df = date_df[date_df["confirmed_cases"] > 0].reset_index()
    
    cases_by_date[date] = date_df

cases_deaths_recovered_totals = [(df.filter(like="confirmed_cases").astype("uint32").agg("sum")[0],
                                  df.filter(like="deaths").astype("uint32").agg("sum")[0],
                                  df.filter(like="recovered").astype("uint32").agg("sum")[0]) 
                                    for df in cases_by_date.values()]
confirmed_cases_totals = [daily_total[0] for daily_total in cases_deaths_recovered_totals]
deaths_totals = [daily_total[1] for daily_total in cases_deaths_recovered_totals]
recovered_totals = [daily_total[2] for daily_total in cases_deaths_recovered_totals]

dataset = cases_by_date
x_column = 'deaths'
y_column = 'recovered'
size_column = 'confirmed_cases'
bubble_column = 'country'
# time_column = dates_list

grid = pd.DataFrame()
col_name_template = '{date}+{header}_grid'
for date in dates_list:
    dataset_by_date = dataset[date]
    for col_name in [x_column, y_column, size_column, bubble_column]:
        temp = col_name_template.format(
            date=date, header=col_name
        )
        if dataset_by_date[col_name].size != 0:
            grid = grid.append({'value': list(dataset_by_date[col_name]), 'key': temp}, 
                               ignore_index=True)

figure = {
    'data': [],
    'layout': {},
    'frames': []
}

# start_day = dates_list[0]
trace = {
    'x': grid.loc[grid['key']==col_name_template.format(
        date=date, header=x_column
    ), 'value'].values[0], 
    'y': grid.loc[grid['key']==col_name_template.format(
        date=date, header=y_column
    ), 'value'].values[0],
    'mode': 'markers',
    'text': grid.loc[grid['key']==col_name_template.format(
        date=date, header=bubble_column
    ), 'value'].values[0],
    'size': grid.loc[grid['key']==col_name_template.format(
        date=date, header=size_column
    ), 'value'].values[0]
}
figure['data'].append(trace)
iplot(figure)
last_day_df = dataset[dates_list[-1]]
# print(last_day_df)
# print(last_day_df[x_column])
# xmax = max(np.log10(last_day_df[x_column]))*1.02
# ymax = max(last_day_df[y_column])
# xmin = min(np.log10(last_day_df[x_column]))*0.98
# xmax = max(np.log10(last_day_df[x_column]))*1.02
# ymin = min(last_day_df[y_column])*0.75
# ymax = max(last_day_df[y_column])*1.25
# # # print(ymax)
# figure['layout']['xaxis'] = {'title': 'Total Deaths per Country', 'type': 'log', 
#                              'range': [xmin, xmax]}   
# figure['layout']['yaxis'] = {'title': 'Total Recovers per Country', 
#                              'range': [ymin, ymax]} 
# figure['layout']['title'] = 'Covid-19'
# figure['layout']['showlegend'] = True
# figure['layout']['hovermode'] = 'closest'
# iplot(figure)

# for date in dates_list:
#     # Make a frame for each date
#     frame = {'data': [], 'name': str(date)}
    
#     # Make a trace for each frame
#     trace = {
#         'x': grid.loc[grid['key']==col_name_template.format(
#             date=date, header=x_column
#         ), 'value'].values[0],
#         'y': grid.loc[grid['key']==col_name_template.format(
#             date=date, header=y_column
#         ), 'value'].values[0],
#         'mode': 'markers',
#         'text': grid.loc[grid['key']==col_name_template.format(
#             date=date, header=bubble_column
#         ), 'value'].values[0],
#         'type': 'scatter'
#     }
#     # Add trace to the frame
#     frame['data'].append(trace)
#     # Add frame to the figure
#     figure['frames'].append(frame) 

# iplot(figure)

# figure['layout']['sliders'] = {
#     'args': [
#         'slider.value', {
#             'duration': 400,
#             'ease': 'cubic-in-out'
#         }
#     ],
#     'initialValue': dates_list[0],
#     'plotlycommand': 'animate',
#     'values': dates_list,
#     'visible': True
# }
# sliders_dict = {
#     'active': 0,
#     'yanchor': 'top',
#     'xanchor': 'left',
#     'currentvalue': {
#         'font': {'size': 20},
#         'prefix': 'Date:',
#         'visible': True,
#         'xanchor': 'right'
#     },
#     'transition': {'duration': 300, 'easing': 'cubic-in-out'},
#     'pad': {'b': 10, 't': 50},
#     'len': 0.9,
#     'x': 0.1,
#     'y': 0,
#     'steps': []
# }

# for date in dates_list:
#     add_slider_steps(sliders_dict, date)
    
# figure['layout']['sliders'] = [sliders_dict]
# # iplot(figure)

# figure['layout']['updatemenus'] = [
#     {
#         'buttons': [
#             {
#                 'args': [None, {'frame': {'duration': 500, 'redraw': False},
#                          'fromcurrent': True, 'transition': {'duration': 300, 
#                                                              'easing': 'quadratic-in-out'}}],
#                 'label': 'Play',
#                 'method': 'animate'
#             },
#             {
#                 'args': [[None], {'frame': {'duration':0, 'redraw': False}, 'mode': 'immediate',
#                 'transition': {'duration': 0}}],
#                 'label': 'Pause',
#                 'method': 'animate'
#             }
#         ],
#         'direction': 'left',
#         'pad': {'r': 10, 't': 87},
#         'showactive': False,
#         'type': 'buttons',
#         'x': 0.1,
#         'xanchor': 'right',
#         'y': 0,
#         'yanchor': 'top'
#     }
# ]
# iplot(figure)
# # Make the grid
# grid = pd.DataFrame()
# col_name_template = '{date}+{header}_grid'
# for date in dates_list:
#     dataset_by_date = dataset[date]
#     for col_name in [x_column, y_column, bubble_column, size_column]:
#         temp = col_name_template.format(
#             date=date, header=col_name
#         )
#         if dataset_by_date[col_name].size != 0:
#             grid = grid.append({'value': list(dataset_by_date[col_name]), 'key': temp}, 
#                                ignore_index=True)
# # grid = make_grid(dataset, column_names, size_column, dates_list)
# # print(grid)
# # Set the layout
# figure, sliders_dict = set_layout(x_title='Total Deaths per Country', y_title='Total Recovered per Country', 
#             title='Covid-19', x_logscale=True, y_logscale=False, 
#             show_slider=True, slider_scale=dates_list, show_button=True, show_legend=False, 
#             height=650)
# # print(grid)
# # Add the base frame
# col_name_template_date = col_name_template.format(date=dates_list[0], header=col_name)
# # trace = {
# #     'x': grid.loc[grid['key']==col_name_template.format(
# #         date=date, header=x_column
# #     ), 'value'].values[0], 
# #     'y': grid.loc[grid['key']==col_name_template.format(
# #         date=date, header=y_column
# #     ), 'value'].values[0],
# #     'mode': 'markers',
# #     'text': grid.loc[grid['key']==col_name_template.format(
# #         date=date, header=bubble_column
# #     ), 'value'].values[0]
# # }

# trace = get_trace(grid=grid, col_name_template=col_name_template_date, 
#                     x_column=x_column, y_column=y_column, 
#                     bubble_column=bubble_column)

# figure['data'].append(trace)

# # Set the layout once more
# figure['layout']['xaxis']['autorange'] = True
# figure['layout']['yaxis']['autorange'] = True
# figure['layout']['sliders'] = [sliders_dict]

# # Plot the animation
# iplot(figure)

# Add time frames
# for date in dates_list:
#     frame = {'data': [], 'name': str(date)}
#     col_name_template_date = col_name_template.format(date=date, header=col_name)
#     trace = {
#         'x': grid.loc[grid['key']==col_name_template.format(
#             date=date, header=x_column
#         ), 'value'].values[0], 
#         'y': grid.loc[grid['key']==col_name_template.format(
#             date=date, header=y_column
#         ), 'value'].values[0],
#         'size': grid.loc[grid['key']==col_name_template.format(
#             date=date, header=size_column
#         ), 'value'].values[0],
#         'mode': 'markers',
#         'text': grid.loc[grid['key']==col_name_template.format(
#             date=date, header=bubble_column
#         ), 'value'].values[0]
#     }
#     frame['data'].append(trace)
#     figure['frames'].append(frame) 
#     add_slider_steps(sliders_dict, date)

# Set the layout once more
# figure['layout']['xaxis']['autorange'] = True
# figure['layout']['yaxis']['autorange'] = True
# figure['layout']['sliders'] = [sliders_dict]

# Plot the animation
# iplot(figure)
# print(grid.loc[grid['key']==col_name_template.format(date=date, header=size_column), 'value'].values[0])