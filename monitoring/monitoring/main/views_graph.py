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

    # AI health assumption logic - Improved (without gender distinction)
    ai_message = ""
    AVERAGE_GROWTH_RATES_UNISEX = {
        '0-2': {'start_height': 50, 'growth_per_year': 25},
        '3-12': {'start_height': 88, 'growth_per_year': 5.8},
        '13-18': {'start_height': 140, 'growth_per_year': 6.5},
    }
    # Ensure all necessary components are available
    if component_age is not None and component_height is not None:
        # Convert age to a float for more accurate comparison (ages like 2.5 are possible)
        try:
            age_years = float(component_age)
        except (ValueError, TypeError):
            ai_message = "Некоректний формат віку. Будь ласка, введіть числове значення."
            return render(request, 'random_graph.html', {'graph_html': mark_safe(graph_html), 'ai_message': mark_safe(ai_message)})

        # Check for hormonal therapy first
        if getattr(ditina, 'pryimaie_gormony', False):
            ai_message += "<b>Увага:</b> Дитина приймає гормональні препарати. Це може суттєво впливати на ріст і розвиток. <b>Обов'язково проконсультуйтеся з лікарем</b> для індивідуальної оцінки та регулярного моніторингу.<br><br>"

        # Calculate estimated average height based on age (without gender)
        estimated_avg_height = 0
        if 0 <= age_years <= 2:
            # A very rough linear approximation for 0-2 years, starting from 50cm at birth
            estimated_avg_height = AVERAGE_GROWTH_RATES_UNISEX['0-2']['start_height'] + (age_years * AVERAGE_GROWTH_RATES_UNISEX['0-2']['growth_per_year'])
        elif 2 < age_years <= 12:
            # Use start_height for 3 years, then add yearly growth
            estimated_avg_height = AVERAGE_GROWTH_RATES_UNISEX['3-12']['start_height'] + ((age_years - 2) * AVERAGE_GROWTH_RATES_UNISEX['3-12']['growth_per_year'])
        elif 12 < age_years <= 18:
            # Use start_height for 13 years, then add yearly growth
            estimated_avg_height = AVERAGE_GROWTH_RATES_UNISEX['13-18']['start_height'] + ((age_years - 12) * AVERAGE_GROWTH_RATES_UNISEX['13-18']['growth_per_year'])
        else:
            ai_message += "На жаль, наша система не розрахована на вік, що виходить за межі 0-18 років для аналізу зросту.<br>"
            return render(request, 'random_graph.html', {'graph_html': mark_safe(graph_html), 'ai_message': mark_safe(ai_message)})

        # Define thresholds for "below/above average" based on a typical standard deviation or percentile
        HEIGHT_DEVIATION_THRESHOLD = 7 # cm, a generalized deviation

        if estimated_avg_height > 0: # Only proceed if an estimated average height was calculated
            if component_height < estimated_avg_height - HEIGHT_DEVIATION_THRESHOLD:
                ai_message += (f"<b>Зріст нижче середнього</b> для дитини вашого віку "
                               f"({component_height} см при {age_years} роках). "
                               f"Розрахований середній зріст: приблизно {estimated_avg_height:.1f} см. "
                               f"<b>Рекомендується звернутися до педіатра</b> для консультації та оцінки розвитку.")
            elif component_height > estimated_avg_height + HEIGHT_DEVIATION_THRESHOLD:
                ai_message += (f"<b>Зріст вище середнього</b> для дитини вашого віку "
                               f"({component_height} см при {age_years} роках). "
                               f"Розрахований середній зріст: приблизно {estimated_avg_height:.1f} см. "
                               f"Це може бути індивідуальною особливістю, але варто <b>спостерігати за динамікою</b> зросту "
                               f"та за потреби проконсультуватися з лікарем.")
            else:
                ai_message += (f"<b>Зріст у межах норми</b> для дитини вашого віку "
                               f"({component_height} см при {age_years} роках). "
                               f"Розрахований середній зріст: приблизно {estimated_avg_height:.1f} см.")
        else:
            ai_message += "На жаль, не вдалося розрахувати середній зріст для наданих даних.<br>"

    else:
        # Handle cases where essential data is missing
        missing_data = []
        if component_age is None:
            missing_data.append("вік")
        if component_height is None:
            missing_data.append("зріст")

        if missing_data:
            ai_message = f"<b>Недостатньо даних для аналізу.</b> Будь ласка, введіть: {', '.join(missing_data)}."
        else:
            ai_message = "Недостатньо даних для аналізу (невідома причина)."

    return render(request, 'random_graph.html', {'graph_html': mark_safe(graph_html), 'ai_message': mark_safe(ai_message)})