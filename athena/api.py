from flask import Flask, request, jsonify
from athena.input_processor import process_input

app = Flask(__name__)


@app.route('/api/v1/athena', methods=['POST'])
def athena_chat():
    data = request.get_json(force=True)
    user_input = data.get('input')
    username = data.get('username', None)

    if user_input:
        response = process_input(user_input, username)
        return jsonify({'response': response})
    else:
        return jsonify({'error': 'Missing input'}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
