'''
    File    : rekapNilaiMhs.py
    About   : Rekap nilai mahasiswa menggunakan database dalam python
    created : 18 Juli 2024
'''

# Import libraries
from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

# Konversi ke object flask
rekap_nilai = Flask(__name__)
rekap_nilai.secret_key = 'supersecretkey' # enkripsi basis data

# Periksa basis data (rekap_nilai.db)
conn = sqlite3.connect('rekap_nilai.db')
c = conn.cursor()

# Membuat tabel mahasiswa
c.execute('''CREATE TABLE IF NOT EXISTS mahasiswa (
    nim TEXT PRIMARY KEY,
    nama TEXT NOT NULL,
    jurusan TEXT NOT NULL
)''')

# Membuat tabel nilai
c.execute('''CREATE TABLE IF NOT EXISTS nilai (
    id_nilai INTEGER PRIMARY KEY AUTOINCREMENT,
    nim TEXT,
    tugas INTEGER,
    uts INTEGER,
    uas INTEGER,
    total INTEGER,
    rata_rata REAL,
    nilai TEXT,
    status TEXT,
    FOREIGN KEY (NIM) REFERENCES mahasiswa (NIM)
)''')

# Baca basis data
def openDB():
    conn = sqlite3.connect('rekap_nilai.db')
    conn.row_factory = sqlite3.Row
    return conn

# Halaman beranda
@rekap_nilai.route('/')
def index():
    conn = openDB()
    mhs = conn.execute('SELECT * FROM mahasiswa').fetchall()
    conn.close()
    return render_template('berandaRekapNilaiMhs.html', mhs=mhs)

# Halaman tambah data mahasiswa
@rekap_nilai.route('/add', methods=('GET', 'POST'))
def add():
    if request.method == 'POST':
        nim = request.form['nim']
        nama = request.form['nama']
        jurusan = request.form['jurusan']
        
        conn = openDB()
        conn.execute('INSERT INTO mahasiswa (nim, nama, jurusan) VALUES (?, ?, ?)', (nim, nama, jurusan))
        conn.commit()
        conn.close()
        flash('Data mahasiswa berhasil ditambahkan!')
        return redirect(url_for('index'))
    return render_template('add.html')

# Halaman tambah nilai mahasiswa
@rekap_nilai.route('/nilai/<nim>', methods=('GET','POST'))
def nilai(nim):
    conn = openDB()
    mhs = conn.execute('SELECT * FROM mahasiswa WHERE NIM = ?', (nim,)).fetchone()
    
    if request.method == 'POST':
        tugas = int(request.form['tugas'])
        uts = int(request.form['uts'])
        uas = int(request.form['uas'])
        total = tugas + uts + uas
        rata_rata = total / 3
        
        # Status nilai Lulus/Tidak Lulus/Gagal
        if (rata_rata >= 75 ):
            status = 'Lulus'
        elif ( 50 <= rata_rata >= 60):
            status = 'Tidak Lulus'
        else:
            status = 'Gagal'
        
        # Nilai huruf A/B/C/D/E
        if (rata_rata >= 85):
            nilai = 'A'
        elif (rata_rata >= 70):
            nilai = 'B'
        elif (rata_rata >= 55):
            nilai = 'C'
        elif (rata_rata >= 40):
            nilai = 'D'
        else:
            nilai = 'E'
        
        conn.execute('INSERT INTO nilai (nim, tugas, uts, uas, total, rata_rata, nilai, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (nim, tugas, uts, uas, total, rata_rata, nilai, status))
        conn.commit()
        flash('Nilai berhasil ditambahkan!')
        return redirect(url_for('nilai', nim=nim))
    
    nilai = conn.execute('SELECT * FROM nilai WHERE nim = ?', (nim,)).fetchall()
    conn.close()
    return render_template('nilai.html', mhs=mhs, nilai=nilai)

# Halaman rubah data mahasiswa
@rekap_nilai.route('/editMahasiswa/<nim>', methods=('GET', 'POST'))
def editMhs(nim):
    conn = openDB()
    mhs = conn.execute('SELECT * FROM mahasiswa WHERE nim = ?', (nim,)).fetchone()
    
    if request.method == 'POST':
        nama = request.form['nama']
        jurusan = request.form['jurusan']
        
        conn.execute('UPDATE mahasiswa SET nama = ?, jurusan = ? WHERE nim = ?', (nama, jurusan, nim))
        conn.commit()
        flash('Data mahasiswa berhasil diupdate!')
        return redirect(url_for('index'))
    
    conn.close()
    return render_template('editMhs.html', mhs=mhs)
    
# Halaman rubah data nilai
@rekap_nilai.route('/editNilai/<nim>', methods=('GET', 'POST'))
def editNilai(nim):
    conn = openDB()
    mhs = conn.execute('SELECT * FROM nilai WHERE nim = ?', (nim,)).fetchone()
    
    if request.method == 'POST':
        tugas = int(request.form['tugas'])
        uts = int(request.form['uts'])
        uas = int(request.form['uas'])
        total = tugas + uts + uas
        rata_rata = total / 3
        
        # Status nilai Lulus/Tidak Lulus/Gagal
        if (rata_rata >= 75 ):
            status = 'Lulus'
        elif ( 50 <= rata_rata >= 60):
            status = 'Tidak Lulus'
        else:
            status = 'Gagal'
        
        # Nilai huruf A/B/C/D/E
        if (rata_rata >= 85):
            nilai = 'A'
        elif (rata_rata >= 70):
            nilai = 'B'
        elif (rata_rata >= 55):
            nilai = 'C'
        elif (rata_rata >= 40):
            nilai = 'D'
        else:
            nilai = 'E'
        
        conn.execute('UPDATE nilai SET tugas = ?, uts = ?, uas = ?, total = ?, rata_rata = ?, nilai = ?, status = ? WHERE nim = ?', (tugas, uts, uas, total, rata_rata, nilai, status, nim))
        conn.commit()
        flash('Data nilai berhasil diupdate!')
        return redirect(url_for('index'))
    
    conn.close()
    return render_template('editNilai.html', mhs=mhs)

# Halaman hapus data mahasiswa
@rekap_nilai.route('/deleteMhs/<nim>', methods=('GET', 'POST'))
def deletMhs(nim):
    conn = openDB()
    conn.execute('DELETE FROM mahasiswa WHERE nim = ?', (nim,))
    conn.commit()
    conn.close()
    flash('Data mahasiswa berhasil dihapus!')
    return redirect(url_for('index'))

# Halaman hapus data nilai
@rekap_nilai.route('/deleteNilai/<nim>', methods=('GET', 'POST'))
def deletNilai(id):
    conn = openDB()
    conn.execute('DELETE FROM nilai WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Data nilai berhasil dihapus!')
    return redirect(url_for('index'))

# Halaman cari data
@rekap_nilai.route('/search', methods=('GET', 'POST'))
def search():
    query = request.form.get('query')
    conn = openDB()
    mhs = conn.execute('SELECT * FROM mahasiswa WHERE nama LIKE ? OR nim LIKE ? OR jurusan LIKE ?', ('%' + query + '%', '%' + query + '%', '%' + query + '%')).fetchall()
    conn.close()
    return render_template('berandaRekapNilaiMhs.html', mhs=mhs)

# Program utama
if __name__ == '__main__':
    rekap_nilai.run()
