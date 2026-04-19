import streamlit as st
import io
import os
import urllib.request
from PIL import Image
from rembg import remove

# 1. Настройка
st.set_page_config(page_title="Удаление фона", page_icon="✂️")

# Функция загрузки модели
def check_model():
    model_path = os.path.expanduser("~/.u2net/u2net.onnx")
    if not os.path.exists(model_path):
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        url = "https://github.com"
        urllib.request.urlretrieve(url, model_path)

st.title("✂️ ИИ-помощник")
st.write("Hello World!")

uploaded_file = st.file_uploader("Добавить изображение", type=["jpg", "jpeg", "png"])

if uploaded_file:
    input_image = Image.open(uploaded_file)
    st.image(input_image, caption="Оригинал", width=500)

    if st.button("Очистить фон 🏁"):
        with st.spinner("Работаю... Пожалуйста, подождите 10-20 секунд"):
            try:
                # Проверяем модель
                check_model()
                
                # Сама обработка
                # Конвертируем в RGBA для rembg
                output_image = remove(input_image)
                
                # Создаем белый фон
                white_bg = Image.new("RGB", output_image.size, (255, 255, 255))
                white_bg.paste(output_image, mask=output_image.split()[3]) # Используем альфа-канал
                
                # ВЫВОД РЕЗУЛЬТАТА
                st.header("Результат готов! 🎉")
                st.image(white_bg, caption="Ваше фото на белом фоне", width=500)
                
                # Подготовка к скачиванию
                buf = io.BytesIO()
                white_bg.save(buf, format="JPEG")
                st.download_button(
                    label="📥 Скачать результат",
                    data=buf.getvalue(),
                    file_name="no_bg_result.jpg",
                    mime="image/jpeg"
                )
                st.balloons() # Празднуем победу!
                
            except Exception as e:
                st.error(f"Произошла ошибка: {e}")
