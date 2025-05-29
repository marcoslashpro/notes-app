from app.website.jarvis.jarvis import Jarvis
from flask import Blueprint, Response, stream_with_context, jsonify, request


agent = Blueprint('agent', __name__)
jarvis = Jarvis(
    model='smollm2:1.7b'
    )


@agent.route('/talk-ai', methods=["POST"])
def talk() -> Response:
    data = request.get_json()
    query = data['query']

    if not data or 'query' not in data:
        return jsonify({
            "error": "Missing 'query' field"
            })

    def generate_response():
        for chunk in jarvis.stream_response(query):
            yield chunk
        yield ""

    return Response(stream_with_context(generate_response()), content_type="text/plain")
