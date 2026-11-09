import os
import base64
import hashlib
from html import escape
from pathlib import Path

import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
from statistik import render as render_statistik
from author import show_author

st.set_page_config(
    page_title='Rak Buku: rekomendasi item-based CF',
    page_icon='📚',
    layout='wide',
    initial_sidebar_state='collapsed'
)

show_author()

HERE = Path(__file__).parent
COVERS = HERE / 'covers'
ART = os.environ.get('ART_DIR', str(HERE / 'app_artifacts'))
TEAL = '#0E7C86'
SPINES = ['#0E7C86', '#7A3E48', '#33572F', '#C0652B', '#3D4C8F', '#6B4E8C', '#2F6B63', '#8A6D1F']

st.markdown('''<style>
@import url('https://fonts.googleapis.com/css2?family=Libre+Caslon+Text:wght@400;700&family=Public+Sans:wght@400;500;600&display=swap');

/* ===== Tema gelap: midnight navy, teal, dan aksen gold ===== */
:root {
    color-scheme: dark;
    --bg: #0B1220;
    --panel: #111C2E;
    --panel-2: #172438;
    --border: #293B53;
    --text: #E8EEF7;
    --muted: #A8B6C8;
    --teal: #35C6B4;
    --gold: #E6B45C;
}

html, body, .stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="stHeader"] {
    background: var(--bg) !important;
    color: var(--text) !important;
}

.stApp, .stApp p, .stApp label, .stApp li,
.stApp [data-testid="stMarkdownContainer"] {
    font-family: 'Public Sans', sans-serif;
    color: var(--text);
}

.stApp h1, .stApp h2, .stApp h3,
.stApp h4 {
    font-family: 'Libre Caslon Text', serif !important;
    color: var(--text) !important;
}

.block-container {
    width: 100% !important;
    max-width: 1400px !important;
    padding-top: 1.4rem !important;
    padding-bottom: 2rem !important;
}

/* Sidebar */
[data-testid="stSidebar"],
[data-testid="stSidebar"] > div {
    background: #0E1929 !important;
}
[data-testid="stSidebar"] * {
    color: var(--text);
}
[data-testid="stSidebar"] [data-testid="stExpander"] {
    background: var(--panel) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px;
}

/* Metric cards */
[data-testid="stMetric"] {
    background: var(--panel-2) !important;
    border: 1px solid var(--border);
    border-left: 4px solid var(--teal);
    padding: 14px 16px;
    border-radius: 8px;
}
[data-testid="stMetric"] label,
[data-testid="stMetric"] [data-testid="stMetricLabel"] {
    color: var(--muted) !important;
}
[data-testid="stMetric"] [data-testid="stMetricValue"] {
    color: var(--text) !important;
}

/* ===== Hero: satu kolom secara permanen.
   Gambar fan sengaja disembunyikan agar tidak mengambil lebar judul
   saat aplikasi tampil di iframe profil Hugging Face. ===== */
div[data-testid="stMarkdownContainer"] {
    width: 100%;
    min-width: 0;
}
.hero,
.hero * {
    box-sizing: border-box;
}
.hero {
    display: block !important;
    width: 100% !important;
    max-width: 100% !important;
    min-width: 0 !important;
    background: linear-gradient(135deg, #12384A 0%, #102638 100%);
    border: 1px solid #24465A;
    border-bottom: 8px solid #A8703F;
    border-radius: 10px 10px 0 0;
    padding: 0 34px;
    margin: 0 0 26px 0;
    overflow: hidden;
}
.hero-text {
    display: block !important;
    width: 100% !important;
    max-width: 100% !important;
    min-width: 0 !important;
    padding: 34px 0;
}
.hero h1 {
    display: block !important;
    width: 100% !important;
    max-width: 720px !important;
    min-width: 0 !important;
    color: #F7F4EC !important;
    font-family: 'Libre Caslon Text', serif !important;
    font-size: clamp(1.65rem, 4vw, 2.45rem) !important;
    line-height: 1.18 !important;
    margin: 0 0 14px 0 !important;
    padding: 0 !important;
    white-space: normal !important;
    word-break: normal !important;
    overflow-wrap: break-word !important;
    letter-spacing: -0.02em;
}
.hero p {
    display: block !important;
    width: 100% !important;
    max-width: 650px !important;
    color: #C5D5E2 !important;
    font-size: 1rem;
    line-height: 1.65;
    margin: 0;
    overflow-wrap: break-word;
}
.hero .fan {
    display: none !important;
}

/* Rak buku */
.shelf {
    display: flex;
    gap: 22px;
    align-items: flex-start;
    overflow-x: auto;
    padding: 18px 14px 12px 14px;
    margin: 8px 0 26px 0;
}
.book {
    flex: 0 0 auto;
    width: 132px;
}
.wrap {position: relative;}
.wrap::after {
    content: '';
    position: absolute;
    left: -11px;
    right: -11px;
    bottom: -9px;
    height: 9px;
    background: linear-gradient(#B98050, #8A5A30);
    border-radius: 0 0 2px 2px;
}
.cv {
    width: 132px;
    height: 196px;
    object-fit: cover;
    display: block;
    border-radius: 3px 6px 6px 3px;
    box-shadow: -3px 0 0 rgba(0,0,0,.25), 4px 6px 12px rgba(0,0,0,.35);
    transition: transform .15s ease;
}
.book:hover .cv {transform: translateY(-4px);}
.nocv {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 12px;
    box-sizing: border-box;
    color: #fff;
    font-family: 'Libre Caslon Text', serif;
    font-size: .85rem;
    text-align: center;
    line-height: 1.25;
}
.nocv span {
    display: -webkit-box;
    -webkit-line-clamp: 6;
    -webkit-box-orient: vertical;
    overflow: hidden;
}
.rk {
    position: absolute;
    top: -9px;
    left: -9px;
    z-index: 2;
    background: var(--gold);
    color: #172438;
    font-weight: 700;
    width: 26px;
    height: 26px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: .8rem;
    box-shadow: 0 2px 4px rgba(0,0,0,.3);
}
.bt {
    font-weight: 600;
    font-size: .82rem;
    margin-top: 20px;
    line-height: 1.3;
    color: var(--text);
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}
.ba {
    font-size: .75rem;
    color: var(--muted);
    margin-top: 2px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.meter {
    height: 5px;
    background: #34465B;
    border-radius: 3px;
    margin-top: 8px;
    overflow: hidden;
}
.meter i {
    display: block;
    height: 100%;
    background: var(--teal);
}
.bm {
    font-size: .72rem;
    color: var(--muted);
    margin-top: 4px;
}
.stars {
    color: var(--gold);
    font-size: .78rem;
    font-weight: 600;
    margin-top: 4px;
}
.why {
    font-size: .72rem;
    line-height: 1.3;
    color: #DCE8F3;
    background: #20354A;
    border: 1px solid #314A62;
    border-radius: 5px;
    padding: 5px 7px;
    margin-top: 7px;
    display: -webkit-box;
    -webkit-line-clamp: 4;
    -webkit-box-orient: vertical;
    overflow: hidden;
}
.detail .dt {
    font-family: 'Libre Caslon Text', serif;
    font-size: 1.5rem;
    line-height: 1.25;
    color: var(--text);
    margin-bottom: 4px;
}

/* Tabs, form controls, buttons, expanders, and tables */
button, [data-testid="baseButton-secondary"],
[data-testid="stDownloadButton"] button {
    border-radius: 7px !important;
}
.stButton button, [data-testid="stDownloadButton"] button {
    background: #173B4B !important;
    color: #EAF4F7 !important;
    border: 1px solid #326477 !important;
}
.stButton button:hover, [data-testid="stDownloadButton"] button:hover {
    border-color: var(--teal) !important;
    color: #FFFFFF !important;
}
[data-testid="stTabs"] button {
    color: var(--muted) !important;
}
[data-testid="stTabs"] button[aria-selected="true"] {
    color: var(--teal) !important;
}
[data-testid="stTabs"] [data-baseweb="tab-highlight"] {
    background: var(--teal) !important;
}
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
[data-testid="stSelectbox"] [data-baseweb="select"],
[data-testid="stMultiSelect"] [data-baseweb="select"] {
    background: var(--panel-2) !important;
    color: var(--text) !important;
    border-color: var(--border) !important;
}
[data-testid="stExpander"] {
    background: var(--panel) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px;
}
[data-testid="stDataFrame"],
[data-testid="stTable"] {
    background: var(--panel) !important;
}
hr {
    border-color: var(--border) !important;
}
[data-testid="stAlert"] {
    background: var(--panel-2) !important;
    color: var(--text) !important;
}

/* ===== Kontras tambahan untuk komponen Streamlit ===== */
.stApp,
.stApp [data-testid="stMarkdownContainer"],
.stApp [data-testid="stWidgetLabel"],
.stApp [data-testid="stCaptionContainer"],
.stApp [data-testid="stText"],
.stApp p,
.stApp li,
.stApp label,
.stApp small {
    color: #E8EEF7 !important;
}

/* DataFrame / table: wrapper mengikuti tema gelap.
   Warna internal Glide Data Grid juga dikendalikan oleh config.toml. */
[data-testid="stDataFrame"],
[data-testid="stDataFrame"] > div,
[data-testid="stTable"],
[data-testid="stTable"] table {
    background: #111C2E !important;
    color: #E8EEF7 !important;
    border-color: #293B53 !important;
}
[data-testid="stTable"] th,
[data-testid="stTable"] td {
    background: #172438 !important;
    color: #E8EEF7 !important;
    border-color: #34465B !important;
}

/* Input, dropdown, slider, checkbox, radio */
[data-baseweb="select"] > div,
[data-baseweb="input"] > div,
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
[data-testid="stDateInput"] input,
[data-testid="stTextArea"] textarea {
    background-color: #172438 !important;
    color: #E8EEF7 !important;
    border-color: #34465B !important;
}
[data-baseweb="popover"],
[data-baseweb="menu"],
[role="listbox"],
[role="option"] {
    background-color: #172438 !important;
    color: #E8EEF7 !important;
}
[data-testid="stSlider"] [data-testid="stMarkdownContainer"] {
    color: #E8EEF7 !important;
}

/* Expander, tabs, alerts */
[data-testid="stExpander"],
[data-testid="stExpander"] details,
[data-testid="stAlert"] {
    background-color: #111C2E !important;
    color: #E8EEF7 !important;
    border-color: #293B53 !important;
}
[data-testid="stExpander"] summary,
[data-testid="stExpander"] summary p {
    color: #E8EEF7 !important;
}
[data-testid="stTabs"] [role="tab"] {
    color: #A8B6C8 !important;
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    color: #35C6B4 !important;
}

/* Code / formula blocks */
[data-testid="stCode"],
.stCodeBlock,
[data-testid="stLatex"] {
    background-color: #111C2E !important;
    color: #E8EEF7 !important;
    border-color: #293B53 !important;
}

/* Download and regular buttons */
.stButton button,
.stDownloadButton button,
[data-testid="stDownloadButton"] button {
    background: #173B4B !important;
    color: #EAF4F7 !important;
    border: 1px solid #326477 !important;
}
.stButton button:hover,
.stDownloadButton button:hover,
[data-testid="stDownloadButton"] button:hover {
    background: #20566A !important;
    color: #FFFFFF !important;
    border-color: #35C6B4 !important;
}

/* Altair charts should not introduce a white plot background */
.vega-embed,
.vega-embed details,
.vega-embed summary {
    background: transparent !important;
}
.vega-embed canvas,
.vega-embed svg {
    background: transparent !important;
}

/* Responsif pada area aplikasi yang sempit */
@media (max-width: 700px) {
    .block-container {
        padding-left: .8rem !important;
        padding-right: .8rem !important;
    }
    .hero {
        padding-left: 18px;
        padding-right: 18px;
    }
    .hero-text {
        padding-top: 24px;
        padding-bottom: 24px;
    }
    .hero h1 {
        font-size: clamp(1.45rem, 6vw, 1.8rem) !important;
    }
    .hero p {
        font-size: .92rem;
    }
}
</style>''', unsafe_allow_html=True)


# ---------- Muat artefak ----------
@st.cache_resource
def load():
    sim = np.load(f'{ART}/sim.npy').astype(np.float32)
    cnt = np.load(f'{ART}/cnt.npy').astype(np.float32)
    b = np.load(f'{ART}/bias.npz')
    ratings = pd.read_csv(f'{ART}/ratings.csv')
    items = pd.read_csv(f'{ART}/items.csv')
    items['Book-Author'] = items['Book-Author'].fillna('Penulis tidak diketahui')
    items['Book-Title'] = items['Book-Title'].fillna('Tanpa judul')
    users = pd.read_csv(f'{ART}/users.csv')
    hist = {u: g for u, g in ratings.groupby('u')}
    return sim, cnt, float(b['mu']), b['bu'], b['bi'], ratings, items, users, hist


sim, cnt, MU, BU, BI, ratings, items, users, hist = load()
m, n = len(users), len(items)
LABELS = (items['Book-Title'].astype(str) + ' — ' + items['Book-Author'].astype(str)).tolist()


@st.cache_resource(max_entries=3)
def shrunk(lam):
    return sim * cnt / (cnt + lam + 1e-9)


# ---------- Komponen tampilan ----------
@st.cache_data(show_spinner=False)
def cover_src(isbn):
    f = COVERS / f'{isbn}.jpg'
    if f.exists():
        return 'data:image/jpeg;base64,' + base64.b64encode(f.read_bytes()).decode()
    return None


def cover_html(j):
    isbn = str(items.at[j, 'ISBN'])
    title = escape(str(items.at[j, 'Book-Title']))
    src = cover_src(isbn)
    if src:
        return f'<img class="cv" src="{src}" alt="{title}">'
    warna = SPINES[int(hashlib.md5(isbn.encode()).hexdigest(), 16) % len(SPINES)]
    return f'<div class="cv nocv" style="background:{warna}"><span>{title}</span></div>'


def meter(val, vmax, teks):
    pct = 0 if vmax <= 0 else max(0, min(100, val / vmax * 100))
    return f'<div class="meter"><i style="width:{pct:.0f}%"></i></div><div class="bm">{teks}</div>'


def shelf(idx, metas):
    out = ['<div class="shelf">']
    for r, (j, meta) in enumerate(zip(idx, metas), 1):
        judul = escape(str(items.at[j, 'Book-Title']))
        penulis = escape(str(items.at[j, 'Book-Author']))
        rata = float(items.at[j, 'mean_rating'])
        out.append('<div class="book"><div class="wrap">' + cover_html(j) + f'<span class="rk">{r}</span></div>'
                   + f'<div class="bt">{judul}</div><div class="ba">{penulis}</div>'
                   + f'<div class="stars">★ {rata:.1f}</div>' + meta + '</div>')
    out.append('</div>')
    st.markdown(''.join(out), unsafe_allow_html=True)


# ---------- Hero ----------
hero_imgs = []
for j in items.sort_values('n_rating', ascending=False).index:
    s = cover_src(str(items.at[j, 'ISBN']))
    if s:
        hero_imgs.append(s)
    if len(hero_imgs) == 5:
        break
rot = [-9, -4, 0, 5, 10]
fan = ''.join(f'<img src="{s}" style="left:{i * 58}px;transform:rotate({rot[i]}deg);z-index:{i}" alt="">'
              for i, s in enumerate(hero_imgs))
st.markdown(
    f'<div class="hero"><div class="hero-text"><h1>Buku apa yang sebaiknya dibaca berikutnya?</h1>'
    f'<p>Dari {m:,} pembaca dan {n:,} buku, sistem ini mencari buku yang disukai pembaca dengan selera serupa. '
    f'Pilih satu buku atau satu pembaca di tab bawah.</p></div><div class="fan">{fan}</div></div>',
    unsafe_allow_html=True)

# ---------- Sidebar ----------
box = st.sidebar.expander('Pengaturan model (lanjutan)')
lam_rank = box.slider('λ shrinkage (ranking)', 0, 100, 50, 5)
lam_pred = box.slider('λ shrinkage (prediksi rating)', 0, 100, 10, 5)
k = box.slider('k tetangga terdekat', 5, 50, 20, 5)
gamma = box.slider('γ peredam', 0.0, 2.0, 0.5, 0.25)
S_rank, S_pred = shrunk(lam_rank), shrunk(lam_pred)
# ---------- Tab 1: ringkasan ----------
with tab1:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric('Pembaca', f'{m:,}')
    c2.metric('Buku', f'{n:,}')
    c3.metric('Rating', f'{len(ratings):,}')
    c4.metric('Sparsity', f'{1 - len(ratings) / (m * n):.2%}')

    st.subheader('Delapan buku yang paling banyak di-rating')
    pop = items.nlargest(8, 'n_rating')
    shelf(pop.index.values,
          [f'<div class="bm">{int(r.n_rating)} rating, rata-rata {r.mean_rating:.1f}</div>' for r in pop.itertuples()])

    st.subheader('Sebaran nilai rating')
    dist = (ratings['Book-Rating'].round().astype(int).value_counts().sort_index()
            .rename_axis('Rating').reset_index(name='Jumlah'))
    chart = (alt.Chart(dist)
             .mark_bar(color=TEAL, cornerRadiusTopLeft=3, cornerRadiusTopRight=3)
             .encode(x=alt.X('Rating:O', title='Nilai rating'),
                     y=alt.Y('Jumlah:Q', title='Jumlah rating'),
                     tooltip=['Rating', 'Jumlah'])
             .properties(height=260, background='#0B1220'))
    st.altair_chart(chart, use_container_width=True)

# ---------- Tab 2: buku mirip ----------
with tab2:
    st.subheader('Pilih sebuah buku, lihat buku yang mirip')
    if st.button('Acak buku'):
        st.session_state['buku_i'] = int(np.random.randint(n))
    i = st.selectbox('Pilih buku', range(n), format_func=lambda x: LABELS[x], key='buku_i')

    def _t(x):
        return '' if pd.isna(x) else escape(str(x))
    try:
        tahun = str(int(float(items.at[i, 'Year-Of-Publication']))) + ', '
    except Exception:
        tahun = ''
    kiri, kanan = st.columns([1, 3])
    with kiri:
        st.markdown('<div class="wrap">' + cover_html(i) + '</div>', unsafe_allow_html=True)
    with kanan:
        st.markdown(
            f'<div class="detail"><div class="dt">{_t(items.at[i, "Book-Title"])}</div>'
            f'<div class="ba">{_t(items.at[i, "Book-Author"])}</div>'
            f'<div class="stars">★ {float(items.at[i, "mean_rating"]):.1f}</div>'
            f'<div class="bm">{tahun}{_t(items.at[i, "Publisher"])}, dirating {int(items.at[i, "n_rating"])} pembaca</div></div>',
            unsafe_allow_html=True)
        rb = (ratings.loc[ratings['i'] == i, 'Book-Rating'].round().astype(int)
              .value_counts().reindex(range(1, 11), fill_value=0)
              .rename_axis('Rating').reset_index(name='Pembaca'))
        st.altair_chart(
            alt.Chart(rb).mark_bar(color=TEAL)
            .encode(x=alt.X('Rating:O', title='Nilai rating'), y=alt.Y('Pembaca:Q', title='Pembaca'),
                    tooltip=['Rating', 'Pembaca'])
            .properties(height=120, background='#0B1220'), use_container_width=True)
    N = st.slider('Jumlah rekomendasi', 3, 20, 5, key='n_sim')
    min_co = st.slider('Minimal pembaca yang me-rating kedua buku', 1, 20, 3)

    s = S_rank[i].copy()
    s[cnt[i] < min_co] = -np.inf
    s[i] = -np.inf
    top = np.argsort(-s)[:N]
    top = top[s[top] > 0]

    if len(top) == 0:
        st.info('Tidak ada buku mirip dengan syarat ini. Turunkan batas minimal pembaca.')
    else:
        smax = float(s[top].max())
        shelf(top, [meter(float(s[j]), smax, f'kemiripan {s[j]:.2f}, {int(cnt[i, j])} pembaca sama') for j in top])
        with st.expander('Lihat angka lengkap'):
            res = items.iloc[top][['Book-Title', 'Book-Author', 'Year-Of-Publication']].copy()
            res['similarity*'] = s[top].round(3)
            res['co-rated'] = cnt[i, top].astype(int)
            st.dataframe(res, hide_index=True)

# ---------- Tab 3: rekomendasi per user ----------
with tab3:
    st.subheader('Rekomendasi untuk satu pembaca')
    u = st.selectbox('Pilih User-ID', range(m), format_func=lambda x: str(users.at[x, 'User-ID']))
    N = st.slider('Jumlah rekomendasi', 3, 20, 10, key='n_user')

    g = hist[u]
    items_u = g['i'].values
    r_u = g['Book-Rating'].values

    st.markdown(f'**Rak milik pembaca {users.at[u, "User-ID"]}**: sudah me-rating {len(g)} buku'
                + (', ditampilkan 8 dengan rating tertinggi.' if len(g) > 8 else '.'))
    order = np.argsort(-r_u)[:8]
    shelf(items_u[order], [f'<div class="bm">rating {r_u[o]:.0f}</div>' for o in order])

    score = np.maximum(S_rank[:, items_u], 0).sum(axis=1)
    score[items_u] = -np.inf
    top = np.argsort(-score)[:N]
    top = top[score[top] > 0]

    st.markdown('**Rekomendasi untuknya**')
    if len(top) == 0:
        st.info('Belum ada sinyal kemiripan untuk pembaca ini.')
    else:
        e = r_u - (MU + BU[u] + BI[items_u])
        preds = []
        for j in top:
            sj, ej = S_pred[j, items_u], e
            if len(sj) > k:
                idx = np.argpartition(-sj, k - 1)[:k]
                sj, ej = sj[idx], ej[idx]
            pos = sj > 0
            adj = (sj[pos] * ej[pos]).sum() / (sj[pos].sum() + gamma) if pos.any() else 0.0
            preds.append(float(np.clip(MU + BU[u] + BI[j] + adj, 1, 10)))
        smax = float(score[top].max())
        def alasan(j):
            sj = S_rank[j, items_u]
            o = int(np.argmax(sj))
            if sj[o] <= 0:
                return ''
            t = escape(str(items.at[items_u[o], 'Book-Title']))
            return f"<div class='why'>karena kamu me-rating <b>{t}</b> ({r_u[o]:.0f})</div>"
        shelf(top, [meter(float(score[j]), smax, f'prediksi rating {p:.1f}') + alasan(j) for j, p in zip(top, preds)])
        hasil = pd.DataFrame({'Peringkat': range(1, len(top) + 1),
                              'Judul': [items.at[j, 'Book-Title'] for j in top],
                              'Penulis': [items.at[j, 'Book-Author'] for j in top],
                              'Skor kemiripan': [round(float(score[j]), 3) for j in top],
                              'Prediksi rating': [round(p, 2) for p in preds]})
        st.download_button('Unduh rekomendasi (CSV)', hasil.to_csv(index=False).encode('utf-8'),
                           file_name=f'rekomendasi_user_{users.at[u, "User-ID"]}.csv', mime='text/csv')
        with st.expander('Lihat angka lengkap'):
            st.dataframe(pd.DataFrame({'Judul': [LABELS[j] for j in top],
                                       'Skor kemiripan': [round(float(score[j]), 3) for j in top],
                                       'Prediksi rating': [round(p, 2) for p in preds]}), hide_index=True)

# ---------- Tab 4: evaluasi ----------
with tab4:
    st.subheader('Evaluasi (leave-one-out: 1 rating per user disisihkan)')
    st.markdown('**Prediksi rating**')
    st.dataframe(pd.DataFrame({
        'Model': ['Rata-rata global', 'Rata-rata user', 'Bias (μ + b_u + b_i)', 'Bias + item-based CF'],
        'RMSE': [1.8171, 1.7757, 1.6357, 1.6087],
        'MAE': [1.4139, 1.3293, 1.2718, 1.2355]}), hide_index=True)
    st.markdown('**Ranking Top-N**')
    st.dataframe(pd.DataFrame({
        'Model': ['Popularitas', 'Item-based CF'],
        'HR@10': [0.0352, 0.2015], 'HR@20': [0.0566, 0.2288]}), hide_index=True)
    st.markdown('**Rumus**')
    st.latex(r'\mathrm{sim}(i,j)=\frac{\sum_{u\in U_{ij}}(r_{ui}-\bar r_u)(r_{uj}-\bar r_u)}'
             r'{\sqrt{\sum_{u\in U_{ij}}(r_{ui}-\bar r_u)^2}\sqrt{\sum_{u\in U_{ij}}(r_{uj}-\bar r_u)^2}}')
    st.latex(r'\mathrm{sim}^{*}(i,j)=\frac{|U_{ij}|}{|U_{ij}|+\lambda}\,\mathrm{sim}(i,j)')
    st.latex(r'\hat r_{ui}=b_{ui}+\frac{\sum_{j\in N_k(i;u)}\mathrm{sim}^{*}(i,j)\,(r_{uj}-b_{uj})}'
             r'{\sum_{j\in N_k(i;u)}|\mathrm{sim}^{*}(i,j)|+\gamma},\qquad b_{ui}=\mu+b_u+b_i')

# ---------- Tab 5: statistik ----------
with tab5:
    render_statistik(ART)

# ---------- Tab 6: tentang model ----------
with tab6:
    st.subheader('Cara kerja dalam tiga langkah')
    st.markdown('**1. Ukur kemiripan antar buku.** Dua buku dianggap mirip kalau pembaca yang sama menilainya sama-sama di atas atau di bawah kebiasaan mereka. Rating tiap pembaca digeser dulu terhadap rata-ratanya sendiri, lalu kemiripan dihitung dengan adjusted cosine.')
    st.latex(r'\mathrm{sim}(i,j)=\frac{\sum_{u\in U_{ij}}(r_{ui}-\bar r_u)(r_{uj}-\bar r_u)}{\sqrt{\sum_{u\in U_{ij}}(r_{ui}-\bar r_u)^2}\sqrt{\sum_{u\in U_{ij}}(r_{uj}-\bar r_u)^2}}')
    st.markdown('**2. Kurangi kemiripan yang rapuh.** Pasangan buku yang hanya dirating oleh sedikit pembaca yang sama bisa tampak sangat mirip karena kebetulan, jadi nilainya disusutkan.')
    st.latex(r'\mathrm{sim}^{*}(i,j)=\frac{|U_{ij}|}{|U_{ij}|+\lambda}\,\mathrm{sim}(i,j)')
    st.markdown('**3. Susun rekomendasi.** Skor sebuah buku untuk seorang pembaca adalah jumlah kemiripannya dengan buku yang sudah dirating pembaca itu. Prediksi rating memakai baseline bias, lalu dikoreksi oleh tetangga terdekat.')
    st.latex(r'\mathrm{score}(u,i)=\sum_{j\in I_u}\max\big(\mathrm{sim}^{*}(i,j),0\big),\qquad \hat r_{ui}=b_{ui}+\frac{\sum_{j\in N_k(i;u)}\mathrm{sim}^{*}(i,j)\,(r_{uj}-b_{uj})}{\sum_{j\in N_k(i;u)}|\mathrm{sim}^{*}(i,j)|+\gamma}')

    st.subheader('Data yang dipakai')
    st.markdown(f'Dataset Book-Crossing yang sudah dibersihkan, lalu difilter: pembaca dengan minimal 3 rating dan buku dengan minimal 10 rating. Hasilnya {m:,} pembaca, {n:,} buku, dan {len(ratings):,} rating, dengan sparsity {1 - len(ratings) / (m * n):.2%}.')

    st.subheader('Keterbatasan')
    st.markdown(
        '- Data sangat jarang terisi. Median pembaca hanya punya beberapa rating, jadi banyak pembaca tidak punya cukup sinyal.\n'
        '- Sekitar 28% pasangan uji tidak punya buku mirip sama sekali, sehingga tidak mungkin masuk daftar rekomendasi.\n'
        '- Hiperparameter dipilih memakai data uji yang sama dengan yang dilaporkan, jadi hasil evaluasi cenderung sedikit optimistis.\n'
        '- Model hanya memakai pola rating. Isi buku, usia, dan lokasi pembaca tidak dipakai.\n'
        '- Cover diambil dari Open Library dan tidak tersedia untuk semua buku. Buku tanpa cover tampil sebagai sampul bertipografi.')


