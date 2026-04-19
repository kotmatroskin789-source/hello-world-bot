import streamlit as st
from rembg import remove
from PIL import Image
import io

st.set_page_config(page_title="Удаление фона ИИ")
st.title("✂️ Удаление фона и замена на белый")

uploaded_file = st.file_uploader("Загрузите фото (JPG, PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # Открываем изображение
    image = Image.open(uploaded_file)
    st.image(image, caption='Оригинал', use_container_width=True)
    
    if st.button('Очистить фон'):
        with st.spinner('Магия ИИ в процессе...'):
            # 1. Удаляем фон (делаем его прозрачным)
            no_bg = remove(image)
            
            # 2. Создаем белый фон и накладываем объект
            # Если картинка в режиме RGBA, конвертируем
            if no_bg.mode == 'RGBA':
                white_bg = Image.new("RGB", no_bg.size, (255, 255, 255))
                white_bg.paste(no_bg, mask=no_bg.split()[3]) # 3 — это альфа-канал
            else:
                white_bg = no_bg.convert("RGB")
            
            # Показываем результат
            st.image(white_bg, caption='Результат на белом фоне', use_container_width=True)
            
            # Подготовка файла для скачивания
            buf = io.BytesIO()
            white_bg.save(buf, format="JPEG")
            st.download_button(
                label="Скачать результат",
                data=buf.getvalue(),
                file_name="result_white_bg.jpg",
                mime="image/jpeg"
            )
