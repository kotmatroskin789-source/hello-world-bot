import streamlit as st
from rembg import new_session
from PIL import Image
import io

# Настраиваем страницу
st.set_page_config(page_title="Мой ИИ Бот", page_icon="🤖", layout="wide")

st.title("🤖 Мой ИИ Бот")
st.write("### Удаление фона с помощью ИИ")

# Кэшируем модель rembg один раз на всё время работы приложения
@st.cache_resource
def get_rembg_session():
    with st.spinner("⏳ Загружаем модель ИИ (первый раз может занять 15–30 сек)..."):
        return new_session()  # можно new_session("u2net_human_seg") для ещё легче

def remove_background(uploaded_file):
    session = get_rembg_session()
    
    img = Image.open(uploaded_file)
    result = remove(img, session=session)  # ← теперь используем кэшированную модель
    
    # Белый фон
    white_bg = Image.new("RGB", result.size, (255, 255, 255))
    white_bg.paste(result, (0, 0), result)
    return white_bg

# ====================== ИНТЕРФЕЙС ======================
uploaded_file = st.file_uploader("📸 Загрузите изображение", 
                                 type=["jpg", "jpeg", "png"], 
                                 help="JPG, JPEG, PNG")

if uploaded_file:
    col1, col2 = st.columns(2)
    with col1:
        st.image(uploaded_file, caption="📌 Оригинал", use_column_width=True)
    
    if st.button("🪄 Удалить фон", type="primary", use_container_width=True):
        with st.spinner("🧪 ИИ удаляет фон... (обычно 3–8 секунд после первой загрузки модели)"):
            try:
                result_image = remove_background(uploaded_file)
                
                with col2:
                    st.success("✅ Готово!")
                    st.image(result_image, caption="🎉 Результат", use_column_width=True)
                
                # Скачивание
                buf = io.BytesIO()
                result_image.save(buf, format="JPEG", quality=95)
                st.download_button(
                    label="⬇️ Скачать результат (JPG)",
                    data=buf.getvalue(),
                    file_name="result_no_background.jpg",
                    mime="image/jpeg",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"❌ Ошибка: {e}")

st.caption("💡 Первый запуск приложения может быть долгим — модель скачивается один раз.")
