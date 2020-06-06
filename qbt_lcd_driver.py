import qbittorrentapi
import subprocess
import time
from dotenv import load_dotenv
load_dotenv()
import os

def format_bytes(size):
    power = 2**10
    n = 0
    power_labels = {0 : 'B', 1: 'KB', 2: 'MB', 3: 'GB', 4: 'TB'}
    return_formats = {0: "{:.0f}", 1: "{:.0f}", 2: "{:.0f}", 3: "{:.2f}", 4: "{:.2f}"}
    while size > power:
        size /= power
        n += 1
    return return_formats[n].format(size) + power_labels[n]

def format_bps(bps):
    power = 2**10
    n = 0
    power_labels = {0 : 'bps', 1: 'Kbps', 2: 'Mbps'}
    return_formats = {0: "{:.0f}", 1: "{:.0f}", 2: "{:.2f}"}
    while bps > power:
        bps /= power
        n += 1
    return return_formats[n].format(bps) + power_labels[n]

qbt_client = qbittorrentapi.Client(host=os.getenv('WEBUI_HOST') + ':' + os.getenv('WEBUI_PORT'), username=os.getenv('WEBUI_USER'), password=os.getenv('WEBUI_PASSWORD'))

try:
    qbt_client.auth_log_in()
except qbittorrentapi.LoginFailed as e:
    print(e)

# display qBittorrent info
print(f'qBittorrent: {qbt_client.app.version}')
print(f'qBittorrent Web API: {qbt_client.app.web_api_version}')

lcd_api_exe = os.getenv('LCD_API_EXE')
print('LCD update process running...')
while True:
    torrent_list = qbt_client.torrents_info()
    seeding_count = 0
    downloading_count = 0
    checking_count = 0
    for torrent in torrent_list:
        if torrent.state == 'forcedUP' or torrent.state == 'uploading':
            seeding_count += 1
        elif torrent.state == 'downloading' or torrent.state == 'stalledDL':
            downloading_count += 1
        elif torrent.state == 'checkingUP' or torrent.state == 'checkingDL':
            checking_count += 1
    #line1 = "U:{seeding}/D:{downloading}/V:{checking}/A:{all}".format(seeding=seeding_count,downloading=downloading_count,checking=checking_count,all=len(torrent_list))
    # cycle between lines 1 & 2 then 3 & 4
    for i in range(10):
        transfer_info = qbt_client.transfer_info()
        #upload_speed = "{:.0f}".format((transfer_info.up_info_speed / 1000))
        upload_speed = format_bps(transfer_info.up_info_speed)
        download_speed = format_bps(transfer_info.dl_info_speed)
        #download_speed = "{:.0f}".format((transfer_info.dl_info_speed / 1000))
        line1 = "UP:{up_speed}".format(up_speed=upload_speed)
        line2 = "DN:{dl_speed}".format(dl_speed=download_speed)
        # update LCD
        subprocess.run([lcd_api_exe, '0', line1])
        subprocess.run([lcd_api_exe, '1', line2])
        time.sleep(1)

    for i in range(10):
        transfer_info = qbt_client.transfer_info()
        #upload_total = "{:.0f}".format((transfer_info.up_info_data / 1000000))
        upload_total = format_bytes(transfer_info.up_info_data)
        download_total = format_bytes(transfer_info.dl_info_data)
        #download_total = "{:.0f}".format((transfer_info.dl_info_data / 1000000))
        line3 = "UP:{up_total}".format(up_total=upload_total)
        line4 = "DN:{dl_total}".format(dl_total=download_total)
        subprocess.run([lcd_api_exe, '0', line3])
        subprocess.run([lcd_api_exe, '1', line4])
        time.sleep(1)