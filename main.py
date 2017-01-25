# Extract main content from blogs, -> Written for downloading Light Novels
# Explicitly for Overlord Volumes but it may be used for different things
# Depending on how much you are willing to change the program itself.
# Lots of thanks to the translators and overlordvolume10.blogspot.com
import urllib2, re, pdf_export, os, tools, webbrowser, urllib
from bs4 import BeautifulSoup

url_bag = []

def crawler(root_url):
    route = get_links(root_url)
    for link in route:
        print link
        construct_chapter(link)

def get_links(url):
    html = urllib2.urlopen(url).read()
    soup = BeautifulSoup(html, "html.parser")
    for link in soup.find_all(class_="posts"):
        tmp_links = (str(link)).split()
        for part in tmp_links:
            if part.startswith("href"):
                m = re.search("\".+\"", part)
                tmp_cln = (m.group()).strip("\"")
                url_bag.append(tmp_cln)
    return url_bag

def txt_pather(filename):
    return os.path.join("texts", filename + ".txt")

def get_images(url = None, soup = None, min_size = 300):
    images = []
    if soup == None:
        html = urllib2.urlopen(url).read()
        soup = BeautifulSoup(html, "html.parser")
    for image in soup.find_all("img", height=True):
        if int(image.get('height', 'n/a')) >= min_size:
            images.append(str(image.get("src")))
    webbrowser.open(str(images[0]))
    return images

def get_text(url = None, soup = None):
    if soup == None:
        html = urllib2.urlopen(url).read()
        soup = BeautifulSoup(html, "html.parser")
    for script in soup(["script", "style"]): script.extract()
    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines()) # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  ")) # drop blank line
    text = '\n'.join(chunk for chunk in chunks if chunk) # Feels like a tongue twister
    text = text.encode('utf-8')
    last_num = text.find("Previous Chapter") # Change for different web pages
    return text[:last_num]
    return text

def construct_chapter(url, images = False, filename = None):
    """Get chapter text and save to text file"""
    global title
    html = urllib2.urlopen(url).read()
    soup = BeautifulSoup(html, "html.parser")
    #-------------------------------------------
    chapter_raw_title = str(soup.find("title"))
    chapter_raw_title = chapter_raw_title.split(":");
    chapter_title = str(chapter_raw_title[1])
    chapter_title = chapter_title.strip("</title>")
    chapter_title = re.sub('[^A-Za-z0-9]+', ' ', chapter_title)

    if filename == None: filename = chapter_title
    if images == True: image = str( (get_images(soup = soup))[0] )
    else: image = None
    main_text = get_text(soup = soup)

    with open(txt_pather(filename), "w+") as txt_file:
        txt_file.write(main_text)

def merge_and_export():
    pdf.set_title(title) # Change for different docs
    pdf.set_author(author) # Change """
    pass

crawler("http://overlordvolume10.blogspot.com.tr/2016/06/V10C25.html")
