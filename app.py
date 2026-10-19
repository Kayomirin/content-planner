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
    "Foot Fetish", "Toe Worship", "Crushing / Trampling", "Socks Fetish", "Striped Socks",
    "Pantyhose Fetish", "Fishnets", "High Heels", "Body Worship", "Ass Worship",
    "Breast Worship", "Armpit Fetish", "Hair Worship", "Hair Brushing", "Femdom",
    "Soft Domme", "Hard Findom", "Financial Domination", "Paypig Control",
    "Total Power Exchange (TPE)", "Contracts & Control", "Mind Games", "Hypnosis",
    "Correction Training", "Spanking", "Humiliation", "Objectification",
    "SPH (Small Penis Humiliation)", "Cuckolding", "Sissification", "Slutification",
    "Beta Loser Degradation", "Virgin Humiliation", "Gooner Control",
    "JOI (Jerk Off Instruction)", "CEI (Cum Eating Instruction)", "Tease & Denial",
    "Pegging", "Toy Control", "Puppy Play", "GFE (Girlfriend Experience)",
    "Bratty Girl", "Chastity & Keyholder", "Techdom & Anydesk", "Giantess Fetish",
    "Spitting & Saliva Fetish", "Facesitting & Squashing", "Farts Fetish",
    "Tummy Fetish", "Wedgie", "Worn Clothes & Used Panties", "Denim & Tight Jeans",
    "Latex & Leather Fetish", "Gloves Fetish"
]

st.set_page_config(page_title="Контент-планнер", page_icon="🔥", layout="wide")
st.title("🔥 Контент-планнер для LoyalFans")
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #f3e8ff 0%, #e9d5ff 100%);
    }
    .stButton > button {
        background-color: transparent;
        border: 2px solid #7c3aed;
        color: #7c3aed;
        border-radius: 12px;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
    }
    .stButton > button:hover {
        background-color: #7c3aed;
        color: white;
    }
    div[data-testid="stVerticalBlock"] > div {
        background: white;
        border-radius: 16px;
        padding: 1rem;
        box-shadow: 0 4px 12px rgba(124, 58, 237, 0.08);
    }
</style>
""", unsafe_allow_html=True)
if "result" not in st.session_state:
    st.session_state.result = None

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
    prompt += "Сгенерируй:\n## ПОСТЫ\nРовно " + str(n_posts) + " постов. Каждый с ### Пост N\n"
    prompt += "## ВИДЕО\nРовно " + str(n_videos) + " видео. Описание + текст + перевод.\n"
    prompt += "## АУДИО\nРовно " + str(n_audios) + " аудио.\n"
    prompt += "## РАССЫЛКИ\nНа " + str(n_mailing_days) + " дней. Каждый день 4 сообщения:\n"
    prompt += "1. MORNING HOOK (бесплатно) с {name}\n"
    prompt += "2. DAYTIME WARM-UP (бесплатно) с {name}\n"
    prompt += "3. EVENING PPV (платно) с {name}\n"
    prompt += "4. MORNING BUMP (бесплатно) с {name}\n"
    prompt += "У каждого сообщения английский + перевод. Обязательно {name}."
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

st.subheader("Настройки")
c1, c2, c3, c4 = st.columns(4)
with c1:
    period = st.selectbox("Период", ["1 день", "3 дня", "Неделя", "Месяц"])
with c2:
    n_posts = st.number_input("Постов всего", 0, 50, 5)
with c3:
    n_videos = st.number_input("Видео всего", 0, 20, 2)
with c4:
    n_audios = st.number_input("Аудио всего", 0, 10, 1)

n_mailing_days = st.slider("Дней рассылок", 0, 30, 7)
fetishes = st.multiselect("Фетиши", DEFAULT_FETISHES, default=["JOI (Jerk Off Instruction)", "Tease & Denial"])

if st.button("Сгенерировать", type="primary", use_container_width=True):
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
