import os
import streamlit as st
from PIL import Image
from google import genai
from google.genai import types

# Configuração da página do Streamlit
st.set_page_config(
    page_title="Detector de Erva-Baleeira",
    page_icon="🌿",
    layout="centered"
)

# Estilização básica
st.title("🌿 Detector de Erva-Baleeira")
st.write("Tire uma foto ou envie uma imagem da planta para verificar se é a **Erva-baleeira** (*Varronia curassavica* / *Cordia verbenacea*).")

# Inicialização do Cliente Gemini
# No Streamlit Cloud, pegamos de st.secrets; localmente, pega das variáveis de ambiente
api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.error("🔑 Chave de API do Gemini não encontrada! Configure a `GEMINI_API_KEY` nas Secrets do Streamlit Cloud.")
    st.stop()

client = genai.Client(api_key=api_key)

# Opção de entrada da imagem (Câmera ou File Uploader)
tab1, tab2 = st.tabs(["📸 Usar Câmera", "📁 Enviar Foto"])

image_input = None

with tab1:
    camera_photo = st.camera_input("Aponte a câmera para a folha/planta")
    if camera_photo:
        image_input = Image.open(camera_photo)

with tab2:
    uploaded_file = st.file_uploader("Escolha um arquivo de imagem", type=["jpg", "jpeg", "png", "webp"])
    if uploaded_file:
        image_input = Image.open(uploaded_file)

# Processamento e Análise
if image_input:
    st.image(image_input, caption="Imagem carregada", use_column_width=True)
    
    if st.button("🔍 Analisar Planta", type="primary"):
        with st.spinner("Analisando características botânicas com Gemini..."):
            try:
                # Prompt instruindo o modelo a identificar especificamente a erva-baleeira
                prompt = """
                Analise esta imagem botânica detalhadamente.
                Identifique se a planta na imagem é a Erva-baleeira (Varronia curassavica / Cordia verbenacea).
                
                Forneça uma resposta estruturada contendo:
                1. **Diagnóstico Principal**: É ou não é Erva-baleeira? (Sim / Não / Incerto)
                2. **Nível de Confiança**: (Ex: Alta, Média, Baixa)
                3. **Características Botânicas Observadas**: Liste os traços observados (ex: margem serrilhada das folhas, nervuras marcadas, inflorescência espiciforme, textura rugosa).
                4. **Possíveis Confusões**: Se houver plantas similares ou se houver dúvida, mencione.
                5. **Resumo / Contexto**: Breve descrição agronômica/médica tradicional da planta, com aviso de segurança.
                """
                
                # Chamada do modelo Gemini 2.5 Flash
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=[image_input, prompt]
                )
                
                st.markdown("---")
                st.subheader("📋 Resultado da Análise Botânica")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Ocorreu um erro durante a análise: {e}")
      
