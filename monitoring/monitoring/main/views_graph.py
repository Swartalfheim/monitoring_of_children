import matplotlib.pyplot as plt
import io
import base64
import random
from django.http import HttpResponse
from django.shortcuts import render
from .models import Ditina

def random_graph(request, ditina_id):
    # Generate random data for demonstration
    ages = list(range(1, 19))  # 1 to 18 inclusive
    heights = [random.randint(50, 180) for _ in ages]

    # Get the real Ditina object
    try:
        ditina = Ditina.objects.get(id=ditina_id)
        component_age = ditina.vik
        component_height = ditina.zrist
    except Ditina.DoesNotExist:
        component_age = None
        component_height = None

    plt.figure(figsize=(6, 4))
    plt.plot(ages, heights, marker='o', color='b')
    # Add a green dot for the component's data if available and valid
    if component_age is not None and component_height is not None and 1 <= component_age <= 18:
        plt.scatter([component_age], [component_height], color='green', s=100, zorder=5, label='Дитина')
        plt.legend()
    plt.title('Випадковий графік віку та зросту')
    plt.xlabel('Вік (роки)')
    plt.ylabel('Зріст (см)')
    plt.grid(True)

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    image_png = buf.getvalue()
    buf.close()
    graph = base64.b64encode(image_png).decode('utf-8')

    return render(request, 'random_graph.html', {'graph': graph})
