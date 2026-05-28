import streamlit as st
import os
import time
import glob
import cv2
import numpy as np
import pytesseract
from PIL import Image
from gtts import gTTS
from googletrans import Translator

# ─────────────────────────────────────────────
# CONFIGURACIÓN DE PÁGINA
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Pink OCR Translator",
    page_icon="💖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# ESTILOS CSS PERSONALIZADOS
# ─────────────────────────────────────────────
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

/* Fondo principal */
.stApp {
    background: linear-gradient(135deg, #0f0f14, #1c1023);
    color: white;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #161621;
    border-right: 1px solid rgba(255,255,255,0.08);
}

/* Sidebar títulos */
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #ff85c2 !important;
    font-weight: 700 !important;
}

/* Sidebar textos */
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label {
    color: #f5f5f7 !important;
}

/* Inputs */
textarea,
input[type="text"] {
    background-color: #1f1f2e !important;
    border: 2px solid #ff4fa3 !important;
    border-radius: 14px !important;
    color: white !important;
}

/* Selectbox */
[data-baseweb="select"] > div {
    background: #1f1f2e !important;
    border: 2px solid #ff4fa3 !important;
    border-radius: 14px !important;
    color: white !important;
}

/* Títulos */
h1 {
    color: #ff4fa3 !important;
    font-size: 3.2rem !important;
    font-weight: 700 !important;
    text-align: center;
}

h2, h3 {
    color: #ff85c2 !important;
}

/* Texto */
p, span, label {
    color: #f5f5f7 !important;
}

/* Cards glassmorphism */
.glass-card {
    background: rgba(255,255,255,0.04);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 24px;
    padding: 28px;
    box-shadow: 0 8px 30px rgba(0,0,0,0.25);
    margin-bottom: 22px;
}

/* Camera input */
[data-testid="stCameraInput"] {
    background: rgba(255,255,255,0.03);
    border-radius: 20px;
    border: 2px solid #ff4fa3;
    padding: 16px;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.03);
    padding: 16px;
    border-radius: 18px;
    border: 2px dashed #ff4fa3;
}

/* Radio */
.stRadio > div {
    background: rgba(255,255,255,0.03);
    padding: 12px;
    border-radius: 16px;
}

/* Checkbox */
.stCheckbox {
    background: rgba(255,255,255,0.03);
    padding: 10px;
    border-radius: 14px;
}

/* Botones */
.stButton > button {
    background: linear-gradient(135deg, #ff4fa3, #ff85c2) !important;
    color: white !important;
    border: none !important;
    border-radius: 16px !important;
    padding: 0.8rem 1.5rem !important;
    font-weight: 600 !important;
    transition: 0.3s ease !important;
    box-shadow: 0 4px 18px rgba(255,79,163,0.3);
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 28px rgba(255,79,163,0.45);
}

/* Resultado */
.result-card {
    background: rgba(255,255,255,0.05);
    border-left: 5px solid #ff4fa3;
    border-radius: 22px;
    padding: 24px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.2);
}

/* Texto detectado */
.detected-text {
    background: rgba(255,255,255,0.03);
    border-radius: 18px;
    padding: 20px;
    line-height: 1.8;
    font-size: 17px;
    color: #f5f5f7;
    border: 1px solid rgba(255,255,255,0.08);
}

/* Audio player */
audio {
    width: 100%;
    margin-top: 12px;
}

/* Scroll */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-thumb {
    background: #ff4fa3;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# FUNCIONES ORIGINALES
# ─────────────────────────────────────────────
text = " "

def text_to_speech(input_language, output_language, text, tld):
    translation = translator.translate(text, src=input_language, dest=output_language)
    trans_text = translation.text
    tts = gTTS(trans_text, lang=output_language, tld=tld, slow=False)

    try:
        my_file_name = text[0:20]
    except:
        my_file_name = "audio"

    tts.save(f"temp/{my_file_name}.mp3")

    return my_file_name, trans_text

def remove_files(n):

    mp3_files = glob.glob("temp/*mp3")

    if len(mp3_files) != 0:

        now = time.time()
        n_days = n * 86400

        for f in mp3_files:
            if os.stat(f).st_mtime < now - n_days:
                os.remove(f)

remove_files(7)

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="glass-card">

<h1>💖 Pink OCR Translator</h1>

<p style='text-align:center; font-size:18px; margin-top:10px;'>
Reconocimiento óptico de caracteres, traducción inteligente y conversión de texto a voz.
</p>

</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:

    st.markdown("## ⚙️ Configuración OCR")

    filtro = st.radio(
        "Filtro para imagen con cámara",
        ('Sí', 'No')
    )

    st.markdown("---")

    st.markdown("## 🌍 Traducción y Voz")

    try:
        os.mkdir("temp")
    except:
        pass

    translator = Translator()

    in_lang = st.selectbox(
        "Seleccione el lenguaje de entrada",
        ("Ingles", "Español", "Bengali", "koreano", "Mandarin", "Japones"),
    )

    if in_lang == "Ingles":
        input_language = "en"
    elif in_lang == "Español":
        input_language = "es"
    elif in_lang == "Bengali":
        input_language = "bn"
    elif in_lang == "koreano":
        input_language = "ko"
    elif in_lang == "Mandarin":
        input_language = "zh-cn"
    elif in_lang == "Japones":
        input_language = "ja"

    out_lang = st.selectbox(
        "Seleccione el lenguaje de salida",
        ("Ingles", "Español", "Bengali", "koreano", "Mandarin", "Japones"),
    )

    if out_lang == "Ingles":
        output_language = "en"
    elif out_lang == "Español":
        output_language = "es"
    elif out_lang == "Bengali":
        output_language = "bn"
    elif out_lang == "koreano":
        output_language = "ko"
    elif out_lang == "Chinese":
        output_language = "zh-cn"
    elif out_lang == "Japones":
        output_language = "ja"

    english_accent = st.selectbox(
        "Seleccione el acento",
        (
            "Default",
            "India",
            "United Kingdom",
            "United States",
            "Canada",
            "Australia",
            "Ireland",
            "South Africa",
        ),
    )

    if english_accent == "Default":
        tld = "com"
    elif english_accent == "India":
        tld = "co.in"
    elif english_accent == "United Kingdom":
        tld = "co.uk"
    elif english_accent == "United States":
        tld = "com"
    elif english_accent == "Canada":
        tld = "ca"
    elif english_accent == "Australia":
        tld = "com.au"
    elif english_accent == "Ireland":
        tld = "ie"
    elif english_accent == "South Africa":
        tld = "co.za"

    display_output_text = st.checkbox("Mostrar texto traducido")

# ─────────────────────────────────────────────
# LAYOUT PRINCIPAL
# ─────────────────────────────────────────────
col1, col2 = st.columns([1,1], gap="large")

# ─────────────────────────────────────────────
# COLUMNA IZQUIERDA
# ─────────────────────────────────────────────
with col1:

    st.markdown("""
    <div class="glass-card">

    <h3>📸 Captura o carga una imagen</h3>

    <p>
    Puedes usar la cámara o subir una imagen para detectar texto automáticamente.
    </p>

    </div>
    """, unsafe_allow_html=True)

    cam_ = st.checkbox("Usar Cámara")

    if cam_:
        img_file_buffer = st.camera_input("Toma una Foto")
    else:
        img_file_buffer = None

    bg_image = st.file_uploader(
        "Cargar Imagen:",
        type=["png", "jpg"]
    )

# ─────────────────────────────────────────────
# COLUMNA DERECHA
# ─────────────────────────────────────────────
with col2:

    st.markdown("""
    <div class="glass-card">

    <h3>🧠 Procesamiento Inteligente</h3>

    <p>
    El sistema reconocerá texto mediante OCR y podrá convertirlo automáticamente en audio traducido.
    </p>

    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# OCR ARCHIVO
# ─────────────────────────────────────────────
if bg_image is not None:

    uploaded_file = bg_image

    st.image(
        uploaded_file,
        caption='Imagen cargada.',
        use_container_width=True
    )

    with open(uploaded_file.name, 'wb') as f:
        f.write(uploaded_file.read())

    st.success(f"Imagen guardada como {uploaded_file.name}")

    img_cv = cv2.imread(f'{uploaded_file.name}')
    img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)

    text = pytesseract.image_to_string(img_rgb)

# ─────────────────────────────────────────────
# OCR CÁMARA
# ─────────────────────────────────────────────
if img_file_buffer is not None:

    bytes_data = img_file_buffer.getvalue()

    cv2_img = cv2.imdecode(
        np.frombuffer(bytes_data, np.uint8),
        cv2.IMREAD_COLOR
    )

    if filtro == 'Con Filtro':
        cv2_img = cv2.bitwise_not(cv2_img)
    else:
        cv2_img = cv2_img

    img_rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)

    text = pytesseract.image_to_string(img_rgb)

# ─────────────────────────────────────────────
# RESULTADO TEXTO
# ─────────────────────────────────────────────
if text != " ":

    st.markdown("""
    <div class="result-card">

    <h3>📝 Texto Detectado</h3>

    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="detected-text">
    {text}
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TEXT TO SPEECH
# ─────────────────────────────────────────────
if st.button("🎧 Convertir a Voz"):

    result, output_text = text_to_speech(
        input_language,
        output_language,
        text,
        tld
    )

    audio_file = open(f"temp/{result}.mp3", "rb")

    audio_bytes = audio_file.read()

    st.markdown("""
    <div class="result-card">

    <h3>🔊 Tu Audio</h3>

    </div>
    """, unsafe_allow_html=True)

    st.audio(audio_bytes, format="audio/mp3", start_time=0)

    if display_output_text:

        st.markdown("""
        <div class="result-card">

        <h3>🌍 Texto Traducido</h3>

        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="detected-text">
        {output_text}
        </div>
        """, unsafe_allow_html=True)
