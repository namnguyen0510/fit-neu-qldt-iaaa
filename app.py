import streamlit as st
from utils_options import *
import pandas as pd
import matplotlib.pyplot as plt
from utils import *
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Set page layout to wide
st.set_page_config(page_title = 'NEU-IAAA',layout="wide")

# Title
st.title("NEU - Intelligent Admission Advisory Assistant (IAAA)")
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(['Home', 'Why NEU?', 'Grade Converter', 'Major Selection', 'FAQs', 'About'])

thpt_sel = ['SAT', 'ĐGNL-DHBK-HN', 'ĐGNL-DHQG-HN', 'ĐGNL-DHQG-TPHCM']

with tab3:
    ga_selection = st.pills('**Chọn điểm ứng tuyển theo khối**', ga_options, selection_mode = 'single', default = ga_options[0])
    col1, col2 = st.columns([1,4])
    with col1:
        with st.container(border = True):
            st.write('**Nhập điểm của bạn**')
            if ('ĐGNL' not in ga_selection) and ('SAT' not in ga_selection):
                ga_comp = ga_selection.split('(')[1].split(')')[0].split(',')
                ga_comp = [x.strip() for x in ga_comp]
                grade_01 = st.number_input(f"Điểm {ga_comp[0]}")
                grade_02 = st.number_input(f"Điểm {ga_comp[1]}")
                grade_03 = st.number_input(f"Điểm {ga_comp[2]}")
                user_score = grade_01+grade_02+grade_03
                st.write("Tổng điểm", grade_01+grade_02+grade_03)
            else:
                user_score = st.number_input(f"Điểm {ga_selection}")
                st.write("Tổng điểm", user_score)
        year_selection = st.selectbox('**Chọn Năm so sánh**', (2022, 2023, 2024, 'All'), index=2)
    with col2:
        #st.write(ga_selection)
        if 'A00' in ga_selection:
            ref_df = pd.read_csv('dset_private/neu-groups/0_A00.csv')
        elif 'A01' in ga_selection:
            ref_df = pd.read_csv('dset_private/neu-groups/1_A01.csv')
        elif 'D01' in ga_selection:
            ref_df = pd.read_csv('dset_private/neu-groups/2_D01.csv')
        elif 'D07' in ga_selection:
            ref_df = pd.read_csv('dset_private/neu-groups/3_D07.csv')
        elif 'IA1' in ga_selection:
            ref_df = pd.read_csv('dset_private/neu-groups/4_IA1.csv')
        elif 'IA2' in ga_selection:
            ref_df = pd.read_csv('dset_private/neu-groups/5_IA2.csv')
        elif 'IA3' in ga_selection:
            ref_df = pd.read_csv('dset_private/neu-groups/6_IA3.csv')
        elif 'IA4' in ga_selection:
            ref_df = pd.read_csv('dset_private/neu-groups/7_IA4.csv')
        elif 'ĐGNL' in ga_selection:
            ref_df = pd.read_csv('dset_private/neu-groups/neu-ts-gpa-2024.csv', sep = ';')
        elif 'SAT' in ga_selection:
            ref_df = pd.read_csv('dset_private/neu-groups/neu-ts-gpa-2024.csv', sep = ';')

        
        if ('ĐGNL' not in ga_selection) and ('SAT' not in ga_selection):
            if year_selection != 'All':
                ref_df = ref_df[ref_df['Năm'] == year_selection]
            user_score = grade_01+grade_02+grade_03
            bench_score = ref_df[ga_comp[0]]+ref_df[ga_comp[1]]+ref_df[ga_comp[2]]
        elif 'SAT' in ga_selection:
            ref_df = ref_df[ref_df['Loại CC Nhóm 1'] == 'SAT']
            bench_score = ref_df['Điểm CCQT Nhóm 1'].astype(str).str.replace(",", ".").astype(float)
        #  'ĐGNL-DHBK-HN', 'ĐGNL-DHQG-HN', 'ĐGNL-DHQG-TPHCM'
        elif ga_selection == 'ĐGNL-DHBK-HN':
            ref_df = ref_df[ref_df['Loại DGNL/DGTD Nhóm 2.1'] == 'DGNLDHBKHN']
            bench_score = ref_df['Điểm DGNL/DGTD 2.1'].astype(str).str.replace(",", ".").astype(float)
        elif ga_selection == 'ĐGNL-DHQG-HN':
            ref_df = ref_df[ref_df['Loại DGNL/DGTD Nhóm 2.1'] == 'DGNLDHQGHN']
            bench_score = ref_df['Điểm DGNL/DGTD 2.1'].astype(str).str.replace(",", ".").astype(float)
        elif ga_selection == 'ĐGNL-DHQG-TPHCM':
            ref_df = ref_df[ref_df['Loại DGNL/DGTD Nhóm 2.1'] == 'DGNLDHQGTPHCM']
            bench_score = ref_df['Điểm DGNL/DGTD 2.1'].astype(str).str.replace(",", ".").astype(float)



        if ga_selection not in thpt_sel:
            with st.container(border=True):
                st.markdown(f'Số điểm của bạn là: **{user_score}**. So sánh với năm **{year_selection}**, điểm của bạn ở thứ tự **{compute_position(user_score,bench_score)[0]}/{len(ref_df)}**.')
            # Create subplots (2 rows, 3 columns)
            fig = make_subplots(rows=2, cols=3, 
                                subplot_titles=[ga_comp[0], ga_comp[1], ga_comp[2], "Box Plot", "Benchmark Score", "Distribution"])

            # Histograms with vertical reference lines
            fig.add_trace(go.Histogram(x=ref_df[ga_comp[0]], opacity=0.2, marker_color='red', name=ga_comp[0]), row=1, col=1)
            fig.add_trace(go.Scatter(x=[grade_01, grade_01], y=[0, 1000], mode='lines', line=dict(color='red', dash='dash'), showlegend=False), row=1, col=1)

            fig.add_trace(go.Histogram(x=ref_df[ga_comp[1]], opacity=0.2, marker_color='green', name=ga_comp[1]), row=1, col=2)
            fig.add_trace(go.Scatter(x=[grade_02, grade_02], y=[0, 1000], mode='lines', line=dict(color='green', dash='dash'), showlegend=False), row=1, col=2)

            fig.add_trace(go.Histogram(x=ref_df[ga_comp[2]], opacity=0.2, marker_color='blue', name=ga_comp[2]), row=1, col=3)
            fig.add_trace(go.Scatter(x=[grade_03, grade_03], y=[0, 1000], mode='lines', line=dict(color='blue', dash='dash'), showlegend=False), row=1, col=3)

            # Boxplot for three categories
            fig.add_trace(go.Box(y=ref_df[ga_comp[0]], marker_color='red', name=ga_comp[0]), row=2, col=1)
            fig.add_trace(go.Box(y=ref_df[ga_comp[1]], marker_color='green', name=ga_comp[1]), row=2, col=1)
            fig.add_trace(go.Box(y=ref_df[ga_comp[2]], marker_color='blue', name=ga_comp[2]), row=2, col=1)

            # Boxplot for benchmark score
            fig.add_trace(go.Box(y=bench_score, marker_color='black', name=f'Tổng điểm: {year_selection}'), row=2, col=2)

            # Histogram for benchmark score with vertical line
            fig.add_trace(go.Histogram(x=bench_score, opacity=0.5, marker_color='gray', name=f'Phân bố điểm: {year_selection}'), row=2, col=3)
            fig.add_trace(go.Scatter(x=[user_score, user_score], y=[0, 100], mode='lines', line=dict(color='gray', dash='dash'), showlegend=False), row=2, col=3)

            # Layout adjustments
            fig.update_layout(height=600, width=800, showlegend=False)
            st.plotly_chart(fig)
            
        else:
            #st.write('NA')
            with st.container(border=True):
                st.markdown(f'Số điểm của bạn là: **{user_score}**. So sánh với năm **{year_selection}**, điểm của bạn ở thứ tự **{compute_position(user_score,bench_score)[0]}/{len(ref_df)}**.')
            # Create subplots (2 rows, 3 columns)
            fig = make_subplots(rows=2, cols=2)
            # Histograms with vertical reference lines
            fig.add_trace(go.Box(y=bench_score, marker_color='red', name=ga_selection), row=1, col=1)
            fig.add_trace(go.Histogram(x=bench_score, opacity=0.2, marker_color='red', name=ga_selection), row=1, col=2)
            fig.add_trace(go.Scatter(x=[user_score, user_score], y=[0, 20], mode='lines', line=dict(color='red', dash='dash'), showlegend=False), row=1, col=2)
            # Layout adjustments
            fig.update_layout(height=600, width=1000, showlegend=True)
            #fig.update_xaxes(range=[1200, 1600], col=2, row=1)  # Sets x-axis from 1 to 4
            st.plotly_chart(fig)
            

    

