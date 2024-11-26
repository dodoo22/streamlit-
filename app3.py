import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import pi

# 自定義 CSS：調整整體佈局
st.markdown("""
<style>
    .main {
        padding: 1rem;
    }
    .stMarkdown h1, h2, h3, h4 {
        font-size: 1.2rem;
    }
    .stMetric {
        margin: 0.2rem 0;
    }
    .stSlider {
        padding: 0.2rem 0;
    }
    .block-container {
        padding: 1rem 1rem;
    }
</style>
""", unsafe_allow_html=True)

# 頁面標題和簡介
st.title("Breast Cancer Predictor")
st.markdown("""
Breast cancer diagnosis involves examining cellular samples through cytology procedures. 
This application provides a comprehensive workflow for detection.
""")

# 主佈局：分成三欄，讓所有內容緊湊地排列
col1, col2, col3 = st.columns([1.5, 2, 1.5])

# 左側：輸入數據滑塊
with col1:
    st.header("Cell Nuclei Measurements")
    radius_mean = st.slider("Radius (mean)", 0.0, 28.11, 14.13)
    texture_mean = st.slider("Texture (mean)", 0.0, 39.28, 27.91)
    perimeter_mean = st.slider("Perimeter (mean)", 0.0, 188.50, 91.97)
    area_mean = st.slider("Area (mean)", 0.0, 2501.0, 654.89)
    smoothness_mean = st.slider("Smoothness (mean)", 0.0, 0.16, 0.10)
    compactness_mean = st.slider("Compactness (mean)", 0.0, 0.35, 0.10)

# 中間：雷達圖
with col2:
    categories = ['Radius', 'Texture', 'Perimeter', 'Area', 'Smoothness', 'Compactness']
    user_values = [radius_mean, texture_mean, perimeter_mean, area_mean, smoothness_mean, compactness_mean]
    mean_values = [14.13, 20.38, 91.97, 654.89, 0.1, 0.15]  # 示例均值
    low_values = [10.0, 15.0, 70.0, 400.0, 0.08, 0.1]  # 示例最低值

    def make_radar_chart(categories, values, mean_values, low_values):
        N = len(categories)
        angles = [n / float(N) * 2 * pi for n in range(N)]
        angles += angles[:1]

        values += values[:1]
        mean_values += mean_values[:1]
        low_values += low_values[:1]

        fig, ax = plt.subplots(figsize=(2.5, 2.5), subplot_kw=dict(polar=True))  # 縮小圖表
        ax.fill(angles, values, color='blue', alpha=0.25, label="User Input")
        ax.fill(angles, mean_values, color='green', alpha=0.25, label="Mean")
        ax.fill(angles, low_values, color='red', alpha=0.25, label="Lowest")

        ax.plot(angles, values, color='blue', linewidth=1.5)
        ax.plot(angles, mean_values, color='green', linewidth=1.5)
        ax.plot(angles, low_values, color='red', linewidth=1.5)

        ax.set_yticks([])
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories, fontsize=8)

        ax.legend(loc='upper right', bbox_to_anchor=(1.2, 0.1), fontsize=7)
        return fig

    st.pyplot(make_radar_chart(categories, user_values, mean_values, low_values))

# 右側：分類結果
with col3:
    st.header("Cell Cluster Status")
    malignant_probability = np.random.uniform(0.5, 1.0)  # 假設性結果
    benign_probability = 1 - malignant_probability

    if malignant_probability > benign_probability:
        status = "Malicious"
        status_color = "red"
    else:
        status = "Benign"
        status_color = "green"

    st.markdown(f"""
    ### Status:
    <span style="color:{status_color}; font-size: 20px; font-weight: bold;">{status}</span>
    """, unsafe_allow_html=True)

    st.metric(label="Benign Probability", value=f"{benign_probability:.3f}")
    st.metric(label="Malignant Probability", value=f"{malignant_probability:.3f}")

    st.markdown("""
    *This analysis is not a substitute for professional diagnosis.*
    """)

