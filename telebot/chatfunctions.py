import yfinance as yf
import json
import telegram

def countSpaces(text):
    return text.count(' ')

def getTextAfterCommand(text):
    return text[text.find(' ') + 1:].strip().replace(' ', '')

def escapeStrForTelegram(text):
    return text.replace(".", "\.").replace("(", "\(").replace("+", "\+").replace(")", "\)").replace("-", "\-")

def makeKeyboard(stringList):
    keyboard = []
    for key, value in stringList.items():
        keyboard.append([telegram.InlineKeyboardButton(key, url=value)])

    return telegram.InlineKeyboardMarkup(keyboard)

def buildQuoteResponse(sPrice, sPriceDiff, sCompanyName, tickerReceived):
    yfUrl = "https://finance.yahoo.com/quote/" + tickerReceived + "/"
    finViz = "https://finviz.com/quote.ashx?t=" + tickerReceived
    tvUrl = "https://www.tradingview.com/chart?symbol=" + tickerReceived
    stringList = {"View in Yahoo Finance": yfUrl, "View in FinViz": finViz, "View in TradingView" : tvUrl}

    keyboardMarkup = makeKeyboard(stringList)
    
    companyNameStr = "_" + sCompanyName + "_\n"
    tickerStr = "*" + tickerReceived.upper() + "*" + "\n"
    priceStr = sPrice + sPriceDiff

    if "surged" in sPriceDiff:
        priceStr = priceStr + "  🚀\n"
    elif "dropped" in sPriceDiff:
        priceStr = priceStr + "  💸\n"

    buildStr = tickerStr + companyNameStr + priceStr

    escapedStr = escapeStrForTelegram(buildStr)

    return escapedStr, keyboardMarkup

def displayQuote(text):
    if countSpaces(text) > 1:
        return "Knn invalid quote", None

    tickerReceived = getTextAfterCommand(text)

    try:
        sPrice, sPriceDiff, sCompanyName = getStock(tickerReceived)
    except ImportError:
        return escapeStrForTelegram("Knn invalid quote, please try again."), None
    except KeyError:
        return escapeStrForTelegram("Can't handle this stock, regularMarketOpen error please try again."), None

    return buildQuoteResponse(sPrice, sPriceDiff, sCompanyName, tickerReceived)

def getStock(symbol):
    currency=''
    price=0
    prev_price=0

    # Fetch the stock symbol Currency
    ticker_meta=yf.Ticker(symbol)
    ticker_dict=ticker_meta.info
    ticker_json=json.dumps(ticker_dict)
    # print(ticker_json)
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
    # message=message.replace("-","\-")
    # message=message.replace("+","\+")
    # message=message.replace(".","\.")
    # message=message.replace("(","\(")
    # message=message.replace(")","\)")
    # message=message.replace("?","\?")
    # message=message.replace("^","\^")
    # message=message.replace("$","\$")
    # message=urllib.parse.quote_plus(message)
    
    return(currency+str("{0:,.2f}".format(price)), price_diff_str, ticker_json['longName'])
