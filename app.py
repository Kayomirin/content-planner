import streamlit as st
from openai import OpenAI
import json

# ====================== НАСТРОЙКИ (ИЗМЕНИ ПОД СЕБЯ) ======================
PERSONA = """
Ты — контент-креатор для Fansly/OnlyFans. 
Твоя персона: [ОПИШИ СЕБЯ: возраст, внешность, характер, тон общения, стиль, как ты общаешься с фанатами].
Ты работаешь с фетишами: [ПЕРЕЧИСЛИ СВОИ ОСНОВНЫЕ ФЕТИШИ].
Тон: игривый, соблазнительный, уверенный, с элементами доминирования/подчинения по ситуации, много эмодзи, разговорный стиль.
Контент всегда оригинальный, креативный, не повторяющийся.
"""

DEFAULT_FETISHES = [
    "JOI", "Findom", "Domination", "Submission", "Feet", "Tease & Denial",
    "SPH", "CEI", "Humiliation", "Praise", "Roleplay", "ASMR", "Custom"
]

# ========================================================================

st.set_page_config(page_title="Fans Content Planner", page_icon="🔥", layout="wide")

st.title("🔥 Контент-планнер для Fansly")
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

def generate_content(period, n_posts, n_videos, n_audios, selected_fetishes, regenerate_item=None):
    client = get_client()
    if not client:
        return None
    
    fetish_str = ", ".join(selected_fetishes) if selected_fetishes else "смешанные"
    
    system = PERSONA + f"""
Ты генерируешь контент-план на {period}.
Выбранные фетиши для этого плана: {fetish_str}.
Контент должен быть на английском языке (корректный, естественный), с переводом на русский в скобках или отдельным блоком.
Стиль: с эмодзи, соблазнительный, под продажу.
Для видео — полное описание сцены + текст, который нужно говорить.
Для аудио — готовый текст для записи.
Для рассылок — постепенные последовательности (welcome → engagement → upsell → soft sell → hard sell).
Всегда делай контент уникальным и креативным.
"""
    
    if regenerate_item:
        user_prompt = f"Перегенерируй только этот элемент: {regenerate_item}\nОстальной план оставь в том же стиле."
    else:
        user_prompt = f"""
Сгенерируй полный контент-план на {period}:
- {n_posts} постов для ленты
- {n_videos} идей/скриптов для видео
- {n_audios} текстов для аудио
- 2-3 последовательности рассылок в личные сообщения (постепенные, ведущие к продаже)

Формат ответа строго в Markdown с заголовками:
## Посты
### Пост 1
(текст на английском)
**Перевод:** ...

## Видео
### Видео 1
Описание сцены + текст для озвучки
**Перевод:** ...

## Аудио
### Аудио 1
Текст для записи
**Перевод:** ...

## Рассылки
### Последовательность 1
1. Сообщение 1
2. Сообщение 2
...
"""
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.9,
            max_tokens=4000
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Ошибка генерации: {e}")
        return None

# Основная форма
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Настройки плана")
    period = st.selectbox("Период", ["1 день", "3 дня", "Неделя", "Месяц"])
    n_posts = st.slider("Постов", 1, 10, 5)
    n_videos = st.slider("Видео", 1, 5, 2)
    n_audios = st.slider("Аудио", 0, 3, 1)
    selected_fetishes = st.multiselect(
        "Фетиши для этого плана",
        options=DEFAULT_FETISHES,
        default=["JOI", "Tease & Denial"]
    )
    
    if st.button("🚀 Сгенерировать план", type="primary", use_container_width=True):
        with st.spinner("Генерирую креативный контент..."):
            result = generate_content(period, n_posts, n_videos, n_audios, selected_fetishes)
            if result:
                st.session_state.generated = result
                st.session_state.history.append(result)
                st.rerun()

with col2:
    if st.session_state.generated:
        st.subheader("Результат")
        st.markdown(st.session_state.generated)
        
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
