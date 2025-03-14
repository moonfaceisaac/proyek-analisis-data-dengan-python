import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import streamlit as st

st.title("Bike Rental Statistical Dashboard")

colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]


time_qtr_df = pd.read_csv("dashboard/time_qtr.csv")
season_time_df = pd.read_csv("dashboard/season_time.csv")
timecyc_time_df = pd.read_csv("dashboard/timecyc_time.csv")
wd_time_df = pd.read_csv("dashboard/wd_time.csv")


st.subheader('Rental Bike performance 2011-2012')
time_qtr_df["yearnquarter"] = time_qtr_df["yearnquarter"].astype(str).str.strip()
time_qtr_df['yr'] = time_qtr_df['yearnquarter'].str.extract(r'(\d{4})').astype(float)
time_qtr_df['quarter'] = time_qtr_df['yearnquarter'].str.extract(r'Q(\d)').astype(float)
time_qtr_df = time_qtr_df.dropna(subset=['yr', 'quarter']).astype({'yr': int, 'quarter': int})
time_qtr_df = time_qtr_df.sort_values(by=['yr', 'quarter'])


with st.sidebar:
    st.write("Welcome to Bike Rental Statistic Dashboard!")
    st.write("Filter Bike Performance 2011-2012 Data:")
    quarter_options = [f"{year}.Q{q}" for year in range(2011, 2013) for q in range(1, 5)]
    selected_range = st.select_slider("Select Quarter Range:", options=quarter_options, value=(quarter_options[0], quarter_options[-1]))
    start_year, start_qtr = map(int, selected_range[0].split('.Q'))
    end_year, end_qtr = map(int, selected_range[1].split('.Q'))


filtered_df = time_qtr_df[(time_qtr_df['yr'] > start_year) | ((time_qtr_df['yr'] == start_year) & (time_qtr_df['quarter'] >= start_qtr))]
filtered_df = filtered_df[(filtered_df['yr'] < end_year) | ((filtered_df['yr'] == end_year) & (filtered_df['quarter'] <= end_qtr))]

total_avg = round(filtered_df["cnt_mean"].max())
st.metric("Highest average in a quarter", value=total_avg)



fig, ax = plt.subplots(figsize=(32, 16))
ax.plot(

    filtered_df["yearnquarter"],
    filtered_df["cnt_mean"],
    marker='o',
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=35)
ax.tick_params(axis='x', labelsize=40,rotation=45)
ax.set_xlabel("Year & Quarter", fontsize=38)
ax.set_ylabel("Average numbers of rental bike recorded", fontsize=38)
ax.set_title("Rental Bike performance 2011-2012 based on average total recorded per quarter", loc="center",fontsize=50)
st.pyplot(fig)


x_val = " "
st.subheader("Total Amount of Bike Rental recorded by time conditions")

option = st.radio("Select Time Conditions:", ["By Season", "By Time Cycle","By Type of Day"])

fig, ax = plt.subplots(figsize=(20, 10))

if option == "By Season":
    sns.barplot(
        y="total_customer",
        x="season",
        hue="season",
        data=season_time_df.sort_values(by="total_customer", ascending=False),
        palette=colors,
        legend=False,
        ax=ax
    )
    ax.yaxis.set_major_formatter(mticker.StrMethodFormatter('{x:,.0f}'))
    x_val = "Season"
    ax.set_title("Total Amount of Bike Rental recorded based on season", loc="center", fontsize=50)
elif option == "By Time Cycle":
    sns.barplot(
        y="total_customer",
        x="time_cycle",
        hue="time_cycle",
        data=timecyc_time_df.sort_values(by="total_customer", ascending=False),
        palette=colors,
        legend=False,
        ax=ax
    )
    x_val = "Time Cycle"
    ax.set_title("Total Amount of Bike Rental recorded based on time cycle", loc="center", fontsize=50)
elif option == "By Type of Day":
    sns.barplot(
        y="total_customer",
        x="workingday",
        hue="workingday",
        data=wd_time_df.sort_values(by="total_customer", ascending=False),
        palette=colors,
        legend=False,
        ax=ax
    )
    ax.yaxis.set_major_formatter(mticker.StrMethodFormatter('{x:,.0f}'))
    x_val = "Type of Day"
    ax.set_title("Total Amount of Bike Rental recorded based on type of day", loc="center", fontsize=50)

ax.set_ylabel("Total Amount of Bike Rental recorded",fontsize=28)
ax.set_xlabel(x_val, fontsize=28)
ax.tick_params(axis='x', labelsize=35)
ax.tick_params(axis='y', labelsize=30)
st.pyplot(fig)
