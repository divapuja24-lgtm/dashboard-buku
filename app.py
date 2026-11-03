import os
import base64
import hashlib
from html import escape
from pathlib import Path

import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(page_title='Rak Buku: rekomendasi item-based CF', page_icon='📚', layout='wide')

HERE = Path(__file__).parent
COVERS = HERE / 'covers'
ART = os.environ.get('ART_DIR', str(HERE / 'app_artifacts'))
TEAL = '#0E7C86'
SPINES = ['#0E7C86', '#7A3E48', '#33572F', '#C0652B', '#3D4C8F', '#6B4E8C', '#2F6B63', '#8A6D1F']

st.markdown('''<style>
@import url('https://fonts.googleapis.com/css2?family=Libre+Caslon+Text:wght@400;700&family=Public+Sans:wght@400;500;600&display=swap');
.stApp, .stApp p, .stApp label, .stApp li {font-family: 'Public Sans', sans-serif;}
.stApp h1, .stApp h2, .stApp h3 {font-family: 'Libre Caslon Text', serif !important; color: #17313B;}
.block-container {padding-top: 1.2rem; max-width: 1200px;}
[data-testid="stMetric"] {background: #fff; border-left: 5px solid #0E7C86; padding: 12px 16px; border-radius: 4px;}
.hero {display: flex; align-items: flex-end; justify-content: space-between; gap: 24px; background: #0B3C49; border-radius: 10px 10px 0 0; padding: 0 40px; margin-bottom: 28px; overflow: hidden; border-bottom: 12px solid #A8703F;}
.hero-text {padding: 38px 0;}
.hero h1 {color: #fff !important; font-size: 2.2rem !important; line-height: 1.2 !important; margin: 0 0 12px 0 !important; padding: 0 !important; max-width: 560px;}
.hero p {color: #CFE3E7; max-width: 520px; font-size: 1rem; line-height: 1.55; margin: 0;}
.fan {position: relative; width: 370px; height: 236px; flex: 0 0 370px;}
.fan img {position: absolute; bottom: 0; height: 200px; width: 134px; object-fit: cover; border-radius: 3px 6px 6px 3px; box-shadow: 4px 6px 14px rgba(0,0,0,.45);}
.shelf {display: flex; gap: 22px; align-items: flex-start; overflow-x: auto; padding: 18px 14px 12px 14px; margin: 8px 0 26px 0;}
.book {flex: 0 0 auto; width: 132px;}
.wrap {position: relative;}
.wrap::after {content: ''; position: absolute; left: -11px; right: -11px; bottom: -9px; height: 9px; background: linear-gradient(#B98050, #8A5A30); border-radius: 0 0 2px 2px;}
.cv {width: 132px; height: 196px; object-fit: cover; display: block; border-radius: 3px 6px 6px 3px; box-shadow: -3px 0 0 rgba(0,0,0,.18), 4px 6px 12px rgba(0,0,0,.25);}
.nocv {display: flex; align-items: center; justify-content: center; padding: 12px; box-sizing: border-box; color: #fff; font-family: 'Libre Caslon Text', serif; font-size: .85rem; text-align: center; line-height: 1.25;}
.nocv span {display: -webkit-box; -webkit-line-clamp: 6; -webkit-box-orient: vertical; overflow: hidden;}
.rk {position: absolute; top: -9px; left: -9px; z-index: 2; background: #F2B134; color: #17313B; font-weight: 600; width: 26px; height: 26px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: .8rem; box-shadow: 0 2px 4px rgba(0,0,0,.25);}
.bt {font-weight: 600; font-size: .82rem; margin-top: 20px; line-height: 1.25; color: #17313B; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;}
.ba {font-size: .75rem; color: #4B6470; margin-top: 2px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;}
.meter {height: 5px; background: #CFDCE0; border-radius: 3px; margin-top: 8px; overflow: hidden;}
.meter i {display: block; height: 100%; background: #0E7C86;}
.bm {font-size: .72rem; color: #4B6470; margin-top: 4px;}
@media (max-width: 800px) {.fan {display: none;} .hero {padding: 0 20px;}}
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
        out.append('<div class="book"><div class="wrap">' + cover_html(j) + f'<span class="rk">{r}</span></div>'
                   + f'<div class="bt">{judul}</div><div class="ba">{penulis}</div>' + meta + '</div>')
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
st.sidebar.header('Parameter model')
lam_rank = st.sidebar.slider('λ shrinkage (ranking)', 0, 100, 50, 5)
lam_pred = st.sidebar.slider('λ shrinkage (prediksi rating)', 0, 100, 10, 5)
k = st.sidebar.slider('k tetangga terdekat', 5, 50, 20, 5)
gamma = st.sidebar.slider('γ peredam', 0.0, 2.0, 0.5, 0.25)
S_rank, S_pred = shrunk(lam_rank), shrunk(lam_pred)

tab1, tab2, tab3, tab4 = st.tabs(['Ringkasan data', 'Buku mirip', 'Rekomendasi user', 'Evaluasi'])

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
             .properties(height=260))
    st.altair_chart(chart, use_container_width=True)

# ---------- Tab 2: buku mirip ----------
with tab2:
    st.subheader('Pilih sebuah buku, lihat buku yang mirip')
    i = st.selectbox('Pilih buku', range(n), format_func=lambda x: LABELS[x])
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
        shelf(top, [meter(float(score[j]), smax, f'prediksi rating {p:.1f}') for j, p in zip(top, preds)])
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
