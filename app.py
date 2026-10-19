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
    if k not in st.session_state:
        st.session_state[k] = d

with st.sidebar:
    st.header("API")
    api_key = st.text_input("API ключ", type="password")
    if not api_key and "XAI_API_KEY" in st.secrets:
        api_key = st.secrets["XAI_API_KEY"]
    provider = st.selectbox("Провайдер", ["Grok (xAI)", "OpenAI"])
    model = st.text_input("Модель", value="grok-4.7" if "Grok" in provider else "gpt-4o")

def get_client():
    if not api_key:
        st.error("Введи API-ключ")
        return None
    if "Grok" in provider:
        return OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")
    return OpenAI(api_key=api_key)

def generate(period, n_posts, n_videos, n_audios, fetishes, n_mailing_days):
    client = get_client()
    if not client:
        return None
    fetish_str = ", ".join(fetishes) if fetishes else "any"
    prompt = PERSONA + "\nПериод: " + period + "\nФетиши: " + fetish_str + "\n\n"
    prompt += "## ПОСТЫ\nРовно " + str(n_posts) + " постов.\n"
    prompt += "## ВИДЕО\nРовно " + str(n_videos) + " видео. У каждого: Название, Описание (чтобы захотелось купить), Текст для озвучки, Перевод, 10 хештегов.\n"
    prompt += "## АУДИО\nРовно " + str(n_audios) + " аудио. У каждого: Название, Описание (чтобы захотелось купить), Текст, Перевод, 10 хештегов.\n"
    prompt += "## РАССЫЛКИ\nНа " + str(n_mailing_days) + " дней. Каждый день 4 сообщения с {name}:\n"
    prompt += "1. MORNING HOOK\n2. DAYTIME WARM-UP\n3. EVENING PPV\n4. MORNING BUMP\n"
    prompt += "У каждого английский + перевод."
    try:
        r = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.85,
            max_tokens=7000
        )
        return r.choices[0].message.content
    except Exception as e:
        st.error(str(e))
        return None

def counter(label, key, min_v=0, max_v=50):
    c1, c2, c3, c4 = st.columns([2.5, 1, 1, 1])
    with c1:
        st.markdown(f"**{label}**")
    with c2:
        if st.button("−", key=f"m_{key}"):
            st.session_state[key] = max(min_v, st.session_state[key] - 1)
    with c3:
        st.markdown(f"<div style='text-align:center;font-size:1.4rem;padding-top:4px'>{st.session_state[key]}</div>", unsafe_allow_html=True)
    with c4:
        if st.button("+", key=f"p_{key}"):
            st.session_state[key] = min(max_v, st.session_state[key] + 1)
    return st.session_state[key]

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
