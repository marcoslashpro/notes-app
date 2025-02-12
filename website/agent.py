from .jarvis import Jarvis
from flask import Blueprint, render_template, Response, stream_with_context, jsonify, request
from flask_login import login_required, current_user
import ollama


agent = Blueprint('agent', __name__)
jarvis = Jarvis(
    model='smollm:360m')


@agent.route('/talk-ai', methods=["POST"])
def talk():
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