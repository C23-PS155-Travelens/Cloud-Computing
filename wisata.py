from flask import Flask, jsonify, request
from flask import Blueprint

wisata_blueprint = Blueprint('wisata', __name__)
app = Flask(__name__)

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

@app.route('/wisata', methods=['GET'])
def daftar_wisata():
    daftar_nama_wisata = [tempat['nama'] for tempat in tempat_wisata]
    return jsonify(daftar_nama_wisata)

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
    app.run(debug=True)
