# https://fathomless-waters-42051.herokuapp.com/

import os
import sys
import json
#Custom libs
import diction
import mth
import wiki

import requests
from flask import Flask, request

app = Flask(__name__)


@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():

    # endpoint for processing incoming messaging events

    data = request.get_json()
    log(data)  # log incoming message for testing purposes

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent a message!

                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    msg = messaging_event["message"]["text"]           # the message's text
                    
                    # call mth.py module
                    if 'math' in msg[0:4].lower():
                        try :
                            iplist = msg.strip().split()
                            func = iplist[1].lower()
                            a = int(iplist[2])
                            b = int(iplist[3])
                            xmth = mth.calc(func, a, b)
                            send_message(sender_id, xmth)
                        except ValueError as err :
                            print err
                            send_message(sender_id, 'Snap! Something terrible happened. Would you please try again?')

                    # call diciton.py module
                    elif 'meaning' in msg[0:7].lower() :
                        try :
                            xmean = []
                            xx = []
                            iplist = msg.strip().split()
                            word = iplist[1]
                            xmean = diction.meaning(word)
                            if xmean[0] != 'Error' :
                                xx = xmean[1]
                                msgstr = word.upper() + ' is a(n) ' + xmean[0] + '.\n' + 'GENERAL MEANING : ' + xx[0]
                            elif xmean[0] == 'Error' :
                                send_message(sender_id, xmean[1])
                        except ValueError as err :
                            print err
                            send_message(sender_id, 'Snap! Something terrible happened. Would you please try again?')
 
                    # call wiki.py module
                    elif 'wiki' in msg[0:4].lower() :
                        try :
                            term = ''
                            iplist = msg.strip().split()
                            for i in iplist[1:] :
                                term = term + i + ' '
                                retlist = []
                                retlist = wiki.summ(term)
                                
                                if retlist[0] == 'Error' :
                                    print retlist
                                    msgstr = retlist[0] + '\n\n' + retlist[1]
                                    send_message(sender_id, msgstr)
                                elif retlist[0] != 'Error' :
                                    print retlist
                                    content = str(retlist[2])
                                    msgstr = retlist[0].upper() + '\n\n' + content[:170] + '...\n\n' + 'Read more about ' + retlist[0] + ' at:\n' + retlist[1]
                                    send_message(sender_id, msgstr)
                        except ValueError as err :
                            print err 
                            send_message(sender_id, 'Snap! Something terrible happened. Would you please try again?')
                    

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200


def send_message(recipient_id, message_text) :

    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(debug=True)
