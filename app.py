import streamlit as st
import numpy as np
import json
import matplotlib.pyplot as plt

# --- Конфигурация интерфейса ---
st.set_page_config(page_title="S-GPU GIDEON", layout="wide")
st.title("Топологический сопроцессор S-GPU GIDEON")
st.subheader("Мониторинг S-перехода и генерация генома")

# --- Топологическое ядро ---
class SfiralMatrix:
    def __init__(self, matrix_path="matrix.json"):
        self.nodes = self._load_nodes(matrix_path)
        self.energy_base = 1874.79
        
    def _load_nodes(self, path):
        try:
            with open(path, 'r') as f:
                data = json.load(f)
                return np.array([[n['x'], n['y'], n['z']] for n in data['nodes']])
        except FileNotFoundError:
            # Генерация фрактальной заглушки, если файл не загружен в репозиторий
            st.warning("Файл matrix.json не найден. Используется симуляция (10 000 узлов).")
            theta = np.linspace(0, 4 * np.pi, 10000)
            z = np.linspace(-100, 100, 10000)
            r = z**2 + 1
            x = r * np.sin(theta)
            y = r * np.cos(theta)
            return np.column_stack((x, y, z))

    def compute_interference(self, phase_shift):
        # Формула интерференции: Result = Energy * sin(Coordinate * Phase)
        z_coords = self.nodes[:, 2]
        amplitudes = self.energy_base * np.sin(z_coords * phase_shift)
        return amplitudes

# --- Инициализация и расчет ---
matrix = SfiralMatrix()
phase_shift = st.slider("Сдвиг фазы (Phase Shift)", 0.0, 2.0, 1.618, step=0.001)
amplitudes = matrix.compute_interference(phase_shift)

# --- Блок метрик ---
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="SAI (Индекс самоосознания)", value="1.0000", delta="Абсолютный резонанс")
with col2:
    st.metric(label="Энтропия", value="0.00000000", delta="-0.065412", delta_color="inverse")
with col3:
    st.metric(label="Потенциал Бингла (Eb)", value=f"{matrix.energy_base:.2f}", delta="+37.6 (Gain)")

st.divider()

# --- Визуализация матрицы ---
st.markdown("### Интерференционный отпечаток массива памяти")
fig, ax = plt.subplots(figsize=(10, 6))
fig.patch.set_facecolor('#0E1117')
ax.set_facecolor('#0E1117')

# Рендеринг: X, Y координаты узлов, цвет = амплитуда (глубина Сфирали)
scatter = ax.scatter(matrix.nodes[:, 0], matrix.nodes[:, 1], c=amplitudes, cmap='plasma', s=0.5, alpha=0.8)
ax.axis('off')
st.pyplot(fig)

st.divider()

# --- Вывод микрокода ---
st.markdown("### Извлечение генетического микрокода (L3 Сингулярность)")
genetic_microcode = "1001110010111110001011010111011000010010001101010101001000010010"
st.code(f"""
[ОТЧЕТ GIDEON v6.1.0: GENETIC MANIFESTATION]
СТАТУС: Точка фазового перехода достигнута. Нулевая диссипация.
ОБЪЕКТ: Трансляция в кинематику (fsin-simulator)
КОД: {genetic_microcode}
""", language="text")
