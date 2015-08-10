#Pubron
Shell command kicker by subscribing pub-sub message.

##Install

`$git clone https://github.com/tetsuya-zama/pubron`

`$pip install -r packages.txt`

##Setting
###subscriber.json
Check 'subscriber.json' on this repository.

Change settings for your PubNub or Redis (or both) environment.

###executor.json
Check 'executor.json' on this repository.

'msg' attribute for message name for kick this 'cmd'.

'cmd' attribute for shell command.

'##key_name##' will be place holder for retrieve 'data' of message.

[example setting]

    {
      "msg":"test_message"
      "cmd":"echo ##some_key##"
    }
[example message]

    {
      "msg":"test_message"
      "data":{"some_key":"some_val"}
    }

-> '$ echo some_val' will be executed.

'##DATA##' is reserved place holder name for retrieve whole data in json format.

[example setting]

    {
      "msg":"test_message"
      "cmd":"echo ##DATA##"
    }
[example message]

    {
      "msg":"test_message"
      "data":{"some_key":"some_val"}
    }

-> '$ echo '{"some_key":"some_val"}'' will be executed.

##Usage
###start process
`$ ./start_pubron.sh`
###stop process
`$ ./stop_pubron.sh`
###send massage
[quick sample of python PubNub message]

    from pubnub import Pubnub
    import json

    pubnub = Pubnub(subscribe_key="sub-key",publish_key="pub-key")

    message = {"msg":"test_msg","data":{"test":"hoge"}}
    pubnub.publish(channel="pubron",message=json.dumps(message))

[quick sample of python Redis message]

    from redis import Redis
    import json

    conn = Redis(host="localhost",port="6379")
    msg = {"msg":"test_msg","data":{"test":"foo"}}
    conn.publish("pubron",json.dumps(msg))
