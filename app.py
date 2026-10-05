import os
from flask import Flask, render_template, request, jsonify
import ollama

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    user_text = data.get('text', '').strip()

    if not user_text:
        return jsonify({'error': 'Please enter text'}), 400

    try:
        prompt = f"Simplify the following text for sign language translation: {user_text}"
        
        response = ollama.chat(model='gemma:2b', messages=[
            {'role': 'user', 'content': prompt}
        ])
        
        simplified_text = response['message']['content'].strip()

        formatted_chars = [char.upper() for char in user_text if char.isalpha()]

        image_paths = []
        for char in formatted_chars:
            image_name = f"{char}.webp"
            full_path = os.path.join(app.root_path, 'static', 'images', image_name)
            
            if os.path.exists(full_path):
                image_paths.append(f"/static/images/{image_name}")

        return jsonify({
            'original': user_text,
            'simplified': simplified_text,
            'images': image_paths
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
    