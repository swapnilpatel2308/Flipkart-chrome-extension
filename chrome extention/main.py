import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
import numpy as np


class Flipkart:
    def __init__(self,url):
        self.url = url
        
    def chack_valid_url(self):
        try:
            if('marketplace=FLIPKART' in self.url):
                self.url = self.url[:self.url.index('marketplace=FLIPKART')]+'marketplace=FLIPKART'
                if('/p/' in self.url):
                    self.url = self.url.replace('/p/','/product-reviews/')
                    return 1
                else:
                    if('/product-reviews/' in self.url):
                        self.url = self.url
                        return 1
                    else:
                        # print("invalid url")
                        return -1
            else:
                # print("not a valid url code 2301")
                return -1
        except:
            return -2

    def chack_response(self):
        try:
            self.response = requests.get(self.url)
            if(self.response.status_code==200):
                return 1
            else:
                return -1
        except:
            return -2
        
    def get_reviews(self):
        try:
            response = requests.get(self.url)
            soup = BeautifulSoup(response.content, 'html.parser')
            rv = soup.find_all(class_='t-ZTKy')
            if(rv == []):
                return 0
            else:
                #find total reviews
                try:
                    totalreviews = soup.find(class_= '_2_R_DZ')
                    totalreview = totalreviews.select('span')[3].text.replace(' Reviews','').replace(',','')
                    totalreview = int(totalreview)
                    return totalreview
                except:
                    return -1
        except:
            return -2
    
    def Sentiment_score(self,text):
        blob = TextBlob(text)
        return blob.sentiment.polarity
        
    def get_data(self,number,totalreview):
        try:
            temp = 0
            pagecount = 0

            negative_count = []
            positive_count = []
            neutral_count = []

            while(temp<=number):
                if(totalreview!=-1):
                    pagecount = pagecount + 1
                    temp_url = self.url + '&page'+str(pagecount)
                    new_response = requests.get(temp_url)
                    new_soup = BeautifulSoup(new_response.content, 'html.parser')
                    rv = new_soup.find_all(class_='t-ZTKy')
                    for k in rv:
                        score = self.Sentiment_score(k.text)
                        if(score>0):
                            positive_count.append(score)
                        elif(score<0):
                            negative_count.append(score)
                        else:
                            neutral_count.append(score)

                        temp = temp + 1
                        # print(temp)
                    if(totalreview!=-1 and temp>totalreview):
                        break
                else:
                    try:
                        pagecount = pagecount + 1
                        temp_url = url + '&page'+str(pagecount)
                        new_response = requests.get(temp_url)
                        new_soup = BeautifulSoup(new_response.content, 'html.parser')
                        rv = new_soup.find_all(class_='t-ZTKy')
                        for k in rv:
                            score = self.Sentiment_score(k.text)
                            if(score>0):
                                positive_count.append(score)
                            elif(score<0):
                                negative_count.append(score)
                            else:
                                neutral_count.append(score)

                            temp = temp + 1
                            # print(temp)
                    except:
                        pass
            return temp,positive_count,negative_count,neutral_count
        except:
            return -2

    def run(self,for_review,number=50):
        if(for_review):
            a1 = self.chack_valid_url()
            if(a1==1):
                a2 = self.chack_response()
                if(a2==1):
                    a3 = self.get_reviews()
                    if(a3==0):
                        # print("there is no reviews for this page...")
                        return [-101]
                    elif(a3==-1 or a3==-2):
                        # print("error in fetching reviews")
                        return [-102]
                    else:
                        # print("total review is ",a3)
                        return [a3]
                else:
                    # print("error in response")
                    return [-103]
            else:
                # print("error in url...")
                return [-104]
        else:
            a1 = self.chack_valid_url()
            if(a1==1):
                a2 = self.chack_response()
                if(a2==1):
                    a3 = self.get_reviews()
                    if(a3==0):
                        # print("there is no reviews for this page...")
                        return [-101]
                    elif(a3!=-2):
                        temp,positive_count,negative_count,neutral_count = self.get_data(number,a3)
                        return (temp,positive_count,negative_count,neutral_count)
                    else:
                        # print("error in fetching data...")
                        return [-102]
                else:
                    # print("error in response")
                    return [-103]
            else:
                # print("error in url...")
                return [-104]

codes = {
    -101 : "there is no reviews for this page...",
    -102 : "error in fetching reviews",
    -103 : "error in response",
    -104 : "error in url..."
}

def return_details(url,countflag):
    review = Flipkart(url)
    if(countflag):
        reviewcount = review.run(True)
        if(reviewcount>0):
            return {
                "return code" : 0,
                "Total Review" : reviewcount
            }
        else:
            return {
                "return code" : -1,
                "error":codes[reviewcount[0]]
            }
    else:
        data = review.run(False)
        if(len(data)==1):
            return {
                "return code" : -1,
                "error" : codes[data[0]]
            }
        else:
            temp,positive_count,negative_count,neutral_count = data[0],data[1],data[2],data[3]
            positive_rate = 0
            negative_rate= 0
            neutral_rate = 0

            if(positive_count!=[]):
                positive_rate = (sum(positive_count)/len(positive_count))
            else:
                positive_rate = -2

            if(negative_count!=[]):
                negative_rate=(sum(negative_count)/len(negative_count))
            else:
                negative_rate = -2

            if(neutral_count!=[]):
                neutral_rate = (sum(neutral_count)/len(neutral_count))
            else:
                neutral_rate = -2

            return {
                "return code" : 1,
                "Total Review chacked" : temp,
                "Positive reviews" : len(positive_count),
                "Negative reviews" : len(negative_count),
                "Neutral reviews" : len(neutral_count),
                "Avarage Positive rate" : positive_rate,
                "Avarage Nagative rate" : negative_rate,
                "Avarage Neutral rate" : neutral_rate
            }        
        
url = 'https://www.flipkart.com/greenberri-virat/p/itm58dbace5999c9?pid=MOBGHZ3TRGEJ9R7G&lid=LSTMOBGHZ3TRGEJ9R7GOQJY0P&marketplace=FLIPKART&q=phone&store=tyy%2F4io&srno=s_1_3&otracker=AS_QueryStore_OrganicAutoSuggest_1_3_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_1_3_na_na_na&fm=Search&iid=en_IDnUZ6fgfnzWtnLKTLDZYJMq4OXYwdstYxXGEFcz5VadHZtYVcJLc%2BoVcZHmJWDiAxbyXqqD0EREV9zQVDqs6A%3D%3D&ppt=sp&ppn=sp&ssid=4ysbajilvk0000001686833814574&qH=f7a42fe7211f98ac'

print(return_details(url,False))