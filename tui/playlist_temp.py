# change the course number as appropriate and ensure the playlist_temp directory exists with all the background.html files
import os, time
import youtubePlaylistmaker as yt

course = 'ITM426'
video_id_master_list = []
for path, dir, files in os.walk('playlist_temp'):
    for name in files:
        full_file_path = path+"/"+name
        mod_num = name[0:4]
        playlist_name = course+" "+mod_num
        print(full_file_path)
        print(playlist_name)
        video_id_master_list.append(yt.scrape_video_ids(full_file_path, playlist_name))
print(video_id_master_list)

playlist_decision = input('Create YouTube PLaylists? (y/n): ').lower()
if playlist_decision =='y':
    login_data = yt.login()
    for list in video_id_master_list:
        playlist_name = list.pop(0)
        json_data = yt.create_playlist(login_data, playlist_name)
        yt.add_list_items(login_data, list, json_data['id'])
        time.sleep(5)
print('script complete.')
exit()