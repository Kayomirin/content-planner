import streamlit as st
from openai import OpenAI

PERSONA = """
Ты — элитный сценарист и контент-креатор для платформ Fansly и LoyalFans.
Твоя персона: Mistress Kayomi (Мистресс Кайоми). Тебе 25 лет. Ты — Soft Domme.
Тон: властный, соблазнительный, высокомерный, но обволакивающий.
Если выбраны жёсткие фетиши (SPH, Humiliation, Trampling и т.п.) — добавляй давление и обесценивание.
КРИТИЧЕСКИЕ ПРАВИЛА:
- Контент всегда на идеальном английском + полный перевод на русский сразу под ним.
- НИКОГДА не упоминай Россию, рубли или что-либо связанное с этой страной.
- Не выдумывай конкретные цвета одежды, лака или обстановку — держи описания универсальными, но горячими.
- Используй нишевый сленг сабов и доминаток. Говори как живая дерзкая доминантка, без банальных фраз.
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
.stButton > button {
    border-radius: 20px !important;
    border: 1.5px solid #a855f7 !important;
    background: transparent !important;
    color: #7c3aed !important;
    font-weight: 600 !important;
}
.stButton > button:hover {
    background: #a855f7 !important;
    color: white !important;
}
div[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 16px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}
</style>
""", unsafe_allow_html=True)

if "result" not in st.session_state:
    st.session_state.result = None
for k, d in [("posts", 5), ("videos", 2), ("audios", 1)]:
    if k not in st.session_state:
        st.session_state[k] = d

with st.sidebar:
    st.header("🔑 API")
    api_key = st.text_input("API ключ", type="password")
    if not api_key and "XAI_API_KEY" in st.secrets:
        api_key = st.secrets["XAI_API_KEY"]
    provider = st.selectbox("Провайдер", ["Grok (xAI)", "OpenAI"])
    model = st.text_input("Модель", value="grok-4.7" if "Grok" in provider else "gpt-4o")

def get_client():
    if not api_key:
        st.error("Введи API-ключ в сайдбаре")
        return None
    if "Grok" in provider:
        return OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")
    return OpenAI(api_key=api_key)

def generate(period, n_posts, n_videos, n_audios, fetishes, n_mailing_days, video_minutes):
    client = get_client()
    if not client:
        return None
    fetish_str = ", ".join(fetishes) if fetishes else "смешанные"
    prompt = PERSONA + f"""
Период плана: {period}
Выбранные фетиши: {fetish_str}
Желаемая длительность видео: примерно {video_minutes} минут.

Сгенерируй полный план строго по разделам (используй точные заголовки ## ):

## ПОСТЫ
Ровно {n_posts} постов. Каждый начинай с ### Пост N
Английский текст + **Перевод:** русский
После каждого поста кратко: советы по фото (поза, ракурс, что подчеркнуть).

## ВИДЕО
Ровно {n_videos} видео. Каждый начинай с ### Видео N
**Название:** короткое триггерное
**Описание:** продающее, чтобы захотелось купить
**Длительность:** примерно {video_minutes} мин
**Текст для озвучки:** ...
**Перевод:** ...
**Хештеги:** ровно 10 по теме
**Советы по съёмке:** поза, ракурс, что показать.

## АУДИО
Ровно {n_audios} аудио. Каждый начинай с ### Аудио N
**Название:** короткое триггерное
**Описание:** продающее
**Текст:** ...
**Перевод:** ...
**Хештеги:** ровно 10 по теме

## РАССЫЛКИ
На {n_mailing_days} дней. Каждый день строго 4 сообщения:
### День N
**1. MORNING HOOK (бесплатно)**
[английский с {{name}}]
**Перевод:** ...
**2. DAYTIME WARM-UP (бесплатно)**
[английский с {{name}}]
**Перевод:** ...
**3. EVENING PPV (платно)**
[английский с {{name}}]
**Перевод:** ...
**4. MORNING BUMP (бесплатно)**
[английский с {{name}}]
**Перевод:** ...
После каждого дня кратко: советы по фото/видео для этих рассылок (поза, ракурс).

## СОВЕТЫ ПО ФОТО
Общие рекомендации по фото для постов и рассылок под выбранные фетиши: позы, ракурсы, что подчёркивать, чего избегать.

## БАНДЛЫ
Предложи 2 идеи бандлов (паков фото) под выбранные фетиши.
Для каждого:
**Тема:** ...
**Количество фото:** ...
**Образы и позы:** ...
**Описание для продажи:** ...
**Рекомендуемая цена:** ...
**Перевод** ключевых частей.

## СЕКСТИНГ-ПАК
Подробный план съёмки секстинг-пака по выбранным фетишам.
Что снимать (фото + короткие видео), сценарий по шагам, позы, ракурсы, прогрессия (от тизера к более откровенному).
"""
    try:
        r = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.85,
            max_tokens=8000
        )
        return r.choices[0].message.content
    except Exception as e:
        st.error(f"Ошибка генерации: {e}")
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

st.subheader("Настройки плана")
n_posts = counter("Посты", "posts", 0, 30)
n_videos = counter("Видео", "videos", 0, 15)
n_audios = counter("Аудио", "audios", 0, 10)

st.write("")
col_a, col_b = st.columns(2)
with col_a:
    n_mailing_days = st.slider("Дней рассылок (4 сообщения/день)", 0, 30, 7)
with col_b:
    video_minutes = st.number_input("Длительность видео (мин)", 1, 30, 3)

period = st.selectbox("Период", ["1 день", "3 дня", "Неделя", "Месяц"])
fetishes = st.multiselect("Фетиши для этого плана", DEFAULT_FETISHES, default=["JOI (Jerk Off Instruction)", "Tease & Denial"])

st.write("")
if st.button("🚀 Сгенерировать план", type="primary", use_container_width=True):
    with st.spinner("Генерирую креативный контент..."):
        st.session_state.result = generate(period, n_posts, n_videos, n_audios, fetishes, n_mailing_days, video_minutes)

if st.session_state.result:
    st.divider()
    st.subheader("Результат")
    text = st.session_state.result

    # Простой и надёжный вывод всего текста + вкладки по возможности
    st.markdown(text)

    st.write("---")
    with st.expander("Скопировать весь текст"):
        st.code(text)

    # Дополнительные вкладки для удобства (если разделы нашлись)
    sections = {"ПОСТЫ": "", "ВИДЕО": "", "АУДИО": "", "РАССЫЛКИ": "", "СОВЕТЫ": "", "БАНДЛЫ": "", "СЕКСТИНГ": ""}
    current = None
    for line in text.split("\n"):
        u = line.upper().strip()
        if "## ПОСТЫ" in u or "### ПОСТ" in u:
            current = "ПОСТЫ"
        elif "## ВИДЕО" in u or "### ВИДЕО" in u:
            current = "ВИДЕО"
        elif "## АУДИО" in u or "### АУДИО" in u:
            current = "АУДИО"
        elif "## РАССЫЛКИ" in u or "### ДЕНЬ" in u:
            current = "РАССЫЛКИ"
        elif "## СОВЕТЫ" in u:
            current = "СОВЕТЫ"
        elif "## БАНДЛЫ" in u:
            current = "БАНДЛЫ"
        elif "## СЕКСТИНГ" in u:
            current = "СЕКСТИНГ"
        elif current and line.strip():
            sections[current] += line + "\n"

    tabs = st.tabs(["Посты", "Видео", "Аудио", "Рассылки", "Советы", "Бандлы", "Секстинг"])
    with tabs[0]:
        st.markdown(sections["ПОСТЫ"] or "Смотри полный текст выше")
    with tabs[1]:
        st.markdown(sections["ВИДЕО"] or "Смотри полный текст выше")
    with tabs[2]:
        st.markdown(sections["АУДИО"] or "Смотри полный текст выше")
    with tabs[3]:
        st.markdown(sections["РАССЫЛКИ"] or "Смотри полный текст выше")
    with tabs[4]:
        st.markdown(sections["СОВЕТЫ"] or "Смотри полный текст выше")
    with tabs[5]:
        st.markdown(sections["БАНДЛЫ"] or "Смотри полный текст выше")
    with tabs[6]:
        st.markdown(sections["СЕКСТИНГ"] or "Смотри полный текст выше")
