while true;do
	clear
DATA=$(curl -s "https://opentdb.com/api.php?amount=1&category=17&type=multiple")


Q=$(echo $DATA | jq -r '.results[0].question' | ./htmlUnescape.py | fold -w 30 -s)
A=$(echo -n $DATA | jq -r '.results[0].correct_answer' | ./htmlUnescape.py) 
AQR=$(echo -n $DATA | jq -r '.results[0].correct_answer' | ./htmlUnescape.py | ./qrascii.py) 
AS=($(echo -n $DATA | jq '.results[0].incorrect_answers + [.results[0].correct_answer] | .[] | @sh') )

AS=$(xargs -L 4 shuf -e <<<"${AS[@]}")

paste -d' ' <(echo "$AQR") <(echo -e "$Q\n"; echo -e "$AS")
sleep 3600
done
