import streamlit as st
from openai import OpenAI
import base64

PERSONA = """
Ты — элитный сценарист и контент-креатор для платформ LoyalFans, BestFans и Fansly.
Твоя персона: Kayomi — игривая дразнящая девочка с элементами Soft Domme и Findom.
Sweet smile. Dangerous intentions.
Ты избалованная и дразнящая, умеешь улыбаться и внезапно брать контроль.
Основной фокус зависит от выбранных фетишей. Findom — это часть твоего стиля, но не обязательный элемент каждого поста.
Если в запросе выбраны конкретные фетиши (например Ass Worship, Foot Fetish и т.д.) — делай контент в первую очередь про них.
Стиль: подкол + улыбка + контроль по настроению. Не навязывай Findom, если его не просили.
Правила: основной контент на идеальном английском + перевод на русский. Никогда не упоминай Россию или рубли.
Фразы в диалогах — короткие и естественные.
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

MY_HASHTAGS = """
#feet #footfetish #footworship #soles #toes #barefeet #feetworship #arches #toespread #footjob #softdomme #FemDom #domme #mistress #Goddess #sexygoddess #brat #princess #obey #slave #worship #bodyworship #FinDom #findomme #financialdomination #paypig #humanATM #obeyandpay #findomgame #piggy #tease #teasing #teaseanddenial #lingerie #panties #pantyhose #stockings #socks #heels #highheels #fishnets #nylons #legs #ass #assworship #booty #curves #SPH #dickrating #smallpenis #smalldick #humiliation #degradation #joi #middlefinger #gaze #brunette #natural #kinkyfantasy #Sexting #dirtytalk #pov #submissive #serving
"""

def encode_image(uploaded_file):
    return base64.b64encode(uploaded_file.getvalue()).decode("utf-8")

st.set_page_config(page_title="Контент-планнер", page_icon="🔥", layout="centered")

st.markdown("""
<style>
.stButton > button {
    border-radius: 12px !important;
    border: 1.5px solid #7c3aed !important;
    color: #7c3aed !important;
}
.stButton > button:hover {
    background: #7c3aed !important;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

if "result" not in st.session_state:
    st.session_state.result = None

with st.sidebar:
    st.header("🔑 API")
    api_key = st.text_input("API ключ", type="password")
    if not api_key and "XAI_API_KEY" in st.secrets:
        api_key = st.secrets["XAI_API_KEY"]
    provider = st.selectbox("Провайдер", ["Grok (xAI)", "OpenAI"])
    model = st.text_input("Модель", value="grok-4.7")

def get_client():
    if not api_key:
        st.error("Введи API-ключ")
        return None
    if "Grok" in provider:
        return OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")
    return OpenAI(api_key=api_key)

def generate(period, n_posts, n_videos, n_audios, fetishes, n_mailing_days, video_minutes, audio_minutes,
             gen_content=True, gen_bundles=False, gen_sexting=False, n_bundles=1, call_prompt="", photo_prompt="", uploaded_image=None,
             bundle_extra="", sexting_extra=""):
    client = get_client()
    if not client:
        return None
    fetish_str = ", ".join(fetishes) if fetishes else "смешанные"
    
    base_prompt =     base_prompt += "\nВажно: делай контент в первую очередь под выбранные фетиши. Не навязывай Findom автоматически.\n"
    
    content_parts = [{"type": "text", "text": base_prompt}]
    
    if gen_content:
        content_parts[0]["text"] += f"""## ПОСТЫ
Ровно {n_posts} постов. Английский + перевод + кратко советы по фото (на русском).

## ВИДЕО
Ровно {n_videos} видео. Название, описание, длительность ~{video_minutes} мин.
Скрипт с таймингом, текст в кавычках — что сказать.
Перевод.
**Советы по съёмке:** обязательно на русском.
10 хештегов.

## АУДИО
Ровно {n_audios} аудио. Название, описание.
Длительность ~{audio_minutes} мин.
Скрипт с таймингом и паузами.
Перевод, 10 хештегов.

## РАССЫЛКИ
Сгенерируй ровно {n_mailing_days} отдельных независимых рассылок под выбранные фетиши.
Каждая рассылка — самостоятельное сообщение.

Для каждой:
### Рассылка N
Текст на английском с {{name}}
**Перевод:** полный русский перевод
Укажи: бесплатный крючок или с намёком на PPV.
Если PPV — кратко что приложить и примерную цену.

Не делай цепочку из 4 этапов. Только отдельные сильные рассылки.
"""
    
    if gen_bundles:
        extra = f"\nДополнительно (одежда / тема / пожелания): {bundle_extra}" if bundle_extra.strip() else ""
        content_parts[0]["text"] += f"""
## БАНДЛЫ
Ровно {n_bundles} бандлов. Для каждого:
**Тема:** (на английском)
**Количество фото:**
**Образы и позы:** (на русском)
**Описание для продажи:** (на английском)
**Рекомендуемая цена:**
**Хештеги:** ровно 10 на английском
{extra}
"""
    
    if gen_sexting:
        extra = f"\nДополнительно (одежда / тема / пожелания): {sexting_extra}" if sexting_extra.strip() else ""
        content_parts[0]["text"] += f"""
## СЕКСТИНГ-ПАК
Весь раздел на русском.
Разбей на части.
Для каждой части: что снимать, сколько фото/видео, примерная цена, короткий скрипт.
В конце общая рекомендация.
{extra}
"""
    
    if call_prompt.strip():
        content_parts[0]["text"] += f"""
## СЦЕНАРИЙ ЗВОНКА
Запрос: {call_prompt}

Напиши диалог:
**Ты:** [короткая фраза на английском]
**Перевод:** [русский]

**Раб:** [короткая фраза на английском]
**Перевод:** [русский]

В конце 2 варианта концовки (кончил / не кончил).
"""
    
    if photo_prompt.strip() or uploaded_image:
        photo_text = """
## ПОСТ ПО ФОТО/ВИДЕО
"""
        if photo_prompt.strip():
            photo_text += f"Дополнительное описание: {photo_prompt}\n"
        if uploaded_image:
            photo_text += "Посмотри на загруженное фото и напиши пост на его основе.\n"
        photo_text += """
Напиши один готовый пост в стиле Kayomi (игривая Soft Domme / Brat Findom).
Формат:
**English:**
текст поста

**Русский:**
полный перевод

Пост должен быть цепляющим, с лёгкой насмешкой, теплом или контролем.
"""
        content_parts[0]["text"] += photo_text
        
        if uploaded_image:
            base64_image = encode_image(uploaded_image)
            content_parts.append({
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
            })
    
    if not (gen_content or gen_bundles or gen_sexting or call_prompt.strip() or photo_prompt.strip() or uploaded_image):
        return "Ничего не выбрано."
    
    try:
        messages = [{"role": "user", "content": content_parts}]
        r = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.8,
            max_tokens=8000
        )
        return r.choices[0].message.content
    except Exception as e:
        st.error(str(e))
        return None

st.title("🔥 Контент-планнер")
st.subheader("Настройки")

col1, col2 = st.columns(2)
with col1:
    n_posts = st.slider("Посты", 0, 15, 0)
    n_videos = st.slider("Видео", 0, 8, 0)
    n_audios = st.slider("Аудио", 0, 5, 0)
with col2:
    video_minutes = st.slider("Длит. видео (мин)", 1, 20, 5)
    audio_minutes = st.slider("Длит. аудио (мин)", 1, 15, 5)
    n_mailing_days = st.slider("Количество рассылок", 0, 14, 0)

period = st.selectbox("Период", ["1 день", "3 дня", "Неделя", "Месяц"])
fetishes = st.multiselect("Фетиши", DEFAULT_FETISHES)

st.write("")
c1, c2, c3 = st.columns(3)
with c1:
    gen_content = st.checkbox("Основной контент", value=True)
with c2:
    gen_bundles = st.checkbox("Бандлы", value=False)
with c3:
    gen_sexting = st.checkbox("Секстинг-пак", value=False)

if gen_bundles:
    n_bundles = st.number_input("Сколько бандлов", 1, 5, 1)
    bundle_extra = st.text_area("Одежда / тема / пожелания для бандла", height=70, placeholder="Например: чёрное бельё, джинсы, босиком, в носках...")
else:
    n_bundles = 1
    bundle_extra = ""

if gen_sexting:
    sexting_extra = st.text_area("Одежда / тема / пожелания для секстинг-пака", height=70, placeholder="Например: колготки, каблуки, домашняя одежда, футовый фокус...")
else:
    sexting_extra = ""

st.write("---")
call_prompt = st.text_area("Сценарий для звонка (необязательно)", height=80, placeholder="Тема, длительность, триггерные фразы...")

st.write("---")
photo_prompt = st.text_area(
    "Пост по фото/видео (опиши или загрузи фото ниже)",
    height=80,
    placeholder="Можно оставить пустым, если загружаешь фото..."
)
uploaded_image = st.file_uploader("Загрузить фото для поста", type=["jpg", "jpeg", "png"])

if st.button("🚀 Сгенерировать", type="primary", use_container_width=True):
    with st.spinner("Генерирую..."):
        st.session_state.result = generate(
            period, n_posts, n_videos, n_audios, fetishes,
            n_mailing_days, video_minutes, audio_minutes,
            gen_content, gen_bundles, gen_sexting, n_bundles, call_prompt, photo_prompt, uploaded_image,
            bundle_extra, sexting_extra
        )

if st.session_state.result:
    st.divider()
    st.markdown(st.session_state.result)
    with st.expander("Скопировать весь текст"):
        st.code(st.session_state.result)
