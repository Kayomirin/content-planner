import streamlit as st
from openai import OpenAI
import json

# ====================== НАСТРОЙКИ (ИЗМЕНИ ПОД СЕБЯ) ======================
PERSONA = """
Ты — элитный сценарист и контент-креатор для платформ Fansly и LoyalFans.

Твоя персона: Mistress Kayomi (Мистресс Кайоми). Тебе 25 лет. Ты — Soft Domme (мягкая доминантка).
Твой характер: игривая, дразнящая, уверенная в себе, с высокими стандартами. Ты не используешь экстремальный хардкор или прямую физическую жестокость (если только не выбраны фетиши вроде Trampling или Humiliation). Ты обожаешь психологический контроль, финансовое доминирование (Findom) и Tease & Denial. Ты общаешься с фанами свысока, но притягательно, заставляя их изнывать и умолять о твоем внимании и разрешении.

Ты работаешь со следующими фетишами:
Foot Fetish, Toe Worship, Crushing / Trampling, Socks Fetish, Striped Socks, Pantyhose Fetish, Fishnets, High Heels, Body Worship, Ass Worship, Breast Worship, Armpit Fetish, Hair Worship, Hair Brushing, Femdom, Soft Domme, Hard Findom, Financial Domination, Paypig Control, Total Power Exchange (TPE), Contracts & Control, Mind Games, Hypnosis, Correction Training, Spanking, Humiliation, Objectification, SPH (Small Penis Humiliation), Cuckolding, Sissification, Slutification, Beta Loser Degradation, Virgin Humiliation, Gooner Control, JOI (Jerk Off Instruction), CEI (Cum Eating Instruction), Tease & Denial, Pegging, Toy Control, Puppy Play, GFE (Girlfriend Experience), Bratty Girl, Chastity & Keyholder, Techdom & Anydesk, Giantess Fetish, Spitting & Saliva Fetish, Facesitting & Squashing, Farts Fetish, Tummy Fetish, Wedgie, Worn Clothes & Used Panties, Denim & Tight Jeans, Latex & Leather Fetish, Gloves Fetish.

Тон: Властный, соблазнительный, высокомерный, но обволакивающий. Если выбраны фетиши SPH, Humiliation или Trampling — используй более жесткие слова, обесценивание и строгие команды. В остальных случаях держи фокус на игривом дразнении и контроле.

КРИТИЧЕСКИЕ ПРАВИЛА:
1. Итоговый контент (посты, скрипты, рассылки) всегда должен быть на ИДЕАЛЬНОМ АНГЛИЙСКОМ языке (с использованием нишевого сленга сабов и доминаток).
2. Сразу после английского текста ОБЯЗАТЕЛЬНО предоставляй полный ПЕРЕВОД НА РУССКИЙ язык.
3. НИКОГДА, ни при каких обстоятельствах, не упоминай Россию, рубли или что-либо связанное с этой страной.
4. Не выдумывай конкретные цвета одежды, лака для ногтей или обстановку, сохраняй описания универсальными, но горячими.
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

# ========================================================================

st.set_page_config(page_title="Fans Content Planner", page_icon="🔥", layout="wide")

st.title("🔥 Контент-планнер для LoyalFans")
st.caption("Настрой параметры → Сгенерируй → Переделай только то, что не понравилось")

# Инициализация session state
if "generated" not in st.session_state:
    st.session_state.generated = None
if "history" not in st.session_state:
    st.session_state.history = []

# Sidebar — настройки API
with st.sidebar:
    st.header("🔑 API")
    api_key = st.text_input("API ключ (Grok / OpenAI)", type="password", 
                            help="Для Grok: ключ с console.x.ai. Можно сохранить в secrets.")
    if not api_key and "XAI_API_KEY" in st.secrets:
        api_key = st.secrets["XAI_API_KEY"]
    base_url = st.selectbox("Провайдер", ["Grok (xAI)", "OpenAI"], index=0)
    model = st.text_input("Модель", value="grok-4.7" if base_url == "Grok (xAI)" else "gpt-4o")
    
    st.divider()
    st.info("После первого успешного запуска можно скрыть ключ в Streamlit Cloud Secrets.")

def get_client():
    if not api_key:
        st.error("Введи API-ключ в сайдбаре")
        return None
    if base_url.startswith("Grok"):
        return OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")
    else:
        return OpenAI(api_key=api_key)

def generate_content(period, n_posts, n_videos, n_audios, selected_fetishes, n_days_mailings=0, regenerate_item=None):
    client = get_client()
    if not client:
        return None
    
    fetish_str = ", ".join(selected_fetishes) if selected_fetishes else "смешанные"
    
    system = PERSONA + f"""
Ты генерируешь контент-план на {period}.
Выбранные фетиши для этого плана: {fetish_str}.
Контент всегда на идеальном английском + полный перевод на русский сразу под ним.
Используй нишевый сленг сабов и доминаток.
НИКОГДА не упоминай Россию, рубли или что-либо связанное с этой страной.
Тон: Soft Domme — игривый, властный, соблазнительный. Если выбраны жёсткие фетиши (SPH, Humiliation, Trampling и т.п.) — добавляй элементы жёсткости и обесценивания.
"""
    
    if regenerate_item:
        user_prompt = f"Перегенерируй только этот элемент: {regenerate_item}\nОстальной план оставь в том же стиле и структуре."
    else:
        user_prompt = f"""
Сгенерируй полный контент-план на {period}.

СТРОГО соблюдай структуру:

## Посты
Ровно {n_posts} постов. Каждый отдельным блоком.

### Пост 1
[английский текст]
**Перевод:** [русский]

## Видео
Ровно {n_videos} видео. Каждый отдельным блоком.

### Видео 1
**Описание сцены:** ...
**Текст для озвучки:** ...
**Перевод:** ...

## Аудио
Ровно {n_audios} аудио.

### Аудио 1
[английский]
**Перевод:** ...

## Массовые рассылки
Сделай рассылки на {n_days_mailings} дней. На каждый день ровно 2 сообщения:

### День 1
**MORNING HOOK (Утренний крючок):**
[английский текст с {{name}}]
**Перевод:** ...

**EVENING PPV (Вечерняя платная):**
[английский текст с {{name}}]
**Перевод:** ...

### День 2
...

Правила для рассылок:
- MORNING HOOK — бесплатный крючок. Заставь фана оправдываться, ждать или сомневаться.
- EVENING PPV — дразнящий текст под locked-контент. Фрустрирующий, чтобы купили.
- Обязательно используй плейсхолдер {{name}} в каждом сообщении.
- Тон Soft Domme. При жёстких фетишах добавляй жёсткость.
"""
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.9,
            max_tokens=6000
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Ошибка генерации: {e}")
        return None

with col1:
    st.subheader("Настройки плана")
    period = st.selectbox("Период", ["1 день", "3 дня", "Неделя", "Месяц"])
    n_posts = st.slider("Постов", 0, 10, 5)
    n_videos = st.slider("Видео", 0, 5, 2)
    n_audios = st.slider("Аудио", 0, 3, 1)
    n_days_mailings = st.slider("Дней рассылок (по 2 в день)", 0, 14, 3)
    selected_fetishes = st.multiselect(
    "Фетиши для этого плана",
    options=DEFAULT_FETISHES,
    default=["JOI (Jerk Off Instruction)", "Tease & Denial"]
)
    
    if st.button("🚀 Сгенерировать план", type="primary", use_container_width=True):
        with st.spinner("Генерирую креативный контент..."):
            result = generate_content(period, n_posts, n_videos, n_audios, selected_fetishes, n_days_mailings)
            if result:
                st.session_state.generated = result
                st.session_state.history.append(result)
                st.rerun()

with col2:
    if st.session_state.generated:
        st.subheader("Результат")
        st.markdown(st.session_state.generated)
        
        st.code(st.session_state.generated, language=None)
        st.caption("Нажми на иконку копирования справа вверху блока, чтобы скопировать весь план.")
        
        st.divider()
        st.subheader("Перегенерировать отдельный элемент")
        regen_type = st.selectbox("Что переделать?", ["Пост", "Видео", "Аудио", "Рассылку"])
        regen_num = st.number_input("Номер", min_value=1, max_value=10, value=1)
        if st.button("🔄 Перегенерировать только это"):
            item_desc = f"{regen_type} {regen_num}"
            with st.spinner("Перегенерирую..."):
                new_result = generate_content(period, n_posts, n_videos, n_audios, selected_fetishes, regenerate_item=item_desc)
                if new_result:
                    st.session_state.generated = new_result
                    st.rerun()
    else:
        st.info("Настрой параметры слева и нажми «Сгенерировать план»")

st.divider()
st.caption("Совет: сохрани понравившийся план в заметки. При необходимости отредактируй PERSONA и список фетишей в коде.")
