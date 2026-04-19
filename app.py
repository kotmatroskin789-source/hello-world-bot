import streamlit as st

# Сразу рисуем интерфейс, чтобы не было белого экрана
st.title("🤖 Мой ИИ Бот")
st.write("### Состояние: Запуск системы...")
st.write("Hello World! Если вы видите этот текст — интерфейс работает ✅")

# Тяжёлые библиотеки загружаем только при обработке (экономим время запуска)
def remove_background(image_file):
    from rembg import remove
    from PIL import Image
    
    # Открываем изображение
    img = Image.open(image_file)
    
    # Удаляем фон (rembg всегда возвращает RGBA)
    result = remove(img)
    
    # Делаем белый фон (самый надёжный способ)
    white_bg = Image.new("RGB", result.size, (255, 255, 255))
    white_bg.paste(result, (0, 0), result)  # ← вот здесь была ошибка
    
    return white_bg


# ====================== ИНТЕРФЕЙС ======================
uploaded_file = st.file_uploader(
    "📸 Добавить изображение",
    type=["jpg", "jpeg", "png"],
    help="Поддерживаются JPG, JPEG и PNG"
)

if uploaded_file:
    st.image(uploaded_file, caption="📌 Оригинал загружен", use_column_width=True)
    
    if st.button("🪄 Удалить фон", type="primary", use_container_width=True):
        with st.spinner("🧪 Магия ИИ в процессе... (это может занять 3–8 секунд)"):
            try:
                result_image = remove_background(uploaded_file)
                
                st.success("✅ Фон успешно удалён!")
                st.image(result_image, caption="🎉 Результат готов!", use_column_width=True)
                
                # Кнопка скачивания
                import io
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
                st.info("Подсказка: Убедитесь, что библиотека `rembg` установлена (`pip install rembg`).")
