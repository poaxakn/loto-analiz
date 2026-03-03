import streamlit as st
import pandas as pd
import random
import matplotlib.pyplot as plt
from collections import Counter
import os

# --- SAYFA AYARLARI ---
st.set_page_config(
    page_title="Loto Master Pro",
    page_icon="🔮",
    layout="centered"
)

# --- ÖZEL TASARIM (CSS) ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    .tahmin-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        font-size: 28px;
        font-weight: bold;
        letter-spacing: 5px;
        margin: 20px 0;
        box-shadow: 0 10px 20px rgba(0,0,0,0.3);
    }
    .metric-card {
        background-color: #1e1e2f;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #4e73df;
    }
    </style>
    """, unsafe_allow_html=True)

# --- VERİ YÜKLEME ---
@st.cache_data # Veriyi her seferinde baştan okuyup uygulamayı yavaşlatmaz
def veri_hazirla():
    if not os.path.exists("sayisal_gecmis.csv"):
        # Dosya yoksa demo verisi oluştur
        data = {"Tarih": pd.date_range(start="2024-01-01", periods=100, freq="W")}
        for i in range(1, 7):
            data[f"S{i}"] = [random.randint(1, 90) for _ in range(100)]
        pd.DataFrame(data).to_csv("sayisal_gecmis.csv", index=False)
    
    df = pd.read_csv("sayisal_gecmis.csv")
    sayilar = pd.to_numeric(df.iloc[:, 1:].values.flatten(), errors='coerce')
    return sayilar[~pd.isna(sayilar)].tolist()

# --- ANA EKRAN ---
st.title("🔮 Loto Analiz Pro")
st.markdown("Samsung S23 Mobil Uyumlu Analiz Paneli")

data_list = veri_hazirla()
sayac = Counter(data_list)

# --- TABLAR ---
tab1, tab2, tab3 = st.tabs(["🎯 Tahmin Al", "📊 İstatistik", "📋 Veri Özeti"])

with tab1:
    st.write("### Akıllı Algoritma")
    st.caption("3 Sıcak + 2 Soğuk + 1 Sürpriz Sayı")
    
    if st.button("ŞANSLI NUMARALARI OLUŞTUR", use_container_width=True):
        # Algoritma
        sicak = [n for n, _ in sayac.most_common(15)]
        soguk = [n for n, _ in sayac.most_common()[:-16:-1]]
        genel = list(set(data_list))
        
        secim = random.sample(sicak, 3) + random.sample(soguk, 2)
        while len(secim) < 6:
            yeni = random.choice(genel)
            if yeni not in secim: secim.append(yeni)
        
        secim.sort()
        sonuc_str = " - ".join([str(int(n)).zfill(2) for n in secim])
        
        st.markdown(f'<div class="tahmin-box">{sonuc_str}</div>', unsafe_allow_html=True)
        st.balloons() # S23 ekranında harika görünür!

with tab2:
    st.write("### Sayı Frekans Grafiği")
    en_cok = sayac.most_common(12)
    s, a = zip(*en_cok)
    
    fig, ax = plt.subplots()
    fig.patch.set_facecolor('#0e1117')
    ax.set_facecolor('#1e1e2f')
    ax.bar([str(int(i)) for i in s], a, color='#667eea')
    ax.tick_params(colors='white')
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')
    plt.xticks(rotation=45)
    
    st.pyplot(fig)

with tab3:
    col1, col2 = st.columns(2)
    col1.metric("Toplam Çekiliş", len(data_list)//6)
    col2.metric("En Çok Çıkan", int(sayac.most_common(1)[0][0]))
    
    st.write("### Son Veriler")
    df_view = pd.read_csv("sayisal_gecmis.csv").tail(10)
    st.dataframe(df_view, use_container_width=True)

st.divider()
st.caption("📱 S23 İpucu: Tarayıcı ayarlarından 'Ana Ekrana Ekle' derseniz uygulama gibi kullanabilirsiniz.")