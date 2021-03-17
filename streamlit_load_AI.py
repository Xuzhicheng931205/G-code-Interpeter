import tensorflow as tf
import streamlit as st

agree = st.checkbox('Show predict power consumption using AI model')
if agree:
    model = tf.keras.models.load_model(r"https://github.com/Xuzhicheng931205/G-code-Interpeter/blob/Gcode/model_comsumption.h5")
    st.write("模型已经加载完了")
