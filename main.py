from flask import Flask, request, jsonify, session, redirect, url_for
import mysql.connector
from google.cloud import storage
from werkzeug.security import check_password_hash, generate_password_hash
app = Flask(__name__)
app.secret_key = 'kuncirahasia'

tempat_wisata = [
    {
        "id": 1,
        "nama": "Bedugul",
        "lokasi": "Bali",
        "alamat": "Jl. Bedugul, Desa Baturiti, Kec. Baturiti, Kabupaten Tabanan, Bali",
        "deskripsi": "Bedugul terletak di dataran tinggi di Bali, Indonesia. Salah satu daya tarik utamanya adalah Danau Bratan yang indah. Di tepi danau, Anda akan menemukan Pura Ulun Danu Bratan yang ikonik dengan arsitektur Bali khasnya. Pura ini didedikasikan untuk Dewi Danu, dewi air dan irigasi dalam kepercayaan Hindu Bali. Selain itu, Anda dapat menikmati kebun botani yang luas di sekitar danau dengan berbagai jenis tanaman eksotis. Bedugul juga terkenal dengan pasar tradisionalnya yang menjual buah-buahan segar, sayuran, dan tanaman hias."
    },
    {
        "id": 2,
        "nama": "Garuda Wisnu Kencana",
        "lokasi": "Bali",
        "alamat": "Jl. Raya Uluwatu, Ungasan, Kec. Kuta Sel., Kabupaten Badung, Bali",
        "deskripsi": "Garuda Wisnu Kencana (GWK) adalah kompleks taman budaya yang terletak di Bukit Ungasan, Bali. Daya tarik utama di GWK adalah patung raksasa Dewa Wisnu yang sedang mengendarai burung legendaris, Garuda. Patung ini merupakan salah satu patung terbesar di dunia dengan tinggi sekitar 121 meter. Selain patung Dewa Wisnu, Anda juga dapat menikmati pemandangan panorama yang menakjubkan dari bukit ini. Di kompleks GWK, terdapat teater terbuka yang sering digunakan untuk pertunjukan seni dan budaya Bali."
    },
    {
        "id": 3,
        "nama": "Ground Zero",
        "lokasi": "Bali",
        "alamat": "Jl. Legian, Kuta, Kabupaten Badung, Bali",
        "deskripsi": "Monumen Bajra Sandi adalah monumen perjuangan yang terletak di Denpasar, Bali. Monumen ini didedikasikan untuk mengenang perjuangan rakyat Bali dalam melawan penjajahan. Bajra Sandi memiliki arsitektur yang menakjubkan dan merupakan landmark penting di Bali. Di dalam monumen, terdapat museum yang menyajikan koleksi bersejarah dan lukisan yang menggambarkan sejarah Bali dan perjuangannya.."
    },
    {
        "id": 4,
        "nama": "Monumen Bajra Sandi",
        "lokasi": "Bali",
        "alamat": "Jl. Raya Puputan No.142, Renon, Kec. Denpasar Tim., Kota Denpasar, Bali",
        "deskripsi": "Patung Dewa Runci terletak di Ubud, Bali. Patung ini menggambarkan Dewa Ruci, tokoh dalam cerita pewayangan Ramayana. Patung ini memiliki tinggi sekitar 25 meter dan terbuat dari beton. Patung Dewa Ruci menjadi ikon kota Ubud dan menarik banyak wisatawan untuk mengagumi keindahannya.."
    },
    {
        "id": 5,
        "nama": "Patung Dewa Runci",
        "lokasi": "Bali",
        "alamat": "Jl. Raya Legian, Legian, Kec. Kuta, Kabupaten Badung, Bali",
        "deskripsi": "Patung dewa yang terkenal di Kuta, Bali."
    },
    {
        "id": 6,
        "nama": "Patung Nakula Sadewa",
        "lokasi": "Bali",
        "alamat": "Jl. Raya Uluwatu, Ungasan, Kec. Kuta Sel., Kabupaten Badung, Bali",
        "deskripsi": "Patung Nakula Sadewa juga terletak di Ubud, Bali. Patung ini menggambarkan dua tokoh pewayangan, Nakula dan Sadewa, yang merupakan saudara kembar dalam cerita Mahabharata. Patung ini menjadi simbol persahabatan dan kesetiaan. Dengan tinggi sekitar 15 meter, patung ini menjadi daya tarik unik di Ubud."
    },
    {
        "id": 7,
        "nama": "Patung Satria Gatotkaca",
        "lokasi": "Bali",
        "alamat": "Jl. Raya Uluwatu, Ungasan, Kec. Kuta Sel., Kabupaten Badung, Bali",
        "deskripsi": "Patung Satria Gatotkaca terletak di Desa Batubulan, Bali. Patung ini menggambarkan tokoh pewayangan, Gatotkaca, yang merupakan pahlawan dalam cerita Mahabharata. Patung ini menjadi simbol keberanian dan kekuatan. Pengunjung dapat mengagumi keindahan patung ini yang terbuat dari batu dan memiliki tinggi sekitar 20 meter."
    },
    {
        "id": 8,
        "nama": "Tanah Lot",
        "lokasi": "Bali",
        "alamat": "Beraban, Kec. Kediri, Kabupaten Tabanan, Bali",
        "deskripsi": "Tanah Lot adalah sebuah pura laut yang terletak di atas batu karang di pesisir barat Bali. Daya tarik utama dari Tanah Lot adalah keindahan alamnya dan pemandangan matahari terbenam yang menakjubkan. Selain itu, pura ini juga memiliki nilai spiritual dan merupakan tempat suci bagi umat Hindu Bali. Anda dapat menjelajahi kompleks pura, menikmati pemandangan laut, dan berinteraksi dengan para pendeta dan pengunjung lainnya."
    },
    {
        "id": 9,
        "nama": "Vihara Dharma Giri",
        "lokasi": "Bali",
        "alamat": "Jl. Bedugul, Desa Candikuning, Kec. Baturiti, Kabupaten Tabanan, Bali",
        "deskripsi": "Vihara Dharma Giri adalah sebuah vihara Buddha yang terletak di desa Pupuan, Bali. Vihara ini dikelilingi oleh pemandangan alam yang indah, termasuk sawah, pegunungan, dan sungai. Tempat ini menawarkan ketenangan dan kedamaian bagi para pengunjung yang ingin bermeditasi atau mempelajari ajaran Buddha. Anda dapat menjelajahi vihara ini, mengagumi arsitektur dan seni yang khas, serta menikmati suasana spiritual yang tenang."
    },
]

@app.route('/')
def home():
    return 'Selamat datang!'

# Konfigurasi database
db = mysql.connector.connect(
    host="34.128.71.133", # Ganti sesuai dengan pengaturan database phpMyAdmin
    user="root", # Ganti sesuai dengan pengaturan database phpMyAdmin 
    password="rootlens123", # Ganti sesuai dengan pengaturan database phpMyAdmin
    database="travellens-app-db" # Ganti sesuai dengan pengaturan database phpMyAdmin
)

# Konfigurasi Google Cloud Storage
storage_client = storage.Client.from_service_account_json('travellensapp-fefd9f0826d5.json')
bucket_name = 'foto-user-travellens'

# Route untuk login
@app.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']

    cursor = db.cursor()

    # Query untuk memeriksa keberadaan username dan password di database
    query = "SELECT * FROM users WHERE username = %s AND password = %s"
    values = (username, password)
    cursor.execute(query, values)
    row = cursor.fetchone()

    if row:
        session['username'] = row[1]
        data = {
            'id': row[0],
            'username': row[1],
            'email': row[3],
            'photo': row[4],
            'address': row[5],
            'phone': row[6]
        }
        resp = jsonify({'status': 'success', 'data': data})
        resp.status_code = 200
        return resp
    else:
        resp = jsonify({'status': 'failed', 'message': 'Login gagal! Password atau username tidak ditemukan.'})
        resp.status_code = 400
        return resp

# Route untuk registrasi
@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    email = request.json.get('email')
    password = request.json.get('password')
    confirm_password = request.json.get('confirm_password')

    cursor = db.cursor()

    # Memeriksa apakah password dan konfirmasi password cocok
    if password != confirm_password:
        return jsonify({'message': 'Password dan konfirmasi password tidak cocok'}), 400

    # Query untuk memeriksa apakah username atau email sudah digunakan
    check_query = "SELECT * FROM users WHERE username = %s OR email = %s"
    check_values = (username, email)
    cursor.execute(check_query, check_values)
    _ = cursor.fetchall()  # Membaca dan mengonsumsi hasil query sebelumnya

    # Memeriksa hasil query
    if cursor.rowcount > 0:
        # Jika username atau email sudah ada, kirimkan pesan gagal
        return jsonify({'message': 'Username atau email sudah digunakan!'})

    # Jika username atau email belum digunakan, lakukan registrasi
    insert_query = "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)"
    insert_values = (username, password, email)
    cursor.execute(insert_query, insert_values)
    db.commit()

    # Registrasi berhasil, kirimkan pesan berhasil
    return jsonify({'message': 'Registrasi berhasil!'})

# Route untuk edit profile
@app.route('/profile/edit/<int:user_id>', methods=['PUT'])
def edit_profile(user_id):
    cursor = db.cursor()

    # Mendapatkan data yang akan diupdate dari body permintaan
    data = request.get_json()
    new_username = data.get('username')
    new_email = data.get('email')
    new_address = data.get('address')
    new_phone = data.get('phone')

    # Mengecek apakah user dengan user_id tertentu ada di database
    query_check_user = "SELECT * FROM users WHERE id = %s"
    cursor.execute(query_check_user, (user_id,))
    user = cursor.fetchone()
    if not user:
        return jsonify({'message': 'User not found'}), 404

    # Mengupdate data pengguna dalam database
    query_update_user = "UPDATE users SET username = %s, email = %s, address = %s, phone = %s WHERE id = %s"
    cursor.execute(query_update_user, (new_username, new_email, new_address, new_phone, user_id))
    db.commit()

    # Mengambil data terbaru dari database
    query_get_user = "SELECT * FROM users WHERE id = %s"
    cursor.execute(query_get_user, (user_id,))
    updated_user = cursor.fetchone()

    # Menyiapkan respons JSON dengan data terbaru
    profile = {
        'username': updated_user[1],
        'email': updated_user[3],
        'address': updated_user[5],
        'phone': updated_user[6],
        'photo': updated_user[4]
    }
    return jsonify(profile)

# Route untuk edit photo profile
@app.route('/profile/edit/photo/<int:user_id>', methods=['PUT'])
def edit_photo_profile(user_id):
    cursor = db.cursor()

    # Mengecek apakah user dengan user_id tertentu ada di database
    query_check_user = "SELECT * FROM users WHERE id = %s"
    cursor.execute(query_check_user, (user_id,))
    user = cursor.fetchone()
    if not user:
        return jsonify({'message': 'User not found'}), 404

    # Mengunggah foto baru ke Google Cloud Storage
    file = request.files.get('photo')
    if file:
        filename = f"profile_{user_id}.jpg"  # otomatis mengatur nama file sesuai dengan ID pengguna
        blob = storage_client.bucket(bucket_name).blob(filename)
        blob.upload_from_file(file)

        # Mengupdate nama file foto di database
        query_update_photo = "UPDATE users SET photo = %s WHERE id = %s"
        cursor.execute(query_update_photo, (filename, user_id))
        db.commit()

    # Mengambil data terbaru dari database
    query_get_user = "SELECT * FROM users WHERE id = %s"
    cursor.execute(query_get_user, (user_id,))
    updated_user = cursor.fetchone()

    # Menyiapkan respons JSON dengan data terbaru
    profile = {
        'username': updated_user[1],
        'email': updated_user[3],
        'address': updated_user[5],
        'phone': updated_user[6],
        'photo': updated_user[4]
    }
    return jsonify(profile)


# Route untuk profile
@app.route('/profile', methods=['GET'])
def get_profile():
    # Mendapatkan data pengguna dari database
    user_id = request.args.get('user_id')  # Mendapatkan ID pengguna dari parameter URL
    cur = mysql.connector.connect()
    cur.execute("SELECT * FROM users WHERE id=%s", (user_id,))
    result = cur.fetchone()
    cur.close()

    if not result:
        return jsonify({'message': 'Pengguna tidak ditemukan'}), 404

    # Mendapatkan informasi nama depan dan alamat pengguna
    first_name = result['username']
    address = result['address']

    # Mengambil URL foto profil dari Google Cloud Storage
    filename = f"profile_{user_id}.jpg"  # otomatis mengatur nama file sesuai dengan ID pengguna
    blob = storage_client.bucket(bucket_name).blob(filename)
    photo_url = blob.public_url

    # Mengembalikan respons dengan informasi pengguna
    return jsonify({
        'message': f'Halo, {first_name}',
        'address': address,
        'photo_url': photo_url
    }), 200

@app.route('/wisata', methods=['GET'])
def daftar_wisata():
    daftar_tempat_wisata = []
    for tempat in tempat_wisata:
        info_tempat = {
            'id': tempat['id'],
            'nama': tempat['nama'],
            'lokasi': tempat['lokasi'],
            'alamat': tempat['alamat'],
            'deskripsi': tempat['deskripsi']
        }
        daftar_tempat_wisata.append(info_tempat)
    return jsonify(daftar_tempat_wisata)


@app.route('/wisata/<int:id>', methods=['GET'])
def detail_wisata(id):
    for tempat in tempat_wisata:
        if tempat['id'] == id:
            return jsonify({
                'nama': tempat['nama'],
                'lokasi': tempat['lokasi'],
                'alamat': tempat['alamat'],
                'deskripsi': tempat['deskripsi']
            })
    return jsonify({'message': 'Wisata tidak ditemukan.'}), 404

@app.route('/wisata/search', methods=['GET'])
def cari_wisata():
    query = request.args.get('query')

    if query:
        hasil_pencarian = []
        for tempat in tempat_wisata:
            if query.lower() in tempat['nama'].lower() or query.lower() in tempat['lokasi'].lower() or query.lower() in tempat['alamat'].lower() or query.lower() in tempat['deskripsi'].lower():
                hasil_pencarian.append({
                    'nama': tempat['nama'],
                    'lokasi': tempat['lokasi'],
                    'alamat': tempat['alamat'],
                    'deskripsi': tempat['deskripsi']
                })

        return jsonify(hasil_pencarian)


if __name__ == '__main__':
    app.run()
