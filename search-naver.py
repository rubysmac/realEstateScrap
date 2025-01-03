import streamlit as st
import pandas as pd
import requests
import json

# Function to fetch data for multiple pages
def fetch_real_estate_data():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://m.land.naver.com/',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    all_data = []
    for page in range(2, 11):  # Loop through pages 1 to 10
        # Simulating API call (replace this with your actual API URL and parameters)
        url = f"https://m.land.naver.com/cluster/ajax/articleList?itemId=&mapKey=&lgeo=&showR0=&rletTpCd=APT%3AJGC%3AABYG%3AOR%3AOPST%3AOBYG%3AVL%3ADDDGG%3AJWJT%3ASGJT%3AHOJT%3ATJ%3ASG%3ASMS%3AGJCG%3AAPTHGJ%3AJGB%3AGM&tradTpCd=A1&z=14&lat=37.5524943&lon=126.9063401&btm=37.5207781&lft=126.8713211&top=37.5841971&rgt=126.941359&totCnt=9920&cortarNo=1144000000&sort=rank&page={page}"
        response = requests.get(url, headers=headers, allow_redirects=True)
        if response.status_code == 200:
            response_json = response.json()
            if response_json.get("code") == "success":  # Check if request was successful
                data = response_json.get("body", [])
                all_data.extend(data)
            else:
                st.error(f"API request failed for page {page}")
                break
        else:
            st.error(f"Failed to fetch data for page {page}. Status code: {response.status_code}")
            break
    return all_data

# Fetch data from all pages
real_estate_data = fetch_real_estate_data()

# Convert data to a DataFrame
df = pd.DataFrame(real_estate_data)

# Select relevant columns and rename them with Korean headers
relevant_columns = {
    'atclNm': '건물명',
    'rletTpNm': '매물종류',
    'tradTpNm': '거래유형',
    'hanPrc': '가격',
    'spc1': '전용면적(㎡)',
    'spc2': '전용면적(평)',
    'flrInfo': '층/총층',
    'direction': '방향',
    'atclFetrDesc': '특징',
    'tagList': '태그',
    'bildNm': '동',
    'atclCfmYmd': '확인일자',
    'sameAddrMaxPrc': '동일단지최고가',
    'sameAddrMinPrc': '동일단지최저가',
    'sameAddrCnt': '동일단지매물수',
}

df = df[relevant_columns.keys()].rename(columns=relevant_columns)

# Streamlit UI
st.title("Real Estate Price Tracker")
st.write("Check real estate prices and make wise decisions!")

# Configure table to be wider
st.write("### Real Estate Listings")
st.dataframe(df.style.set_properties(**{"text-align": "left"}), use_container_width=True)

# Download CSV button
if not df.empty:
    csv = df.to_csv(index=False)
    st.download_button(
        label="Download Table as CSV",
        data=csv,
        file_name="real_estate_data.csv",
        mime="text/csv",
    )
else:
    st.warning("No data available to display or download.")
