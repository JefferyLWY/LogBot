import io
import sys
import time
import random
import datetime

def addZero(x):
    x = str(x)
    if len(x) == 1:
        return "0" + x
    else:
        return x

def genCart(prods, itemNoLst):
    cartline = ""
    for I in prods:
        cartline = cartline + I + ':' + str(random.choice(itemNoLst)) + ','
    return cartline[:-1]

def generateCheckouts(initUser, noUsers, noCheckouts, prodLst, cartConfig):
    checkOutLst = []
    users = list(range(initUser,noUsers + initUser))
    for x in range(noCheckouts):
        usr = random.choice(users)
        cart = ""
        logline = "page|checkout"
        randomIP = "{}.{}.{}.{}".format(random.randint(0,255),random.randint(0,255),random.randint(0,255),random.randint(0,255))
        randomDT = "2018-{}-{} {}:{}:{}".format(addZero(random.randint(1,12)),
                                                addZero(random.randint(0,29)),
                                                addZero(random.randint(0,23)),
                                                addZero(random.randint(0,60)),
                                                addZero(random.randint(0,60)))
        if usr < (int((noUsers-initUser)*(1/3))+initUser):
            cart = genCart(random.sample(prodLst[0],random.choice(cartConfig[0])),cartConfig[1])
            logline = "{}|{}|{}|{}|{}".format(logline,randomIP,usr,randomDT,cart)
        elif usr > (int((noUsers-initUser)*(2/3))+initUser):
            cart = genCart(random.sample(prodLst[1],random.choice(cartConfig[0])),cartConfig[1])
            logline = "{}|{}|{}|{}|{}".format(logline,randomIP,usr,randomDT,cart)
        else:
            cart = genCart(random.sample(prodLst[2],random.choice(cartConfig[0])),cartConfig[1])
            logline = "{}|{}|{}|{}|{}".format(logline,randomIP,usr,randomDT,cart)
        checkOutLst.append(logline)
    return checkOutLst

def generateVisits(initUser, noUsers, noVisits, prodLst):
    visitLst = []
    users = list(range(initUser, noUsers + initUser))
    for x in range(noVisits):
        usr = random.choice(users)
        logline = "product"
        randomIP = "{}.{}.{}.{}".format(random.randint(0,255),random.randint(0,255),random.randint(0,255),random.randint(0,255))
        randomDT = "2018-{}-{} {}:{}:{}".format(addZero(random.randint(1,12)),
                                                addZero(random.randint(0,29)),
                                                addZero(random.randint(0,23)),
                                                addZero(random.randint(0,60)),
                                                addZero(random.randint(0,60)))
        if usr < (int((noUsers-initUser)*(1/3))+initUser):
            logline = "{}|{}|{}|{}|{}".format(logline,random.choice(prodLst[0]),randomIP,usr,randomDT)
        elif usr > (int((noUsers-initUser)*(2/3))+initUser):
            logline = "{}|{}|{}|{}|{}".format(logline,random.choice(prodLst[1]),randomIP,usr,randomDT)
        else:
            logline = "{}|{}|{}|{}|{}".format(logline,random.choice(prodLst[2]),randomIP,usr,randomDT)
        visitLst.append(logline)
    return visitLst

if __name__ == '__main__':

    #Loading Product Clusters
    casualMan = ["SKU-" + str(prod).strip() for prod in open("casualMen.txt",'r').read().splitlines()]
    sportyMan = ["SKU-" + str(prod).strip() for prod in open("sportyMen.txt",'r').read().splitlines()]
    formalMan = ["SKU-" + str(prod).strip() for prod in open("formalMen.txt",'r').read().splitlines()]

    casualWmn = ["SKU-" + str(prod).strip() for prod in open("casualWmn.txt",'r').read().splitlines()]
    formalWmn = ["SKU-" + str(prod).strip() for prod in open("formalWmn.txt",'r').read().splitlines()]
    sportyWmn = ["SKU-" + str(prod).strip() for prod in open("sportyWmn.txt",'r').read().splitlines()]

    #Cart Configurations
    cartNoLst = [1] * 8 + [2] * 12 + [3] * 16 + [4] * 10 + [5] * 8 + [6] * 2
    itemNoLst = [1] * 50 + [2] * 10 + [3] * 5 + [4] * 1

    noMan = int(input("No. of Male Customers: "))
    noWmn = int(input("No. of Female Customers: "))

    if sys.argv[1] == 'rand':
        print("GEN Selected")
        
        noVisitM = int(input("No. of Clicks (Man): "))
        noVisitW = int(input("No. of Clicks (Women): "))
        noCheckoutM = int(input("No. of Checkouts (Man): "))
        noCheckoutW = int(input("No. of Checkouts (Women): "))

        #Generating Visits
        menVisits = generateVisits(0, noMan, noVisitM, [casualMan,sportyMan,formalMan])
        wmnVisits = generateVisits(noMan, noWmn, noVisitW, [casualWmn,sportyWmn,formalWmn])
        
        #Generating Purchases
        menCheckouts = generateCheckouts(0, noMan, noCheckoutM, [casualMan,sportyMan,formalMan], [cartNoLst,itemNoLst])
        wmnCheckouts = generateCheckouts(noMan, noWmn, noCheckoutW, [casualWmn,sportyWmn,formalWmn], [cartNoLst,itemNoLst])

        #Wrap up
        final = menVisits + wmnVisits + menCheckouts + wmnCheckouts
        random.shuffle(final)
        with open('./logs.txt', mode='wt', encoding='utf-8') as logfile:
            logfile.write('\n'.join(str(line) for line in final))
        print("Logs generated successfully.")
    
    elif sys.argv[1] == 'bot':
        print("BOT Selected")
        visitTraffic = int(input("Click Traffic Volume: "))
        visitDisplacement = int(input("Click Displacement: "))
        checkoutTraffic = int(input("Checkout Traffic Volume: "))
        checkoutDisplacement = int(input("Checkout Displacement: "))
        delay = int(input("Stream Delay (SEC): "))

        while True:
            #Generating Visits
            visits = int((visitTraffic + random.randint(-visitDisplacement,visitDisplacement))/2)
            menVisits = generateVisits(0, noMan, visits, [casualMan,sportyMan,formalMan])
            wmnVisits = generateVisits(noMan, noWmn, visits, [casualWmn,sportyWmn,formalWmn])

            #Generating Purchases
            checkouts = int((checkoutTraffic + random.randint(-checkoutDisplacement,checkoutDisplacement))/2)
            menCheckouts = generateCheckouts(0, noMan, checkouts, [casualMan,sportyMan,formalMan], [cartNoLst,itemNoLst])
            wmnCheckouts = generateCheckouts(noMan, noWmn, checkouts, [casualWmn,sportyWmn,formalWmn], [cartNoLst,itemNoLst])

            #Wrap up
            final = menVisits + wmnVisits + menCheckouts + wmnCheckouts
            random.shuffle(final)
            print(final)
            time.sleep(delay) 

    else:
        print("Invalid Input")