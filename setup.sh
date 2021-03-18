#!/usr/bin/bash
echo "----------------------------------------------"
echo "-- Pi Information Collector Client Installs --"
echo "----------------------------------------------"

echo "----------------------------------------------"
echo "Updating APT and installing dependent packages"
echo "----------------------------------------------"
sudo apt-get update && sudo apt-get install -y git python3-pip

echo "----------------------------------------------"
echo "Installing additional python libraries"
echo "----------------------------------------------"
pip3 install pika psutil netifaces

echo "----------------------------------------------"
echo "Downloading scripts from git repo"
echo "----------------------------------------------"
git clone https://github.com/noitcerid/pi_info_mq.git /home/pi/pi_info_mq

echo "----------------------------------------------"
echo "Setting file permissions on scripts"
echo "----------------------------------------------"
chmod a+x /home/pi/pi_info_mq/client.py

echo "----------------------------------------------"
echo "Setting up Cron job to regularly execute client script"
echo "----------------------------------------------"
# echo "1 * * * * /usr/bin/python3 /home/pi/pi_info_mq/client.py" | sudo tee /etc/cron.d/pi_info_mq
crontab -e

echo "----------------------------------------------"
echo "--      Client installation complete!       --"
echo "----------------------------------------------"