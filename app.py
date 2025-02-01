from flask import Flask, render_template, jsonify, session, redirect, url_for, request, render_template_string
from datetime import datetime
import folium

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for sessions

@app.route('/')
def home():
    current_user = session.get('user')
    return render_template('dashboard.html', current_user=current_user)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    session['user'] = data.get('username')
    return jsonify({'success': True})

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

@app.route('/get_time')
def get_time():
    current_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    return jsonify({'datetime': current_time})

@app.route('/map')
def map_view():
    lat, lon = 17.6128, 78.4803
    
    # Create a Folium map centered at the given coordinates
    map = folium.Map(location=[lat, lon], zoom_start=15)
    folium.Marker([lat, lon], popup="Medchal, Hyderabad").add_to(map)

    # Generate the map HTML
    map_html = map._repr_html_()

    # Render the map HTML within a simple template
    return render_template_string("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>GPS Map</title>
        </head>
        <body>
            <h1>GPS Map</h1>
            <div>{{ map_html|safe }}</div>
        </body>
        </html>
    """, map_html=map_html)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=500)
