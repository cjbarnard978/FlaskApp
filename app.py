
from flask import Flask
import sqlite3

app = Flask(__name__)

@app.route('/saints')
def show_saints():
    conn = sqlite3.connect('scotsirishsaints.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute('SELECT * FROM saints')  # Change 'saints' to your actual table name
    rows = cur.fetchall()
    html = '<table border="1">'
    html += '<tr>' + ''.join(f'<th>{col}</th>' for col in rows[0].keys()) + '</tr>' if rows else ''
    for row in rows:
        html += '<tr>' + ''.join(f'<td>{row[col]}</td>' for col in row.keys()) + '</tr>'
    html += '</table>'
    return html if rows else 'No data found.'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)