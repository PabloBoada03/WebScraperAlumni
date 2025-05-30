import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Cargar variables de entorno desde .env
load_dotenv()

# Obtener la API key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY no está definida. Verifica el archivo .env.")

# Configurar cliente
client = genai.Client(api_key=api_key)
model = "gemini-2.0-flash"

# Configuración del modelo
generate_content_config = types.GenerateContentConfig(
    temperature=0.1,
    top_p=0.95,
    top_k=40,
    max_output_tokens=8192,
    response_mime_type="text/plain",
)

# Template base
template = (
    "You are an information extractor. Extract ONLY the information described in the section below, from the text provided.\n\n"
    "TEXT:\n{dom_content}\n\n"
    "INSTRUCTION:\n{parse_description}\n\n"
    "RULES:\n"
    "1. IGNORE all content related to cookies, analytics, tracking scripts, HTML storage, or metadata.\n"
    "2. Do NOT list any cookie names, durations, types, or related storage elements.\n"
    "3. DO NOT output content not directly related to the description.\n"
    "4. DO NOT summarize or paraphrase the content.\n"
    "5. If no matching content is found, respond with an empty string: ''.\n"
    "Return ONLY clean and direct extracted data, nothing else."
)


def parse(dom_chunks, parse_description):
    parsed_results = []

    for i, chunk in enumerate(dom_chunks, start=1):
        input_text = template.format(
            dom_content=chunk,
            parse_description=parse_description
        )

        contents = [
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=input_text)]
            ),
        ]

        response_text = ""
        try:
            for chunk_response in client.models.generate_content_stream(
                model=model,
                contents=contents,
                config=generate_content_config,
            ):
                if chunk_response.text:
                    response_text += chunk_response.text

            print(f"Parsed batch: {i} of {len(dom_chunks)}")
            parsed_results.append(response_text)

        except Exception as e:
            print(f"Error al procesar el chunk {i}: {e}")
            parsed_results.append(f"[Error en el chunk {i}: {e}]")

    return "\n".join(parsed_results)
