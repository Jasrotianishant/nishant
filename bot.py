from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route('/mybot', methods = ['POST'])

def mybot():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    responded = False
    if(incoming_msg == "hi"):
        msg.body("Hello")
        responded = True
    elif(incoming_msg == "who"):
        msg.body("I am your bot.")
        responded = True
    elif 'quote' in incoming_msg:
        r = request.get('https://api.forismatic.com/api/1.0/?method=getQuote&lang=en&format=jsonp&jsonp=?')
        if r.status_code == 200:
            data = r.json()
            quote = f'{data["quoteText"]} ({data["quoteAuthor"]})'
        else:
            quote = "I am Sorry, I can't retrieve quote at the moment"
        msg.body(quote)
        responded = True
    elif not responded:
        msg.body("I can only tell you about quotes and my identity.")

    return str(resp)

if __name__=="__main__":
    app.run()
