import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

#import dataframe
rumah_5kota = pd.read_csv('rumah_5kota.csv')
ihpr = pd.read_csv('ihpr.csv', delimiter=';')
inflasi = pd.read_csv('inflasi.csv', delimiter=';')
upah_bulanan = pd.read_csv('upah_bulanan_indo.csv', delimiter=';', index_col='tahun')
ump_jkt = pd.read_csv('ump_jakarta.csv', delimiter=';')
kpr_bi7drr = pd.read_csv('kpr_bi7drr.csv', delimiter=';')
alasan = pd.read_csv('alasan_blm_punya_rumah.csv', delimiter=';')

st.title('Generasi Muda Semakin Kesulitan Memiliki Rumah Sendiri')

#pembuka
with st.container():
    st.caption(
        '''
        (Terdapat) 12,75 juta backlog itu artinya yang antri membutuhkan rumah, apalagi Indonesia 
        demografinya masih relatif muda artinya generasi muda ini kemudian akan berumah tangga maka 
        mereka membutuhkan rumah tapi mereka berumah tangga can't afford untuk mendapatkan rumah. 
        Purchasing power mereka dibandingkan rumahnya (yang) lebih tinggi sehingga mereka enak dengan 
        either tinggal di mertua atau nyewa
        '''
    )
    st.write(
        '''
        Pernyataan tersebut disampaikan oleh Menteri Keuangan RI Ibu Sri Mulyani dalam seminar 
        [Road to G20 - Securitization Summit 2022 - Day 1](https://www.youtube.com/watch?v=u7kHXmbaBr4&t=2483s) 
        pada Rabu, 6 Juli 2022. Sebuah survei yang dilakukan rumah.com dalam Rumah.com Consumer Sentiment 
        Study Semester II 2020 mengkonfirmasi masih besarnya proporsi generasi muda yang masih 
        tinggal dengan orang tuanya.
        '''
    )

    tinggal_dgn_ortu = pd.DataFrame({
    'Tinggal dengan Orang Tua': ('Ya', 'Tidak'),
    'Persentase': (34, 66)
    })
    ortu_chart = px.pie(tinggal_dgn_ortu, values='Persentase', names='Tinggal dengan Orang Tua',
                        title='Generasi Milenial Tinggal Bersama Orang Tua', hole=0.5)
    
    ortu_chart.update_layout(title_font_size=30)
    ortu_chart.update_traces(textfont_size=17, textfont_color='white', textinfo='percent+label')

    st.plotly_chart(ortu_chart)
    st.write(
        '''
        sumber: [Rumah.com Consumer Sentiment Study Semester II 2020 (n=675)](https://www.rumah.com/panduan-properti/milenial-belum-tertarik-beli-rumah-di-usia-muda-31226)
        '''
    )

    st.write(
        '''
        Perlu ditekankan bahwa jawaban tidak tinggal dengan orang tua masih bisa berarti menyewa rumah, 
        sehingga angka milenial yang belum memiliki rumah sendiri masih bisa lebih tinggi. 
        Mengapa masih banyak generasi muda yang sudah berkeluarga namun masih tinggal bersama orang tua? 
        Mari sama-sama kita akan bahas dari segi harga perumahan dan kondisi finansial generasi muda.
        '''
    )

#data rumah
with st.container():
    st.header('Seberapa Tinggi Harga Rumah')

    st.write(
        '''
        Kenaikan harga rumah dapat dipengaruhi oleh berbagai faktor. Dalam seminar yang sama, Sri Mulyani 
        menyatakan faktor tersebut antara lain yaitu harga tanah dan bahan baku bangunan, serta posisi 
        ekuilibrium permintaan dan penawaran. Adapula pandemi menjadi faktor yang dapat mengurangi kestabilan 
        harga rumah. Dalam bagian ini kita akan melihat bagaimana kondisi harga rumah saat ini serta tren 
        pergerakannya dari beberapa tahun ke belakang.
        '''
    )

    median_harga_5kota = rumah_5kota.groupby(['Kota', 'Kategori'])[['Harga']].median().reset_index()

    grafik_placeholder1 = st.empty()

    tipe_kategori = 'Kecil'
    kecil1, sedang1, besar1 = st.columns(3)
    with kecil1:
        if st.button('Kecil (≤ 90m2)'):
            tipe_kategori = 'Kecil'
    with sedang1:
        if st.button('Sedang (91-150m2)'):
            tipe_kategori = 'Sedang'
    with besar1:
        if st.button('Besar (≥ 151m2)'):
            tipe_kategori = 'Besar'

    grafik_rmh_5kt = px.bar(median_harga_5kota.query(f'Kategori == "{tipe_kategori}"'), x='Harga', y='Kota',
                            title=f'Median Rumah di 5 Kota 2022 - Tipe {tipe_kategori}')
    grafik_rmh_5kt.update_yaxes(categoryorder='total ascending')
    grafik_rmh_5kt.update_layout(title_font_size=30)

    grafik_placeholder1.plotly_chart(grafik_rmh_5kt)
    st.write(
        '''
        sumber: [Lamudi](https://www.lamudi.co.id/)
        '''
    )

    st.write(
        '''
        Harga rumah secara rata-rata berada pada kisaran 500 juta hingga 7,5 miliar rupiah tergantung 
        ukuran dan lokasinya. Pada ketiga kategori Kota Jakarta memiliki nilai median harga rumah tertinggi.
        '''
    )

    grafik_placeholder2 = st.empty()

    wilayah = st.selectbox('Wilayah', ('Gabungan 18 Kota', 'Jabodebek-Banten', 
                                       'Bandung', 'Surabaya', 'Medan', 'Makassar'))

    tren_harga_rumah = make_subplots(specs=[[{'secondary_y': True}]])

    tren_harga_rumah.add_trace(
        go.Bar(x=ihpr.query(f'lokasi == "{wilayah}"')['tahun'], 
               y=ihpr.query(f'lokasi == "{wilayah}"')['ihpr'],
               name='IHPR (2012 = 100)'),
        secondary_y=False
    )
    tren_harga_rumah.add_trace(
        go.Scatter(x=ihpr.query(f'lokasi == "{wilayah}"')['tahun'], 
                   y=ihpr.query(f'lokasi == "{wilayah}"')['delta_ihpr'],
                   name='Kenaikan IHPR'),
        secondary_y=True
    )
    tren_harga_rumah.add_trace(
        go.Scatter(x=inflasi['tahun'], 
                   y=inflasi['inflasi'],
                   name='Inflasi Nasional',
                   line=dict(color='orange')),
        secondary_y=True
    )    
    tren_harga_rumah.update_layout(title_text='Indeks Harga Properti Residensial (IHPR) & Inflasi', title_font_size=30)
    tren_harga_rumah.update_yaxes(title_text='IHPR', secondary_y=False)
    tren_harga_rumah.update_yaxes(title_text='Kenaikan IHPR & Inflasi (%)', showgrid=False, secondary_y=True)

    grafik_placeholder2.plotly_chart(tren_harga_rumah)
    st.write(
        '''
        sumber: [Bank](https://www.bi.go.id/id/publikasi/laporan/Pages/SHPR-Triwulan-I-2022.aspx) 
        [Indonesia](https://www.bi.go.id/id/statistik/indikator/data-inflasi.aspx)
        '''
    )

    st.write(
        '''
        Terlihat bahwa terjadi tren kenaikan harga rumah dari tahun ke tahun. Meskipun demikian, 
        kenaikan tersebut melambat seiring berjalannya waktu. Hal ini terlebih ketika memasuki era 
        pandemi di mana kenaikan harga rumah rata-rata hanya mencapai kurang lebih 1,5% (kecuali Medan). 

        Penting untuk diperhatikan bahwa tren persentase pergerakan IHPR selalu mengikuti tren pergerakan 
        inflasi. Inflasi pada kuartal 2 tahun 2022 mengalami kenaikan sebesar 300bps (3%), yang 
        mengindikasikan bahwa harga rumah dapat naik tinggi kembali dalam beberapa waktu mendatang.
        '''
    )

    kpr_grafik = go.Figure()
    kpr_grafik.add_trace(
        go.Scatter(x=kpr_bi7drr['tanggal'], y=kpr_bi7drr['kpr_median'], name='KPR per Kuartal')
    )
    kpr_grafik.add_trace(
        go.Bar(x=kpr_bi7drr['tanggal'], y=kpr_bi7drr['bi7drr'], name='BI7DRR per Kuartal')
    )
    kpr_grafik.update_layout(title_text='Median KPR & BI7DRR', title_font_size=30)
    kpr_grafik.update_yaxes(title_text='%')

    st.plotly_chart(kpr_grafik)
    st.write(
        '''
        sumber: [Otoritas Jasa Keuangan](https://www.ojk.go.id/id/kanal/perbankan/Pages/Suku-Bunga-dasar.aspx) 
        dan [Bank Indonesia](https://www.bi.go.id/id/statistik/indikator/bi-7day-rr.aspx)
        '''
    )
    st.write(
        '''
        Menurunnya tren BI7DRR disebabkan oleh langkah bank sentral untuk mendorong momentum pemulihan 
        ekonomi nasional serta angka inflasi yang rendah. Hal ini harus dapat dimanfaatkan oleh orang-orang 
        yang ingin membeli rumah sendiri dengan bunga yang relatif lebih rendah, terlebih dengan angka inflasi 
        2022 yang kembali naik mengindikasikan angka bunga KPR yang rendah tidak akan bertahan lama lagi.
        '''
    )

#data finansial anak muda
with st.container():
    st.header('Bagaimana dengan Finansial Generasi Muda')

    st.write(
        '''
        Lalu bagaimana dengan kondisi finansial generasi muda, apakah sudah dapat memenuhi harga rumah 
        yang semakin tinggi.
        '''
    )

    grafik_upah = px.imshow(upah_bulanan, text_auto=True)
    grafik_upah.update_layout(title_text='Rerata Upah Bulanan Berdasarkan Umur 2016-2022', title_font_size=30)
    grafik_upah.update_xaxes(title_text='Umur')
    grafik_upah.update_yaxes(title_text='Tahun')

    st.plotly_chart(grafik_upah)
    st.write(
        '''
        sumber: [Badan Pusat Statistik](https://www.bps.go.id/subject/19/upah-buruh.html#subjekViewTab3)
        '''
    )

    st.write(
        '''
        Sebagai tenaga kerja baru dengan pengalaman minim, sangat sulit untuk generasi muda untuk dapat 
        meraih posisi tinggi dalam suatu perusahaan dibandingkan dengan usia yang lebih tua. 
        Pandemi juga mengakibatkan pengurangan pendapatan bulanan yang membuat kondisi finansial generasi muda 
        menjadi buruk.
        '''
    )

    grafik_ump = make_subplots(specs=[[{'secondary_y': True}]])
    grafik_ump.add_trace(
        go.Bar(x=ump_jkt['tahun'], y=ump_jkt['ump_jakarta'], name='UMP Jakarta'),
        secondary_y=False
    )
    grafik_ump.add_trace(
        go.Scatter(x=ump_jkt['tahun'], y=ump_jkt['persentase'], 
                   name='Perubahan UMP Jakarta', line=dict(color='lime')),
        secondary_y=True
    )
    grafik_ump.add_trace(
        go.Scatter(x=ihpr.query('lokasi == "Jabodebek-Banten" & tahun >= 2013')['tahun'],
                   y=ihpr.query('lokasi == "Jabodebek-Banten" & tahun >= 2013')['delta_ihpr'],
                   name='Perubahan IHPR Jakarta', line=dict(color='red')),
        secondary_y=True
    )
    grafik_ump.update_layout(title_text='UMP & IHPR Jakarta', title_font_size=30)
    grafik_ump.update_yaxes(title_text='Upah Minimum Provinsi', secondary_y=False)
    grafik_ump.update_yaxes(title_text='Kenaikan UMP & IHPR (%)', showgrid=False, secondary_y=True)

    st.plotly_chart(grafik_ump)
    st.write(
        '''
        sumber: [Badan Pusat Statistik](https://jakarta.bps.go.id/statictable/2015/04/20/83/upah-minimum-provinsi-dan-inflasi-di-dki-jakarta-1999-2020.html) 
        dan [Bank Indonesia](https://www.bi.go.id/id/statistik/indikator/data-inflasi.aspx)
        '''
    )
    st.write(
        '''
        Asumsikan anak milenial Jakarta mendapatkan gaji UMP, apabila sejak tahun 2017 terdapat surplus 
        perubahan UMP kisaran 6%, memasuki tahun 2021 tingkat kenaikan UMP hampir sama dengan IHPR. Hal ini 
        membuat generasi muda harus dapat lebih memperbesar prioritas keuangannya untuk menabung apabila 
        ingin memiliki rumah sendiri. Hal ini akan lebih parah apabila yang bersangkutan termasuk ke dalam 
        generasi sandwich, yaitu generasi yang harus menanggung ekonomi banyak pihak (orang tua dan keluarga 
        barunya).

        Sekarang bayangkan anak milenial tersebut berniat membeli rumah di Jakarta dengan harga yang murah. 
        Ia menemukan rumah murah dengan harga Rp400juta (yang merupakan kuantil 0,1 dalam data). Rumah 
        tersebut ia beli dengan DP 20% KPR 8,75% (asumsi fixed) tenor 30 tahun.
        '''
    )

    st.table(
        pd.DataFrame((
            ('Harga Rumah', 'Rp400.000.000'),
            ('DP%', '20%'),
            ('KPR', '8,75%'),
            (r'Sisihan penghasilan 20% untuk ditabung', 'Rp928.370'),
            ('------------------------', '------------------------'),
            ('Biaya DP', 'Rp80.000.000'),
            ('Cicilan bulanan', 'Rp3.146.802'),
            ('Total bunga', 'Rp732.848.584'),
            ('Total bunga + pinjaman', 'Rp1.132.848.584')
        ), columns=('Keterangan', 'Nilai'))
    )

    st.write(
        r'''
        Biaya DP yang harus dibayarkan adalah setara dengan 7 tahun gaji bulanannya 
        serta cicilan bulanan sebesar 68% gaji bulanannya! Cukup jelas mengapa generasi muda semakin 
        kesulitan untuk dapat membeli rumahnya sendiri.
        '''
    )

    grafik_alasan = px.bar(alasan, x='Persentase', y='Alasan', orientation='h',
                           title='Alasan Milenial Belum Memiliki Rumah Sendiri')
    grafik_alasan.update_layout(title_font_size=30)
    grafik_alasan.update_yaxes(categoryorder='total ascending')

    st.plotly_chart(grafik_alasan)
    st.write(
        '''
        sumber: Perumnas dan diwartakan oleh [Kompas](https://www.kompas.com/properti/read/2021/12/01/150000821/81-juta-milenial-indonesia-belum-punya-rumah)
        '''
    )

    st.write(
        r'''
        Hasil survei di atas mengkonfirmasi alasan-alasan mengapa masih banyak generasi muda yang belum 
        memiliki hunian tempat tinggalnya sendiri. Terdapat 63,12% responden yang memiliki jawaban yang 
        berhubungan dengan persoalan finansial.
        '''
    )

#penutup
with st.container():
    st.subheader('Apa yang Dapat Kita Ambil')

    st.write(
        '''
        Selalu rencanakan keuangan dengan baik, mulai dari budgeting bulanan, strategi alokasi pemasukan 50/30/20, 
        hingga menanam uang dalam aset produktif. Kondisi di masa depan semakin lama semakin disruptif dan 
        tidak ada yang tahu akan seperti apa. Hal ini termasuk perencaaan dalam memiliki perumahan bagi 
        generasi muda. Konsultasikan dengan ahli untuk perencanaan pembelian hunian agar memiliki jawaban 
        pasti apakah sudah siap untuk membeli rumah atau belum. Adapula berbagai inisiatif oleh pemerintah 
        seperti FLPP dan rumah bersubsidi sangat dibutuhkan oleh masyarakat terlebih lagi generasi muda 
        yang masih belum memiliki kekuatan finansial yang mumpuni.
        '''
    )