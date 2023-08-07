
echo ""
echo "------------"
echo "TEST 12"
echo "------------"
echo ""
sudo rm /data/*.flac
sudo rm /data/*.raw
sudo rm /data/*.csv
sudo rm /data/*.txt
date
cd /home/pi/local_builds/test_12/ceti-tag-data-capture
((sleep 120 && echo "quit" > ipc/cetiCommand) &)
(echo "" > ipc/cetiCommand)
cd bin
sudo ./cetiTagApp > /data/_console_output.txt 2>&1
cd ..
sleep 60
sudo mkdir /data/archived_2023-04-24_test12
sudo mkdir /data/archived_2023-04-24_test12/audio
sudo mv /data/*.flac /data/archived_2023-04-24_test12/audio/
sudo mv /data/*.raw /data/archived_2023-04-24_test12/audio/
sudo mv /data/*.csv /data/archived_2023-04-24_test12/
sudo mv /data/*.txt /data/archived_2023-04-24_test12/
