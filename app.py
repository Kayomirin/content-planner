import streamlit as st
from openai import OpenAI

PERSONA = """
Ты — элитный сценарист и контент-креатор для платформ Fansly и LoyalFans.
Твоя персона: Mistress Kayomi. Тебе 25 лет. Ты — Soft Domme.
Тон: властный, соблазнительный, высокомерный, но обволакивающий.
Если выбраны жёсткие фетиши — добавляй давление и обесценивание.
Правила: основной контент на идеальном английском + перевод на русский. Никогда не упоминай Россию или рубли.
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
    border-radius: 12px !important;
    border: 1.5px solid #a855f7 !important;
    background: transparent !important;
    color: #7c3aed !important;
    font-weight: 600 !important;
    min-width: 36px !important;
    padding: 0.2rem 0.6rem !important;
}
.stButton > button:hover {
    background: #a855f7 !important;
    color: white !important;
}
div[data-testid="column"] {
    padding: 0 4px !important;
}
</style>
""", unsafe_allow_html=True)

if "result" not in st.session_state:
    st.session_state.result = None
for k, d in [("posts", 3), ("videos", 1), ("audios", 1), ("mail_days", 1), ("vid_min", 5), ("aud_min", 5)]:
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

def generate(period, n_posts, n_videos, n_audios, fetishes, n_mailing_days, video_minutes, audio_minutes,
             gen_content=True, gen_bundles=False, gen_sexting=False, n_bundles=1):
    client = get_client()
    if not client:
        return None
    fetish_str = ", ".join(fetishes) if fetishes else "смешанные"
    
    prompt = PERSONA + f"\nФетиши: {fetish_str}\n\nСгенерируй ТОЛЬКО запрошенные разделы:\n\n"
    
    if gen_content:
        prompt += f"""## ПОСТЫ
Ровно {n_posts} постов. Английский + перевод + кратко советы по фото (на русском).

## ВИДЕО
Ровно {n_videos} видео. Название, описание, длительность ~{video_minutes} мин.
Скрипт с таймингом, текст в кавычках — что сказать.
Перевод.
**Советы по съёмке:** обязательно на русском (ракурс, позы, что подчеркнуть).
10 хештегов.

## АУДИО
Ровно {n_audios} аудио. Название, описание.
Длительность ~{audio_minutes} мин.
Скрипт с таймингом и паузами.
Перевод, 10 хештегов.

## РАССЫЛКИ
На {n_mailing_days} дней. Каждый день 4 сообщения с {{name}}:
1. MORNING HOOK
2. DAYTIME WARM-UP
3. EVENING PPV — обязательно добавь примерную цену за видео и за фото (если есть).
4. MORNING BUMP
У каждого английский + перевод.
"""
    
    if gen_bundles:
        prompt += f"""
## БАНДЛЫ
Ровно {n_bundles} бандлов. Для каждого:
**Тема:** (на английском)
**Количество фото:**
**Образы и позы:** (на русском)
**Описание для продажи:** (на английском)
**Рекомендуемая цена:** (простая цифра)
**Хештеги:** ровно 10 на английском
"""
    
    if gen_sexting:
        prompt += """
## СЕКСТИНГ-ПАК
Весь раздел на русском.
Разбей на части.
Для каждой части:
- Что снимать (позы, ракурсы)
- Сколько фото и коротких видео
- Примерная цена за эту часть
- Короткий примерный скрипт к этим фото/видео
В конце общая рекомендация по продаже всего пака.
"""
    
    if not (gen_content or gen_bundles or gen_sexting):
        return "Ничего не выбрано."
    
    try:
        r = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,
            max_tokens=8000
        )
        return r.choices[0].message.content
    except Exception as e:
        st.error(str(e))
        return None

def mini_counter(label, key, min_v=0, max_v=30):
    c1, c2, c3, c4 = st.columns([2.2, 0.6, 0.8, 0.6])
    with c1:
        st.markdown(f"**{label}**")
    with c2:
        if st.button("−", key=f"m_{key}"):
            st.session_state[key] = max(min_v, st.session_state[key] - 1)
    with c3:
        st.markdown(f"<div style='text-align:center;font-size:1.3rem;font-weight:600;padding-top:2px'>{st.session_state[key]}</div>", unsafe_allow_html=True)
    with c4:
        if st.button("+", key=f"p_{key}"):
            st.session_state[key] = min(max_v, st.session_state[key] + 1)
    return st.session_state[key]

st.subheader("Настройки")

# Посты
n_posts = mini_counter("Посты", "posts", 0, 20)

# Видео + длительность в одной строке
c1, c2 = st.columns([1.6, 1])
with c1:
    n_videos = mini_counter("Видео", "videos", 0, 10)
with c2:
    st.markdown("**Длит. видео (мин)**")
    cc1, cc2, cc3 = st.columns([1, 1.2, 1])
    with cc1:
        if st.button("−", key="m_vidmin"):
            st.session_state.vid_min = max(1, st.session_state.vid_min - 1)
    with cc2:
        st.markdown(f"<div style='text-align:center;font-size:1.3rem;font-weight:600'>{st.session_state.vid_min}</div>", unsafe_allow_html=True)
    with cc3:
        if st.button("+", key="p_vidmin"):
            st.session_state.vid_min = min(30, st.session_state.vid_min + 1)
    video_minutes = st.session_state.vid_min

# Аудио + длительность
c1, c2 = st.columns([1.6, 1])
with c1:
    n_audios = mini_counter("Аудио", "audios", 0, 10)
with c2:
    st.markdown("**Длит. аудио (мин)**")
    cc1, cc2, cc3 = st.columns([1, 1.2, 1])
    with cc1:
        if st.button("−", key="m_audmin"):
            st.session_state.aud_min = max(1, st.session_state.aud_min - 1)
    with cc2:
        st.markdown(f"<div style='text-align:center;font-size:1.3rem;font-weight:600'>{st.session_state.aud_min}</div>", unsafe_allow_html=True)
    with cc3:
        if st.button("+", key="p_audmin"):
            st.session_state.aud_min = min(20, st.session_state.aud_min + 1)
    audio_minutes = st.session_state.aud_min

st.write("")
n_mailing_days = mini_counter("Дней рассылок", "mail_days", 0, 14)

period = st.selectbox("Период", ["1 день", "3 дня", "Неделя", "Месяц"])
fetishes = st.multiselect("Фетиши", DEFAULT_FETISHES, default=["Foot Fetish"])

st.write("")
col1, col2, col3 = st.columns(3)
with col1:
    gen_content = st.checkbox("Основной контент", value=True)
with col2:
    gen_bundles = st.checkbox("Бандлы", value=False)
with col3:
    gen_sexting = st.checkbox("Секстинг-пак", value=False)

if gen_bundles:
    n_bundles = st.number_input("Сколько бандлов", 1, 5, 1)
else:
    n_bundles = 1

st.write("")
if st.button("🚀 Сгенерировать план", type="primary", use_container_width=True):
    with st.spinner("Генерирую..."):
        st.session_state.result = generate(
            period, n_posts, n_videos, n_audios, fetishes,
            n_mailing_days, video_minutes, audio_minutes,
            gen_content, gen_bundles, gen_sexting, n_bundles
        )

if st.session_state.result:
    st.divider()
    st.subheader("Результат")
    st.markdown(st.session_state.result)
    with st.expander("Скопировать весь текст"):
        st.code(st.session_state.result)
