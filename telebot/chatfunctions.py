def addquote(text):
    print(text)

def getStock(symbol):

    currency=''
    price=0
    prev_price=0

    # Fetch the stock symbol Currency
    ticker_meta=yf.Ticker(symbol)
    ticker_dict=ticker_meta.info
    ticker_json=json.dumps(ticker_dict)
    ticker_json=json.loads(ticker_json)
    if ticker_json["currency"] != '':
        currency=ticker_json["currency"]

    # Fetch the stock symbol daily data
    ticker=yf.download(symbol, period="1d")
    #DEBUG: print(ticker)
    if prev_price == 0:
        prev_price=(ticker["Open"][0]).round(2)
    else:
        prev_price=price
    price=(ticker["Close"][0]).round(2)
    if prev_price == 0 or price == prev_price:
        price_change_str = ''
        price_diff_str = ''
    elif price > prev_price:
        price_diff = (price-prev_price).round(2)
        price_change_str = "surged"
        price_diff_str = "("+price_change_str+" +"+str("{0:,.2f}".format(price_diff)).replace(',', '\'')+")"
    else:
        price_diff = (prev_price-price).round(2)
        price_change_str = "dropped"
        price_diff_str = "("+price_change_str+" -"+str("{0:,.2f}".format(price_diff)).replace(',', '\'')+")"

    # Build message string with escaping url critical chars
    message=symbol+" @ *"+currency+" "+str("{0:,.2f}".format(price)).replace(',', '\'')+"* "+price_diff_str
    message=message.replace("-","\-")
    message=message.replace("+","\+")
    message=message.replace(".","\.")
    message=message.replace("(","\(")
    message=message.replace(")","\)")
    message=message.replace("?","\?")
    message=message.replace("^","\^")
    message=message.replace("$","\$")
    # message=urllib.parse.quote_plus(message)
    
    return(message)
