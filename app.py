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
    
    prompt = f"""{PERSONA}
Период: {period}
Фетиши: {fetish_str}

Сгенерируй строго по структуре:

## ПОСТЫ
Ровно {n_posts} постов. Каждый начинай с ### Пост N
Английский текст + **Перевод:** русский

## ВИДЕО
Ровно {n_videos} видео. Каждый начинай с ### Видео N
**Название:** короткое триггерное название
**Описание:** текст, который вызывает желание купить
**Текст для озвучки:** ...
**Перевод:** ...
**Хештеги:** ровно 10 хештегов по теме

## АУДИО
Ровно {n_audios} аудио. Каждый начинай с ### Аудио N
**Название:** короткое триггерное название
**Описание:** текст, который вызывает желание купить
**Текст:** ...
**Перевод:** ...
**Хештеги:** ровно 10 хештегов по теме

## РАССЫЛКИ
На {n_mailing_days} дней. Каждый день 4 сообщения:
1. MORNING HOOK (бесплатно) с {{name}}
2. DAYTIME WARM-UP (бесплатно) с {{name}}
3. EVENING PPV (платно) с {{name}}
4. MORNING BUMP (бесплатно) с {{name}}
У каждого: английский + перевод. Обязательно {{name}}.
"""
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
