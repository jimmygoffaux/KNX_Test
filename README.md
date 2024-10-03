# KNX_Test

## install rasbian
Installing raspbian on raspberry pi (used raspberry pi imager) 
https://www.raspberrypi.com/software/
Don't forget to active SSH before download : 
![image](https://github.com/user-attachments/assets/ef2ba6f3-4771-4200-8363-def7cde9b519)

## for remote acces on raspberry pi 
```
sudo apt install tightvncserver
sudo apt install xrdp
```

## copy all file on raspberry pi 
import all file on raspberry pi from Github 
install git on raspberry pi : 
```
sudo apt-get install git
```
go to the location where you want to copy the files
```
cd /home/tester/Desktop
git clone https://github.com/jimmygoffaux/KNX_Test.git
```

## install all the librairie 
copy the pip_install.txt file to the raspberry pi and run the following command from the file location:
```
pip install -r pip_install.txt
```
