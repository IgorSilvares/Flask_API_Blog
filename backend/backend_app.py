from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    sort = request.args.get('sort')
    direction = request.args.get('direction')

    if sort and direction:
        if sort not in ['title', 'content']:
            return jsonify({'error': 'Invalid sort parameter'}), 400
        if direction not in ['asc', 'desc']:
            return jsonify({'error': 'Invalid direction parameter'}), 400

        if direction == 'asc':
            sorted_posts = sorted(POSTS, key=lambda x: x[sort])
        else:
            sorted_posts = sorted(POSTS, key=lambda x: x[sort], reverse=True)
        
        return jsonify(sorted_posts), 200
    else:
        return jsonify(POSTS), 200

@app.route('/api/posts', methods=['POST'])
def add_post():
    data = request.get_json()

    if 'title' not in data or 'content' not in data or not data['title'].strip() or not data['content'].strip():
        return jsonify({'error': 'Title or content missing'}), 400

    title = data['title']
    content = data['content']
    
    POSTS.append({'id': len(POSTS) + 1, 'title': title, 'content': content})

    return jsonify({'id': len(POSTS), 'title': title, 'content': content}), 201


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    for post in POSTS:
        if post['id'] == post_id:
            POSTS.remove(post)
            return jsonify({'message': 'Post with id ' + str(post_id) +  ' has been deleted successfully'}), 200
    return jsonify({'error': 'Post not found'}), 404


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    data = request.get_json()

    if 'title' not in data:
        data['title'] = POSTS[post_id - 1]['title']

    if 'content' not in data:
        data['content'] = POSTS[post_id - 1]['content']

    for post in POSTS:
        if post['id'] == post_id:
            post['title'] = data['title']
            post['content'] = data['content']
            return jsonify({'message': 'Post with id ' + str(post_id) +  ' has been updated successfully'}), 200
    return jsonify({'error': 'Post not found'}), 404


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    query_title = request.args.get('title')
    query_content = request.args.get('content')
    results = []
    for post in POSTS:
        if query_title and query_title.lower() in post['title'].lower():
            results.append(post)
        elif query_content and query_content.lower() in post['content'].lower():
            results.append(post)
    return jsonify(results)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
