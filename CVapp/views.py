from django.shortcuts import render
from dotenv import load_dotenv
import os
import openai  

# Carga las API keys y otros valores de entorno
_ = load_dotenv('api_keys_1.env')
openai.api_key = os.getenv('openai_apikey')

def custom_resume_view(request):
    if request.method == 'POST':
        return mejorar_cv(request)  # Llama a la función de mejorar_cv
    return render(request, 'CVapp/custome_resume.html')

def mejorar_cv(request):
    cv_text = request.POST.get('cv_text')
    vacancy_text = request.POST.get('vacancy_text')

    # Crear el prompt para la IA
    prompt = (
        f"Aquí está la descripción de una vacante: {vacancy_text}\n\n"
        f"Este es el CV actual:\n{cv_text}\n\n"
        f"Por favor, mejora el CV resaltando las palabras clave que se ajusten a la vacante y eliminando información innecesaria, teniendo en cuenta que no se debe eliminar la informacion personal , ni dar datos que sean mentiras ."
    )

    # Llamar a la API de OpenAI para generar el nuevo CV
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt},
        ],
        max_tokens=1024,
        temperature=0.7,
    )

    # Obtener el texto del CV mejorado
    new_cv = response['choices'][0]['message']['content'].strip()

    # Renderizar la página de nuevo con el nuevo CV
    return render(request, 'CVapp/custome_resume.html', {
        'cvFile': cv_text,
        'vacancy': vacancy_text,
        'newCv': new_cv,
    })
