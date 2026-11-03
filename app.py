# =====================================================================
# DASHBOARD HARGA CABAI RAWIT KABUPATEN BANYUMAS
# Halaman 1 - Beranda: insight harga (pertanyaan -> insight -> rekomendasi)
# Halaman 2 - Prediksi: simulasi model pada periode uji 18 Agu - 31 Des 2025
#
# File yang dibutuhkan (satu folder dengan app.py):
#   data/dinperindag_2023-2025_clean.xlsx
#   model_r2/  (hasil STEP 15 notebook REVISI 2)
# =====================================================================
import html
import json
import os
import warnings

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

warnings.filterwarnings('ignore')
st.set_page_config(page_title="Harga Cabai Rawit Banyumas", layout="wide", initial_sidebar_state="expanded")

# ─────────────────────────────────────────────────────────────────────
# GAYA TAMPILAN (latar terang dikunci agar tetap terbaca di tema Dark)
# ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
:root { --ink:#111827; --sub:#6B7280; --line:#E5E7EB; --bg:#F8FAFC; --card:#FFFFFF;
        --navy:#1E3A5F; --blue:#2563EB; --red:#DC2626; --green:#16A34A; --amber:#D97706; }
.stApp { background: var(--bg); color-scheme: light; }
[data-testid="stMain"], section.main { color: var(--ink); }
[data-testid="stMain"] [data-testid="stMarkdownContainer"],
[data-testid="stMain"] [data-testid="stMarkdownContainer"] p,
[data-testid="stMain"] [data-testid="stMarkdownContainer"] li,
[data-testid="stMain"] [data-testid="stMarkdownContainer"] b,
[data-testid="stMain"] [data-testid="stMarkdownContainer"] strong,
[data-testid="stMain"] [data-testid="stWidgetLabel"] p,
[data-testid="stMain"] label, [data-testid="stMain"] h1, [data-testid="stMain"] h2,
[data-testid="stMain"] h3 { color: var(--ink) !important; }
[data-testid="stMain"] [data-testid="stCaptionContainer"],
[data-testid="stMain"] [data-testid="stCaptionContainer"] p { color: var(--sub) !important; }
[data-testid="stSidebar"] { background: #1E293B; }
[data-testid="stSidebar"] * { color: #E2E8F0 !important; }
.main .block-container { padding-top: 1.6rem; max-width: 1250px; }

.judul { border-bottom: 1px solid var(--line); padding-bottom: .7rem; margin-bottom: 1rem; }
.judul h1 { font-size: 1.55rem; margin: 0; color: var(--ink) !important; }
.judul p { margin: .25rem 0 0; color: var(--sub) !important; font-size: .92rem; }

.bagian { margin: 2.1rem 0 .6rem; }
.bagian .no { display:inline-block; background: var(--navy); color:#fff !important; border-radius: 6px;
              padding: 1px 9px; font-size: .8rem; font-weight: 700; margin-right: .5rem; }
.bagian .jd { font-size: 1.15rem; font-weight: 700; color: var(--ink); }
.bagian .q  { color: var(--sub) !important; font-style: italic; margin-top: .2rem; font-size: .95rem; }

.kartu { background: var(--card); border: 1px solid var(--line); border-radius: 12px; padding: .9rem 1rem;
         min-height: 112px; }
.kartu .lb { font-size: .78rem; color: var(--sub) !important; }
.kartu .vl { font-size: 1.45rem; font-weight: 800; color: var(--ink) !important; margin: .15rem 0; }
.kartu .ds { font-size: .8rem; color: var(--sub) !important; }
.naik { color: var(--red) !important; font-weight: 700; }
.turun { color: var(--green) !important; font-weight: 700; }

.status { border-radius: 12px; padding: .9rem 1rem; min-height: 112px; border: 1px solid var(--line); }
.status .lb { font-size: .78rem; color: var(--sub) !important; }
.status .vl { font-size: 1.35rem; font-weight: 800; margin: .15rem 0; }
.st-normal { background: #F0FDF4; } .st-normal .vl { color: var(--green) !important; }
.st-waspada { background: #FFFBEB; } .st-waspada .vl { color: var(--amber) !important; }
.st-siaga { background: #FEF2F2; } .st-siaga .vl { color: var(--red) !important; }
.status .ds { font-size: .8rem; color: var(--ink) !important; }

.insight, .rekom, .info { border-radius: 10px; padding: .85rem 1.05rem; margin: .45rem 0; font-size: .92rem;
                          line-height: 1.6; color: var(--ink) !important; }
.insight { background: #EFF6FF; border-left: 4px solid var(--blue); }
.rekom   { background: #F0FDF4; border-left: 4px solid var(--green); }
.info    { background: #FFFBEB; border-left: 4px solid var(--amber); }
.insight .t, .rekom .t, .info .t { font-weight: 800; font-size: .8rem; letter-spacing: .4px; display:block;
                                   margin-bottom: .15rem; }
.insight .t { color: var(--blue) !important; } .rekom .t { color: var(--green) !important; }
.info .t { color: var(--amber) !important; }
.insight b, .rekom b, .info b { color: var(--ink) !important; }
.ringkas { background: var(--card); border: 1px solid var(--line); border-radius: 12px; padding: .9rem 1.1rem;
           margin-top: .7rem; }
.ringkas ul { padding-left: 1.7rem !important; margin: .45rem 0 .1rem !important; }
.ringkas li { margin: .3rem 0; padding-left: .25rem; }
.subjudul { margin: 2.2rem 0 .6rem; padding-top: 1.1rem; border-top: 1px solid var(--line);
            font-weight: 700; font-size: 1rem; color: var(--ink) !important; }
.subjudul.pertama { margin-top: .4rem; padding-top: 0; border-top: none; }
.tbl { overflow: auto; border: 1px solid var(--line); border-radius: 10px; background: var(--card);
       margin: .3rem 0 .9rem; }
.tbl table { border-collapse: collapse !important; width: 100%; font-size: .85rem; margin: 0 !important; }
.tbl th { position: sticky; top: 0; background: #F1F5F9 !important; color: var(--ink) !important; text-align: left;
          padding: .5rem .75rem !important; border: none !important; border-bottom: 1px solid var(--line) !important;
          font-weight: 700; }
.tbl td { padding: .42rem .75rem !important; border: none !important; border-bottom: 1px solid #F1F5F9 !important;
          color: var(--ink) !important; background: var(--card) !important; }
.tbl th.n, .tbl td.n { text-align: right; white-space: nowrap; font-variant-numeric: tabular-nums; }
.tbl tr:last-child td { border-bottom: none !important; }
[data-testid="stExpander"] { background: var(--card); border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────
# FUNGSI BANTU
# ─────────────────────────────────────────────────────────────────────
BLN = ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des']
BLN_P = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober',
         'November', 'Desember']


def rp(v):
    return "Rp" + f"{int(round(v)):,}".replace(',', '.')


def pct(v, d=1, tanda=False):
    s = f"{v:+.{d}f}%" if tanda else f"{v:.{d}f}%"
    return s.replace('.', ',')


def tgl(d):
    d = pd.Timestamp(d)
    return f"{d.day} {BLN[d.month - 1]} {d.year}"


def nama(p):
    return str(p).title()


def arah(v, d=1):
    """Persen dengan warna: merah = naik (harga naik buruk bagi konsumen), hijau = turun."""
    cls = 'naik' if v > 0 else 'turun'
    return f'<span class="{cls}">{pct(v, d, True)}</span>'


def bagian(no, judul, pertanyaan):
    st.markdown(f'<div class="bagian"><span class="no">{no}</span><span class="jd">{judul}</span>'
                f'<div class="q">Pertanyaan: {pertanyaan}</div></div>', unsafe_allow_html=True)


def kotak(jenis, isi):
    label = {'insight': 'INSIGHT', 'rekom': 'REKOMENDASI', 'info': 'CATATAN'}[jenis]
    st.markdown(f'<div class="{jenis}"><span class="t">{label}</span>{isi}</div>', unsafe_allow_html=True)


def subjudul(teks, pertama=False):
    st.markdown(f'<div class="subjudul{" pertama" if pertama else ""}">{teks}</div>', unsafe_allow_html=True)


def kartu(label, nilai, ket):
    return f'<div class="kartu"><div class="lb">{label}</div><div class="vl">{nilai}</div><div class="ds">{ket}</div></div>'


def _angka(v, desimal):
    """Angka berformat Indonesia: titik untuk ribuan, koma untuk desimal."""
    if pd.isna(v):
        return '–'
    if isinstance(v, (int, np.integer)):
        desimal = 0
    return f"{v:,.{desimal}f}".replace(',', '_').replace('.', ',').replace('_', '.')


def tabel(df, desimal=0, fmt=None, tinggi=None):
    """Tabel HTML biasa (tanpa komponen tabel interaktif Streamlit) supaya tetap tampil
    walau browser gagal memuat file JavaScript tambahan."""
    fmt = fmt or {}
    angka = {c: (c in fmt or pd.api.types.is_numeric_dtype(df[c])) for c in df.columns}
    th = ''.join(f'<th class="{"n" if angka[c] else ""}">{html.escape(str(c))}</th>' for c in df.columns)
    baris = []
    for r in df.itertuples(index=False):
        sel = []
        for c, v in zip(df.columns, r):
            if c in fmt:
                teks = html.escape(str(fmt[c](v)))
            elif angka[c]:
                teks = _angka(v, desimal)
            else:
                teks = html.escape(str(v))
            sel.append(f'<td class="{"n" if angka[c] else ""}">{teks}</td>')
        baris.append('<tr>' + ''.join(sel) + '</tr>')
    gaya_t = f' style="max-height:{tinggi}px"' if tinggi else ''
    st.markdown(f'<div class="tbl"{gaya_t}><table><thead><tr>{th}</tr></thead><tbody>{"".join(baris)}</tbody></table></div>',
                unsafe_allow_html=True)


def gaya(fig, tinggi=330, **kw):
    fig.update_layout(height=tinggi, plot_bgcolor='#FFFFFF', paper_bgcolor='#FFFFFF',
                      font=dict(color='#111827', size=12), margin=dict(t=30, b=30, l=10, r=10),
                      legend=dict(orientation='h', y=1.12, x=0, font=dict(color='#111827', size=11)),
                      hoverlabel=dict(font_size=12), **kw)
    fig.update_xaxes(tickfont=dict(color='#111827', size=11), gridcolor='rgba(100,116,139,0.15)')
    fig.update_yaxes(tickfont=dict(color='#111827', size=11), gridcolor='rgba(100,116,139,0.15)')
    return fig


def mape(yt, yp):
    yt, yp = np.asarray(yt, float), np.asarray(yp, float)
    m = yt > 500
    return float(np.mean(np.abs((yt[m] - yp[m]) / yt[m])) * 100) if m.any() else float('nan')


def mae(yt, yp):
    return float(np.mean(np.abs(np.asarray(yt, float) - np.asarray(yp, float))))


# ─────────────────────────────────────────────────────────────────────
# DATA
# ─────────────────────────────────────────────────────────────────────
KOLOM = {'Rawit Merah': ('harga_rawit_merah', 'is_observed_merah'),
         'Rawit Hijau': ('harga_rawit_hijau', 'is_observed_hijau')}


@st.cache_data
def muat_data():
    df = pd.read_excel('data/dinperindag_2023-2025_clean.xlsx', sheet_name='cabai_rawit')
    df['tanggal'] = pd.to_datetime(df['tanggal'])
    lokasi = df.groupby('nama_pasar')[['latitude', 'longitude']].first()
    pv = {j: df.pivot_table(index='tanggal', columns='nama_pasar', values=k) for j, (k, _) in KOLOM.items()}
    obs = {j: df.pivot_table(index='tanggal', columns='nama_pasar', values=o) for j, (_, o) in KOLOM.items()}
    return df, lokasi, pv, obs


@st.cache_data
def muat_model():
    D = 'model_r2' if os.path.exists('model_r2') else 'model'
    a = {k: np.load(f'{D}/{k}.npy') for k in ['pred_m_rp', 'pred_h_rp', 'y_m_rp', 'y_h_rp', 'pred_gru_m_rp',
                                               'pred_gru_h_rp', 'pred_persist_m_rp', 'pred_persist_h_rp',
                                               'history_train', 'history_val']}
    a['best_epoch'] = int(np.load(f'{D}/best_epoch.npy')[0])
    if os.path.exists(f'{D}/pred_jarak_m_rp.npy'):
        for k in ['pred_jarak_m_rp', 'pred_jarak_h_rp', 'history_jarak_train', 'history_jarak_val',
                  'best_epoch_jarak']:
            a[k] = np.load(f'{D}/{k}.npy')
    pasar = np.load(f'{D}/daftar_pasar.npy', allow_pickle=True).tolist()
    with open(f'{D}/info_dashboard.json') as f:
        info = json.load(f)
    return a, pasar, info


df, LOKASI, PV, OBS = muat_data()
PASAR = sorted(PV['Rawit Merah'].columns)
TMIN, TMAX = df['tanggal'].min(), df['tanggal'].max()


# ─────────────────────────────────────────────────────────────────────
# LOGIKA INSIGHT
# ─────────────────────────────────────────────────────────────────────
def seri(jenis, pasar):
    """Harga harian: satu pasar, atau rata-rata 14 pasar (harga kabupaten)."""
    p = PV[jenis]
    return p.mean(axis=1) if pasar == 'Semua pasar' else p[pasar]


def status_harga(s, d):
    """Lampu status dari perubahan 30 hari: >=50% Siaga, >=25% Waspada, selain itu Normal."""
    s = s.loc[:d]
    if len(s) < 31:
        return 'Normal', 0.0
    ch = (s.iloc[-1] / s.iloc[-31] - 1) * 100
    return ('Siaga' if ch >= 50 else 'Waspada' if ch >= 25 else 'Normal'), ch


@st.cache_data
def cari_lonjakan(jenis):
    """Peristiwa lonjakan: harga kabupaten naik >50% dalam 30 hari (jeda >60 hari = peristiwa baru).
    Untuk tiap peristiwa, dicatat tanggal tiap pasar mulai naik >30% di atas harga normalnya
    (median 31-60 hari sebelum peristiwa) selama 3 hari berturut-turut."""
    pv = PV[jenis]
    avg = pv.mean(axis=1)
    ch = avg / avg.shift(30) - 1
    awal = []
    for d in ch[ch > 0.5].index:
        if not awal or (d - awal[-1][-1]).days > 60:
            awal.append([d])
        else:
            awal[-1].append(d)
    hasil = []
    for grup in awal:
        c = grup[0]
        base = pv.loc[c - pd.Timedelta(days=60):c - pd.Timedelta(days=31)].median()
        win = pv.loc[c - pd.Timedelta(days=45):c + pd.Timedelta(days=30)]
        mulai = {}
        for p in pv.columns:
            run = (win[p] >= 1.3 * base[p]).astype(int).rolling(3).sum()
            h = run[run >= 3]
            mulai[p] = h.index[0] - pd.Timedelta(days=2) if len(h) else pd.NaT
        s = pd.Series(mulai).sort_values()
        puncak_tgl = avg.loc[c:c + pd.Timedelta(days=45)].idxmax()
        hasil.append(dict(tanggal=c, mulai=s, base=base, puncak=float(avg.loc[puncak_tgl]), puncak_tgl=puncak_tgl,
                          base_avg=float(base.mean())))
    return hasil


# ─────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### Cabai Rawit Banyumas")
    st.caption("Dashboard harga & prediksi")
    page = st.radio("Menu", ["Beranda: Insight Harga", "Prediksi: Simulasi Model"], label_visibility="collapsed")
    st.markdown("---")
    st.markdown(f"""<div style='font-size:.8rem;line-height:1.9'>
    Sumber data: DKUKMP Kab. Banyumas<br>
    Periode data: {tgl(TMIN)} – {tgl(TMAX)}<br>
    Cakupan: 14 pasar tradisional<br>
    Komoditas: Rawit Merah & Hijau</div>""", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<div style='font-size:.72rem;opacity:.7'>© 2026 Fathimah Ella Syarif<br>Sistem Informasi<br>"
                "Telkom University Purwokerto</div>", unsafe_allow_html=True)


# =====================================================================
# HALAMAN 1: BERANDA - INSIGHT HARGA
# =====================================================================
if page == "Beranda: Insight Harga":
    st.markdown('<div class="judul"><h1>Insight Harga Cabai Rawit Kabupaten Banyumas</h1>'
                '<p>Untuk DKUKMP dan TPID: kondisi harga, pasar yang perlu diperhatikan, dan tindak lanjutnya</p>'
                '</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 1.2, 1.6])
    with c1:
        jenis = st.radio("Jenis cabai", list(KOLOM), horizontal=True)
    with c2:
        pasar = st.selectbox("Pasar", ['Semua pasar'] + PASAR, format_func=lambda p: p if p == 'Semua pasar' else nama(p))
    with c3:
        # Pilihan periode cepat (berbahasa Indonesia, dihitung dari tanggal data terakhir, bukan dari hari ini)
        PERIODE = {
            '3 bulan terakhir (Okt–Des 2025)': (TMAX - pd.DateOffset(months=3) + pd.Timedelta(days=1), TMAX),
            '6 bulan terakhir (Jul–Des 2025)': (TMAX - pd.DateOffset(months=6) + pd.Timedelta(days=1), TMAX),
            'Tahun 2025': (pd.Timestamp('2025-01-01'), pd.Timestamp('2025-12-31')),
            'Tahun 2024': (pd.Timestamp('2024-01-01'), pd.Timestamp('2024-12-31')),
            'Tahun 2023': (TMIN, pd.Timestamp('2023-12-31')),
            'Semua data (2023–2025)': (TMIN, TMAX),
            'Pilih tanggal sendiri': None}
        pil = st.selectbox("Periode", list(PERIODE))
    if PERIODE[pil] is None:
        d1, d2 = st.columns(2)
        with d1:
            dari = st.date_input("Dari tanggal", value=pd.Timestamp('2025-10-01').date(),
                                 min_value=TMIN.date(), max_value=TMAX.date(), format="DD/MM/YYYY")
        with d2:
            sampai = st.date_input("Sampai tanggal", value=TMAX.date(),
                                   min_value=TMIN.date(), max_value=TMAX.date(), format="DD/MM/YYYY")
        if sampai < dari:
            st.info("Tanggal akhir harus sesudah tanggal awal.")
            st.stop()
        A, B = pd.Timestamp(dari), pd.Timestamp(sampai)
    else:
        A, B = PERIODE[pil]
    if (B - A).days < 6:
        st.info("Pilih periode minimal 7 hari agar perubahan harga bisa dibaca.")
        st.stop()
    nama_p = 'harga rata-rata 14 pasar' if pasar == 'Semua pasar' else f'Pasar {nama(pasar)}'
    lama = (B - A).days + 1
    A0, B0 = A - pd.Timedelta(days=lama), A - pd.Timedelta(days=1)
    ada_sebelum = A0 >= TMIN

    S = seri(jenis, pasar)                       # harga harian pasar terpilih / rata-rata kabupaten
    Sp = S.loc[A:B]
    pv_p = PV[jenis].loc[A:B]                    # semua pasar dalam periode
    rata_pasar = pv_p.mean().sort_values(ascending=False)
    status, ch30 = status_harga(S, B)

    # ── 0. RINGKASAN ─────────────────────────────────────────────────
    bagian("0", "Ringkasan", f"Bagaimana kondisi harga {jenis} ({nama_p}) per {tgl(B)}, dan perlu tindakan apa?")
    k = st.columns(5)
    akhir = float(Sp.iloc[-1])
    k[0].markdown(kartu(f"Harga per {tgl(B)}", rp(akhir) + "/kg", nama_p), unsafe_allow_html=True)
    if ada_sebelum:
        rt, rt0 = Sp.mean(), S.loc[A0:B0].mean()
        k[1].markdown(kartu("Rata-rata periode", rp(rt), f"{arah((rt / rt0 - 1) * 100)} vs {lama} hari sebelumnya"),
                      unsafe_allow_html=True)
    else:
        k[1].markdown(kartu("Rata-rata periode", rp(Sp.mean()), "tidak ada periode pembanding"), unsafe_allow_html=True)
    idx_max = pv_p.stack().idxmax()
    k[2].markdown(kartu("Harga tertinggi di satu pasar", rp(pv_p.stack().max()),
                        f"{nama(idx_max[1])}, {tgl(idx_max[0])}"), unsafe_allow_html=True)
    k[3].markdown(kartu("Selisih antarpasar (rata-rata periode)", rp(rata_pasar.iloc[0] - rata_pasar.iloc[-1]),
                        f"{nama(rata_pasar.index[0])} vs {nama(rata_pasar.index[-1])}"), unsafe_allow_html=True)
    ket_status = {'Normal': 'kenaikan 30 hari di bawah 25%', 'Waspada': 'naik 25–50% dalam 30 hari',
                  'Siaga': 'naik ≥50% dalam 30 hari'}[status]
    if ch30 <= -25:
        ket_status = 'harga turun tajam dalam 30 hari'
    k[4].markdown(f'<div class="status st-{status.lower()}"><div class="lb">Status per {tgl(B)}</div>'
                  f'<div class="vl">{status.upper()}</div><div class="ds">Perubahan 30 hari {pct(ch30, 1, True)}'
                  f'<br>({ket_status})</div></div>', unsafe_allow_html=True)

    # ringkasan otomatis 3 poin (diisi setelah semua bagian dihitung)
    slot_ringkas = st.empty()

    # ── 1. TREN ─────────────────────────────────────────────────────
    bagian("1", "Tren harga pada periode terpilih",
           "Kapan harga naik dan turun, dan seberapa besar perubahannya?")
    q25, q75 = S.quantile(0.25), S.quantile(0.75)
    f1 = go.Figure()
    f1.add_trace(go.Scatter(x=[Sp.index[0], Sp.index[-1], Sp.index[-1], Sp.index[0]], y=[q25, q25, q75, q75],
                            fill='toself', fillcolor='rgba(148,163,184,0.18)', line=dict(width=0),
                            name='Rentang harga biasa (2023–2025)', hoverinfo='skip'))
    f1.add_trace(go.Scatter(x=Sp.index, y=Sp.values, name=f'{jenis}, {nama_p}',
                            line=dict(color='#DC2626' if jenis == 'Rawit Merah' else '#16A34A', width=2.4),
                            hovertemplate='%{x|%d %b %Y}<br>Rp %{y:,.0f}<extra></extra>'))
    tp, tl = Sp.idxmax(), Sp.idxmin()
    f1.add_trace(go.Scatter(x=[tp, tl], y=[Sp.max(), Sp.min()], mode='markers+text',
                            text=[f"Puncak {rp(Sp.max())}", f"Terendah {rp(Sp.min())}"],
                            textposition=['top center', 'bottom center'], marker=dict(size=9, color='#111827'),
                            showlegend=False, hoverinfo='skip'))
    gaya(f1, 340, yaxis_tickprefix='Rp ', yaxis_tickformat=',.0f')
    st.plotly_chart(f1, use_container_width=True)

    awal = float(Sp.iloc[0])
    c7 = (Sp / S.shift(7).loc[A:B] - 1) * 100
    t7 = c7.idxmax() if c7.notna().any() else None
    teks = (f"{jenis} {nama_p} bergerak dari <b>{rp(awal)}</b> ({tgl(A)}) menjadi <b>{rp(akhir)}</b> ({tgl(B)}), "
            f"atau {arah((akhir / awal - 1) * 100)} (<b>{'+' if akhir >= awal else '−'}{rp(abs(akhir - awal))}</b>/kg). ")
    ada_puncak = tp != Sp.index[0] and Sp.max() > akhir * 1.02
    if ada_puncak:
        teks += (f"Puncaknya <b>{rp(Sp.max())}</b> pada {tgl(tp)} ({arah((Sp.max() / awal - 1) * 100)} dari awal periode), "
                 f"lalu turun <span class='turun'>{pct(abs(akhir / Sp.max() - 1) * 100)}</span> sampai akhir periode. ")
    if t7 is not None and c7.max() > 10:
        teks += (f"Kenaikan tercepat terjadi pada 7 hari menjelang {tgl(t7)}: {arah(c7.max())} "
                 f"(dari {rp(S.loc[t7 - pd.Timedelta(days=7)])} ke {rp(S.loc[t7])}). ")
    if akhir > q75:
        teks += f"Harga akhir periode <b>di atas rentang biasa</b> 2023–2025 ({rp(q25)}–{rp(q75)})."
    elif akhir < q25:
        teks += f"Harga akhir periode <b>di bawah rentang biasa</b> 2023–2025 ({rp(q25)}–{rp(q75)})."
    else:
        teks += f"Harga akhir periode masih <b>dalam rentang biasa</b> 2023–2025 ({rp(q25)}–{rp(q75)})."
    kotak('insight', teks)
    ch14 = (akhir / float(S.loc[:B].iloc[-15]) - 1) * 100 if len(S.loc[:B]) > 15 else 0
    if status == 'Siaga':
        rek = ("Harga naik sangat cepat. <b>Siapkan operasi pasar / pasar murah</b> dan koordinasi pasokan dalam "
               "1–2 minggu ke depan, mulai dari pasar termahal di Bagian 3.")
    elif status == 'Waspada':
        rek = ("Harga mulai naik tajam. <b>Tingkatkan pemantauan menjadi harian</b> dan siapkan rencana operasi "
               "pasar bila kenaikan berlanjut melewati 50% dalam 30 hari.")
    elif (akhir / awal - 1) * 100 <= -25 and not (ada_puncak and akhir < Sp.max() * 0.8 and Sp.max() > awal * 1.1):
        rek = ("Harga turun tajam. Konsumen diuntungkan, tetapi <b>perhatikan dampaknya bagi petani dan pedagang</b>"
               + (f", terutama karena harga sudah di bawah rentang biasa ({rp(q25)})" if akhir < q25 else "")
               + ". Koordinasikan dengan dinas terkait bila penurunan berlanjut.")
    elif ada_puncak and akhir < Sp.max() * 0.8:
        rek = ("Harga sudah turun dari puncaknya. Intervensi dapat <b>dikurangi bertahap</b>, tetapi pemantauan tetap "
               f"dijalankan sampai harga kembali ke rentang biasa (di bawah {rp(q75)}).")
    elif ch14 > 10:
        rek = "Harga cenderung naik dalam 2 minggu terakhir. <b>Pantau lebih rapat</b> pasar-pasar di Bagian 5."
    else:
        rek = "Kondisi relatif stabil. <b>Pemantauan rutin</b> sudah cukup."
    kotak('rekom', rek)

    # ── 2. POLA TAHUNAN ─────────────────────────────────────────────
    bagian("2", "Pola harga bulanan antar tahun",
           "Apakah lonjakan harga selalu terjadi di bulan yang sama setiap tahun?")
    bul = S.groupby([S.index.year, S.index.month]).mean().unstack(0)
    f2 = go.Figure()
    for th, w, ds in [(2023, '#94A3B8', 'dash'), (2024, '#F59E0B', 'solid'), (2025, '#2563EB', 'solid')]:
        if th in bul.columns:
            f2.add_trace(go.Scatter(x=[BLN[m - 1] for m in bul.index], y=bul[th], name=str(th), mode='lines+markers',
                                    line=dict(color=w, width=2.6, dash=ds), marker=dict(size=7),
                                    hovertemplate='%{x} ' + str(th) + '<br>Rp %{y:,.0f}<extra></extra>'))
    gaya(f2, 320, yaxis_tickprefix='Rp ', yaxis_tickformat=',.0f')
    st.plotly_chart(f2, use_container_width=True)
    puncak = {th: (int(bul[th].idxmax()), float(bul[th].max())) for th in bul.columns}
    tahunan = S.groupby(S.index.year).mean()
    teks = "Bulan dengan harga rata-rata tertinggi: " + "; ".join(
        f"<b>{BLN_P[m - 1]} {th}</b> ({rp(v)})" for th, (m, v) in puncak.items()) + ". "
    bulan_beda = len({m for m, _ in puncak.values()}) > 1
    teks += ("Puncak harga <b>tidak jatuh di bulan yang sama</b> setiap tahun. " if bulan_beda
             else "Puncak harga jatuh di bulan yang sama setiap tahun. ")
    if 2024 in tahunan and 2025 in tahunan:
        teks += (f"Rata-rata 2025 {rp(tahunan[2025])}, {arah((tahunan[2025] / tahunan[2024] - 1) * 100)} "
                 f"dibanding 2024 ({rp(tahunan[2024])}).")
    kotak('insight', teks)
    kotak('rekom', ("Karena waktu lonjakan berpindah-pindah, <b>jangan hanya bersiaga pada bulan tertentu</b>. "
                    "Gunakan sinyal kenaikan di Bagian 5 sebagai pemicu persiapan operasi pasar, dan sediakan cadangan "
                    "anggaran yang bisa digunakan kapan saja dalam setahun." if bulan_beda else
                    "Siapkan operasi pasar menjelang bulan puncak yang berulang."))

    # ── 3. DI MANA MAHAL ────────────────────────────────────────────
    bagian("3", "Peta dan peringkat harga antarpasar",
           f"Pasar dan wilayah mana yang termahal pada {tgl(A)} – {tgl(B)}, dan berapa selisihnya?")
    loc = LOKASI.loc[rata_pasar.index]
    cm, cb = st.columns([1.15, 1])
    with cm:
        Map = getattr(go, 'Scattermap', None)
        trace_kw = dict(lat=loc['latitude'], lon=loc['longitude'], mode='markers+text',
                        text=[nama(p) for p in rata_pasar.index], textposition='top center',
                        customdata=np.stack([rata_pasar.values], axis=1),
                        hovertemplate='<b>%{text}</b><br>Rata-rata Rp %{customdata[0]:,.0f}<extra></extra>')
        mk = dict(size=17, color=rata_pasar.values, colorscale='YlOrRd', showscale=True,
                  colorbar=dict(title='Rp/kg', tickformat=',.0f', len=.8))
        if Map is not None:
            f3 = go.Figure(Map(marker=mk, **trace_kw))
            f3.update_layout(map=dict(style='open-street-map', zoom=9.4,
                                      center=dict(lat=float(loc['latitude'].mean()), lon=float(loc['longitude'].mean()))))
        else:
            f3 = go.Figure(go.Scattermapbox(marker=mk, **trace_kw))
            f3.update_layout(mapbox=dict(style='open-street-map', zoom=9.4,
                                         center=dict(lat=float(loc['latitude'].mean()), lon=float(loc['longitude'].mean()))))
        f3.update_layout(height=430, margin=dict(t=5, b=5, l=5, r=5), paper_bgcolor='#FFFFFF')
        st.plotly_chart(f3, use_container_width=True)
    with cb:
        urut = rata_pasar.sort_values()
        warna = ['#DC2626' if p in rata_pasar.index[:3] else ('#16A34A' if p in rata_pasar.index[-3:] else '#94A3B8')
                 for p in urut.index]
        if pasar != 'Semua pasar':
            warna = ['#1E3A5F' if p == pasar else w for p, w in zip(urut.index, warna)]
        f3b = go.Figure(go.Bar(y=[nama(p) for p in urut.index], x=urut.values, orientation='h', marker_color=warna,
                               text=[rp(v) for v in urut.values], textposition='outside',
                               hovertemplate='%{y}<br>Rp %{x:,.0f}<extra></extra>'))
        f3b.add_vline(x=float(urut.mean()), line_dash='dash', line_color='#111827',
                      annotation_text=f'Rata-rata {rp(urut.mean())}', annotation_position='top')
        gaya(f3b, 430, showlegend=False, xaxis_range=[0, float(urut.max()) * 1.25], xaxis_tickformat=',.0f')
        st.plotly_chart(f3b, use_container_width=True)
    top, bot = rata_pasar.index[0], rata_pasar.index[-1]
    sel = rata_pasar.iloc[0] - rata_pasar.iloc[-1]
    teks = (f"Termahal <b>Pasar {nama(top)}</b> ({rp(rata_pasar.iloc[0])}/kg), termurah <b>Pasar {nama(bot)}</b> "
            f"({rp(rata_pasar.iloc[-1])}/kg): selisih <b>{rp(sel)}/kg</b> ({pct(sel / rata_pasar.iloc[-1] * 100)} "
            f"lebih mahal). Tiga pasar termahal: {', '.join(nama(p) for p in rata_pasar.index[:3])}. ")
    r_lon = np.corrcoef(loc['longitude'], rata_pasar.values)[0, 1]
    bt = LOKASI['longitude'].sort_values()
    barat, timur = rata_pasar[bt.index[:2]].mean(), rata_pasar[bt.index[-2:]].mean()
    if abs(r_lon) >= 0.6:
        teks += (f"Ada pola wilayah: <b>makin ke {'timur' if r_lon > 0 else 'barat'} makin mahal</b>. Dua pasar paling "
                 f"timur ({', '.join(nama(p) for p in bt.index[-2:])}) rata-rata {rp(timur)}, dua pasar paling barat "
                 f"({', '.join(nama(p) for p in bt.index[:2])}) {rp(barat)}, selisih {rp(abs(timur - barat))}/kg.")
    else:
        teks += "Pada periode ini tidak terlihat pola wilayah yang jelas (barat–timur)."
    kotak('insight', teks)
    kotak('rekom', (f"<b>Prioritaskan operasi pasar / pasar murah</b> di {', '.join(nama(p) for p in rata_pasar.index[:3])}. "
                    f"Selisih harga yang lebar menunjukkan ada pasar dengan harga lebih rendah (misalnya {nama(bot)}); "
                    "<b>periksa jalur pasokan dan distribusi</b> ke pasar termahal. Data ini hanya berisi harga, sehingga "
                    "penyebab selisih perlu dipastikan lewat pengecekan lapangan."))

    # ── 4. NAIK / TURUN TERBESAR ────────────────────────────────────
    bagian("4", "Perubahan harga per pasar",
           f"Pasar mana yang harganya naik atau turun paling besar dibanding {lama} hari sebelumnya?")
    if not ada_sebelum:
        kotak('info', f"Periode pembanding ({lama} hari sebelum {tgl(A)}) berada di luar data. "
                      "Geser tanggal awal periode agar bagian ini bisa dihitung.")
    else:
        sebelum = PV[jenis].loc[A0:B0].mean()
        sesudah = pv_p.mean()
        ubah = pd.DataFrame({'sebelum': sebelum, 'sesudah': sesudah})
        ubah['rp'] = ubah['sesudah'] - ubah['sebelum']
        ubah['pct'] = ubah['rp'] / ubah['sebelum'] * 100
        satuan = st.radio("Tampilkan perubahan dalam", ["Rupiah", "Persen"], horizontal=True, key='satuan4')
        kol = 'rp' if satuan == 'Rupiah' else 'pct'
        ubah = ubah.sort_values(kol)
        f4 = go.Figure(go.Bar(y=[nama(p) for p in ubah.index], x=ubah[kol], orientation='h',
                              marker_color=['#DC2626' if v > 0 else '#16A34A' for v in ubah[kol]],
                              customdata=np.stack([ubah['sebelum'], ubah['sesudah'], ubah['rp'], ubah['pct']], axis=1),
                              text=[(('+' if v > 0 else '−') + rp(abs(v))) if kol == 'rp' else pct(v, 1, True)
                                    for v in ubah[kol]], textposition='outside',
                              hovertemplate='<b>%{y}</b><br>Sebelum Rp %{customdata[0]:,.0f}<br>Sesudah Rp %{customdata[1]:,.0f}'
                                            '<br>Perubahan Rp %{customdata[2]:,.0f} (%{customdata[3]:.1f}%)<extra></extra>'))
        f4.add_vline(x=0, line_color='#111827')
        lim = float(ubah[kol].abs().max()) * 1.3
        gaya(f4, 430, showlegend=False, xaxis_range=[-lim if ubah[kol].min() < 0 else -lim * .05, lim])
        st.plotly_chart(f4, use_container_width=True)
        st.caption(f"Perbandingan rata-rata harga {tgl(A)} – {tgl(B)} dengan {tgl(A0)} – {tgl(B0)}. "
                   "Merah = naik, hijau = turun.")
        n_naik = int((ubah['rp'] > 0).sum())
        bn, bt_ = ubah['rp'].idxmax(), ubah['rp'].idxmin()
        def _ub(p):
            v, q = ubah.loc[p, 'rp'], ubah.loc[p, 'pct']
            kata = 'naik' if v > 0 else 'turun'
            return (f"dari {rp(ubah.loc[p, 'sebelum'])} menjadi {rp(ubah.loc[p, 'sesudah'])} "
                    f"(<b>{'+' if v > 0 else '−'}{rp(abs(v))}/kg</b>, {kata} {pct(abs(q))})")
        if n_naik > 0:
            teks = (f"<b>{n_naik} dari {len(ubah)} pasar</b> mengalami kenaikan. Kenaikan terbesar di "
                    f"<b>Pasar {nama(bn)}</b>: {_ub(bn)}. ")
            teks += (f"Penurunan terbesar di Pasar {nama(bt_)}: {_ub(bt_)}." if ubah.loc[bt_, 'rp'] < 0
                     else f"Kenaikan terkecil di Pasar {nama(bt_)}: {_ub(bt_)}.")
        else:
            teks = (f"<b>Harga turun di semua {len(ubah)} pasar.</b> Penurunan terbesar di <b>Pasar {nama(bt_)}</b>: "
                    f"{_ub(bt_)}; penurunan terkecil di Pasar {nama(bn)}: {_ub(bn)}.")
        kotak('insight', teks)
        top3 = ubah.sort_values('rp', ascending=False).index[:3]
        kotak('rekom', (f"<b>Verifikasi harga dan pasokan</b> di pasar dengan kenaikan terbesar "
                        f"({', '.join(nama(p) for p in top3)}): pastikan harga yang tercatat benar, lalu cek apakah ada "
                        "gangguan pasokan atau distribusi. Bila kenaikan terjadi serentak di hampir semua pasar, masalahnya "
                        "kemungkinan di tingkat kabupaten (pasokan dari sentra), bukan di satu pasar.")
              if n_naik > 0 else "Harga turun di semua pasar. Belum perlu intervensi; lanjutkan pemantauan rutin.")

    # ── 5. SINYAL DINI ──────────────────────────────────────────────
    bagian("5", "Sinyal peringatan dini",
           "Saat terjadi lonjakan harga, pasar mana yang biasanya naik duluan dan berapa lama pasar lain menyusul?")
    eps = cari_lonjakan(jenis)
    if not eps:
        kotak('info', "Tidak ditemukan lonjakan (harga kabupaten naik >50% dalam 30 hari) pada data ini.")
    else:
        label_ep = [f"{BLN_P[e['puncak_tgl'].month - 1]} {e['puncak_tgl'].year} (puncak {rp(e['puncak'])})" for e in eps]
        pilih_default = len(eps) - 1
        for i, e in enumerate(eps):
            if A <= e['puncak_tgl'] <= B or A <= e['tanggal'] <= B:
                pilih_default = i
        ep_i = st.selectbox("Pilih peristiwa lonjakan", range(len(eps)), index=pilih_default,
                            format_func=lambda i: label_ep[i])
        e = eps[ep_i]
        s = e['mulai'].dropna()
        f5 = go.Figure()
        f5.add_trace(go.Scatter(x=s.values, y=[nama(p) for p in s.index], mode='markers+text',
                                marker=dict(size=13, color=list(range(len(s))), colorscale='Reds_r', line=dict(width=1, color='#111827')),
                                text=[tgl(d)[:-5] for d in s.values], textposition='middle right',
                                hovertemplate='<b>%{y}</b><br>Mulai naik %{x|%d %b %Y}<extra></extra>', showlegend=False))
        f5.add_vline(x=e['tanggal'], line_dash='dash', line_color='#DC2626')
        f5.add_annotation(x=e['tanggal'], y=1.06, yref='paper', showarrow=False,
                          text='Harga kabupaten +50% dalam 30 hari', font=dict(color='#DC2626', size=11))
        gaya(f5, 60 + 28 * max(len(s), 3), yaxis=dict(autorange='reversed'))
        st.plotly_chart(f5, use_container_width=True)
        st.caption("Titik = tanggal pasar mulai naik >30% di atas harga normalnya (median 31–60 hari sebelum peristiwa) "
                   "selama 3 hari berturut-turut. Pasar yang tidak naik sebesar itu tidak ditampilkan.")
        jeda = (s.iloc[min(6, len(s) - 1)] - s.iloc[0]).days
        # frekuensi masuk 3 tercepat di semua peristiwa
        frek = pd.Series([p for ee in eps for p in ee['mulai'].dropna().index[:3]]).value_counts()
        semua_jeda = [(ee['mulai'].dropna().iloc[min(6, len(ee['mulai'].dropna()) - 1)] - ee['mulai'].dropna().iloc[0]).days
                      for ee in eps if len(ee['mulai'].dropna()) > 1]
        teks = (f"Pada lonjakan {label_ep[ep_i].split(' (')[0]}, harga kabupaten naik dari sekitar {rp(e['base_avg'])} ke "
                f"puncak <b>{rp(e['puncak'])}</b> ({tgl(e['puncak_tgl'])}). Pasar yang naik duluan: "
                + ", ".join(f"<b>{nama(p)}</b> ({tgl(d)})" for p, d in s.iloc[:3].items())
                + f". Separuh pasar (7 pasar) sudah ikut naik <b>{jeda} hari</b> setelah pasar pertama; "
                  f"{len(s)} dari 14 pasar naik lebih dari 30%. ")
        teks += (f"Dari {len(eps)} lonjakan {jenis} sejak 2023, pasar yang paling sering termasuk 3 tercepat: "
                 + ", ".join(f"<b>{nama(p)}</b> ({n} kali)" for p, n in frek.head(3).items())
                 + f". Jeda sampai separuh pasar ikut naik umumnya sekitar <b>{int(np.median(semua_jeda))} hari</b> (median).")
        kotak('insight', teks)
        kotak('rekom', (f"Jadikan <b>{', '.join(nama(p) for p in frek.head(3).index)}</b> sebagai pasar pantau utama. "
                        "Jika <b>2–3 pasar</b> naik lebih dari 30% di atas harga bulan sebelumnya selama 3 hari berturut-turut, "
                        f"anggap sebagai <b>alarm dini</b>: biasanya ada waktu sekitar {int(np.median(semua_jeda))} hari "
                        "sebelum separuh pasar ikut naik untuk menyiapkan pasokan dan operasi pasar. Pasar yang naik duluan "
                        "tidak selalu sama, jadi pantau semua pasar dan jangan hanya bergantung pada satu pasar."))

    # ── RINGKASAN OTOMATIS (di bagian atas) ─────────────────────────
    poin = [f"Status <b>{status}</b>: {jenis} {nama_p} per {tgl(B)} {rp(akhir)}/kg "
            f"(30 hari terakhir {pct(ch30, 1, True)}).",
            f"Pasar termahal pada periode ini <b>{nama(top)}</b>, {rp(sel)}/kg lebih mahal dari {nama(bot)}."]
    if eps:
        poin.append(f"Pasar yang paling sering naik duluan saat lonjakan: <b>{', '.join(nama(p) for p in frek.head(2).index)}</b>.")
    slot_ringkas.markdown('<div class="ringkas"><b>3 hal terpenting</b><ul>' + ''.join(f'<li>{p}</li>' for p in poin)
                          + '</ul></div>', unsafe_allow_html=True)

    # ── CATATAN DATA ────────────────────────────────────────────────
    st.markdown("---")
    asli = OBS[jenis].loc[A:B].mean().mean() * 100
    th_asli = OBS[jenis].groupby(OBS[jenis].index.year).mean().mean(axis=1) * 100
    peringatan = (" <b>Data asli pada periode ini kurang dari 70%, sehingga insight perlu ditafsirkan dengan hati-hati.</b>"
                  if asli < 70 else "")
    kotak('info', (f"Pada periode terpilih, <b>{pct(asli)}</b> harga berasal dari pencatatan langsung di pasar; sisanya "
                   "diisi dengan harga terakhir yang tercatat. Data asli per tahun: "
                   + ", ".join(f"{th} {pct(v)}" for th, v in th_asli.items())
                   + ". Status: Normal (&lt;25% dalam 30 hari), Waspada (25–50%), Siaga (≥50%). "
                   "Rekomendasi disusun dari pola harga dan perlu dicocokkan dengan kondisi lapangan." + peringatan))
    unduh = df[(df['tanggal'] >= A) & (df['tanggal'] <= B)][['tanggal', 'nama_pasar', KOLOM[jenis][0], KOLOM[jenis][1]]]
    st.download_button("Unduh data periode ini (CSV)", unduh.to_csv(index=False).encode('utf-8'),
                       file_name=f"harga_{jenis.replace(' ', '_').lower()}_{A.date()}_{B.date()}.csv", mime='text/csv')


# =====================================================================
# HALAMAN 2: PREDIKSI - SIMULASI MODEL
# =====================================================================
else:
    ARR, PSR_M, INFO = muat_model()
    TGL_ASAL = pd.to_datetime(INFO['tgl_asal'])          # tanggal prediksi dibuat (harga terakhir diketahui)
    H = ARR['pred_m_rp'].shape[1]                         # 30 hari
    MODEL = {'ST-GCN korelasi': ('pred_m_rp', 'pred_h_rp'), 'ST-GCN jarak': ('pred_jarak_m_rp', 'pred_jarak_h_rp'),
             'GRU tanpa graf': ('pred_gru_m_rp', 'pred_gru_h_rp'),
             'Naive persistence': ('pred_persist_m_rp', 'pred_persist_h_rp')}
    MODEL = {m: k for m, k in MODEL.items() if k[0] in ARR}
    WARNA = {'ST-GCN korelasi': '#2563EB', 'ST-GCN jarak': '#7C3AED', 'GRU tanpa graf': '#F59E0B',
             'Naive persistence': '#6B7280'}
    PENJ = {'ST-GCN korelasi': 'model utama; memakai harga pasar lain yang pergerakannya mirip',
            'ST-GCN jarak': 'memakai harga pasar lain yang lokasinya berdekatan',
            'GRU tanpa graf': 'hanya memakai riwayat harga pasar itu sendiri',
            'Naive persistence': 'cara paling sederhana: harga ke depan dianggap sama dengan harga terakhir'}
    MIN_MULAI, MAKS_MULAI = TGL_ASAL[0] + pd.Timedelta(days=1), TGL_ASAL[-1] + pd.Timedelta(days=1)

    st.markdown('<div class="judul"><h1>Simulasi Prediksi Harga</h1>'
                '<p>Seandainya model dipakai pada Agustus–Desember 2025, seberapa dekat tebakannya dengan harga '
                'sebenarnya, dan apakah lebih baik dari cara sederhana?</p></div>', unsafe_allow_html=True)
    kotak('info', (f"Ini <b>simulasi</b> pada periode uji ({tgl(MIN_MULAI)} – {tgl(TGL_ASAL[-1] + pd.Timedelta(days=H))}): "
                   "harga aktualnya sudah diketahui, sehingga ketepatan model bisa diperiksa. Data periode ini tidak "
                   "dipakai saat model belajar."))

    c1, c2, c3 = st.columns([1.2, 1, 2])
    with c1:
        pasar = st.selectbox("Pasar", ['Semua pasar (rata-rata)'] + PSR_M,
                             format_func=lambda p: p if p.startswith('Semua') else nama(p))
    with c2:
        jenis = st.radio("Jenis cabai", list(KOLOM), horizontal=True, key='jenis_pred')
    with c3:
        dipilih = st.multiselect("Model yang dibandingkan", list(MODEL),
                                 default=[m for m in ['ST-GCN korelasi', 'Naive persistence'] if m in MODEL])
    c4, c5 = st.columns([1, 2])
    with c4:
        mulai = pd.Timestamp(st.date_input("Tanggal awal yang diprediksi", value=pd.Timestamp('2025-10-01').date(),
                                           min_value=MIN_MULAI.date(), max_value=MAKS_MULAI.date(),
                                           format="DD/MM/YYYY"))
    with c5:
        n_hari = st.slider("Berapa hari yang diprediksi (maksimal 30)", 1, H, 14)
    if not dipilih:
        st.info("Centang minimal satu model.")
        st.stop()
    idx = int(np.where(TGL_ASAL == mulai - pd.Timedelta(days=1))[0][0])
    tgl_pred = pd.date_range(mulai, periods=n_hari, freq='D')
    dibuat = TGL_ASAL[idx]
    st.caption(f"Rentang yang diprediksi: **{tgl(tgl_pred[0])} – {tgl(tgl_pred[-1])}** ({n_hari} hari). "
               f"Prediksi dibuat pada **{tgl(dibuat)}**, memakai data harga sampai tanggal itu.")

    j = 0 if jenis == 'Rawit Merah' else 1
    ykey = ['y_m_rp', 'y_h_rp'][j]
    if pasar.startswith('Semua'):
        ambil = lambda a: a[idx, :n_hari, :].mean(axis=1)
        hist = PV[jenis].mean(axis=1)
    else:
        ip = PSR_M.index(pasar)
        ambil = lambda a: a[idx, :n_hari, ip]
        hist = PV[jenis][pasar]
    akt = ambil(ARR[ykey])
    pred = {m: ambil(ARR[MODEL[m][j]]) for m in dipilih}
    hasil = pd.DataFrame({m: {'MAPE': mape(akt, p), 'MAE': mae(akt, p)} for m, p in pred.items()}).T
    terbaik = hasil['MAPE'].idxmin()

    # kartu per model
    kk = st.columns(len(dipilih))
    for col, m in zip(kk, dipilih):
        lencana = ' · <span class="turun">paling akurat</span>' if m == terbaik and len(dipilih) > 1 else ''
        col.markdown(kartu(m, f"meleset {pct(hasil.loc[m, 'MAPE'])}",
                           f"rata-rata {rp(hasil.loc[m, 'MAE'])}/kg{lencana}"), unsafe_allow_html=True)

    # grafik utama
    f = go.Figure()
    h0 = hist.loc[dibuat - pd.Timedelta(days=30):dibuat]
    f.add_trace(go.Scatter(x=h0.index, y=h0.values, name='Harga 30 hari sebelumnya', line=dict(color='#94A3B8', width=2),
                           hovertemplate='%{x|%d %b %Y}<br>Rp %{y:,.0f}<extra>Historis</extra>'))
    f.add_trace(go.Scatter(x=tgl_pred, y=akt, name='Harga aktual', line=dict(color='#111827', width=3),
                           mode='lines+markers', marker=dict(size=5),
                           hovertemplate='%{x|%d %b %Y}<br>Rp %{y:,.0f}<extra>Aktual</extra>'))
    for m in dipilih:
        f.add_trace(go.Scatter(x=tgl_pred, y=pred[m], name=m,
                               line=dict(color=WARNA[m], width=2.2, dash='dot' if m == 'Naive persistence' else 'dash'),
                               hovertemplate='%{x|%d %b %Y}<br>Rp %{y:,.0f}<extra>' + m + '</extra>'))
    f.add_vline(x=dibuat, line_dash='dot', line_color='#9CA3AF')
    f.add_annotation(x=dibuat, y=1.05, yref='paper', text='prediksi dibuat', showarrow=False,
                     font=dict(size=11, color='#6B7280'))
    gaya(f, 380, yaxis_tickprefix='Rp ', yaxis_tickformat=',.0f')
    st.plotly_chart(f, use_container_width=True)

    # dua grafik kecil: MAE (Rp) dan MAPE (%)
    g1, g2 = st.columns(2)
    for col, met, judul, fmt in [(g1, 'MAE', 'Rata-rata meleset (Rp/kg)', lambda v: rp(v)),
                                 (g2, 'MAPE', 'Rata-rata meleset (%)', lambda v: pct(v))]:
        fb = go.Figure(go.Bar(x=list(hasil.index), y=hasil[met], marker_color=[WARNA[m] for m in hasil.index],
                              text=[fmt(v) for v in hasil[met]], textposition='outside'))
        gaya(fb, 260, showlegend=False, title=dict(text=judul, font=dict(size=13)),
             yaxis_range=[0, float(hasil[met].max()) * 1.3])
        col.plotly_chart(fb, use_container_width=True)

    # insight & rekomendasi
    teks = (f"Untuk {jenis} {'rata-rata 14 pasar' if pasar.startswith('Semua') else 'Pasar ' + nama(pasar)} "
            f"pada {tgl(tgl_pred[0])} – {tgl(tgl_pred[-1])}, yang paling dekat dengan harga aktual adalah "
            f"<b>{terbaik}</b>: meleset rata-rata <b>{rp(hasil.loc[terbaik, 'MAE'])}/kg ({pct(hasil.loc[terbaik, 'MAPE'])})</b>. ")
    lain = [m for m in dipilih if m != terbaik]
    if lain:
        teks += "Model lain: " + "; ".join(f"{m} {rp(hasil.loc[m, 'MAE'])}/kg ({pct(hasil.loc[m, 'MAPE'])})" for m in lain) + ". "
    teks += (f"Harga aktual bergerak dari {rp(akt[0])} ke {rp(akt[-1])} ({arah((akt[-1] / akt[0] - 1) * 100)}) "
             f"selama rentang ini.")
    kotak('insight', teks)
    RS = INFO['ringkasan']
    if 'Naive persistence' in RS:
        terbaik_all = min(RS, key=lambda m: RS[m]['MAPE Rata2'])
        kotak('rekom', (f"Hasil satu rentang tanggal bisa berbeda dari keseluruhan. Pada seluruh periode uji, model paling "
                        f"akurat adalah <b>{terbaik_all}</b> ({pct(RS[terbaik_all]['MAPE Rata2'], 2)}). Karena itu, "
                        "<b>harga terakhir yang tercatat tetap menjadi patokan utama</b> untuk perkiraan beberapa hari ke depan, "
                        "dan prediksi model dipakai sebagai pembanding, bukan satu-satunya dasar keputusan. Makin jauh ke depan, "
                        "makin besar melesetnya (lihat bagian di bawah)."))

    # tabel per tanggal
    st.markdown("**Tabel per tanggal**")
    tb = pd.DataFrame({'Tanggal': [tgl(d) for d in tgl_pred], 'Harga aktual (Rp)': akt})
    for m in dipilih:
        tb[f'{m} (Rp)'] = pred[m]
        tb[f'Meleset {m} (Rp)'] = np.abs(pred[m] - akt)
    num = [c for c in tb.columns if c != 'Tanggal']
    tabel(tb, desimal=0, tinggi=420)
    st.download_button("Unduh tabel (CSV)", tb.round(0).to_csv(index=False).encode('utf-8'),
                       file_name=f"simulasi_{jenis.replace(' ', '_').lower()}_{tgl_pred[0].date()}_{n_hari}hari.csv",
                       mime='text/csv')

    # ── bagian lanjutan (buka-tutup) ────────────────────────────────
    with st.expander("Makin jauh menebak, makin meleset? (seluruh periode uji)"):
        st.markdown("**Hari ke-1** = tebakan untuk 1 hari setelah prediksi dibuat, **hari ke-30** = 30 hari setelahnya. "
                    "Ini bukan tanggal kalender: setiap titik adalah rata-rata dari semua tanggal di periode uji.")
        Y = ARR[ykey] if pasar.startswith('Semua') else ARR[ykey][:, :, [PSR_M.index(pasar)]]
        fh = go.Figure()
        per_h = {}
        for m in dipilih:
            P = ARR[MODEL[m][j]] if pasar.startswith('Semua') else ARR[MODEL[m][j]][:, :, [PSR_M.index(pasar)]]
            per_h[m] = [float(np.mean([mape(Y[:, h, i], P[:, h, i]) for i in range(Y.shape[2])])) for h in range(H)]
            fh.add_trace(go.Scatter(x=list(range(1, H + 1)), y=per_h[m], name=m, mode='lines+markers',
                                    line=dict(color=WARNA[m], width=2.2), marker=dict(size=4)))
        gaya(fh, 300, xaxis_title='Hari ke- (setelah prediksi dibuat)', yaxis_title='MAPE (%)')
        st.plotly_chart(fh, use_container_width=True)
        m0 = dipilih[0]
        kotak('insight', f"{m0}: meleset {pct(per_h[m0][0])} untuk hari ke-1, {pct(per_h[m0][6])} untuk hari ke-7, dan "
                         f"{pct(per_h[m0][-1])} untuk hari ke-30.")

    with st.expander("Detail untuk peneliti"):
        hs = [1, 7, 14, 21, 30]
        urutan = [m for m in ['Naive persistence', 'GRU tanpa graf', 'ST-GCN jarak', 'ST-GCN korelasi'] if m in RS]

        # ── (a) Tabel perbandingan model ──
        tab3 = pd.DataFrame([{'Model': m, **{f'H{h}': RS[m][f'MAPE H{h}'] for h in hs},
                              'Merah': RS[m]['MAPE Merah'], 'Hijau': RS[m]['MAPE Hijau'], 'Rata-rata': RS[m]['MAPE Rata2'],
                              'RMSE Merah (Rp)': rp(RS[m]['RMSE Merah']), 'RMSE Hijau (Rp)': rp(RS[m]['RMSE Hijau']),
                              '5 seed': (f"{np.mean(list(RS[m]['per_seed'].values())):.2f} ± "
                                         f"{np.std(list(RS[m]['per_seed'].values()), ddof=1):.2f}".replace('.', ',')
                                         if 'per_seed' in RS[m] else '–')} for m in urutan])
        subjudul("(a) MAPE (%) seluruh periode uji (Tabel III paper)", pertama=True)
        tabel(tab3, desimal=2)
        best = min(urutan, key=lambda m: RS[m]['MAPE Rata2'])
        n_h = sum(min(urutan, key=lambda m: RS[m][f'MAPE H{h}']) == best for h in hs)
        teks = (f"Model dengan MAPE rata-rata terkecil adalah <b>{best}</b> ({pct(RS[best]['MAPE Rata2'], 2)}), dan model "
                f"ini paling akurat di <b>{n_h} dari {len(hs)}</b> horizon yang ditampilkan. ")
        if 'ST-GCN korelasi' in RS:
            k_ = RS['ST-GCN korelasi']
            teks += (f"MAPE ST-GCN korelasi naik dari {pct(k_['MAPE H1'], 2)} (hari ke-1) menjadi {pct(k_['MAPE H30'], 2)} "
                     f"(hari ke-30), dan Rawit Hijau ({pct(k_['MAPE Hijau'], 2)}) lebih mudah diprediksi dibanding Rawit Merah "
                     f"({pct(k_['MAPE Merah'], 2)}). ")
        best_rmse = min(urutan, key=lambda m: RS[m]['RMSE Merah'])
        if best_rmse != best:
            teks += (f"Menurut RMSE Rawit Merah, yang paling kecil justru <b>{best_rmse}</b> ({rp(RS[best_rmse]['RMSE Merah'])}): "
                     "model ini lebih jarang meleset sangat jauh, walaupun rata-rata persentase melesetnya lebih besar.")
        kotak('insight', teks)

        # ── (b) Uji signifikansi ──
        try:
            from scipy import stats
            baris = []
            sk = RS.get('ST-GCN korelasi', {}).get('per_seed')
            for m in ['GRU tanpa graf', 'ST-GCN jarak']:
                so = RS.get(m, {}).get('per_seed')
                if sk and so:
                    kk_ = [s for s in sk if s in so]
                    baris.append((f"ST-GCN korelasi vs {m}", 'paired t-test',
                                  stats.ttest_rel([sk[s] for s in kk_], [so[s] for s in kk_]).pvalue))
            for m in ['ST-GCN korelasi', 'GRU tanpa graf', 'ST-GCN jarak']:
                so = RS.get(m, {}).get('per_seed')
                if so and 'Naive persistence' in RS:
                    baris.append((f"{m} vs naive persistence", 'one-sample t-test',
                                  stats.ttest_1samp(list(so.values()), RS['Naive persistence']['MAPE Rata2']).pvalue))
            if baris:
                subjudul("(b) Uji signifikansi (MAPE 5 seed)")
                tabel(pd.DataFrame(baris, columns=['Perbandingan', 'Uji', 'p']),
                      fmt={'p': lambda v: '< 0,001' if v < 0.001 else f'{v:.3f}'.replace('.', ',')})
                beda = [b for b in baris if b[2] < 0.05]
                sama = [b for b in baris if b[2] >= 0.05]
                teks = ("Nilai p di bawah 0,05 berarti selisihnya <b>bukan kebetulan</b>; di atas 0,05 berarti selisihnya "
                        "masih bisa terjadi hanya karena pengacakan saat melatih model (5 seed), sehingga kedua model "
                        "dianggap <b>setara</b>. ")
                fp_ = lambda v: 'p < 0,001' if v < 0.001 else f'p = {v:.3f}'.replace('.', ',')
                if beda:
                    teks += "Berbeda nyata: " + "; ".join(f"{b[0]} ({fp_(b[2])})" for b in beda) + ". "
                if sama:
                    teks += "Setara: " + "; ".join(f"{b[0]} ({fp_(b[2])})" for b in sama) + ". "
                if beda and sama:
                    teks += ("Artinya, ketiga model berbasis pembelajaran setara satu sama lain, tetapi semuanya kalah secara "
                             "nyata dari naive persistence; informasi harga pasar lain tidak menambah akurasi.")
                kotak('insight', teks)
        except ImportError:
            pass

        # ── (c) MAPE per pasar ──
        subjudul(f"(c) MAPE per pasar, {jenis}, seluruh periode uji (%)")
        Yj = ARR[ykey]
        pp = pd.DataFrame({m: [mape(Yj[:, :, i], ARR[MODEL[m][j]][:, :, i]) for i in range(len(PSR_M))] for m in dipilih},
                          index=[nama(p) for p in PSR_M]).sort_values(dipilih[0])
        fp = go.Figure([go.Bar(y=pp.index, x=pp[m], name=m, orientation='h', marker_color=WARNA[m]) for m in dipilih])
        gaya(fp, 460, barmode='group', xaxis_title=f'MAPE {jenis} (%)')
        st.plotly_chart(fp, use_container_width=True)
        m0 = dipilih[0]
        teks = (f"Untuk {m0}, pasar paling mudah diprediksi <b>{pp.index[0]}</b> ({pct(pp[m0].iloc[0])}) dan paling sulit "
                f"<b>{pp.index[-1]}</b> ({pct(pp[m0].iloc[-1])}), selisih {pct(pp[m0].iloc[-1] - pp[m0].iloc[0]).rstrip('%')} poin persen. ")
        if len(dipilih) > 1:
            m1 = dipilih[1]
            n_m = int((pp[m0] < pp[m1]).sum())
            teks += f"{m0} lebih akurat dari {m1} di <b>{n_m} dari {len(pp)} pasar</b>."
        kotak('insight', teks)

        # ── (d) Training loss ──
        subjudul("(d) Proses belajar model (training loss)")
        hist_m = {'ST-GCN korelasi': ('history_train', 'history_val', ARR['best_epoch'])}
        if 'history_jarak_train' in ARR:
            hist_m['ST-GCN jarak'] = ('history_jarak_train', 'history_jarak_val', int(ARR['best_epoch_jarak'][0]))
        for m, (a_, b_, be) in hist_m.items():
            ft = go.Figure()
            ft.add_trace(go.Scatter(y=ARR[a_], name='Train loss', line=dict(color='#2563EB')))
            ft.add_trace(go.Scatter(y=ARR[b_], name='Validation loss', line=dict(color='#DC2626')))
            ft.add_vline(x=be - 1, line_dash='dash', line_color='#6B7280')
            gaya(ft, 260, title=dict(text=f'Training loss {m} (seed 10), best epoch {be}', font=dict(size=13)),
                 xaxis_title='Epoch')
            st.plotly_chart(ft, use_container_width=True)
        mtr, mte = INFO.get('mape_train'), INFO.get('mape_test')
        if mtr and mte:
            tr_, te_ = (mtr['merah'] + mtr['hijau']) / 2, (mte['merah'] + mte['hijau']) / 2
            teks = (f"ST-GCN korelasi berhenti belajar pada epoch ke-<b>{ARR['best_epoch']}</b> (saat validation loss "
                    f"terendah). Pada data latih model meleset <b>{pct(tr_, 2)}</b>, sedangkan pada data uji "
                    f"<b>{pct(te_, 2)}</b>. ")
            teks += ("Kesalahan di data uji jauh lebih besar: model mempelajari pola 2023–2024 yang tidak berulang dengan "
                     "cara yang sama pada 2025, misalnya waktu lonjakan akhir tahun yang bergeser." if te_ > tr_ * 1.2
                     else "Kesalahan di data latih dan data uji tidak jauh berbeda.")
            kotak('insight', teks)

        # ── (e) Pemeriksaan data asli ──
        asli_ = INFO.get('mape_target_asli')
        if asli_:
            subjudul("(e) MAPE hanya pada harga yang benar-benar tercatat")
            ta = pd.DataFrame([{'Model': k, 'MAPE semua target (%)': RS[k]['MAPE Rata2'] if k in RS else np.nan,
                                'MAPE target data asli (%)': v['rata2']} for k, v in asli_.items()])
            tabel(ta, desimal=2)
            urut_a = ta.sort_values('MAPE target data asli (%)')['Model'].tolist()
            urut_s = ta.sort_values('MAPE semua target (%)')['Model'].tolist()
            teks = ("Sekitar 3% harga pada periode uji adalah hasil pengisian (bukan catatan lapangan). Setelah titik "
                    "tersebut dibuang, " + ("<b>urutan model tidak berubah</b>" if urut_a == urut_s
                                            else "<b>urutan model berubah</b>"))
            if urut_a[0] == urut_s[0]:
                teks += (f" dan model terbaik tetap <b>{urut_a[0]}</b>, sehingga kesimpulan tidak dipengaruhi data hasil "
                         "pengisian.")
            else:
                teks += f"; model terbaik menjadi <b>{urut_a[0]}</b> (sebelumnya {urut_s[0]})."
            kotak('insight', teks)

        # ── Kesimpulan untuk penelitian ──
        subjudul("Saran untuk penelitian lanjutan")
        kotak('rekom', ("<b>Untuk penelitian lanjutan:</b> (1) tambahkan variabel di luar harga, seperti cuaca, pasokan dari "
                        "sentra produksi, dan harga pasar induk, karena harga antarpasar di Banyumas terlalu kompak untuk "
                        "saling memberi informasi baru; (2) tambahkan penanda hari besar berbasis kalender Hijriah; "
                        "(3) evaluasi pada beberapa periode uji (rolling-origin), bukan hanya Agustus–Desember 2025; "
                        "(4) abaikan titik hasil pengisian saat melatih model."))
