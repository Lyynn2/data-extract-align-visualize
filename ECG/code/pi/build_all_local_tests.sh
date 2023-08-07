
echo ""
echo "------------"
echo "TEST 09"
echo "------------"
echo ""
cd ~/local_builds/test_09/ceti-tag-data-capture
(find src/ -name "*.o" -type f -delete); (rm bin/cetiTagApp); make
echo ""
echo "------------"
echo "TEST 10"
echo "------------"
echo ""
cd ~/local_builds/test_10/ceti-tag-data-capture
(find src/ -name "*.o" -type f -delete); (rm bin/cetiTagApp); make
echo ""
echo "------------"
echo "TEST 11"
echo "------------"
echo ""
cd ~/local_builds/test_11/ceti-tag-data-capture
(find src/ -name "*.o" -type f -delete); (rm bin/cetiTagApp); make

cd ~/local_builds