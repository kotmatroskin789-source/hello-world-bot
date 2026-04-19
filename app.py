import streamlit as st
import sys

st.title("🛠 Финальная отладка импорта")

# Пытаемся импортировать по очереди, чтобы найти слабое звено
st.write("Начинаю загрузку модулей...")

try:
    import PIL
    st.success("✅ Pillow загружен")
    
    import onnxruntime
    st.success("✅ ONNX Runtime загружен")

    from rembg import remove
    st.success("✅ Библиотека REMBG загружена успешно!")
    
    st.balloons() # Праздничные шарики, если всё ок!

except Exception as e:
    st.error("❌ Ошибка при импорте!")
    st.exception(e) # Это выведет подробный технический отчет
    st.write("Технические данные для Гугла:", sys.exc_info())

st.divider()
st.info("Если выше все галочки зеленые — можно возвращать основной код бота.")
