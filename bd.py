from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Создание базы данных при старте
def init_db():
    conn = sqlite3.connect('deletedModal.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS deleted_rows (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticker TEXT NOT NULL,
        link TEXT,
        result TEXT,
        reason TEXT,
        dir TEXT,
        tf TEXT
    )
    ''')
    conn.commit()
    conn.close()

@app.route('/api/deleted_rows', methods=['GET'])
def get_deleted_rows():
    conn = sqlite3.connect('deletedModal.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM deleted_rows')
    rows = cursor.fetchall()
    conn.close()

    # Преобразуем в список словарей
    result = [
        {"id": row[0], "ticker": row[1], "link": row[2], "result": row[3], "reason": row[4], "dir": row[5], "tf": row[6]}
        for row in rows
    ]
    return jsonify(result)

@app.route('/api/deleted_rows', methods=['POST'])
def add_deleted_row():
    data = request.json
    ticker = data.get("ticker")
    link = data.get("link")
    result = data.get("result")
    reason = data.get("reason")
    dir = data.get("dir")
    tf = data.get("tf")

    conn = sqlite3.connect('deletedModal.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO deleted_rows (ticker, link, result, reason, dir, tf)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (ticker, link, result, reason, dir, tf))
    conn.commit()
    conn.close()

    return jsonify({"message": "Row added successfully"}), 201

@app.route('/api/deleted_rows/<int:row_id>', methods=['DELETE'])
def delete_deleted_row(row_id):
    conn = sqlite3.connect('deletedModal.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM deleted_rows WHERE id = ?', (row_id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Row deleted successfully"})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)