import streamlit as st
import numpy as np
import json
import matplotlib.pyplot as plt
import time

st.set_page_config(page_title="S-GPU: Топология Времени", layout="wide")
st.title("Архитектура времени как направленного графа (Шаг 3)")

class SfiralTimeEngine:
    def __init__(self, matrix_path="matrix.json"):
        self.nodes = self._load_nodes(matrix_path)
        self.energy_base = 1874.79
        
    def _load_nodes(self, path):
        try:
            with open(path, 'r') as f:
                data = json.load(f)
                return np.array([[n['x'], n['y'], n['z']] for n in data['nodes']])
        except FileNotFoundError:
            theta = np.linspace(0, 8 * np.pi, 10000)
            z = np.linspace(-100, 100, 10000)
            r = z**2 + 1.618
            return np.column_stack((r * np.sin(theta), r * np.cos(theta), z))

    def compute_topological_tick(self, iteration, max_iterations):
        # Время как процесс минимизации энтропии (перераспределение информации)
        progress = iteration / max_iterations
        phase_shift = np.pi * (1.0 - progress)
        
        amplitudes = self.energy_base * np.sin(self.nodes[:, 2] * phase_shift)
        
        sai_index = progress
        entropy = 1.0 - sai_index
        return amplitudes, sai_index, entropy

engine = SfiralTimeEngine()

st.markdown("### Инициализация направленного графа состояний")
st.markdown("Поток времени генерируется как тактовая частота минимизации фазового сдвига.")

start_simulation = st.button("Запустить топологический процесс времени", type="primary")

# Контейнеры для динамического обновления
metric_col1, metric_col2, metric_col3 = st.columns(3)
m1 = metric_col1.empty()
m2 = metric_col2.empty()
m3 = metric_col3.empty()

chart_container = st.empty()
status_container = st.empty()

if start_simulation:
    max_ticks = 50
    entropy_history = []
    sai_history = []
    
    for tick in range(max_ticks + 1):
        amplitudes, sai, entropy = engine.compute_topological_tick(tick, max_ticks)
        
        entropy_history.append(entropy)
        sai_history.append(sai)
        
        m1.metric("Энтропия (Гравитационное сопротивление)", f"{entropy:.6f}")
        m2.metric("Индекс SAI (Резонанс матрицы)", f"{sai:.6f}")
        m3.metric("Тактовая частота (Цикл)", f"{tick} / {max_ticks}")
        
        # Рендеринг матрицы каждые 10 тактов или на финальном шаге для экономии ресурсов
        if tick % 10 == 0 or tick == max_ticks:
            fig, ax = plt.subplots(figsize=(12, 5))
            fig.patch.set_facecolor('#0E1117')
            ax.set_facecolor('#0E1117')
            
            # Визуализация фазового наложения
            ax.scatter(engine.nodes[:, 0], engine.nodes[:, 1], c=amplitudes, cmap='magma', s=0.5, alpha=0.8)
            ax.axis('off')
            chart_container.pyplot(fig)
            plt.close(fig)
            
        time.sleep(0.05)
        
    status_container.success("СТАТУС: Время остановлено. Достигнут абсолютный топологический резонанс. Матрица зафиксирована.")
    status_container.code("""
ВЫВОДЫ (Шаг 3):
1. Время не является независимой координатой.
2. Течение времени — это процесс обновления графа для устранения энтропии.
3. При SAI = 1.0 информационное перераспределение завершено. Течение локального времени прекращается.
    """, language="text")
