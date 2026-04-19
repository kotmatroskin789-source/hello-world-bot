import streamlit as st
import os
import psutil
import platform
import sys

st.set_page_config(page_title="System Diagnosis")

st.title("🖥 Диагностика системы")

# 1. Базовая проверка интерфейса
st.success("✅ Если вы видите этот текст, значит Streamlit работает и отрисовывает интерфейс!")

# 2. Информация о системе
st.header("1. Информация о сервере")
col1, col2 = st.columns(2)
with col1:
    st.write(f"**ОС:** {platform.system()} {platform.release()}")
    st.write(f"**Python:** {sys.version.split()[0]}")
with col2:
    mem = psutil.virtual_memory()
    st.write(f"**Доступно RAM:** {mem.available / (1024**3):.2f} GB")
    st.write(f"**Всего RAM:** {mem.total / (1024**3):.2f} GB")

# 3. Тест дисковой подсистемы (нужно для загрузки модели ИИ)
st.header("2. Проверка прав записи")
try:
    test_file = "test_write.txt"
    with open(test_file, "w") as f:
        f.write("test")
    os.remove(test_file)
    st.success("✅ Права на запись есть (модель ИИ сможет скачаться).")
except Exception as e:
    st.error(f"❌ Нет прав на запись: {e}")

# 4. Попытка импорта тяжелой библиотеки
st.header("3. Тест импорта ИИ (rembg)")
if st.button("Запустить импорт rembg"):
    with st.spinner("Пробую импортировать библиотеку..."):
        try:
            import rembg
            st.success(f"✅ Библиотека rembg успешно импортирована! Версия: {rembg.__version__}")
            st.info("Это значит, ресурсов памяти (RAM) хватает для запуска.")
        except Exception as e:
            st.error(f"❌ Ошибка при импорте rembg: {e}")
            st.warning("Скорее всего, серверу не хватает оперативной памяти (OOM).")

# 5. Вывод логов памяти
st.header("4. Текущие процессы")
st.write(f"Занято памяти процессом: {psutil.Process(os.getpid()).memory_info().rss / (1024**2):.2f} MB")
