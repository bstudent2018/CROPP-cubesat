#!/bin/bash
echo "Start updating system..."
sudo cp ./kernel.img /boot/kernel.img
sudo cp ./kernel7.img /boot/kernel7.img
sudo cp ./kernel7l.img /boot/kernel7l.img

sudo cp ./*.dtb /boot/
sudo cp ./overlays/*.dtb* /boot/overlays
sudo cp -rf ./lib/* /lib
echo "--------------------------------------"
echo "Enable i2c0 adapter..."
echo "--------------------------------------"
sudo modprobe i2c-dev
# add dtparam=i2c_vc=on to /boot/config.txt
awk 'BEGIN{ count=0 }       \
{                           \
    if($1 == "dtparam=i2c_vc=on"){       \
        count++;            \
    }                       \
}END{                       \
    if(count <= 0){         \
        system("sudo sh -c '\''echo dtparam=i2c_vc=on >> /boot/config.txt'\''"); \
    }                       \
}' /boot/config.txt
echo "Add dtoverlay=arducam to /boot/config.txt "
echo "--------------------------------------"
awk 'BEGIN{ count=0 }       \
{                           \
    if($1 == "dtoverlay=arducam"){       \
        count++;            \
    }                       \
}END{                       \
    if(count <= 0){         \
        system("sudo sh -c '\''echo dtoverlay=arducam >> /boot/config.txt'\''"); \
    }                       \
}' /boot/config.txt
echo "Add gpu=400M to /boot/config.txt "
awk 'BEGIN{ count=0 }       \
{                           \
    if($1 == "gpu_mem=400"){       \
        count++;            \
    }                       \
}END{                       \
    if(count <= 0){         \
        system("sudo sh -c '\''echo gpu_mem=400 >> /boot/config.txt'\''"); \
    }                       \
}' /boot/config.txt
echo "Add cma=128M to /boot/cmdline.txt "
echo "--------------------------------------"
sudo sed 's/cma=128M//g' -i /boot/cmdline.txt
sudo sed 's/[[:blank:]]*$//' -i /boot/cmdline.txt
sudo sed 's/$/& cma=128M/g' -i /boot/cmdline.txt
sudo install -p -m 777 ./arducamstill/arducamstill /usr/bin
echo "reboot now?(y/n):"
read USER_INPUT
case $USER_INPUT in
'y'|'Y')
    echo "reboot"
    sudo reboot
;;
*)
    echo "cancel"
;;
esac
