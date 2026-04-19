import streamlit as st
import io

# Сначала настраиваем страницу
st.set_page_config(page_title="Удаление фона", page_icon="✂️")

# Выводим приветствие сразу
st.write("# Hello World!")
st.title("✂️ ИИ-помощник")
st.info("Я готов к работе! Добавьте изображение ниже.")

# Поле загрузки
uploaded_file = st.file_uploader("Добавить изображение", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # Отображаем то, что загрузили
    from PIL import Image
    image = Image.open(uploaded_file)
    st.image(image, caption="Оригинал загружен", use_container_width=True)

    if st.button("Очистить фон 🏁"):
        with st.spinner("Магия ИИ в процессе... (в первый раз это может занять минуту)"):
            try:
                from rembg import remove
                
                # Сама обработка
                output = remove(image)
                
                # Делаем фон белым
                white_bg = Image.new("RGB", output.size, (255, 255, 255))
                if output.mode == 'RGBA':
                    white_bg.paste(output, mask=output.split())
                else:
                    white_bg.paste(output)
                
                st.success("Готово!")
                st.image(white_bg, caption="Результат", use_container_width=True)
                
                # Кнопка скачивания
                buf = io.BytesIO()
                white_bg.save(buf, format="JPEG")
                st.download_button(
                    label="📥 Скачать результат",
                    data=buf.getvalue(),
                    file_name="no_bg.jpg",
                    mime="image/jpeg"
                )
            except Exception as e:
                st.error(f"Произошла ошибка: {e}")
