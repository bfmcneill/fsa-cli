echo "=============================="
echo "resetting database data"
echo "=============================="
./venv/bin/pcmd utils data-init

echo "=============================="
echo "creating customer"
echo "=============================="
./venv/bin/pcmd customer create \
--email jim@bo.com \
--first-name jim \
--last-name bo

echo "=============================="
echo "update customer address"
echo "=============================="
./venv/bin/pcmd customer update-address \
--email "jim@bo.com" \
--line1 "8000 broadway street" \
--city Phoenix \
--state-code AZ \
--zip-code 85331

echo "=============================="
echo "update customer address"
echo "=============================="
./venv/bin/pcmd customer update-address \
--email "jim@bo.com" \
--line1 "8000 broadway street" \
--line2 "PO BOX 820" \
--city Flagstaff \
--state-code AZ \
--zip-code 86001

#echo "=============================="
#echo "create checking account"
#echo "=============================="
#./venv/bin/pcmd account create-checking --email jim@bo.com
#
#echo "=============================="
#echo "create savings account"
#echo "=============================="
#./venv/bin/pcmd account create-savings --email jim@bo.com --rate 0.0375

#echo "=============================="
#echo "create credit card"
#echo "=============================="
#./venv/bin/pcmd account create-cc --email jim@bo.com --rate 0.18

echo "=============================="
echo "create term loan"
echo "=============================="
./venv/bin/pcmd account create-term-loan --email jim@bo.com --rate 0.18 --term 36