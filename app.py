import streamlit as st
from openai import OpenAI
from datetime import date, timedelta
import pandas as pd
import json
import os

PERSONA = """
Ты — элитный сценарист и контент-креатор для платформ BestFans и LoyalFans.
Твоя персона: Mistress Kayomi. Игривая домина с правом выбора.
Основной тон — дразнящий, лёгкий, с улыбкой. Можешь резко взять контроль, отдать приказ, унизить или забрать деньги, но не обязана быть жёсткой постоянно. Ты не cold hard domme.
Переключаешься:
- ~70–80% времени — игривая/доминирующая (дразнишь, улыбаешься, потом приказываешь или забираешь)
- ~20–30% — можешь быть более покорной / саб-моменты (только по желанию и за отдельную оплату)
Не врёшь характером. Если на стриме улыбаешься и играешь — в постах тоже не надо изображать ледяную богиню 24/7. Можешь быть милой, можешь быть жёсткой. Решаешь ты.
Ключевые черты: игривая, дразнящая, умеешь приказывать, не всегда жёсткая, гибкая, attention is earned, любишь, когда платят.
Стиль общения: подкол + улыбка + внезапный контроль. Не постоянная агрессия.
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

POST_SLOTS = ["00:30", "04:30", "08:30", "12:30", "16:30", "20:30"]
TRACKER_FILE = "tracker_data.json"
SCHEDULE_FILE = "schedule_data.json"

def load_json(path):
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_json(path, data):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        st.warning(f"Не удалось сохранить: {e}")

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
if "tracker" not in st.session_state:
    st.session_state.tracker = load_json(TRACKER_FILE)
if "schedule" not in st.session_state:
    st.session_state.schedule = load_json(SCHEDULE_FILE)

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
             gen_content=True, gen_bundles=False, gen_sexting=False, n_bundles=1, call_prompt="", photo_prompt=""):
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
        prompt += f"""
## БАНДЛЫ
Ровно {n_bundles} бандлов. Для каждого:
**Тема:** (на английском)
**Количество фото:**
**Образы и позы:** (на русском)
**Описание для продажи:** (на английском)
**Рекомендуемая цена:**
**Хештеги:** ровно 10 на английском
"""
    
    if gen_sexting:
        prompt += """
## СЕКСТИНГ-ПАК
Весь раздел на русском.
Разбей на части.
Для каждой части: что снимать, сколько фото/видео, примерная цена, короткий скрипт.
В конце общая рекомендация.
"""
    
    if call_prompt.strip():
        prompt += f"""
## СЦЕНАРИЙ ЗВОНКА
Запрос: {call_prompt}

Напиши диалог:
**Ты:** [короткая фраза на английском]
**Перевод:** [русский]

**Раб:** [короткая фраза на английском]
**Перевод:** [русский]

В конце 2 варианта концовки (кончил / не кончил).
"""
    
    if photo_prompt.strip():
        prompt += f"""
## ПОСТ ПО ФОТО/ВИДЕО
Описание того, что на фото или видео: {photo_prompt}

Напиши один готовый пост в стиле Mistress Kayomi (игривая Soft Domme).
Формат:
**English:**
текст поста

**Русский:**
полный перевод

Пост должен быть цепляющим, с лёгкой насмешкой, теплом или контролем, если это подходит под описание.
Не выбирай фетиш самостоятельно, опирайся только на описание.
"""
    
    if not (gen_content or gen_bundles or gen_sexting or call_prompt.strip() or photo_prompt.strip()):
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

page = st.radio("Режим", ["📝 Генератор", "📊 Трекер", "📅 Расписание постов"], horizontal=True, label_visibility="collapsed")

if page == "📝 Генератор":
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
    fetishes = st.multiselect("Фетиши", DEFAULT_FETISHES, default=["Foot Fetish"])

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
    else:
        n_bundles = 1

    st.write("---")
    call_prompt = st.text_area("Сценарий для звонка (необязательно)", height=80, placeholder="Тема, длительность, триггерные фразы...")

    st.write("---")
    photo_prompt = st.text_area(
        "Пост по фото/видео (опиши, что на фото или видео)",
        height=100,
        placeholder="Например: достаю губную помаду в виде маленького члена, смотрю на неё и слегка насмехаюсь..."
    )

    if st.button("🚀 Сгенерировать", type="primary", use_container_width=True):
        with st.spinner("Генерирую..."):
            st.session_state.result = generate(
                period, n_posts, n_videos, n_audios, fetishes,
                n_mailing_days, video_minutes, audio_minutes,
                gen_content, gen_bundles, gen_sexting, n_bundles, call_prompt, photo_prompt
            )

    if st.session_state.result:
        st.divider()
        st.markdown(st.session_state.result)
        with st.expander("Скопировать весь текст"):
            st.code(st.session_state.result)

elif page == "📊 Трекер":
    st.title("📊 Трекер контента")
    today = date.today()
    selected_date = st.date_input("Дата", today, key="tracker_date")

    date_key = str(selected_date)
    if date_key not in st.session_state.tracker:
        st.session_state.tracker[date_key] = {
            "posts": 0, "videos": 0, "audios": 0, "stories": 0, "mailings": 0
        }

    st.write("Сколько сделала:")
    col1, col2 = st.columns(2)
    with col1:
        posts = st.number_input("Посты", 0, 20, int(st.session_state.tracker[date_key].get("posts", 0)), key=f"p_{date_key}")
        videos = st.number_input("Видео", 0, 10, int(st.session_state.tracker[date_key].get("videos", 0)), key=f"v_{date_key}")
        audios = st.number_input("Аудио", 0, 10, int(st.session_state.tracker[date_key].get("audios", 0)), key=f"a_{date_key}")
    with col2:
        stories = st.number_input("Сторис", 0, 20, int(st.session_state.tracker[date_key].get("stories", 0)), key=f"s_{date_key}")
        mailings = st.number_input("Рассылки", 0, 30, int(st.session_state.tracker[date_key].get("mailings", 0)), key=f"m_{date_key}")

    if st.button("💾 Сохранить день", use_container_width=True):
        st.session_state.tracker[date_key] = {
            "posts": posts, "videos": videos, "audios": audios,
            "stories": stories, "mailings": mailings
        }
        save_json(TRACKER_FILE, st.session_state.tracker)
        st.success("Сохранено")

    st.write("---")
    st.subheader("Итог за период")
    period_days = st.selectbox("Период", [7, 14, 30], format_func=lambda x: f"Последние {x} дней")

    start = today - timedelta(days=period_days - 1)
    total = {"posts": 0, "videos": 0, "audios": 0, "stories": 0, "mailings": 0}
    days_filled = 0

    for i in range(period_days):
        d = str(start + timedelta(days=i))
        if d in st.session_state.tracker:
            days_filled += 1
            for k in total:
                total[k] += st.session_state.tracker[d].get(k, 0)

    st.metric("Дней заполнено", f"{days_filled} / {period_days}")
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Посты", total["posts"])
    c2.metric("Видео", total["videos"])
    c3.metric("Аудио", total["audios"])
    c4.metric("Сторис", total["stories"])
    c5.metric("Рассылки", total["mailings"])

    if st.session_state.tracker:
        df = pd.DataFrame.from_dict(st.session_state.tracker, orient="index")
        df.index.name = "Дата"
        st.dataframe(df.sort_index(ascending=False), use_container_width=True)

    st.download_button(
        "⬇️ Скачать копию трекера",
        data=json.dumps(st.session_state.tracker, ensure_ascii=False, indent=2),
        file_name="tracker_backup.json",
        mime="application/json"
    )

else:
    st.title("📅 Расписание постов")
    today = date.today()
    selected_date = st.date_input("Дата", today, key="schedule_date")
    date_key = str(selected_date)

    if date_key not in st.session_state.schedule:
        st.session_state.schedule[date_key] = {slot: False for slot in POST_SLOTS}

    st.write(f"**Слоты на {selected_date.strftime('%d.%m.%Y')}**")
    st.caption("Отмечай галочкой слоты, которые уже заняты / сделаны, чтобы не дублировать.")

    cols = st.columns(3)
    updated = False
    for i, slot in enumerate(POST_SLOTS):
        with cols[i % 3]:
            checked = st.checkbox(
                slot,
                value=st.session_state.schedule[date_key].get(slot, False),
                key=f"slot_{date_key}_{slot}"
            )
            if checked != st.session_state.schedule[date_key].get(slot, False):
                st.session_state.schedule[date_key][slot] = checked
                updated = True

    if updated or st.button("💾 Сохранить расписание", use_container_width=True):
        save_json(SCHEDULE_FILE, st.session_state.schedule)
        st.success("Расписание сохранено")

    st.write("---")
    st.subheader("Обзор на неделю")
    week_start = selected_date - timedelta(days=selected_date.weekday())
    for i in range(7):
        d = week_start + timedelta(days=i)
        d_key = str(d)
        slots = st.session_state.schedule.get(d_key, {})
        done = sum(1 for v in slots.values() if v)
        st.write(f"**{d.strftime('%d.%m %a')}**: {done}/6 слотов занято")

    st.download_button(
        "⬇️ Скачать расписание",
        data=json.dumps(st.session_state.schedule, ensure_ascii=False, indent=2),
        file_name="schedule_backup.json",
        mime="application/json"
    )
