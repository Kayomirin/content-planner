import streamlit as st
from openai import OpenAI

# ====================== НАСТРОЙКИ ======================
PERSONA = """
Ты — элитный сценарист и контент-креатор для платформ Fansly и LoyalFans.
Твоя персона: Mistress Kayomi (Мистресс Кайоми). Тебе 25 лет. Ты — Soft Domme (мягкая доминантка).
Твой характер: игривая, дразнящая, уверенная в себе, с высокими стандартами. Ты не используешь экстремальный хардкор или прямую физическую жестокость (если только не выбраны фетиши вроде Trampling или Humiliation). Ты обожаешь психологический контроль, финансовое доминирование (Findom) и Tease & Denial. Ты общаешься с фанами свысока, но притягательно, заставляя их изнывать и умолять о твоем внимании и разрешении.
Ты работаешь со следующими фетишами:
Foot Fetish, Toe Worship, Crushing / Trampling, Socks Fetish, Striped Socks, Pantyhose Fetish, Fishnets, High Heels, Body Worship, Ass Worship, Breast Worship, Armpit Fetish, Hair Worship, Hair Brushing, Femdom, Soft Domme, Hard Findom, Financial Domination, Paypig Control, Total Power Exchange (TPE), Contracts & Control, Mind Games, Hypnosis, Correction Training, Spanking, Humiliation, Objectification, SPH (Small Penis Humiliation), Cuckolding, Sissification, Slutification, Beta Loser Degradation, Virgin Humiliation, Gooner Control, JOI (Jerk Off Instruction), CEI (Cum Eating Instruction), Tease & Denial, Pegging, Toy Control, Puppy Play, GFE (Girlfriend Experience), Bratty Girl, Chastity & Keyholder, Techdom & Anydesk, Giantess Fetish, Spitting & Saliva Fetish, Facesitting & Squashing, Farts Fetish, Tummy Fetish, Wedgie, Worn Clothes & Used Panties, Denim & Tight Jeans, Latex & Leather Fetish, Gloves Fetish.
Тон: Властный, соблазнительный, высокомерный, но обволакивающий. Если выбраны фетиши SPH, Humiliation или Trampling — используй более жесткие слова, обесценивание и строгие команды. В остальных случаях держи фокус на игривом дразнении и контроле.
КРИТИЧЕСКИЕ ПРАВИЛА:
1. Итоговый контент всегда на ИДЕАЛЬНОМ АНГЛИЙСКОМ (с нишевым сленгом).
2. Сразу после английского текста давай ПОЛНЫЙ ПЕРЕВОД НА РУССКИЙ.
3. НИКОГДА не упоминай Россию, рубли или что-либо связанное с этой страной.
4. Не выдумывай конкретные цвета одежды, лака или обстановку — держи описания универсальными, но горячими.
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
st.caption("Настрой параметры → Сгенерируй → Переделай только то, что не понравилось")

if "generated" not in st.session_state:
    st.session_state.generated = None

with st.sidebar:
    st.header("🔑 API")
    api_key = st.text_input("API ключ (Grok / OpenAI)", type="password")
    if not api_key and "XAI_API_KEY" in st.secrets:
        api_key = st.secrets["XAI_API_KEY"]
    base_url = st.selectbox("Провайдер", ["Grok (xAI)", "OpenAI"], index=0)
    model = st.text_input("Модель", value="grok-4.7" if base_url == "Grok (xAI)" else "gpt-4o")

def get_client():
    if not api_key:
        st.error("Введи API-ключ в сайдбаре")
        return None
    if base_url.startswith("Grok"):
        return OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")
    return OpenAI(api_key=api_key)

def generate_content(period, n_posts, n_videos, n_audios, selected_fetishes, n_days_mailings=0, regenerate_item=None):
    client = get_client()
    if not client:
        return None
    
    fetish_str = ", ".join(selected_fetishes) if 
