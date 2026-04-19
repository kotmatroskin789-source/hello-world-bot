import streamlit as st
from rembg import remove
from PIL import Image
import io

# 1. Настройка страницы
st.set_page_config(page_title="ИИ Удаление фона", page_icon="🤖")

# 2. Приветствие (показывается всегда)
st.write("# Hello World!")

# 3. Заголовок и описание
st.title("✂️ ИИ-помощник для удаления фона")
st.info("Я готов к работе! Загрузите фото, чтобы заменить фон на белый.")

# 4. Кнопка загрузки изображения
uploaded_file = st.file_uploader("Добавить изображение", type=["jpg", "jpeg", "png"])

# 5. Основная логика работы
if uploaded_file:
    # Отображаем загруженное фото
    image = Image.open(uploaded_file)
    st.image(image, caption='Ваш оригинал', use_container_width=True)
    
    # Кнопка запуска обработки
    if st.button('Очистить фон 🏁'):
        with st.spinner('Магия ИИ в процессе... 🏁'):
            # Удаление фона
            no_bg = remove(image)
            
            # Создание белого фона
            white_bg = Image.new("RGB", no_bg.size, (255, 255, 255))
            
            if no_bg.mode == 'RGBA':
                white_bg.paste(no_bg, mask=no_bg.split())
            else:
                white_bg.paste(no_bg)
            
            # Результат
            st.success("Готово! Фон заменен на белый 🏁")
            st.image(white_bg, caption='Результат', use_container_width=True)
            
            # Кнопка скачивания
            buf = io.BytesIO()
            white_bg.save(buf, format="JPEG")
            st.download_button(
                label="📥 Скачать готовое изображение",
                data=buf.getvalue(),
                file_name="white_bg_result.jpg",
                mime="image/jpeg"
            )
else:
    # Инструкция, если фото еще не выбрано
    st.warning("👈 Нажмите кнопку выше, чтобы добавить изображение.")
