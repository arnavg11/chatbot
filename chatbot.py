#GUI part
from tkinter import *
from random import *
from re import *
# font style
BG_GRAY = "#ABB2B9"
BG_COLOR = "#17202A"
TEXT_COLOR = "#EAECEE"

FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"

#chatbot class
class Chatbot:
    def __init__(self):
        self.root = Tk()
        self.setupMainWindow()

    def setupMainWindow(self):
        self.root.title = "Ferns and Petals"
        self.root.resizable (height=False, width=False)
        self.root.configure(width = 470, height = 550, bg = BG_COLOR)

        headLabel = Label(self.root,bg = BG_COLOR,fg = TEXT_COLOR,text = "Welcome",font = FONT_BOLD,pady = 10)
        headLabel.place(relwidth = 1)
        # divider
        line = Label(self.root,width = 450,bg = BG_GRAY)
        line.place(relwidth = 1, rely = .07,relheight = .012)
        #main chat
        self.textWidget = Text(self.root, width = 20,height = 2,bg = BG_COLOR,fg = TEXT_COLOR,font = FONT,padx = 5,pady = 5)
        self.textWidget.place(relheight = .745, relwidth = 1, rely =.08)
        self.textWidget.insert(END, getInitResponse())
        self.textWidget.configure(cursor = "arrow", state = DISABLED)
        #scroll bar
        scrlBar = Scrollbar(self.textWidget)
        scrlBar.place(relheight = 1, relx = .974)
        scrlBar.configure(command = self.textWidget.yview())
        # typing area(layout)
        bottomLabel = Label(self.root,bg = BG_GRAY, height = 80)
        bottomLabel.place(relwidth = 1, rely = 0.825)
        # message entry box
        self.msg_entry = Entry(bottomLabel, bg = "#2C3E50", fg = TEXT_COLOR, font = FONT)
        self.msg_entry.place(relwidth = .9,relheight = .06,rely = .008, relx = .011)
        self.msg_entry.focus()
        self.msg_entry.bind("<Return>",self.onEnterPressed)

    def onEnterPressed(self,event):
        msg  =self.msg_entry.get()
        self.insertMessage(msg,"You")

    def insertMessage(self,msg,sender):
        if not msg:
            return
        self.msg_entry.delete(0,END)
        msg1 = sender+": "+msg+"\n\n"
        self.textWidget.configure(state = NORMAL)
        #edit chat
        self.textWidget.insert(END,msg1)
        self.textWidget.configure(state = DISABLED)

        if context!="end":
            msg1 = "Abbot" + ": " + getResponse(msg)+"\n\n"
            self.textWidget.configure(state=NORMAL)
            # edit chat
            self.textWidget.insert(END, msg1)
            self.textWidget.configure(state=DISABLED)
            self.textWidget.see(END)

    def run(self):
        self.root.mainloop()

#logic part

def mutatedIn(msg,comparators):
    bestMatchScore = 0
    for m in msg.split(" "):
        m = m.lower()
        for i in comparators:
                score = 0
                l  =len(m)
                for j in range(l):
                    try:
                        if i[j].isalpha():
                                if m[j] == i[j]:
                                   score+=1.0/l
                                elif j == 0:
                                    if m[j+1] == i[j]:
                                        score+=.5/l
                                elif j == len(m)-1:
                                    if m[j - 1] == i[j]:
                                        score += .5 / l
                                else:
                                    if m[j+1] == i[j]:
                                        score+=.5/l
                                    elif m[j - 1] == i[j]:
                                        score += .5 / l
                    except IndexError:
                        continue
                if bestMatchScore<score:
                    bestMatchScore = score
    return bestMatchScore
context = "first"
promotion = ""
outlets = ["chennai", "bangalore", "delhi", "lucknow", "mumbai", "chandigarh"]
foreignOutletDict = {"india":"Chennai, Bangalore, Delhi, Lucknow, Mumbai and Chandigarh",
                     "canda":"Toronto, Montreal and Vancouver",
                     "russia": "Moscow, Kazan, Omsk and St. Petersburgh",
                     "japan": "Tokyo, Kyoto and Osaka"}

def processOrder(msg):
    return "Splendid! we have processed your order and it shall arrive by 19th August"
def rating(n):
    pass
def getDate(msg):
    return "your order will arrive on or before 19th August. You have my word!"
def sendFeedback(msg):
    return "Thank you for your feedback. We always strive to achieve excellence"
def getResponse(msg):
    global context
    x = mutatedIn(msg,["yes","yeah","y","sure","ok"])
    isQuestion = mutatedIn(msg.split(" ")[0], ["what", "where", "when","how","are","can","do","is"])+int(msg[-1]=="?")
    if context == "first" and x>.9:
        context = "bought"
        return "Awesome! I knew you would like it. Kindly send your user id if you are already a member of ferns and plants otherwise you can search for it on our site."
    elif context == "bought":
            if msg.isalnum():
                context = "rating"
                return processOrder(msg)+"\n\nPlease feel free to give me a rating from 0 to 5 stars in the chatbox below."
            else:
                return "oops! it seems you have made a mistake in writing your user id. Try writing only the user id and nothing else."
    elif context == "rating":
        for i in msg:
            if i.isdigit():
                if 0<=float(i)<=5:
                    rating(i)
                    context = ""
                    return "Thank You very much!"
                else:
                    return "it seems you have entered a rating in the incorrect range"
        return "Sorry I couldn't detect any number. Would you mind typing it again and try not to put any non-digit character near it. Also, we do not accept fractonal ratings."
    elif context == "getDate":
        if msg.isalnum():
            context = ""
            return getDate(msg)
        else:
            return "oops! it seems you have made a mistake in typing your user id. Try writing only the user id and nothing else."
    elif context == "check area":
        context = ""
        if msg.lower() in outlets:

            return "I have good news! We do have an outlet in your city."
        return "I have bad news. We unfortunately do not serve your city at present but we do hope to open one of our outlets there in the future."
    elif context == "foreign country":
        context = ""
        try:
            cities = foreignOutletDict[msg]
            return "In your country, we have layouts in "+cities
        except KeyError:
            return "Sorry, either you have not written the name of your country properly or we do not operate in your country"
    elif context == "feedback":
        context = ""
        return sendFeedback(msg)
    elif isQuestion>.8 and mutatedIn(msg,["vegan","veg","non-veg","nonveg","egg","eggless","organic"])>.7:
        context = ""
        return "All our cakes our 100% organic and vegetarian. Even though we don't use eggs, we assure you that our cakes are delicious and fulfilling. Our dairy is taken from the finest cows across the globe"
    elif isQuestion>.7 and mutatedIn(msg,["refund","return"])>.7:
        context = ""
        return "You can read our return policies at chefscakes.com/returns"
    elif isQuestion>.8 and mutatedIn(msg,["deliver","operate","set","setup"]):
        context = "check area"
        return "We have offices set up all across India. Kindly enter your city name and I'll check wether you can have our dairy delights."

    elif mutatedIn(msg,["delivery","deliver","date"])>.7:
            #asking for delivery date
            context = "getDate"
            return "Kindly type your userid below so that I can search for your order"
    elif isQuestion>.8 and mutatedIn(msg,['tos','policy','privacy',"service","terms"])>.7:
        context = ""
        return "You can read our policies at chefscakes.com/tos"
    elif isQuestion>.8 and mutatedIn(msg,["outside","foreign","countries","country","offices"]):
        context = "foreign countries"
        return "We do operate in countries other than India. Kindly type below the name of our country and i shall tell you our outlets in the country"
    elif mutatedIn(msg,["feedback","comment"]):
        context = "feedback"
        return "kindly enter your feedback below so that i can send it to my executives"
    return "It seems I am having some difficulties understanding you, perhaps you could repeat that in easier words or you could wait on the line till some executive comes on the line"


def getInitResponse():
    starters = ["Hello I am Abbot how may I serve you today?"]
    offers = ["Could I possibly interest you in our newest product yet: the Sugary Birthday"]
    promotion = choice(offers)
    return "Abbot: "+choice(starters)+"(if you have some feedback or complaint to give us simply type feedback or comment in the box below)\n"+promotion+"\n\n"

if __name__ == "__main__":
    app = Chatbot()
    app.run()
