import os

ans = input('Are you sure you want to remove all pictures ?')
if ans == 'y' or ans == 'Y':
    for i in os.listdir('../face_db/face_save'):
        os.remove('../face_db/face_save/' + i)
    print("remove successful...")
else:
    print("remove failed...")
    exit(0)