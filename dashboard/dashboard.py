import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st


colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]


time_qtr_df = pd.read_csv("dashboard/time_qtr.csv")
all_time_df = pd.read_csv("dashboard/all_time.csv")


time_qtr_df['year'] = time_qtr_df['yearnquarter'].str.extract(r'(\d{4})').astype(int)
time_qtr_df['quarter'] = time_qtr_df['yearnquarter'].str.extract(r'Q(\d)').astype(int)
time_qtr_df = time_qtr_df.sort_values(by=['year', 'quarter'])


st.subheader('Rental Bike Usage Trend')

col1, _ = st.columns(2)  

with col1:
    max_user = time_qtr_df["cnt_max"].max()
    st.metric("Highest amount of rental user per year along with quarter", value=max_user)


fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    time_qtr_df["yearnquarter"],
    time_qtr_df["cnt_mean"],
    marker='o',
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
ax.set_xlabel("Year & Quarter", fontsize=18)
ax.set_ylabel("Average Rental Users", fontsize=18)

st.pyplot(fig)

st.subheader("Bike rental usage total")
    
col1, col2 = st.columns(2)
    
with col1:
    fig, ax = plt.subplots(figsize=(20, 10))
    
    sns.barplot(
        y="total_customer", 
        x="season",
        hue="season",
        data=all_time_df.sort_values(by="total_customer", ascending=False),
        palette=colors,
        legend=False,
        ax=ax
    )
    ax.set_title("Total amount Bike rental usage by season ", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)
    
with col2:
    fig, ax = plt.subplots(figsize=(20, 10))
    

    
    sns.barplot(
        y="total_customer", 
        x="time_cycle",
        hue="time_cycle",
        data=all_time_df.sort_values(by="total_customer", ascending=False),
        palette=colors,
        legend=False,
        ax=ax
    )
    ax.set_title("Total Amount Bike rental usage by time cycle", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)
    