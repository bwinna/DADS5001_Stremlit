import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import pydeck as pdk
import numpy as np
import time
import altair as alt
from urllib.error import URLError


# ตั้งค่าหน้าสำหรับ Streamlit
st.set_page_config(page_title="Starbucks World Location", page_icon="🌍")

st.markdown("# Starbucks Location")
st.sidebar.header("Filter Options")

# อ่านข้อมูลจากไฟล์ CSV ที่อยู่ในโฟลเดอร์ปัจจุบัน
file_path = r"C:\Users\Winna\DADS_tool\week11_streamlit_2\directory.csv"
data = pd.read_csv(file_path)

# ตรวจสอบว่าคอลัมน์ 'Latitude' และ 'Longitude' อยู่ใน DataFrame
if 'Latitude' in data.columns and 'Longitude' in data.columns:
    # แปลงคอลัมน์ Latitude และ Longitude ให้เป็น float
    data['Latitude'] = pd.to_numeric(data['Latitude'], errors='coerce')
    data['Longitude'] = pd.to_numeric(data['Longitude'], errors='coerce')

    # ลบข้อมูลที่มี Latitude หรือ Longitude เป็น NaN
    data = data.dropna(subset=['Latitude', 'Longitude'])

    # เพิ่มกล่องเลือกประเทศ
    country_list = data['Country'].unique().tolist()
    selected_country = st.selectbox("Select a country", ["All"] + country_list)

    # กรองข้อมูลตามประเทศที่เลือก
    if selected_country != "All":
        data = data[data['Country'] == selected_country]

    # เพิ่มกล่องเลือกเมือง
    city_list = data['City'].unique().tolist()
    selected_city = st.selectbox("Select a city", ["All"] + city_list)

    # กรองข้อมูลตามเมืองที่เลือก
    if selected_city != "All":
        data = data[data['City'] == selected_city]

    # แสดงข้อมูลตัวอย่างหลังจากการกรอง
    st.write("📋 **Filtered Data**", data.head())

    # สร้างแผนที่ด้วย ColumnLayer
    if not data.empty:
        layer = pdk.Layer(
            'ColumnLayer',
            data=data,
            get_position=['Longitude', 'Latitude'],
            get_elevation=100,
            elevation_scale=50,
            radius=500,
            get_fill_color=[255, 0, 0, 160],
            pickable=True,
            auto_highlight=True,
        )

        # สร้างแผนที่ pydeck
        view_state = pdk.ViewState(
            latitude=data['Latitude'].mean(),
            longitude=data['Longitude'].mean(),
            zoom=10,
            pitch=45,
        )

        st.pydeck_chart(pdk.Deck(
            map_style='mapbox://styles/mapbox/light-v10',
            initial_view_state=view_state,
            layers=[layer],
        ))
    else:
        st.warning("No data available for the selected filters.")
else:
    st.error("The file does not contain 'Latitude' and 'Longitude' columns.")

# ส่วนของการสร้าง Bar Chart
st.markdown("## Number of Starbucks Locations by Country")

# ตรวจสอบว่าคอลัมน์ 'Country' อยู่ใน DataFrame
if 'Country' in data.columns:
    # นับจำนวนสาขา Starbucks ในแต่ละประเทศ (ไม่สนใจการกรองเมือง)
    original_data = pd.read_csv(file_path)
    country_count = original_data['Country'].value_counts().reset_index()
    country_count.columns = ['Country', 'Count']

    # สร้าง Bar Chart ด้วย Altair
    bar_chart = alt.Chart(country_count).mark_bar().encode(
        x=alt.X('Country:N', sort='-y', title='Country'),
        y=alt.Y('Count:Q', title='Number of Locations'),
        color=alt.value('green'),
        tooltip=['Country', 'Count']
    ).properties(
        title='Number of Starbucks Locations by Country',
        width=800,
        height=400
    )

    # แสดง Bar Chart ใน Streamlit
    st.altair_chart(bar_chart, use_container_width=True)
else:
    st.error("The file does not contain a 'Country' column.")
######################################################################################

# ตรวจสอบว่าคอลัมน์ 'Country' อยู่ใน DataFrame
if 'Country' in data.columns:
    # นับจำนวนสาขา Starbucks ในแต่ละประเทศ (ไม่สนใจการกรองเมือง)
    original_data = pd.read_csv(file_path)
    country_count = original_data['Country'].value_counts().reset_index()
    country_count.columns = ['Country', 'Count']

    # สร้าง Bar Chart ด้วย Plotly
    fig = px.bar(
        country_count,
        x='Country',
        y='Count',
        color='Count',
        color_continuous_scale='Blues',
        title='Number of Starbucks Locations by Country',
        labels={'Count': 'Number of Locations', 'Country': 'Country'},
        height=600,
    )

    # แสดง Bar Chart ใน Streamlit
    st.plotly_chart(fig, use_container_width=True)
else:
    st.error("The file does not contain a 'Country' column.")


#######################################################################################
# ตรวจสอบว่าคอลัมน์ 'City' อยู่ใน DataFrame
if 'City' in data.columns:
    # สร้าง Histogram ด้วย Plotly
    fig = px.histogram(
        data,
        x='City',
        nbins=30,
        title='Distribution of Starbucks Locations by City',
        labels={'City': 'City', 'count': 'Number of Locations'},
        color_discrete_sequence=['#FF5733']
    )

    # แสดง Histogram ใน Streamlit
    st.plotly_chart(fig, use_container_width=True)
else:
    st.error("The file does not contain a 'City' column.")

#####################################################################################


# ส่วนของการสร้าง Histogram ด้วย Plotly (Top 10 Locations)
st.markdown("## Top 10 Cities with the Most Starbucks Locations")

# ตรวจสอบว่าคอลัมน์ 'City' อยู่ใน DataFrame
if 'City' in data.columns:
    # นับจำนวนสาขา Starbucks ในแต่ละเมือง
    city_count = data['City'].value_counts().reset_index()
    city_count.columns = ['City', 'Count']

    # กรองเฉพาะ Top 10 เมืองที่มีจำนวนสาขามากที่สุด
    top_10_cities = city_count.head(10)

    # สร้าง Histogram ด้วย Plotly
    fig = px.bar(
        top_10_cities,
        x='City',
        y='Count',
        color='Count',
        color_continuous_scale='Blues',
        title='Top 10 Cities with Most Starbucks Locations',
        labels={'Count': 'Number of Locations', 'City': 'City'},
        height=600,
    )

    # แสดง Histogram ใน Streamlit
    st.plotly_chart(fig, use_container_width=True)
else:
    st.error("The file does not contain a 'City' column.")

#######################################################################################

# สร้าง Scatter Plot ด้วย Plotly
st.markdown("## Starbucks Locations Scatter Plot")

if not data.empty:
    fig = px.scatter_mapbox(
        data,
        lat='Latitude',
        lon='Longitude',
        hover_name='Store Name',
        hover_data=['City', 'Country', 'Store Number'],
        color_discrete_sequence=['red'],
        zoom=5,
        height=600,
    )

    # ตั้งค่าแผนที่ให้ใช้ Mapbox
    fig.update_layout(
        mapbox_style="open-street-map",
        title='Starbucks Locations',
        margin={"r":0,"t":50,"l":0,"b":0}
    )

    # แสดง Scatter Plot ใน Streamlit
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No data available for the selected filters.")




#######################################################################################
