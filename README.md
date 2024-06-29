
# UpdatePlaylistPondere

UpdatePlaylistPondere is a Python application designed to enhance the Spotify experience by dynamically prioritizing tracks in user playlists based on their addition dates. The app ensures newer tracks are played more often while maintaining a mix of older favorites.

## Features

- **Track Retrieval and Analysis:** Retrieves all tracks from a specified playlist and analyzes their addition dates.
- **Dynamic Prioritization:** Tracks are weighted based on how recently they were added:
  - Tracks added within the last two weeks are played more frequently.
  - Tracks added within the last month are played less frequently.
  - Tracks added within the last six months are played even less frequently.
  - Tracks added within the last year are played rarely.
  - Tracks added more than a year ago are played the least.
- **Playlist Management:** Updates the user's playlist by reordering tracks according to their weights.

## Requirements

- Python 3.x
- `spotipy` library

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/baptistegoncalves/UpdatePlaylistPondere.git
   cd UpdatePlaylistPondere
   ```

2. Install the required Python packages:

   ```sh
   pip install spotipy
   ```

3. Set up your Spotify Developer credentials by creating an app on the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications). Make sure to note your `client_id`, `client_secret`, and set the `redirect_uri` to `http://localhost:8888/callback`.

## Usage

1. Replace the placeholder values in the script with your Spotify Developer credentials and playlist IDs:

   ```python
   sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
       client_id='YOUR_CLIENT_ID',
       client_secret='YOUR_CLIENT_SECRET',
       redirect_uri='http://localhost:8888/callback',
       scope='playlist-read-private playlist-modify-private'
   ))

   original_playlist_id = 'YOUR_ORIGINAL_PLAYLIST_ID'
   weighted_playlist_id = 'YOUR_WEIGHTED_PLAYLIST_ID'
   ```

2. Run the script:

   ```sh
   python3 update_playlist.py
   ```

## How It Works

1. **Authentication:** The script uses OAuth 2.0 to authenticate with Spotify.
2. **Track Retrieval:** The `get_playlist_tracks` function retrieves all tracks from the original playlist.
3. **Weight Calculation:** The `weight_tracks` function calculates weights for each track based on their addition dates.
4. **Playlist Update:** The `update_weighted_playlist` function updates the weighted playlist by reordering tracks according to their weights.

## Contributing

Feel free to fork the repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

If you have any questions or suggestions, please open an issue or contact me directly through GitHub.
