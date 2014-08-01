emission
========

Carbon-like musings

Example Bash Script to send data:

#!/bin/bash

# check to see if any swap is being used
swap_mb=$(free -m | grep Swap | awk '{print $3}')

key=myapp.$(hostname).swap_used
apiKey=not_a_real_api_key

remote_target=http://flrrb.com:8000/api/alert

if [[ ${swap_mb:-0} -gt 0 ]]; then
	code=2
else
	code=0
fi

msg="${swap_mb:-0}MB of Swap is being used"

curl -d "{\"apiKey\":\"$apiKey\",\"status_code\":$code,\"key\":\"$key\",\"comment\":\"$msg\"}" "$remote_target"
