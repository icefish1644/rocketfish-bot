def countSpaces(text):
    return text.count(' ')

def getTextAfterCommand(text):
    return text[text.find(' ') + 1:].strip().replace(' ', '')

def displayQuote(text):
    if countSpaces(text) > 1:
        return "Knn invalid quote"

    tickerReceived = getTextAfterCommand(text)

    return "You have provided " + tickerReceived + " as ticker symbol"