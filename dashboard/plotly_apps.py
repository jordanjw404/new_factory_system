# dashboard/plotly_apps.py

from django_plotly_dash import DjangoDash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go
from orders.models import Order
from django.db.models import Count

# 1) Instantiate your Dash app
app = DjangoDash("OrdersByStatus")

# 2) Query your Order model
qs = (
    Order.objects
         .values('status')
         .annotate(count=Count('id'))
         .order_by('status')
)
statuses = [row['status'] for row in qs]
counts   = [row['count'] for row in qs]

# 3) Build a Plotly bar chart
fig = go.Figure([go.Bar(x=statuses, y=counts)])
fig.update_layout(
    title="Orders by Status",
    xaxis_title="Status",
    yaxis_title="Number of Orders"
)

# 4) Define the layout using Dash components
app.layout = html.Div([
    html.H3("Orders by Status"),
    dcc.Graph(id="orders-by-status-chart", figure=fig)
])
