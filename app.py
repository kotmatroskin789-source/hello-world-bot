import streamlit as st
import io
from PIL import Image

# Это должно быть ПЕРВОЙ строкой кода
st.set_page_config(page_title="ИИ Бот")

st.title("🤖 ИИ Удаление фона")
st.write("Hello World! Если этот текст виден — мы победили блокировку.")

uploaded_file = st.file_uploader("Добавить изображение", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Оригинал", width=300)

    if st.button("Очистить фон 🏁"):
        try:
            # Импортируем строго внутри кнопки
            from rembg import remove
            
            with st.spinner("ИИ обрабатывает фото..."):
                # Самое простое удаление без лишних настроек
                result = remove(image)
                
                # Создаем белый фон
                white_bg = Image.new("RGB", result.size, (255, 255, 255))
                if result.mode == 'RGBA':
                    white_bg.paste(result, mask=result.split())
                else:
                    white_bg.paste(result)
                
                st.image(white_bg, caption="Готово!", width=300)
                
                # Подготовка к скачиванию
                buf = io.BytesIO()
                white_bg.save(buf, format="JPEG")
                st.download_button("📥 Скачать", buf.getvalue(), "res.jpg", "image/jpeg")
                st.balloons()
        except Exception as e:
            st.error(f"Система заблокировала процесс: {e}")
            st.info("Попробуйте нажать кнопку еще раз, иногда загрузка модели со второго раза проходит через кэш.")
