import io
import sys
import time
import random
import datetime

#Loading Product Clusters
casualMan = [str(prod).strip() for prod in open("casualMen.txt",'r').read().splitlines()]
sportyMan = [str(prod).strip() for prod in open("sportyMen.txt",'r').read().splitlines()]
formalMan = [str(prod).strip() for prod in open("formalMen.txt",'r').read().splitlines()]

casualWmn = [str(prod).strip() for prod in open("casualWmn.txt",'r').read().splitlines()]
formalWmn = [str(prod).strip() for prod in open("formalWmn.txt",'r').read().splitlines()]
sportyWmn = [str(prod).strip() for prod in open("sportyWmn.txt",'r').read().splitlines()]

def addZero(x):
    x = str(x)
    if len(x) == 1:
        return "0" + x
    else:
        return x

def crossSelect(x):
    if x == 0:
        y, z = 1, 2
    elif x == 1:
        y, z = 2, 0
    else:
        y, z = 0, 1
    return random.choice([x] * 15 + [y] * 1 + [z] * 1)

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
        randomDT = "{}:{}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                                  addZero(random.randint(0,60)))

        if usr < (int((noUsers)*(1/3))+initUser):
            cart = genCart(random.sample(prodLst[0],random.choice(cartConfig[0])),cartConfig[1])
            logline = "{}|{}|{}|{}|{}".format(logline,randomIP,usr,randomDT,cart)
        elif usr > (int((noUsers)*(2/3))+initUser-1):
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
        randomDT = "{}:{}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                                  addZero(random.randint(0,60)))

        if usr < (int((noUsers)*(1/3))+initUser):
            logline = "{}|{}|{}|{}|{}".format(logline,random.choice(prodLst[crossSelect(0)]),randomIP,usr,randomDT)
        elif usr > (int((noUsers)*(2/3))+initUser-1):
            logline = "{}|{}|{}|{}|{}".format(logline,random.choice(prodLst[crossSelect(1)]),randomIP,usr,randomDT)
        else:
            logline = "{}|{}|{}|{}|{}".format(logline,random.choice(prodLst[crossSelect(2)]),randomIP,usr,randomDT)
        visitLst.append(logline)
    return visitLst

if __name__ == '__main__':

    #Cart Configurations
    cartNoLst = [1] * 8 + [2] * 12 + [3] * 16 + [4] * 10 + [5] * 8 + [6] * 2
    itemNoLst = [1] * 50 + [2] * 10 + [3] * 5 + [4] * 1

    noMan = int(input("No. of Male Customers: "))
    noWmn = int(input("No. of Female Customers: "))

    mCasual = "{} - {}".format(0, int(noMan*1/3)-1)
    mSporty = "{} - {}".format(int(noMan*1/3), int(noMan*2/3)-1)
    mFormal = "{} - {}".format(int(noMan*2/3), noMan-1)
    print("Man IDs: \nCasual: {}\nSporty: {}\nFormal: {}".format(mCasual, mSporty, mFormal))

    wCasual = "{} - {}".format(noMan, int(noWmn*1/3)+noMan-1)
    wSporty = "{} - {}".format(int(noWmn*1/3)+noMan, int(noWmn*2/3)+noMan-1)
    wFormal = "{} - {}".format(int(noWmn*2/3)+noMan, noWmn+noMan-1)
    print("Woman IDs: \nCasual: {}\nSporty: {}\nFormal: {}".format(wCasual, wSporty, wFormal))

    #File generator
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
    

    #Log Bot
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
            with open('/var/www/html/blog/wp-content/plugins/trackloger/logs/user_log.txt', mode='a') as logfile:
                logfile.write('\n'.join(str(line) for line in final))
                logfile.write('\n')
            for log in final:
                print(log)
            print(' ')
            time.sleep(delay) 

    else:
        print("Invalid Input")
