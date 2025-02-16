from flask import Flask, request, jsonify
import hashlib

app = Flask(__name__)

@app.route('/hash', methods=['POST'])
def hash_string():
    input_data = request.get_data(as_text=True).strip()
    if not input_data:
        return "No input provided", 400
    
    sha256_hash = hashlib.sha256(input_data.encode()).hexdigest()
    return sha256_hash

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
