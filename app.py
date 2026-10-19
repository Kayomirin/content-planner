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

if "result" not in st.session_state:
    st.session_state.result = None

with st.sidebar:
    st.header("🔑 API")
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
    prompt = f"""
{PERSONA}
Период: {period}
Выбранные фетиши: {fetish_str}

Сгенерируй строго по структуре:

## ПОСТЫ
Ровно {n_posts} постов. Каждый начинай с ### Пост N
Английский текст + **Перевод:** русский

## ВИДЕО
Ровно {n_videos} видео. Каждый начинай с ### Видео N
Описание сцены + Текст для озвучки + **Перевод:**

## АУДИО
Ровно {n_audios} аудио. Каждый начинай с ### Аудио N
Английский + **Перевод:**

## РАССЫЛКИ
На {n_mailing_days} дней. Для каждого дня сделай 4 сообщения строго в таком порядке:

### День N

**1. MORNING HOOK (бесплатно)**
[английский текст с {{name}}]
**Перевод:** ...
Суть: разбудить базу, задать вопрос, заставить оправдываться. Высокомерно-игривый тон. Без прямой просьбы денег.

**2. DAYTIME WARM-UP (бесплатно)**
[английский текст с {{name}}]
**Перевод:** ...
Суть: создать интригу и дефицит. Намекнуть на горячий контент, который они пока не заслужили. Tease & Denial.

**3. EVENING PPV (платно)**
[английский текст с {{name}}]
**Перевод:** ...
Суть: текст под locked-сообщение. Фрустрация + жёсткий призыв купить. «Разблокируй, чтобы доказать, что ты хороший мальчик».

**4. MORNING BUMP (бесплатно, на следующий день)**
[английский текст с {{name}}]
**Перевод:** ...
Суть: короткое сообщение тем, кто не купил вчера. Лёгкая насмешка над нерешительностью. «Так и будешь пялиться на размытый экран?»

Правила для рассылок:
- Обязательно {{name}} в каждом сообщении.
- Тон Soft Domme. При жёстких фетишах добавляй 
