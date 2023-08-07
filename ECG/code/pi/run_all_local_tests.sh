

echo ""
echo "------------"
echo "TEST 09"
echo "------------"
echo ""
date
sudo rm /data/*.flac
sudo rm /data/*.raw
sudo rm /data/*.csv
sudo rm /data/*.txt
cd /home/pi/local_builds/test_09/ceti-tag-data-capture
((sleep 780 && echo "quit" > ipc/cetiCommand) &)
(echo "" > ipc/cetiCommand)
cd bin
sudo ./cetiTagApp > /data/_console_output.txt 2>&1
cd ..
sleep 60
sudo mkdir /data/archived_2023-04-21_test09
sudo mkdir /data/archived_2023-04-21_test09/audio
sudo mv /data/*.flac /data/archived_2023-04-21_test09/audio/
sudo mv /data/*.raw /data/archived_2023-04-21_test09/audio/
sudo mv /data/*.csv /data/archived_2023-04-21_test09/
sudo mv /data/*.txt /data/archived_2023-04-21_test09/

echo ""
echo "------------"
echo "TEST 10"
echo "------------"
echo ""
date
sudo rm /data/*.flac
sudo rm /data/*.raw
sudo rm /data/*.csv
sudo rm /data/*.txt
cd /home/pi/local_builds/test_10/ceti-tag-data-capture
((sleep 780 && echo "quit" > ipc/cetiCommand) &)
(echo "" > ipc/cetiCommand)
cd bin
sudo ./cetiTagApp > /data/_console_output.txt 2>&1
cd ..
sleep 60
sudo mkdir /data/archived_2023-04-21_test10
sudo mkdir /data/archived_2023-04-21_test10/audio
sudo mv /data/*.flac /data/archived_2023-04-21_test10/audio/
sudo mv /data/*.raw /data/archived_2023-04-21_test10/audio/
sudo mv /data/*.csv /data/archived_2023-04-21_test10/
sudo mv /data/*.txt /data/archived_2023-04-21_test10/

echo ""
echo "------------"
echo "TEST 11"
echo "------------"
echo ""
date
sudo rm /data/*.flac
sudo rm /data/*.raw
sudo rm /data/*.csv
sudo rm /data/*.txt
cd /home/pi/local_builds/test_11/ceti-tag-data-capture
((sleep 780 && echo "quit" > ipc/cetiCommand) &)
(echo "" > ipc/cetiCommand)
cd bin
sudo ./cetiTagApp > /data/_console_output.txt 2>&1
cd ..
sleep 60
sudo mkdir /data/archived_2023-04-21_test11
sudo mkdir /data/archived_2023-04-21_test11/audio
sudo mv /data/*.flac /data/archived_2023-04-21_test11/audio/
sudo mv /data/*.raw /data/archived_2023-04-21_test11/audio/
sudo mv /data/*.csv /data/archived_2023-04-21_test11/
sudo mv /data/*.txt /data/archived_2023-04-21_test11/

