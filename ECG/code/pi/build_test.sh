
echo ""
echo "------------"
echo "TEST 08"
echo "------------"
echo ""
cd ~/local_builds/test_08/ceti-tag-data-capture
(find src/ -name "*.o" -type f -delete); (rm bin/cetiTagApp); make

cd ~/local_builds