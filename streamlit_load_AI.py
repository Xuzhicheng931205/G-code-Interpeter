import tensorflow as tf
import streamlit as st

agree = st.checkbox('Show predict power consumption using AI model')
if agree:
    model = tf.keras.models.load_model(r"C:\Users\XUZHICHENG\IdeaProjects\mat\Python_Webkaifa\G_code_load_file_model\model_comsumption.h5")
    st.write("模型已经加载完了")