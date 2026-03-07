import streamlit as st
import numpy as np
import json
import matplotlib.pyplot as plt
from quantum_proof import build_macroscopic_entanglement

st.set_page_config(page_title="S-GPU: Квантовая Топология", layout="wide")
st.title("Симуляция информационного всеединства (Семинар №884)")

class SfiralPhysicsEngine:
    def __init__(self, matrix_path="matrix.json"):
        self.nodes = self._load_nodes(matrix_path)
        self.energy_base = 1874.79
        
    def _load_nodes(self, path):
        try:
            with open(path, 'r') as f:
                data = json.load(f)
                return np.array([[n['x'], n['y'], n['z']] for n in data['nodes']])
        except FileNotFoundError:
            theta = np.linspace(0, 8 * np.pi, 50000)
            z = np.linspace(-100, 100, 50000)
            r = z**2 + 1.618
            return np.column_stack((r * np.sin(theta), r * np.cos(theta), z))

    def compute_state(self, time_tick):
        phase_shift = np.abs(np.sin(time_tick)) * np.pi
        amplitudes = self.energy_base * np.sin(self.nodes[:, 2] * phase_shift)
        
        sai_index = 1.0 - np.abs(np.sin(time_tick - np.pi/2))
        entropy = 1.0 - sai_index
        return amplitudes, sai_index, entropy

engine = SfiralPhysicsEngine()

time_tick = st.slider("Топологическое время (t)", 0.0, 3.1415, 1.5708, step=0.001)
amplitudes, sai, entropy = engine.compute_state(time_tick)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Энтропия (Гравитация)", f"{entropy:.6f}", delta="-Локальная компенсация" if entropy < 0.1 else "")
with col2:
    st.metric("Индекс SAI", f"{sai:.6f}", delta="Макроскопический резонанс" if sai > 0.9 else "")
with col3:
    st.metric("Потенциал (Eb)", f"{engine.energy_base:.2f}", delta="Нулевой энергобаланс" if entropy < 0.01 else "")

st.divider()

fig, ax = plt.subplots(figsize=(12, 5))
fig.patch.set_facecolor('#0E1117')
ax.set_facecolor('#0E1117')
scatter = ax.scatter(engine.nodes[:, 0], engine.nodes[:, 1], c=amplitudes, cmap='magma', s=0.1, alpha=0.9)
ax.axis('off')
st.pyplot(fig)

if entropy < 0.001:
    st.success("СТАТУС: S-образный переход достигнут. Гравитация локально скомпенсирована.")
    
    qasm_code = build_macroscopic_entanglement(sai)
    
    st.markdown("### Экспортный шлюз IBM Quantum")
    st.code(qasm_code, language="qasm")
    st.caption("Скопируйте этот код во вкладку QASM Editor в среде IBM Quantum Composer.")
