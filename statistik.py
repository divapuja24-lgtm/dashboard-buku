import json
from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st

TEAL = '#0E7C86'


def _csv(d, name):
    f = d / name
    return pd.read_csv(f) if f.exists() else None


def _fmt_p(p):
    return '< 1e-300' if p == 0 else f'{p:.2e}'


def bar(df, cat, val, t_cat, t_val, urut=None, horizontal=False, height=280):
    base = alt.Chart(df).mark_bar(color=TEAL)
    if horizontal:
        ch = base.encode(y=alt.Y(f'{cat}:N', sort='-x' if urut is None else urut, title=t_cat),
                         x=alt.X(f'{val}:Q', title=t_val), tooltip=[cat, val])
    else:
        ch = base.encode(x=alt.X(f'{cat}:N', sort=urut, title=t_cat),
                         y=alt.Y(f'{val}:Q', title=t_val), tooltip=[cat, val])
    st.altair_chart(ch.properties(height=height), use_container_width=True)


def render(art):
    d = Path(art) / 'stats'
    sf = d / 'summary.json'
    if not sf.exists():
        st.info('Berkas statistik belum ada. Jalankan langkah S1 di Colab, lalu unggah folder app_artifacts/stats.')
        return
    S = json.loads(sf.read_text())
    st.caption('Statistik di tab ini dihitung dari seluruh data cleaned (sebelum filter untuk model), '
               'kecuali tabel mentah vs cleaned.')

    t1, t2, t3, t4, t5 = st.tabs(['Rating', 'Pengguna', 'Buku', 'Uji statistik', 'Data mentah vs cleaned'])

    # ---------- Rating ----------
    with t1:
        r = S['rating']
        c = st.columns(5)
        c[0].metric('Jumlah rating', f"{r['n']:,}")
        c[1].metric('Rata-rata', f"{r['mean']:.2f}")
        c[2].metric('Median', f"{r['median']:.1f}")
        c[3].metric('Simpangan baku', f"{r['std']:.2f}")
        c[4].metric('Skewness', f"{r['skew']:.2f}")
        arah = 'menumpuk di nilai tinggi' if r['skew'] < 0 else 'menumpuk di nilai rendah'
        st.caption(f"Kurtosis berlebih {r['kurtosis_excess']:.2f}, Q1 {r['q1']:.1f}, Q3 {r['q3']:.1f}. "
                   f"Skewness {r['skew']:.2f} berarti rating cenderung {arah}.")
        df = _csv(d, 'rating_dist.csv')
        if df is not None:
            st.subheader('Distribusi rating')
            bar(df, 'rating', 'jumlah', 'Nilai rating', 'Jumlah', urut=list(df['rating']))
        st.latex(r'g_1=\frac{\frac1n\sum_i(x_i-\bar x)^3}{\left(\frac1n\sum_i(x_i-\bar x)^2\right)^{3/2}},\qquad '
                 r'g_2=\frac{\frac1n\sum_i(x_i-\bar x)^4}{\left(\frac1n\sum_i(x_i-\bar x)^2\right)^{2}}-3')

    # ---------- Pengguna ----------
    with t2:
        u = S['usia']
        c = st.columns(4)
        c[0].metric('User dengan usia terisi', f"{u['n_terisi']:,}")
        c[1].metric('Rata-rata usia', f"{u['mean']:.1f}")
        c[2].metric('Median usia', f"{u['median']:.0f}")
        c[3].metric('Simpangan baku usia', f"{u['std']:.1f}")
        left, right = st.columns(2)
        with left:
            df = _csv(d, 'age_dist.csv')
            if df is not None:
                st.subheader('Sebaran kelompok usia')
                bar(df, 'kelompok_usia', 'jumlah', 'Kelompok usia', 'Jumlah user', urut=list(df['kelompok_usia']))
        with right:
            df = _csv(d, 'country_dist.csv')
            if df is not None:
                st.subheader('15 negara terbanyak')
                bar(df, 'negara', 'jumlah', 'Negara', 'Jumlah user', horizontal=True)
        df = _csv(d, 'user_activity.csv')
        a = S['aktivitas_user']
        if df is not None:
            st.subheader('Aktivitas user: jumlah rating per user')
            bar(df, 'kelompok', 'jumlah', 'Jumlah rating yang diberikan', 'Jumlah user', urut=list(df['kelompok']))
            st.caption(f"Rata-rata {a['mean']:.1f} rating per user, median {a['median']:.0f}, "
                       f"persentil ke-90 {a['p90']:.0f}, maksimum {a['max']:,}. "
                       'Rata-rata jauh di atas median menandakan distribusi long tail: '
                       'sedikit user sangat aktif, sebagian besar hanya me-rating sedikit buku.')
        left, right = st.columns(2)
        with left:
            df = _csv(d, 'rating_by_age.csv')
            if df is not None:
                st.subheader('Rata-rata rating per kelompok usia')
                st.dataframe(df, hide_index=True)
        with right:
            df = _csv(d, 'rating_by_country.csv')
            if df is not None:
                st.subheader('Rata-rata rating per negara')
                st.dataframe(df.sort_values('rata2', ascending=False), hide_index=True)

    # ---------- Buku ----------
    with t3:
        p = S['popularitas_buku']
        df = _csv(d, 'book_popularity.csv')
        if df is not None:
            st.subheader('Popularitas buku: jumlah rating per buku')
            bar(df, 'kelompok', 'jumlah', 'Jumlah rating yang diterima', 'Jumlah buku', urut=list(df['kelompok']))
            st.caption(f"Rata-rata {p['mean']:.1f} rating per buku, median {p['median']:.0f}, "
                       f"persentil ke-90 {p['p90']:.0f}, maksimum {p['max']:,}.")
        df = _csv(d, 'top_books.csv')
        if df is not None:
            st.subheader('20 buku paling banyak di-rating')
            st.dataframe(df.rename(columns={'n': 'jumlah rating', 'rata2': 'rata-rata rating'}), hide_index=True)
        left, right = st.columns(2)
        with left:
            df = _csv(d, 'top_authors.csv')
            if df is not None:
                st.subheader('Penulis teratas')
                st.dataframe(df, hide_index=True)
        with right:
            df = _csv(d, 'top_publishers.csv')
            if df is not None:
                st.subheader('Penerbit teratas')
                st.dataframe(df, hide_index=True)
        df = _csv(d, 'pub_year.csv')
        if df is not None:
            st.subheader('Buku menurut dekade terbit')
            bar(df, 'dekade', 'jumlah', 'Dekade', 'Jumlah buku', urut=list(df['dekade']))

    # ---------- Uji statistik ----------
    with t4:
        j = S['uji']
        st.subheader('1. Korelasi Spearman: jumlah rating dan rata-rata rating buku')
        st.markdown('H0: tidak ada hubungan monoton antara popularitas buku (jumlah rating) dan rata-rata ratingnya.')
        st.latex(r'\rho = 1-\frac{6\sum_{i=1}^{n}d_i^2}{n(n^2-1)}')
        rho = j['spearman_rho']
        kuat = ('sangat lemah' if abs(rho) < 0.1 else 'lemah' if abs(rho) < 0.3
                else 'sedang' if abs(rho) < 0.5 else 'kuat')
        arah = 'positif' if rho > 0 else 'negatif'
        c = st.columns(3)
        c[0].metric('ρ Spearman', f'{rho:.3f}')
        c[1].metric('Nilai-p', _fmt_p(j['spearman_p']))
        c[2].metric('n buku', f"{j['spearman_n']:,}")
        st.markdown(f"Hubungan {arah} dan **{kuat}**. "
                    + ('H0 ditolak pada α = 0,05.' if j['spearman_p'] < 0.05 else 'H0 tidak ditolak pada α = 0,05.'))

        st.subheader('2. Uji Kruskal-Wallis: rating antar kelompok usia')
        st.markdown('H0: distribusi rating sama di semua kelompok usia.')
        st.latex(r'H=\frac{12}{N(N+1)}\sum_{j=1}^{k}\frac{R_j^2}{n_j}-3(N+1),\qquad '
                 r'\varepsilon^2=\frac{H}{N-1}')
        e2 = j['epsilon2']
        efek = ('sangat kecil' if e2 < 0.01 else 'kecil' if e2 < 0.06 else 'sedang' if e2 < 0.14 else 'besar')
        c = st.columns(4)
        c[0].metric('H', f"{j['kruskal_H']:.2f}")
        c[1].metric('Derajat bebas', f"{j['kruskal_k'] - 1}")
        c[2].metric('Nilai-p', _fmt_p(j['kruskal_p']))
        c[3].metric('ε²', f'{e2:.4f}')
        st.markdown(f"N = {j['kruskal_n']:,}. "
                    + ('H0 ditolak pada α = 0,05. ' if j['kruskal_p'] < 0.05 else 'H0 tidak ditolak pada α = 0,05. ')
                    + f'Ukuran efek **{efek}** (pegangan kasar). '
                    'Dengan N sebesar ini, perbedaan yang sangat kecil pun bisa signifikan, '
                    'jadi ukuran efek lebih menentukan daripada nilai-p.')

    # ---------- Mentah vs cleaned ----------
    with t5:
        raw, cl = S['raw'], S['cleaned']
        st.subheader('Jumlah data sebelum dan sesudah cleaning')
        st.dataframe(pd.DataFrame({
            'Tabel': ['Rating', 'Buku', 'Pengguna'],
            'Mentah': [raw['ratings'], raw['books'], raw['users']],
            'Cleaned': [cl['ratings'], cl['books'], cl['users']]}), hide_index=True)
        c = st.columns(3)
        c[0].metric('Interaksi implisit (rating 0, mentah)', f"{raw['implicit_0']:,}")
        c[1].metric('Interaksi eksplisit (mentah)', f"{raw['explicit']:,}")
        c[2].metric('Rentang rating cleaned', f"{cl['rating_min']:.0f} sampai {cl['rating_max']:.0f}")
        st.caption('Model rekomendasi hanya memakai rating eksplisit.')
        df = _csv(d, 'missing.csv')
        if df is not None:
            st.subheader('Missing value per kolom')
            st.dataframe(df, hide_index=True)
