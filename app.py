import streamlit as st
import io
import os
import urllib.request
from PIL import Image

# 1. Принудительная загрузка модели, если её нет
def download_model():
    model_path = os.path.expanduser("~/.u2net/u2net.onnx")
    if not os.path.exists(model_path):
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        url = "https://github.com"
        with st.spinner("Загрузка ИИ-модели (170МБ)... Пожалуйста, подождите."):
            urllib.request.urlretrieve(url, model_path)
            st.success("Модель успешно загружена!")

st.set_page_config(page_title="Удаление фона", page_icon="✂️")
st.title("✂️ ИИ-помощник")

uploaded_file = st.file_uploader("Добавить изображение", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Оригинал загружен", width="stretch")

    if st.button("Очистить фон 🏁"):
        try:
            # Сначала проверяем/скачиваем модель
            download_model()
            
            from rembg import remove
            
            with st.spinner("Удаление фона..."):
                output = remove(image)
                
                # Создание белого фона
                white_bg = Image.new("RGB", output.size, (255, 255, 255))
                if output.mode == 'RGBA':
                    white_bg.paste(output, mask=output.split())
                else:
                    white_bg.paste(output)
                
                st.image(white_bg, caption="Результат на белом фоне", width="stretch")
                
                buf = io.BytesIO()
                white_bg.save(buf, format="JPEG")
                st.download_button("📥 Скачать результат", buf.getvalue(), "result.jpg", "image/jpeg")
        except Exception as e:
            st.error(f"Произошла ошибка: {e}")
