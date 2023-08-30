from flask import Flask, request, redirect
import spotipy
from spotipy.oauth2 import SpotifyOAuth

app = Flask(__name__)

@app.route('/')
def index():
    html_form = '''
    <html>
    <head>
        <style>
            body {
                background-image: url('"D:\Personal_Project\game\image.jpg"'); /* Replace with your image URL */
                background-size: cover;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            form {
                background-color: rgba(255, 255, 255, 0.7);
                padding: 20px;
                border-radius: 10px;
                text-align: center;
            }
            input[type="text"] {
                width: 100%;
                padding: 10px;
                margin-bottom: 10px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            input[type="submit"] {
                background-color: #fddb3a;
                color: #000;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                cursor: pointer;
            }
        </style>
    </head>
    <body>
        <form method="post" action="/create_playlist">
            <label for="song_name">Enter Song Name:</label><br>
            <input type="text" name="song_name"><br>
            <label for="artist_name">Enter Artist Name:</label><br>
            <input type="text" name="artist_name"><br>
            <input type="submit" value="Create Playlist">
        </form>
    </body>
    </html>
    '''
    return html_form

@app.route('/create_playlist', methods=['POST'])
def create_playlist():
    song_name = request.form.get('song_name')
    artist_name = request.form.get('artist_name')
    
    sp_oauth = SpotifyOAuth(
        client_id='02e1f0ea5b3945ec8dd3ade27a7c838c',
        client_secret='ca325c1f7bef43699e68730f6964f0f8',
        redirect_uri='http://localhost:5000/callback',
        scope='playlist-modify-public'
    )
    
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url + '&state=' + song_name + '|' + artist_name)

@app.route('/callback')
def callback():
    sp_oauth = SpotifyOAuth(
        client_id='02e1f0ea5b3945ec8dd3ade27a7c838c',
        client_secret='ca325c1f7bef43699e68730f6964f0f8',
        redirect_uri='http://localhost:5000/callback'
    )
    token_info = sp_oauth.get_access_token(request.args['code'])
    sp = spotipy.Spotify(auth=token_info['access_token'])
    
    # Retrieve user ID
    user_info = sp.current_user()
    user_id = user_info['id']
    
    # Use the spotipy library to search for the entered song and artist
    song_name, artist_name = request.args.get('state').split('|')
    query = f'track:{song_name} artist:{artist_name}'
    results = sp.search(q=query, type='track', limit=1)
    
    if results['tracks']['items']:
        track_id = results['tracks']['items'][0]['id']
        
        # Create a new playlist
        playlist_name = "Recommended Playlist"
        playlist_description = f"Playlist based on {song_name} by {artist_name}"
        playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=True, description=playlist_description)
        
        # Get recommended tracks based on the entered song
        recommended_tracks = sp.recommendations(seed_tracks=[track_id], limit=10)
        track_ids = [track['id'] for track in recommended_tracks['tracks']]
        
        # Add recommended tracks to the playlist
        sp.playlist_add_items(playlist_id=playlist['id'], items=track_ids)
        
        return "Playlist created successfully!"
    
    return "Song not found."

if __name__ == '__main__':
    app.run(host='localhost', port=5000)
