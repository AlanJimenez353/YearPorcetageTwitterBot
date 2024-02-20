from openai import OpenAI

# Define your OpenAI API key
api_key = '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'

# Configure the API key
client= OpenAI(api_key=api_key)
def calcular_porcentaje_transcurrido():
    from datetime import datetime
    now = datetime.now()

    year_start = datetime(now.year, 1, 1)
    days_passed = (now - year_start).days

    total_days_in_year = (datetime(now.year + 1, 1, 1) - year_start).days

    percentage_passed = (days_passed / total_days_in_year) * 100

    return int(round(percentage_passed))
  
""""
def obtener_respuesta():
    prompt = "Calcula el porcentaje del año que ha transcurrido."
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
            {"role": "user", "content": prompt}
        ]
    )
    return completion.choices[0].message

    respuesta = obtener_respuesta()
    print(respuesta)
"""

porcentaje_transcurrido = calcular_porcentaje_transcurrido()

print(f"El {porcentaje_transcurrido}% del año ya ha transcurrido.")
