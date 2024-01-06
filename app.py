from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)  

conn = sqlite3.connect('building_planner.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS shapes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT,
        x INTEGER,
        y INTEGER,
        annotation TEXT
    )
''')
conn.commit()
conn.close()

@app.route('/save_shape', methods=['POST'])
def save_shape():
    try:
        # Check if the request has the correct content type
        if request.is_json:
            data = request.get_json()
            conn = sqlite3.connect('building_planner.db')
            cursor = conn.cursor()
            cursor.executemany('''
                INSERT INTO shapes (type, x, y, annotation) VALUES (?, ?, ?, ?)
            ''', [(shape['type'], shape['x'], shape['y'], shape['annotation']) for shape in data])
            conn.commit()
            conn.close()
            return jsonify({'message': 'Shapes saved successfully'}), 200
        else:
            return jsonify({'error': 'Invalid content type, expected application/json'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
