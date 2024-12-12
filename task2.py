import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static  
import streamlit as st


df1 = pd.read_csv('Unemployment_in_India.csv')
df2 = pd.read_csv('Unemployment_Rate_upto_11_2020.csv')


df1.columns = df1.columns.str.strip()
df2.columns = df2.columns.str.strip()
df1['Date'] = pd.to_datetime(df1['Date'].str.strip(), format='%d-%m-%Y')
df2['Date'] = pd.to_datetime(df2['Date'].str.strip(), format='%d-%m-%Y')


df1.dropna(inplace=True)



df2['latitude'] = pd.to_numeric(df2['latitude'], errors='coerce')
df2['longitude'] = pd.to_numeric(df2['longitude'], errors='coerce')
df2['Estimated Unemployment Rate (%)'] = pd.to_numeric(df2['Estimated Unemployment Rate (%)'], errors='coerce')


df2_clean = df2.dropna(subset=['latitude', 'longitude'])


df2_clean = df2_clean[(df2_clean['latitude'] >= 6.5) & (df2_clean['latitude'] <= 37.5) &
                      (df2_clean['longitude'] >= 68.5) & (df2_clean['longitude'] <= 97.5)]


merged_df = pd.concat([df1, df2], ignore_index=True)


avg_unemployment = merged_df.groupby('Date')['Estimated Unemployment Rate (%)'].mean()



# Interface Streamlit
st.title("Analysis of Unemployment Rate in India during Covid-19")
st.subheader("1. Average Unemployment Rate Trend")


st.line_chart(avg_unemployment)


st.subheader("2. Unemployment Rate by Region")
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x='Region', y='Estimated Unemployment Rate (%)', data=merged_df, ax=ax)
ax.set_title('Unemployment Rate by Region')
ax.set_xlabel('Region')
ax.set_ylabel('Unemployment rate (%)')
plt.xticks(rotation=90)
st.pyplot(fig)


st.subheader("3. Correlation Matrix")
numeric_columns = merged_df.select_dtypes(include=['float64', 'int64'])
correlation = numeric_columns.corr()
fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(correlation, annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
ax.set_title('Correlation Matrix')
st.pyplot(fig)


df1['Year'] = df1['Date'].dt.year
df2['Year'] = df2['Date'].dt.year

df1_2019 = df1[df1['Year'] == 2019]
df2_2019 = df2[df2['Year'] == 2019]
df1_2020 = df1[df1['Year'] == 2020]
df2_2020 = df2[df2['Year'] == 2020]


avg_unemployment_2019 = df1_2019['Estimated Unemployment Rate (%)'].mean()
avg_unemployment_2020 = df2_2020['Estimated Unemployment Rate (%)'].mean()


unemployment_comparison = pd.DataFrame({
    'Year': ['2019', '2020'],
    'Unemployment Rate': [avg_unemployment_2019, avg_unemployment_2020]
})


st.markdown("### 4. Unemployment Rates in 2019 and 2020")



fig, ax = plt.subplots(figsize=(6, 6))  

ax.pie(unemployment_comparison['Unemployment Rate'], labels=unemployment_comparison['Year'], autopct='%1.1f%%', startangle=90, colors=['#66b3ff', '#ff6666'])
ax.set_title('Comparison of the unemployment rate in 2019 and 2020')

st.pyplot(fig)
