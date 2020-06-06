import qbittorrentapi
import subprocess
import time
from dotenv import load_dotenv
load_dotenv()
import os
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
        upload_speed = "{:.0f}".format((transfer_info.up_info_speed / 1000))
        download_speed = "{:.0f}".format((transfer_info.dl_info_speed / 1000))
        line1 = "UP:{up_speed}Kbps".format(up_speed=upload_speed)
        line2 = "DN:{dl_speed}Kbps".format(dl_speed=download_speed)
        # update LCD
        subprocess.run([lcd_api_exe, '0', line1])
        subprocess.run([lcd_api_exe, '1', line2])
        time.sleep(1)

    for i in range(10):
        transfer_info = qbt_client.transfer_info()
        upload_total = "{:.0f}".format((transfer_info.up_info_data / 1000000))
        download_total = "{:.0f}".format((transfer_info.dl_info_data / 1000000))
        line3 = "UP:{up_total}MB".format(up_total=upload_total)
        line4 = "DN:{dl_total}MB".format(dl_total=download_total)
        subprocess.run([lcd_api_exe, '0', line3])
        subprocess.run([lcd_api_exe, '1', line4])
        time.sleep(1)