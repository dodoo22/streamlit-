import streamlit as st
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

# 主佈局：分成三欄
col1, col2, col3 = st.columns([1.5, 2, 1.5])

# 左側：輸入數據滑塊
with col1:
    st.header("Cell Nuclei Measurements")
    # 滑桿輸入
    radius_mean = st.slider("Radius (mean)", 0.0, 28.11, 14.13)
    texture_mean = st.slider("Texture (mean)", 0.0, 39.28, 20.38)
    perimeter_mean = st.slider("Perimeter (mean)", 0.0, 188.50, 91.97)
    area_mean = st.slider("Area (mean)", 0.0, 2501.0, 654.89)
    smoothness_mean = st.slider("Smoothness (mean)", 0.0, 0.16, 0.1)
    compactness_mean = st.slider("Compactness (mean)", 0.0, 0.35, 0.15)

    # 用戶輸入值列表
    user_values = [
        radius_mean,
        texture_mean,
        perimeter_mean,
        area_mean,
        smoothness_mean,
        compactness_mean
    ]

# 中間：雷達圖
with col2:
    # 固定的參考數據
    categories = ['Radius', 'Texture', 'Perimeter', 'Area', 'Smoothness', 'Compactness']
    mean_values = [14.13, 20.38, 91.97, 654.89, 0.1, 0.15]  # 固定均值
    low_values = [10.0, 15.0, 70.0, 400.0, 0.08, 0.1]       # 固定最低值
    min_values = [0.0, 0.0, 0.0, 0.0, 0.08, 0.1]           # 特徵最小值
    max_values = [28.11, 39.28, 188.5, 2501.0, 0.16, 0.35] # 特徵最大值

    # 數據標準化函數
    def normalize(values, min_vals, max_vals):
        return [(v - min_v) / (max_v - min_v) if max_v > min_v else 0
                for v, min_v, max_v in zip(values, min_vals, max_vals)]

    # 標準化用戶輸入與參考數據
    norm_user_values = normalize(user_values, min_values, max_values) + [normalize(user_values, min_values, max_values)[0]]
    norm_mean_values = normalize(mean_values, min_values, max_values) + [normalize(mean_values, min_values, max_values)[0]]
    norm_low_values = normalize(low_values, min_values, max_values) + [normalize(low_values, min_values, max_values)[0]]

    # 繪製雷達圖
    def make_radar_chart(categories, user_values, mean_values, low_values):
        N = len(categories)
        angles = [n / float(N) * 2 * pi for n in range(N)]
        angles += angles[:1]  # 確保雷達圖閉合

        fig, ax = plt.subplots(figsize=(4, 4), subplot_kw=dict(polar=True))
        # 填充區域
        ax.fill(angles, user_values, color='blue', alpha=0.25, label="User Input")
        ax.fill(angles, mean_values, color='green', alpha=0.25, label="Mean")
        ax.fill(angles, low_values, color='red', alpha=0.25, label="Lowest")
        # 繪製邊框線
        ax.plot(angles, user_values, color='blue', linewidth=1.5)
        ax.plot(angles, mean_values, color='green', linewidth=1.5)
        ax.plot(angles, low_values, color='red', linewidth=1.5)

        # 設置類別標籤
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories, fontsize=10)
        ax.set_yticks([])  # 隱藏內部的圓形刻度線
        ax.legend(loc='upper right', bbox_to_anchor=(1.1, 0.1), fontsize=8)

        return fig

    st.pyplot(make_radar_chart(categories, norm_user_values, norm_mean_values, norm_low_values))

# 右側：分類結果
with col3:
    st.header("Cell Cluster Status")
    malignant_probability = np.random.uniform(0.5, 1.0)  # 假設性結果
    benign_probability = 1 - malignant_probability

    if malignant_probability > benign_probability:
        status = "Malignant"
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


