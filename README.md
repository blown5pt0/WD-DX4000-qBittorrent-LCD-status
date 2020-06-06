# WD-DX4000-QBittorrent-LCDStatus
### Display transfer stats from qBittorrent on the DX4000's LCD

At the moment, cycles between two very basic sets of info: Current Up/Down transfer rate and Session Total Uploaded/Downloaded.. For example:

```
UP:512Kbps
DN:1400Kbps
```
```
UP:4000MB
DN:16000MB
```

- Requires Python 3
- Only tested with WD DX4000 NAS
- Works with qBittorrent v3.5 and higher

# Install

- Enable qBittorrent WebUI and set authentication parameters
- Copy `.env_example` to `.env` and update parameters to match Web UI setup
- Install dependencies with `pip install -r requirements.txt`
- Start script with `python qbt_lcd_driver.py`

To exit the script, use CTRL + C



