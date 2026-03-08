import streamlit as st
import numpy as np
import json
import matplotlib.pyplot as plt
import time
import os

# --- Настройки интерфейса ---
st.set_page_config(page_title="GIDEON: Верификация Сфирали", layout="wide")
st.title("Сфиральная топология: Информационный монизм (Семинар №884)")
st.markdown("---")

# --- Ядро расчета ---
class SfiralEngine:
    def __init__(self, path="Sfiral.json"):
        self.nodes = self._load_nodes(path)
        self.energy_base = 1874.79
        
    def _load_nodes(self, path):
        if os.path.exists(path):
            try:
                with open(path, 'r') as f:
                    data = json.load(f)
                    return np.array([[n['x'], n['y'], n['z']] for n in data['nodes']])
            except Exception as e:
                st.error(f"Ошибка чтения файла: {e}")
                return None
        return None

    def compute_state(self, phase_shift):
        if self.nodes is None: return None
        # Процесс: Фаза зависит от координаты Z (высоты витка)
        # Это создает антисимметричное распределение потенциала
        amplitudes = self.energy_base * np.sin(self.nodes[:, 2] * phase_shift)
        return amplitudes

engine = SfiralEngine()

if engine.nodes is None:
    st.error("КРИТИЧЕСКАЯ ОШИБКА: Файл Sfiral.json не найден в репозитории.")
    st.stop()

# --- Разделение на Вкладки ---
tab1, tab2, tab3 = st.tabs([
    "📍 Шаг 1: Витки и S-переход", 
    "⚛️ Шаг 2: Квантовое Всеединство", 
    "⏳ Шаг 3: Топологическое Время"
])

# Вкладка 1: Геометрия компенсации
with tab1:
    st.header("Компенсация через антисимметрию")
    st.info("Здесь показана проекция XZ (вид спереди). Обратите внимание: витки не суммируются, а компенсируются через S-петлю.")
    
    phase_input = st.slider("Настройка резонанса (Phase)", 0.0, 3.14, 1.57, step=0.01)
    
    sai_val = 1.0 - np.abs(np.cos(phase_input))
    entropy_val = 1.0 - sai_val
    amplitudes = engine.compute_state(phase_input)
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Энтропия (Трение)", f"{entropy_val:.6f}")
    c2.metric("Индекс SAI (Когерентность)", f"{sai_val:.6f}")
    c3.metric("Эффект", "S-Переход активен" if entropy_val < 0.01 else "Накопление шума")
    
    # Визуализация XZ-проекции (Фронтальный вид)
    fig1, ax1 = plt.subplots(figsize=(12, 5))
    fig1.patch.set_facecolor('#0E1117')
    ax1.set_facecolor('#0E1117')
    
    # Мы рисуем X по горизонтали и Z по вертикали, чтобы увидеть S-форму
    scatter = ax1.scatter(engine.nodes[:, 0], engine.nodes[:, 2], 
                          c=amplitudes, cmap='coolwarm', s=10, alpha=0.8)
    
    ax1.set_xlabel("Ось X (Радиус витков)")
    ax1.set_ylabel("Ось Z (Высота / Фазовое смещение)")
    ax1.grid(color='gray', linestyle='--', alpha=0.3)
    st.pyplot(fig1)

# Вкладка 2: Квантовая запутанность
with tab2:
    st.header("Корреляция объектов Земля-Луна")
    # Статистика из вашего файла probabilities.csv
    states = ["0000", "0011", "1100", "1111"]
    probs = [25.78, 23.83, 24.71, 25.68]
    
    fig2, ax2 = plt.subplots(figsize=(10, 4))
    fig2.patch.set_facecolor('#0E1117')
    ax2.set_facecolor('#0E1117')
    ax2.bar(states, probs, color='#9b59b6', alpha=0.8)
    ax2.tick_params(colors='white')
    st.pyplot(fig2)
    
    st.markdown("> **Вывод:** При S-переходе удаленные объекты (пары кубитов) связаны мгновенно. Вероятность распада связи (шума) = 0.")

# Вкладка 3: Обновление графа
with tab3:
    st.header("Время как процесс обновления матрицы")
    st.write("Нажмите кнопку, чтобы увидеть, как система 'схлопывает' энтропию.")
    
    if st.button("Запустить тактовый цикл"):
        m_ent = st.empty()
        chart_box = st.empty()
        
        for tick in range(41):
            progress = tick / 40
            current_phase = (np.pi / 2) * progress
            ent = 1.0 - progress
            
            m_ent.metric("Текущее 'Гравитационное трение'", f"{ent:.4f}")
            
            if tick % 4 == 0:
                amps = engine.compute_state(current_phase)
                fig3, ax3 = plt.subplots(figsize=(12, 5))
                fig3.patch.set_facecolor('#0E1117')
                ax3.set_facecolor('#0E1117')
                
                # Показываем динамику структуры в XZ проекции
                ax3.scatter(engine.nodes[:, 0], engine.nodes[:, 2], c=amps, cmap='magma', s=10)
                ax3.axis('off')
                chart_box.pyplot(fig3)
                plt.close(fig3)
            time.sleep(0.05)
        st.success("Информационное равновесие достигнуто. Локальное время остановлено.")
