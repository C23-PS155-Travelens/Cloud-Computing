from flask import Flask
from auth import auth_blueprint
from wisata import wisata_blueprint

app = Flask(__name__)

# Daftarkan blueprint auth
app.register_blueprint(auth_blueprint)

# Daftarkan blueprint wisata
app.register_blueprint(wisata_blueprint)

@app.route('/')
def hello():
    return 'API berhasil'

if __name__ == '__main__':
    app.run()
