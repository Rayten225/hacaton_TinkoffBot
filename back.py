from flask import Flask, request, jsonify
from gpt import generate_message
app = Flask(__name__)
@app.route('/assist', methods=['POST'])
def assist():
    data = request.get_json()

    if not data or 'query' not in data:
        return jsonify({
            "detail": [
                {
                    "loc": ["body", "query"],
                    "msg": "field required",
                    "type": "value_error.missing"
                }
            ]
        }), 422

    query = data['query']
    response_text = generate_message('query')
    response_links = ["https://www.tinkoff.ru/"]

    return jsonify({
        "text": response_text,
        "links": response_links
    }), 200

if __name__ == '__main__':
    app.run(debug=True)
