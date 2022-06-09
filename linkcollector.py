'''
Autore: Zhao Luca
Data: 17 Giungo 2021
class obj: (17 giu)
        -to create threads that *parses, collects and sorts links related to keywords
         extracted from a modular database.
            *parsing (non-detailed description):
                (WHILE LIST HAS ELEMENT LOOP)

                0-lock semaphore to access the database (under the form of list),
                 extracts first row and post semaphore.
                1-search on google "https://google.com/search=?"+ COMUNE +"%20"+ AZIENDA, list all
                 resulting links (page 1) related to the keyword searched (COMUNE + AZIENDA)
                1-or just simply use the google Custom search API.
                2-categorize links into 3 classes: Socials, News, Others.

            *output:
                3-save all links to .csv file. creates 3 files per AZIENDA.
                4-repeat 0.

                (WHILE LIST HAS ELEMENT LOOP)

            main parameters: str local modular-database abs path, INT numbers of threads
            main attributes: lock semaphore(under the form of list), LIST database

Possibili miglioramenti (18 giu):
    -UNSURE: aggiungimento di try except blocks per assicurare il flow completo dello script
    -aggiungimento di una sub-directory alla directory di output che contiene log di errori
     e di runtime exception
    -

'''
try:
    import time
    import pandas
    import os
    from threading import Thread
    from threading import Lock
    from googlesearch import *
except ImportError:
    print("Requested modules not installed")

#una funzione che sovrascrive un file di path {filename} con tutti gli elementi della {list}
def save_lists_in_file(filename, list):
    if len(list) > 0:
        f = open(filename, "w+")
        for elem in list:
            f.write(str(elem) + "\n")
        f.close()
        return True

    return False

class Collector(Thread):
    def __init__(self, name, links_collector, num_results):
        super(Collector,self).__init__()

        self.name = name
        self.lc=links_collector
        self.num_results=num_results

        self.citta=""
        self.azienda=""

        self.socials=["facebook","instagram","twitter","tiktok"]

    def adds_social(self, social):
        self.socials.append(social)

    def add_socials(self, socials):
        self.socials=self.socials+socials

    def is_social(self, url):
        for social in self.socials:
            if social in url:
                return True
        return False

    def acquire_keyword(self):   #method that acquires keyword from database (acts like a queue)
        src=self.lc
        rawdata=[]

        #extracting keyword from database
        if src.mutex.acquire():
            rawdata=src.database[0].copy()
            src.database.pop(0)
            src.mutex.release()

        #init citta azienda
        self.citta=str(rawdata[0])
        self.azienda=str(rawdata[1])

        #return keyword to search
        return self.citta+" "+self.azienda

    def collect_links(self, keyword): #method that collects all the links related to the keyword
        return search(term=keyword, num_results=self.num_results, lang="it")

    def collect_news(self, keyword): #method that collects all the links of news related to the keyword
        return search_news(term=keyword, azienda=self.azienda, num_results=self.num_results, lang="it")

    def save_links(self, links, news):  #method that sorts and outputs links to output dir
        social_links=[]
        #extract social links
        for link in links:
            if self.is_social(link):
                social_links.append(link)
                links.remove(link)

        #save links
        filename=self.lc.output_prefix+"_"+self.citta+"_"+self.azienda.replace(".","").lower()+".txt"

        Thread(target=save_lists_in_file, args= (self.lc.socials_dirpath+filename, social_links)).start()
        Thread(target=save_lists_in_file, args= (self.lc.others_dirpath+filename, links)).start()
        Thread(target=save_lists_in_file, args= (self.lc.news_dirpath+filename, news)).start()

    def run(self):
        #repeat until database is empty
        while len(self.lc.database) > 0:

        # 1) acquire database, get the keyword to search (città + azienda) from it,
        #  remove the extracted element and release database
            keyword=self.acquire_keyword()

        # 3) categorize and store the links
                        # 2) extract all the links from google serp, using previously extracted keywords
            self.save_links(self.collect_links(keyword),self.collect_news(keyword))


class LinksCollector(Thread):
    def __init__(self, name, database_path, output_path, output_prefix, delimiter, num_results, qty_threads):
        super(LinksCollector, self).__init__()

        self.name = name
        self.database_path = database_path
        self.qty_threads = qty_threads
        self.output_path = output_path
        self.output_prefix = output_prefix
        self.delimiter = delimiter
        self.num_results = num_results

        self.mutex = Lock()
        self.database = self.__toList()  # ottenere database sotto forma di lista

        self.__init_paths()

    def __init_paths(self): #method that initializes and builds paths of output files
        # init dir paths
        self.out_dirpath =self.output_path+ "linkcollector_out_" + self.output_prefix

        self.news_dirpath = self.out_dirpath + "\\"
        self.socials_dirpath = self.out_dirpath + "\\"
        self.others_dirpath = self.out_dirpath + "\\"

        self.news_dirpath += "news_" + self.output_prefix + "\\"
        self.socials_dirpath += "socials_" + self.output_prefix + "\\"
        self.others_dirpath += "others_" + self.output_prefix + "\\"

        os.mkdir(self.out_dirpath)
        os.mkdir(self.news_dirpath)
        os.mkdir(self.socials_dirpath)
        os.mkdir(self.others_dirpath)

    def __toList(self): #cast database to a list
    #open database.csvasePat
        aziendecsv = pandas.read_csv(
                            self.database_path,
                            names=["citta","aziende"],
                            encoding="cp1252",
                            delimiter=self.delimiter
                        )

    #form list > [ [STR comune, STR azienda], [com, azi], ...]
        citta=aziendecsv.citta.tolist()
        aziende=aziendecsv.aziende.tolist()
        database=[]

        i=0
        while i < len(aziende):
            database.append([ str(citta[i]),str(aziende[i]) ])
            i+=1
    #return list
        return database

    def acquire(self):  #mutex acquire
        if self.mutex.acquire():
            return True

        return False

    def release(self):  #mutex release
        self.mutex.release()

    def run(self):
        for i in range(self.qty_threads):
            t=Collector("spider" + str(i), self, self.num_results)
            t.start()


###################################################################################
#test
LinksCollector(
    "My link collector",    #NAME,
    ".\\prova\\analisi_montascale.csv", #DATABASE PATH
    "C:\\Users\\xizh0\\Documents\\",    #OUTPUT PATH
    "montascale",   #OUTPUT FILE PREFIX
    ",",    #DELIM ITER
    5,  #ELEMENTS/SERP
    9   #QTY OF THREADS
).start()
