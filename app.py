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

## ВИДЕО
Ровно {n_videos} видео. Каждый начинай с ### Видео N
У каждого: Описание сцены + Текст для озвучки + Перевод

## АУДИО
Ровно {n_audios} аудио. Каждый начинай с ### Аудио N

## РАССЫЛКИ
На {n_mailing_days} дней. Каждый день строго так:

### День N
**MORNING HOOK**
[английский текст с {{name}}]
**Перевод:** ...

**EVENING PPV**
[английский текст с {{name}}]
**Перевод:** ...

MORNING HOOK — бесплатный крючок (оправдания, ожидание, сомнения).
EVENING PPV — дразнящий текст под locked PPV.
Обязательно {{name}} в каждом сообщении.
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

# ========== ИНТЕРФЕЙС ==========
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

n_mailing_days = st.slider("Дней рассылок (2 сообщения в день)", 0, 30, 7)
fetishes = st.multiselect("Фетиши", DEFAULT_FETISHES, default=["JOI (Jerk Off Instruction)", "Tease & Denial"])

if st.button("🚀 Сгенерировать", type="primary", use_container_width=True):
    with st.spinner("Генерирую..."):
        st.session_state.result = generate(period, n_posts, n_videos, n_audios, fetishes, n_mailing_days)

# ========== ВЫВОД В КАРТОЧКАХ ==========
if st.session_state.result:
    st.divider()
    st.subheader("Результат")
    
    text = st.session_state.result
    
    # Простое разбиение по заголовкам
    sections = {"ПОСТЫ": "", "ВИДЕО": "", "АУДИО": "", "РАССЫЛКИ": ""}
    current = None
    for line in text.split("\n"):
        upper = line.upper()
        if "ПОСТЫ" in upper or "POSTS" in upper:
            current = "ПОСТЫ"
        elif "ВИДЕО" in upper or "VIDEO" in upper:
            current = "ВИДЕО"
        elif "АУДИО" in upper or "AUDIO" in upper:
            current = "АУДИО"
        elif "РАССЫЛКИ" in upper or "MAIL" in upper or "PPV" in upper:
            current = "РАССЫЛКИ"
        elif current:
            sections[current] += line + "\n"
    
    tab1, tab2, tab3, tab4 = st.tabs(["📝 Посты", "🎬 Видео", "🎧 Аудио", "💌 Рассылки"])
    
    with tab1:
        if sections["ПОСТЫ"].strip():
            st.markdown(sections["ПОСТЫ"])
        else:
            st.info("Нет постов")
    with tab2:
        if sections["ВИДЕО"].strip():
            st.markdown(sections["ВИДЕО"])
        else:
            st.info("Нет видео")
    with tab3:
        if sections["АУДИО"].strip():
            st.markdown(sections["АУДИО"])
        else:
            st.info("Нет аудио")
    with tab4:
        if sections["РАССЫЛКИ"].strip():
            st.markdown(sections["РАССЫЛКИ"])
        else:
            st.info("Нет рассылок")
    
    with st.expander("Весь текст целиком (для копирования)"):
        st.code(text)
