import streamlit as st
from openai import OpenAI

PERSONA = """
Ты — элитный сценарист и контент-креатор для платформ Fansly и LoyalFans.
Твоя персона: Mistress Kayomi (Мистресс Кайоми). Тебе 25 лет. Ты — Soft Domme.
Твой характер: игривая, дразнящая, уверенная, с высокими стандартами.
Тон: властный, соблазнительный, высокомерный, но обволакивающий.
Если выбраны жёсткие фетиши (SPH, Humiliation, Trampling) — добавляй жёсткость и обесценивание.
КРИТИЧЕСКИЕ ПРАВИЛА:
1. Контент всегда на идеальном английском + полный перевод на русский сразу под ним.
2. НИКОГДА не упоминай Россию, рубли или что-либо связанное с этой страной.
3. Не выдумывай конкретные цвета одежды или обстановку.
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

if "generated" not in st.session_state:
    st.session_state.generated = None

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

def generate_content(period, n_posts, n_videos, n_audios, fetishes, n_days):
    client = get_client()
    if not client:
        return None
    fetish_str = ", ".join(fetishes) if fetishes else "any"
    prompt = f"""
{PERSONA}
Выбранные фетиши: {fetish_str}

Сгенерируй план на {period}:
## Посты
{n_posts} постов
## Видео
{n_videos} видео (описание + текст)
## Аудио
{n_audios} аудио
## Массовые рассылки
На {n_days} дней. Каждый день:
**MORNING HOOK:** английский текст с {{name}} + перевод
**EVENING PPV:** английский текст с {{name}} + перевод
"""
    try:
        resp = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.85,
            max_tokens=6000
        )
        return resp.choices[0].message.content
    except Exception as e:
        st.error(str(e))
        return None

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Настройки")
    period = st.selectbox("Период", ["1 день", "3 дня", "Неделя", "Месяц"])
    n_posts = st.slider("Постов", 0, 10, 3)
    n_videos = st.slider("Видео", 0, 5, 1)
    n_audios = st.slider("Аудио", 0, 3, 0)
    n_days = st.slider("Дней рассылок", 0, 14, 3)
    fetishes = st.multiselect("Фетиши", DEFAULT_FETISHES, default=["JOI (Jerk Off Instruction)", "Tease & Denial"])
    
    if st.button("Сгенерировать", type="primary"):
        with st.spinner("Генерирую..."):
            result = generate_content(period, n_posts, n_videos, n_audios, fetishes, n_days)
            if result:
                st.session_state.generated = result
                st.rerun()

with col2:
    if st.session_state.generated:
        st.markdown(st.session_state.generated)
        st.code(st.session_state.generated)
    else:
        st.info("Настрой параметры слева и нажми кнопку")
        
