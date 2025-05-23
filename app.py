
import streamlit as st
import fitz  # PyMuPDF
import openai

st.set_page_config(page_title="Análise Veterinária com IA")

st.title("🔍 Analisador Veterinário Inteligente")
st.write("Envie um relatório veterinário em PDF e receba uma previsão baseada em IA.")

# Entrada da chave da OpenAI
api_key = st.text_input("🔑 Sua chave da OpenAI (sk-...)", type="password")

# Upload do PDF
arquivo_pdf = st.file_uploader("📄 Envie o PDF do relatório veterinário", type="pdf")

# Botão de análise
if st.button("📊 Analisar") and arquivo_pdf and api_key:
    # Ler PDF
    with fitz.open(stream=arquivo_pdf.read(), filetype="pdf") as doc:
        texto = ""
        for pagina in doc:
            texto += pagina.get_text()
    
    # Enviar para o ChatGPT
    openai.api_key = api_key
    prompt = f"""
Você é um veterinário experiente. Leia o seguinte relatório e classifique a gravidade do estado do cachorro em uma das opções:
1. Não é tão grave
2. Grave, mas vai viver
3. Muito grave, pode morrer

Relatório:
{texto}

Responda apenas com uma das opções acima e uma breve justificativa.
"""
    with st.spinner("Analisando com IA..."):
        try:
            resposta = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.3,
            )
            resultado = resposta.choices[0].message.content
            st.success("✅ Resultado da análise:")
            st.write(resultado)
        except Exception as e:
            st.error(f"Erro ao usar a API da OpenAI: {e}")
else:
    st.info("🔁 Envie o PDF e informe sua chave para começar.")
