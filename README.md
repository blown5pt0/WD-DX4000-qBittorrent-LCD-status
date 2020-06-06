# WD-DX4000-QBittorrent-LCDStatus
### Display transfer stats from qBittorrent on the DX4000's LCD

At the moment, cycles between three basic sets of info: 
- Current up/down transfer rate
    ```
    UP: 155KB/s
    DN: 12.5MB/s
    ```
- Session total uploaded/downloaded
     ```
    UP: 380MB
    DN: 16.51GB
    ```
- Torrent counts (S: Seeding, D: Downloading, V: Verifying/Checking, A: All Torrents)
    ```
    S: 120  D: 200  
    V: 000  A: 140
    ```

### Requirements
- Python 3
- WD DX4000 NAS running Windows Storage Server 2008
- qBittorrent v3.5 and higher

# Install

- Enable WebUI within qBittorrent and set authentication parameters
- Copy `.env_example` to `.env` and update parameters to match those used during Web UI setup
- Install dependencies with `pip install -r requirements.txt`
- Start script with `python qbt_lcd_driver.py`
