import qbittorrentapi
import subprocess
import time
from dotenv import load_dotenv
load_dotenv()
import os

# Function to convert the transfer total values to a human-readable format
def format_xfer_total(bytes):
    power = 2**10
    n = 0
    power_labels = {0 : 'B', 1: 'KB', 2: 'MB', 3: 'GB', 4: 'TB'}
    return_formats = {0: "{:.0f}", 1: "{:.0f}", 2: "{:.0f}", 3: "{:.2f}", 4: "{:.2f}"}
    while bytes > power:
        bytes /= power
        n += 1
    return return_formats[n].format(bytes) + power_labels[n]

# Function to convert the transfer rate value to a human-readable format
def format_xfer_rate(bytes_per_sec):
    if bytes_per_sec > 0:
        power = 2**10
        n = 0
        power_labels = {0 : 'B/s', 1: 'KB/s', 2: 'MB/s'}
        return_formats = {0: "{:.0f}", 1: "{:.0f}", 2: "{:.2f}"}
        while bytes_per_sec > power:
            bytes_per_sec /= power
            n += 1
        return return_formats[n].format(bytes_per_sec) + power_labels[n]
    else:
        return 'Idle'

# Initialize the qBittorrent API client
qbt_client = qbittorrentapi.Client(host=os.getenv('WEBUI_HOST') + ':' + os.getenv('WEBUI_PORT'), username=os.getenv('WEBUI_USER'), password=os.getenv('WEBUI_PASSWORD'))

# Authenticate with the API
try:
    qbt_client.auth_log_in()
except qbittorrentapi.LoginFailed as e:
    print('An error was encountered while trying to connect to the qBittorrent API:')
    print(e)

# display connected qBittorrent version info
print('Connected to:')
print(f'qBittorrent: {qbt_client.app.version}')
print(f'qBittorrent Web API: {qbt_client.app.web_api_version}')

# Define WD LCD API exe
lcd_api_exe = os.getenv('LCD_API_EXE')

print('LCD update process running - Press [CTRL] + C to terminate.')

# Main loop
while True:
    # Fetch list of loaded torrents
    torrent_list = qbt_client.torrents_info()
    seeding_count = 0
    downloading_count = 0
    checking_count = 0
    # Count torrent states
    for torrent in torrent_list:
        if torrent.state == 'forcedUP' or torrent.state == 'uploading':
            seeding_count += 1
        elif torrent.state == 'downloading' or torrent.state == 'stalledDL':
            downloading_count += 1
        elif torrent.state == 'checkingUP' or torrent.state == 'checkingDL':
            checking_count += 1
    # Cycle between the three information displays. Display each for 5 seconds while updating the values every second.
    for i in range(5):
        # Current Upload and Download transfer rates
        # UP:32Mbps
        # DN:150Mbps
        #
        transfer_info = qbt_client.transfer_info()
        upload_speed = format_xfer_rate(transfer_info.up_info_speed)
        download_speed = format_xfer_rate(transfer_info.dl_info_speed)
        line1 = "UP: {up_speed}".format(up_speed=upload_speed)
        line2 = "DN: {dl_speed}".format(dl_speed=download_speed)
        # update LCD
        subprocess.run([lcd_api_exe, '0', line1])
        subprocess.run([lcd_api_exe, '1', line2])
        time.sleep(1)

    for i in range(5):
        # Current Upload and Download transfer totals for session
        # UP:1.90GB
        # DN:69.34GB
        #
        transfer_info = qbt_client.transfer_info()
        upload_total = format_xfer_total(transfer_info.up_info_data)
        download_total = format_xfer_total(transfer_info.dl_info_data)
        line3 = "UP: {up_total}".format(up_total=upload_total)
        line4 = "DN: {dl_total}".format(dl_total=download_total)
        # update LCD
        subprocess.run([lcd_api_exe, '0', line3])
        subprocess.run([lcd_api_exe, '1', line4])
        time.sleep(1)

    for i in range(5):
        # Display torrent state counts -- S = seeding, D = downloading, V = verifying/checking, A = all
        # S:40 D:10
        # V:0 A:50
        #
        line5 = "S: {seed_count}  D: {download_count}".format(seed_count=seeding_count,download_count=downloading_count)
        line6 = "V: {verify_total}  A: {all_count}".format(verify_total=checking_count,all_count=len(torrent_list))
        # update LCD
        subprocess.run([lcd_api_exe, '0', line5])
        subprocess.run([lcd_api_exe, '1', line6])
        time.sleep(1)