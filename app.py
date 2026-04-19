import streamlit as st
import io

st.set_page_config(page_title="Удаление фона", page_icon="✂️")

st.write("# Hello World!")
st.title("✂️ ИИ-помощник")
st.info("Я готов к работе!")

uploaded_file = st.file_uploader("Добавить изображение", type=["jpg", "jpeg", "png"])

if uploaded_file:
    from PIL import Image
    image = Image.open(uploaded_file)
    # Исправили параметр согласно логам: width="stretch"
    st.image(image, caption="Оригинал загружен", width="stretch")

    if st.button("Очистить фон 🏁"):
        # Создаем пустой элемент для статуса
        status_text = st.empty()
        status_text.info("⏳ Инициализация ИИ... (при первом запуске это займет до 1 минуты)")
        
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
            
            status_text.success("✅ Готово!")
            st.image(white_bg, caption="Результат", width="stretch")
            
            # Кнопка скачивания
            buf = io.BytesIO()
            white_bg.save(buf, format="JPEG")
            st.download_button(
                label="📥 Скачать результат",
                data=buf.getvalue(),
                file_name="result_white.jpg",
                mime="image/jpeg"
            )
        except Exception as e:
            st.error(f"Произошла ошибка: {e}")
