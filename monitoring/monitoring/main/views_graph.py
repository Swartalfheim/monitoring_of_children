import matplotlib
matplotlib.use('Agg') 

import matplotlib.pyplot as plt
import io
import base64
from django.shortcuts import render
from .models import Ditina
import matplotlib.patheffects as patheffects
import plotly.graph_objs as go
from django.utils.safestring import mark_safe

def random_graph(request, ditina_id):
    example_measurements = [
        (0, 50), (0.25, 60), (0.5, 67), (0.75, 72), (1, 75),
        (1.25, 78), (1.5, 81), (1.75, 84), (2, 87), (2.25, 89),
        (2.5, 91), (2.75, 94), (3, 96), (3.5, 99), (4, 103),
        (4.5, 106), (5, 110), (5.5, 113), (6, 116), (6.5, 119),
        (7, 122), (7.5, 125), (8, 128), (8.5, 131), (9, 134),
        (9.5, 137), (10, 140), (10.5, 142), (11, 145), (11.5, 148),
        (12, 150), (12.5, 152), (13, 155), (13.5, 157), (14, 160),
        (14.5, 162), (15, 165), (15.5, 167), (16, 169), (16.5, 170),
        (17, 172), (17.5, 173), (18, 175)
    ]
    example_ages = [age for age, height in example_measurements]
    example_heights = [height for age, height in example_measurements]

    try:
        ditina = Ditina.objects.get(id=ditina_id)
        component_age = ditina.vik
        component_height = ditina.zrist
        user_name = f"{ditina.imya} {ditina.prizvische}".strip()
    except Ditina.DoesNotExist:
        component_age = None
        component_height = None
        user_name = 'Ваша дитина'

    # Plotly graph
    trace1 = go.Scatter(
        x=example_heights,
        y=example_ages,
        mode='lines+markers',
        marker=dict(size=8, color='#1f77b4'),
        line=dict(color='#1f77b4', width=2),
        name='Типові вимірювання',
        text=[f"Вік: {age} років<br>Зріст: {height} см" for age, height in example_measurements],
        hoverinfo='text',
    )
    data = [trace1]
    # Add user dot if available
    if component_age is not None and component_height is not None and 0 <= component_age <= 18:
        trace2 = go.Scatter(
            x=[component_height],
            y=[component_age],
            mode='markers+text',
            marker=dict(size=16, color='#e83e8c', line=dict(width=2, color='black')),
            name=user_name,
            text=[user_name],
            textposition='top center',
            hoverinfo='text',
        )
        data.append(trace2)
    layout = go.Layout(
        title='Графік: Зріст — Вік (реальні дані)',
        xaxis=dict(title='Зріст (см)', tickfont=dict(size=12)),
        yaxis=dict(title='Вік (роки)', tickfont=dict(size=12), dtick=1, range=[0, 18]),
        plot_bgcolor='#f8f9fa',
        paper_bgcolor='#f8f9fa',
        legend=dict(font=dict(size=12)),
        margin=dict(l=60, r=30, t=60, b=60),
        hoverlabel=dict(bgcolor='white', font_size=13, font_family='Arial'),
    )
    fig = go.Figure(data=data, layout=layout)
    graph_html = fig.to_html(full_html=False, include_plotlyjs='cdn')
    return render(request, 'random_graph.html', {'graph_html': mark_safe(graph_html)})
