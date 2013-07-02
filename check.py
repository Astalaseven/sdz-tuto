from BeautifulSoup import BeautifulSoup
import urllib2
import cPickle as pickle

def getNewList():
    url = urllib2.urlopen("http://www.siteduzero.com/tutoriels/archives")
    soup = BeautifulSoup(url)

    tutos = []
    for content in soup.findAll('li', {'class': 'tuto'}):
        for meta, text in zip(content.findAll('a'), content.findAll('span', {'class' : 'courseTitle'})):
            try:
                tutos.append([meta['href'], text['title']])
            except KeyError:
                pass
    return tutos

def saveTutoList(liste):
    with open("old-tutos.p", "wb") as fichier:
        pickle.dump(liste, fichier)
    fichier.close()

def getOldList():
    try:
        with open("old-tutos.p", "rb") as fichier:
            old_list = pickle.load(fichier)
        fichier.close()
        return old_list
    except IOError:
        return False

def compareList(new_list, old_list):
    diff = []
    for item in new_list:
        if item not in old_list:
            diff.append(item)

    if diff:
        print "There are " + str(len(diff)) + " new " + ("tutos", "tuto")[len(diff) == 1] + "\n"
        for item in diff:
            print "\033[1m" + item[1] + "\033[0m"
            print "    (http://siteduzero.com" + item[0] + ")"

    else:
        print "No new tuto"
    return diff



if not getOldList():
    saveTutoList(getNewList())

compareList(getNewList(), getOldList())
