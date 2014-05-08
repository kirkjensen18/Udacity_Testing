# Udacity cs258 - Software Testing
# Lesson 4 - Homework 1
# Fuzzing data to test a common application

file_list=[
  ""
  ]

# Tried these for modifying jpegs, gifs, and pngs, and found no bugs.  Just corrupted images. Not sure what I expected.
# app = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
# app = "C:\\Windows\\System32\\mspaint.exe"
# app = "C:\\Program Files (x86)\\VideoLAN\\VLC\\vlc.exe"
 app = "C:\\Program Files\\Microsoft Office 15\\root\\office15"
fuzz_dir = "C:\\Users\\Kirk (Local)\\Documents\\GitHub\\Udacity_Testing\\Lesson 4\\Fuzzed\\"

FuzzFactor = 500
num_tests = 20
#num_tests = 500

########### end configuration ##########

import math
import random
import string
import subprocess
import time
import os


stats = []

for i in range(num_tests):
    file_choice = file_list[i % len(file_list)]
    #app = random.choice(apps)

    buf = bytearray(open(file_choice, 'rb').read())


    # start Charlie Miller code
    numwrites=random.randrange(math.ceil((float(len(buf)) / FuzzFactor)))+1

    for j in range(numwrites):
        rbyte = random.randrange(256)
        rn = random.randrange(len(buf))
        buf[rn] = int(rbyte)
    # end Charlie Miller code

    fuzz_output = fuzz_dir + str(i) + file_choice[::-1][:4][::-1]
    open(fuzz_output, 'wb').write(buf)
    
    process = subprocess.Popen([app, fuzz_output])
    statinfo = os.stat(file_choice)
    time.sleep(15)  #time.sleep(int(statinfo.st_size/10000))
    crashed = process.poll()
    if not crashed:
        process.terminate()
    else:
        stats.append((app, file_choice))

results = open("C:\\Users\\Kirk (Local)\\Documents\\GitHub\\Udacity_Testing\\Lesson 4\\log.txt", "wt")
print ("%d crashes\n" % len(stats))
for c in stats:
    print (c)
    results.write(c[0] + c[1])
