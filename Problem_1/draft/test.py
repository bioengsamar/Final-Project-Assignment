import plotly.express as px
import plotly.graph_objects as go

fig = go.Figure(data=[go.Scatter(
    x=[1, 2, 3, 4], y=[10, 11, 12, 13],
    mode='markers',
    marker_size=[40, 60, 80, 100])
])

fig.show()

# df = px.data.gapminder()

# fig = px.scatter(df.query("year==2007"), x="gdpPercap", y="lifeExp",
# 	         size="pop", color="continent",
#                  hover_name="country", log_x=True, size_max=60)
# fig.show()