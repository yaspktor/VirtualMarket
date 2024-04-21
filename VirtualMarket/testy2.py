import yfinance as yf

# ticker = yf.Ticker("AMZN").news

# for i in ticker:
#     print(i['title'])
    
# ticker2 = yf.Ticker("AMZN").info
# print(ticker2["longBusinessSummary"])
# #print company logo url

def companyDesc(symbol):
    try: 
        desc = yf.Ticker(symbol).info
        news = yf.Ticker(symbol).news
        return {
            "desc": desc["longBusinessSummary"],
            "news": news
        }
    except Exception as e:
        #wypisz error
        print(e)
        print("Error CompanyDesc")
        return None
    
data = companyDesc("GOOGL")
print(data["news"][0]['title'])
#url
print(data["news"][0]['thumbnail']['resolutions'][0]['url'])

#min of 2 resolutions
print(min(1,2))

print(data["news"][0])

for news in data["news"]:
    #print url picture
    print(news)
    print("-------------------")
    
    
