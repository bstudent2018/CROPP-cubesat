import os

dirr = "/home/pi/Desktop/v6/output/d/"
list = os.listdir(dirr)


for count,filename in enumerate(list):
    letter = filename[3]
    _,date,time = filename.split('_')
    time = time[:-4].replace(':','')
    
    dest = dirr+letter +"_"+ date +"_"+ time + ".jpg"
    os.rename(dirr+filename,dest)

print(os.listdir(dirr))
