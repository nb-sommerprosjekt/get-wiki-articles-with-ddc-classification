import wikipedia
from bs4 import BeautifulSoup
import requests
def get_articles():
    wikipedia.set_lang("no")
    sok = wikipedia.search('"Eksterne baser (Autoritetsdata) GND"', results = 5000)
    pages = []
    error_searchTerm = open("error_file.txt","w")
    url_file = open("url_wiki_save.txt","w")
    for title in sok:

        try:
            page = wikipedia.page(title)
            pages.append(page)
            urls = []
        except wikipedia.exceptions.DisambiguationError:
            print("Dette var feil")
            error_searchTerm.write(title+'\n')
        text = open("wiki_data/"+title+".txt","w")
        meta_path = "wiki_data/"+title+"-meta.txt"
        meta_file = open(meta_path,"w")
        if get_gnd_url_from_html(page.html()) is not None:
            meta_file.write(get_gnd_url_from_html(page.html()))
        else:
            meta_file.write("mangler meta-data")
        text.write(page.content)
        text.close()
        meta_file.close()

def get_gnd_url_from_html(html_doc):
    #html_doc = open(html_doc_path, "r")
    #print("lololol")
    soup = BeautifulSoup(html_doc,'html.parser')

    for link  in soup.find_all('a'):
        if link.get('href') is not None:
            if "d-nb.info" in link.get('href'):
                gnd_link = link.get('href')
                return get_dewey_from_gnd(gnd_link)



def get_dewey_from_gnd (url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    td_soup = iter(soup.find_all('td'))

    td_all = []
    for td in td_soup :
        iter_td = iter(td)
        for element in td:
            if "DDC-Notation" in element:
                td_all.append(next(td_soup))
    dewey =[]
    for element in td_all:
        dewey = str(element).replace('<td>','')
        dewey = dewey.replace('</td>','')
        dewey = dewey.replace('<br/>',' ')
        dewey = dewey.strip()
        dewey_u_html = BeautifulSoup(dewey).text
        dewey_stripped = dewey_u_html.strip()
        print(dewey_stripped)

        return dewey_u_html


    #print(len(td_all))
    #print(type(td_all))
    #print(len(td_all[9]))
    #print(type(dewey))
    #print(dewey)
    #print(type(td_all[0]))
    #print(len(td_all))

if __name__ == '__main__':
    get_articles()
    #get_gnd_url_from_htlm()