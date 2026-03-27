from flask import Flask, render_template, request, jsonify
from Crypto.Cipher import DES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad, unpad
import base64

app = Flask(__name__)

# RSA Keys
rsa_key = RSA.generate(2048)
private_key = rsa_key
public_key = rsa_key.publickey()

# DES Key
DES_KEY = b'8bytekey'

# Caesar
def caesar(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            base = 65 if char.isupper() else 97
            result += chr((ord(char) - base + shift) % 26 + base)
        else:
            result += char
    return result

@app.route('/')
def home():
    return render_template('index.html')

# Caesar API
@app.route('/caesar', methods=['POST'])
def caesar_route():
    data = request.json
    text = data['text']
    shift = int(data['shift'])

    encrypted = caesar(text, shift)
    decrypted = caesar(encrypted, -shift)

    return jsonify({
        "encrypted": encrypted,
        "decrypted": decrypted
    })

# DES API
@app.route('/des', methods=['POST'])
def des_route():
    data = request.json
    text = data['text']

    cipher = DES.new(DES_KEY, DES.MODE_ECB)

    try:
        encrypted = cipher.encrypt(pad(text.encode(), 8))
        encrypted_b64 = base64.b64encode(encrypted).decode()

        decrypted = unpad(cipher.decrypt(encrypted), 8).decode()

        return jsonify({
            "encrypted": encrypted_b64,
            "decrypted": decrypted
        })
    except:
        return jsonify({"error": "DES Error"})

# RSA API
@app.route('/rsa', methods=['POST'])
def rsa_route():
    data = request.json
    text = data['text']

    try:
        cipher_enc = PKCS1_OAEP.new(public_key)
        encrypted = cipher_enc.encrypt(text.encode())
        encrypted_b64 = base64.b64encode(encrypted).decode()

        cipher_dec = PKCS1_OAEP.new(private_key)
        decrypted = cipher_dec.decrypt(encrypted).decode()

        return jsonify({
            "encrypted": encrypted_b64,
            "decrypted": decrypted
        })
    except:
        return jsonify({"error": "RSA Error"})

if __name__ == "__main__":
    app.run(debug=True)