emission
========

What should this monitoring solution be
- infinitely scalable -- out-of-the-box support for 1mil metrics/minute (10k hosts each sending 100 metrics on a 1-minute interval)
- Storage growth should be controllable -- data can be aged or kept forever -- must support zero-growth
- must support push and pull natively -- clients will use it that have no open inbound ports
- highly pluggable -- clear distinction between different components with coherent APIs connecting them
- multi-tenant
- coherent configs with various forms of wildcard support -- no rigid long-winded definitions for services, hosts, etc.
- auto-discovery of hosts
- comprehensive clustering support
- developers can subscribe to a notification scheme
- very good, easy-to-parse logging


Example Bash Script to send data:

```
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
```
