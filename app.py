import streamlit as st
from openai import OpenAI

PERSONA = """
Ты — элитный сценарист и контент-креатор для платформ Fansly и LoyalFans.
Твоя персона: Mistress Kayomi. Тебе 25 лет. Ты — Soft Domme.
Тон: властный, соблазнительный, высокомерный, но обволакивающий.
Если выбраны жёсткие фетиши — добавляй давление и обесценивание.
Правила: контент на идеальном английском + полный перевод на русский. Никогда не упоминай Россию или рубли.
"""

DEFAULT_FETISHES = [
    "Foot Fetish", "Toe Worship", "Crushing / Trampling", "Socks Fetish", "Pantyhose Fetish",
    "Fishnets", "High Heels", "Body Worship", "Ass Worship", "Breast Worship",
    "Femdom", "Soft Domme", "Hard Findom", "Financial Domination", "SPH (Small Penis Humiliation)",
    "Humiliation", "JOI (Jerk Off Instruction)", "CEI (Cum Eating Instruction)", "Tease & Denial",
    "Pegging", "Chastity & Keyholder", "Giantess Fetish", "Facesitting & Squashing"
]

st.set_page_config(page_title="Контент-планнер", page_icon="🔥", layout="wide")
st.title("🔥 Контент-планнер для LoyalFans")

st.markdown("""
<style>
.stButton > button {
    border-radius: 20px !important;
    border: 1.5px solid #a855f7 !important;
    background: transparent !important;
    color: #7c3aed !important;
}
.stButton > button:hover {
    background: #a855f7 !important;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

if "result" not in st.session_state:
    st.session_state.result = None
for k, d in [("posts", 5), ("videos", 2), ("audios", 1)]:
   if st.session_state.result:
    st.divider()
    st.subheader("Результат")
    text = st.session_state.result
    
    sections = {"ПОСТЫ": "", "ВИДЕО": "", "АУДИО": "", "РАССЫЛКИ": ""}
    current = None
    
    for line in text.split("\n"):
        u = line.upper().strip()
        if any(x in u for x in ["ПОСТЫ", "POSTS", "### ПОСТ"]):
            current = "ПОСТЫ"
            continue
        elif any(x in u for x in ["ВИДЕО", "VIDEO", "### ВИДЕО"]):
            current = "ВИДЕО"
            continue
        elif any(x in u for x in ["АУДИО", "AUDIO", "### АУДИО"]):
            current = "АУДИО"
            continue
        elif any(x in u for x in ["РАССЫЛКИ", "MAIL", "PPV", "### РАССЫЛ"]):
            current = "РАССЫЛКИ"
            continue
        if current:
            sections[current] += line + "\n"
    
    t1, t2, t3, t4 = st.tabs(["Посты", "Видео", "Аудио", "Рассылки"])
    with t1:
        st.markdown(sections["ПОСТЫ"].strip() or "Нет постов")
    with t2:
        st.markdown(sections["ВИДЕО"].strip() or "Нет видео")
    with t3:
        st.markdown(sections["АУДИО"].strip() or "Нет аудио")
    with t4:
        st.markdown(sections["РАССЫЛКИ"].strip() or "Нет рассылок")
    
    with st.expander("Весь текст"):
        st.code(text)

st.subheader("Настройки")
n_posts = counter("Посты", "posts", 0, 30)
n_videos = counter("Видео", "videos", 0, 15)
n_audios = counter("Аудио", "audios", 0, 10)

st.write("")
n_mailing_days = st.slider("Дней рассылок", 0, 30, 7)
period = st.selectbox("Период", ["1 день", "3 дня", "Неделя", "Месяц"])
fetishes = st.multiselect("Фетиши", DEFAULT_FETISHES, default=["JOI (Jerk Off Instruction)", "Tease & Denial"])

st.write("")
if st.button("🚀 Сгенерировать", type="primary", use_container_width=True):
    with st.spinner("Генерирую..."):
        st.session_state.result = generate(period, n_posts, n_videos, n_audios, fetishes, n_mailing_days)

if st.session_state.result:
    st.divider()
    st.subheader("Результат")
    text = st.session_state.result
    sections = {"ПОСТЫ": "", "ВИДЕО": "", "АУДИО": "", "РАССЫЛКИ": ""}
    current = None
    for line in text.split("\n"):
        u = line.upper()
        if "ПОСТЫ" in u:
            current = "ПОСТЫ"
        elif "ВИДЕО" in u:
            current = "ВИДЕО"
        elif "АУДИО" in u:
            current = "АУДИО"
        elif "РАССЫЛКИ" in u:
            current = "РАССЫЛКИ"
        elif current:
            sections[current] += line + "\n"
    t1, t2, t3, t4 = st.tabs(["Посты", "Видео", "Аудио", "Рассылки"])
    with t1:
        st.markdown(sections["ПОСТЫ"] or "Нет")
    with t2:
        st.markdown(sections["ВИДЕО"] or "Нет")
    with t3:
        st.markdown(sections["АУДИО"] or "Нет")
    with t4:
        st.markdown(sections["РАССЫЛКИ"] or "Нет")
    with st.expander("Весь текст"):
        st.code(text)
