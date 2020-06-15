import requests
from bs4 import BeautifulSoup
import os
from os import listdir
from os.path import isfile, join

def read_embeds():
    dictURL = {}
    # List file names in embed directory
    mypath = "./embeds/"
    files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    # Iterate through files
    print("Cleaning embeds...")
    for file in files:
        filename = mypath + file
        with open(filename,"r") as f:
            text = f.read()
            print("Unclean Embed:", text)
            # fetch the next url
            # CHANGE!
            start = text.find("wvideo=")+ len("wvideo=")
            cleanText = text[start:].split('\"')[0]
            print("Cleaned text:", cleanText)
            extractedURL = "https://fast.wistia.net/embed/iframe/" + cleanText + "?videoFoam=true"
            dictURL[file.split('.')[0]] = extractedURL
            print("Extracted URL", extractedURL)
    # Create dict of filename:URL
    return dictURL

def extract_download_url(URL):
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')

    pull = str(soup.find("link", rel="preload").next_sibling.next_sibling.next_sibling.next_sibling)
    start = pull.find("url")+6
    stop = pull.find("created_at")-3
    result = pull[start:stop]

    return result

def download_videos(dictURL):

    for name in dictURL:
        link = dictURL[name]
        '''iterate through all links in video_links
        and download them one by one'''

        # obtain filename by splitting url and getting
        # last string
        directory = "./course/Module_" + name.split('-')[0] + "/" + name.split('-')[-1]
        file_name = link.split('/')[-1]
        full_file_name = directory + "/" + file_name

        # Create directory
        if not os.path.exists(directory):
            os.makedirs(directory)
            print("new folder created")

        print("Downloading file:%s"%full_file_name)

        # create response object
        r = requests.get(link, stream = True)

        # download started
        with open(full_file_name, 'wb') as f:
            for chunk in r.iter_content(chunk_size = 1024*1024):
                if chunk:
                    f.write(chunk)

        print(full_file_name, "downloaded!")

    print("All videos downloaded!")
    return

# MAIN
if __name__ == "__main__":
    print("Beginning to scrape...")
    # Create a list of URLs from copied embeds
    uncleanDictURL = read_embeds()
    cleanDictURL = {}

    # Clean each url
    for name in uncleanDictURL:
        cleanDictURL[name] = extract_download_url(uncleanDictURL[name])

    print("cleaned URL dictionary", cleanDictURL)
    download_videos(cleanDictURL)
