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
- Не выдумывай конкретные цвета одежды, лака или обстановку.
- Используй нишевый сленг. Говори как живая дерзкая доминантка.
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
        st.error("Введи API-ключ")
        return None
    if "Grok" in provider:
        return OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")
    return OpenAI(api_key=api_key)

def generate(period, n_posts, n_videos, n_audios, fetishes, n_mailing_days, video_minutes,
             gen_content=True, gen_bundles=False, gen_sexting=False, n_bundles=2):
    client = get_client()
    if not client:
        return None
    fetish_str = ", ".join(fetishes) if fetishes else "смешанные"
    
    prompt = PERSONA + f"\nПериод: {period}\nФетиши: {fetish_str}\nДлительность видео: ~{video_minutes} мин.\n\n"
    prompt += "Сгенерируй ТОЛЬКО запрошенные разделы. Используй точные заголовки ## \n\n"
    
    if gen_content:
        prompt += f"""## ПОСТЫ
Ровно {n_posts} постов. Каждый с ### Пост N
Английский + **Перевод:**
Кратко советы по фото (поза, ракурс).

## ВИДЕО
Ровно {n_videos} видео. Каждый с ### Видео N
**Название:**
**Описание:** (продающее)
**Длительность:** ~{video_minutes} мин
**Текст для озвучки:**
**Перевод:**
**Хештеги:** 10 шт
**Советы по съёмке:**

## АУДИО
Ровно {n_audios} аудио. Каждый с ### Аудио N
**Название:**
**Описание:**
**Текст:**
**Перевод:**
**Хештеги:** 10 шт

## РАССЫЛКИ
На {n_mailing_days} дней. Каждый день 4 сообщения с {{name}}:
### День N
**1. MORNING HOOK**
**2. DAYTIME WARM-UP**
**3. EVENING PPV**
**4. MORNING BUMP**
У каждого английский + перевод + кратко советы по фото.
"""
    
    if gen_bundles:
        prompt += f"""
## БАНДЛЫ
Сгенерируй ровно {n_bundles} идей бандлов (паков фото) под выбранные фетиши.
Для каждого бандла:
**Тема:**
**Количество фото:**
**Образы и позы:**
**Описание для продажи:**
**Рекомендуемая цена:**
**Хештеги:** ровно 10 хештегов по теме
Перевод ключевых частей.
"""
    
    if gen_sexting:
        prompt += """
## СЕКСТИНГ-ПАК
Подробный план съёмки секстинг-пака по выбранным фетишам.
Что снимать (фото + короткие видео), сценарий по шагам, позы, ракурсы, прогрессия.
В конце добавь:
**Рекомендации по цене:** как лучше продавать этот пак (ориентировочная цена, как дробить или продавать целиком).
"""
    
    if not (gen_content or gen_bundles or gen_sexting):
        return "Ничего не выбрано для генерации."
    
    try:
        r = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.85,
            max_tokens=8000
        )
        return r.choices[0].message.content
    except Exception as e:
        st.error(f"Ошибка: {e}")
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
    n_mailing_days = st.slider("Количество дней для рассылок", 0, 30, 7)
with col_b:
    video_minutes = st.number_input("Длительность видео (мин)", 1, 30, 3)

period = st.selectbox("Период", ["1 день", "3 дня", "Неделя", "Месяц"])
fetishes = st.multiselect("Фетиши для этого плана", DEFAULT_FETISHES, default=["JOI (Jerk Off Instruction)", "Tease & Denial"])

st.write("")
col1, col2, col3 = st.columns(3)
with col1:
    gen_content = st.checkbox("Основной контент", value=True)
with col2:
    gen_bundles = st.checkbox("Бандлы", value=False)
with col3:
    gen_sexting = st.checkbox("Секстинг-пак", value=False)

if gen_bundles:
    n_bundles = st.number_input("Сколько бандлов сгенерировать", 1, 10, 2)
else:
    n_bundles = 2

st.write("")
if st.button("🚀 Сгенерировать план", type="primary", use_container_width=True):
    with st.spinner("Генерирую..."):
        st.session_state.result = generate(
            period, n_posts, n_videos, n_audios, fetishes,
            n_mailing_days, video_minutes,
            gen_content, gen_bundles, gen_sexting, n_bundles
        )

if st.session_state.result:
    st.divider()
    st.subheader("Результат")
    st.markdown(st.session_state.result)
    with st.expander("Скопировать весь текст"):
        st.code(st.session_state.result)
        
