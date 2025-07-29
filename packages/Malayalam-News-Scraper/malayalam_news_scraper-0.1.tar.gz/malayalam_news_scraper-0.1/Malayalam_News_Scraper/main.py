import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0"
}


#FOR TRUE COPY
def TrueCopy(url):
  response = requests.get(url, headers=headers)
  soup = BeautifulSoup(response.content, "html.parser")

  # Extract the heading (adjusted for the new tag and class)
  title_tag = soup.find("h1", {"itemprop": "headline", "class": "title is__sans"})
  title = title_tag.get_text(strip=True) if title_tag else "No heading found"

  # Date
  date_tag = soup.find("div", class_="post_date")
  date = date_tag.get_text(strip=True) if date_tag else None

  # Author (if available)
  author_tag = soup.find("div", class_="author-name")
  author = author_tag.get_text(strip=True) if author_tag else None

  # Article content
  content_div = soup.find("div", class_="article_content")
  paragraphs = content_div.find_all("p") if content_div else []
  article_text = "\n".join(p.get_text(strip=True) for p in paragraphs)

  return {
        "title": title,
        "publish_date": date,
        "content": article_text
    }

#For Asianet News



def Asianet(url):
  # Request the page
  response = requests.get(url, headers=headers)
  soup = BeautifulSoup(response.content, "html.parser")

  # Extract <meta name="description">
  meta_description_tag = soup.find("meta", attrs={"name": "description"})
  meta_description = meta_description_tag["content"] if meta_description_tag else "No meta description found"

  # Extract <title> tag from the <head>
  page_title_tag = soup.find("title")
  page_title = page_title_tag.get_text(strip=True) if page_title_tag else None
  # Extract main news title (heading)
  title_tag = soup.find("h1", class_="story-heading")
  title = title_tag.get_text(strip=True) if title_tag else None

  # Extract publish date
  date_tag = soup.find("div", class_="authordate")
  publish_date = date_tag.get_text(strip=True) if date_tag else None
  # Extract news content
  postbody_div = soup.find("div", class_="PostBody postbodyneww")
  paragraphs = []
  if postbody_div:
      for p_tag in postbody_div.find_all("p"):
          text = p_tag.get_text(strip=True)
          if text:
              paragraphs.append(text)

  full_news = "\n\n".join(paragraphs)

  return {
        "title": page_title,
        "publish_date": publish_date,
        "content": full_news
    }
  return page_title, publish_date, full_news


#JaiHind
def JaiHind(url):
  # Request the page
  response = requests.get(url, headers=headers)

  # Check if the request was successful
  if response.status_code == 200:
      # Parse the content with BeautifulSoup
      soup = BeautifulSoup(response.content, 'html.parser')

      # Extract title
      title_tag = soup.find("h1", class_="inner-main-head1")
      title = title_tag.get_text(strip=True) if title_tag else "No title found"

      # Extract publish date
      date_tag = soup.find("div", class_="inner-news-date")
      publish_date = date_tag.get_text(strip=True) if date_tag else "No date found"

      # Extract news content
      news_content_div = soup.find("div", class_="news-content-inner")
      paragraphs = []

      # Ensure content is found
      if news_content_div:
          print(news_content_div.get_text(strip=True))  # Check if content exists
          for p_tag in news_content_div.find_all("p"):
              text = p_tag.get_text(strip=True)
              if text:
                  paragraphs.append(text)

      full_news = "\n\n".join(paragraphs)

      return {
        "title": title,
        "publish_date": publish_date,
        "content": full_news
    }


#Manorama

# Request the page
def Manorama(url):
  response = requests.get(url, headers=headers)
  soup = BeautifulSoup(response.content, "html.parser")

  # Extract <meta name="description">
  meta_description_tag = soup.find("meta", attrs={"name": "description"})
  meta_description = meta_description_tag["content"] if meta_description_tag else "No meta description found"

  # Extract <title> tag from the <head>
  page_title_tag = soup.find("title")
  page_title = page_title_tag.get_text(strip=True) if page_title_tag else None

  # Extract main news title (heading)
  title_tag = soup.find("h1", class_="article-header--title")
  title = title_tag.get_text(strip=True) if title_tag else None

  # Extract publish date
  date_tag = soup.find("div", class_="article-header--tagline")
  publish_date = date_tag.get_text(strip=True) if date_tag else None
  # Extract news content
  postbody_div = soup.find("div", class_="rte")
  paragraphs = []
  if postbody_div:
      for p_tag in postbody_div.find_all("p"):
          text = p_tag.get_text(strip=True)
          if text:
              paragraphs.append(text)

  full_news = "\n\n".join(paragraphs)


  return {
        "title": page_title,
        "publish_date": publish_date,
        "content": full_news
    }

#Mathrubhumi

def Mathrubhumi(url):
  # Request the page
  response = requests.get(url, headers=headers)

  # Check if the request was successful
  if response.status_code == 200:
      # Parse the content with BeautifulSoup
      soup = BeautifulSoup(response.content, 'html.parser')

      # Extract title
      title_tag = soup.find("h1", class_="malayalam")
      title = title_tag.get_text(strip=True) if title_tag else "No title found"

      # Extract publish date
      date_tag = soup.find("div", class_="mpp-story-column-profile-desc")
      publish_date = date_tag.get_text(strip=True) if date_tag else "No date found"

      # Extract news content
      news_content_div = soup.find("div", class_="article_contents")
      paragraphs = []

      # Ensure content is found
      if news_content_div:
          print(news_content_div.get_text(strip=True))  # Check if content exists
          for p_tag in news_content_div.find_all("p"):
              text = p_tag.get_text(strip=True)
              if text:
                  paragraphs.append(text)

      full_news = "\n\n".join(paragraphs)
      return {
        "title": title,
        "publish_date": publish_date,
        "content": full_news
    }


#Reporter

def Reporter(url):
  # Request the page
  response = requests.get(url, headers=headers)

  # Check if the request was successful
  if response.status_code == 200:
      # Parse the content with BeautifulSoup
      soup = BeautifulSoup(response.content, 'html.parser')

      # Extract title
      title_tag = soup.find("div", class_="newsDetailMainHead")
      title = title_tag.get_text(strip=True) if title_tag else "No title found"

      # Extract publish date
      date_tag = soup.find("div", class_="read")
      publish_date = date_tag.get_text(strip=True) if date_tag else "No date found"

      # Extract news content
      news_content_div = soup.find("div", class_="wrapper")
      paragraphs = []

      # Ensure content is found
      if news_content_div:
          print(news_content_div.get_text(strip=True))  # Check if content exists
          for p_tag in news_content_div.find_all("p"):
              text = p_tag.get_text(strip=True)
              if text:
                  paragraphs.append(text)

      full_news = "\n\n".join(paragraphs)

      return {
        "title": title,
        "publish_date": publish_date,
        "content": full_news
    }

def Janayugam(url):
  # Request the page
  response = requests.get(url, headers=headers)

  # Check if the request was successful
  if response.status_code == 200:
      # Parse the content with BeautifulSoup
      soup = BeautifulSoup(response.content, 'html.parser')

      # Extract title
      title_tag = soup.find("h1", class_="title featured_title")
      title = title_tag.get_text(strip=True) if title_tag else "No title found"

      # Extract publish date
      date_tag = soup.find("div", class_="date_name")
      publish_date = date_tag.get_text(strip=True) if date_tag else "No date found"

      # Extract news content
      news_content_div = soup.find("div", class_="news-content")
      paragraphs = []

      # Ensure content is found
      if news_content_div:
          # print(news_content_div.get_text(strip=True))  # Check if content exists
          for p_tag in news_content_div.find_all("p"):
              text = p_tag.get_text(strip=True)
              if text:
                  paragraphs.append(text)

      full_news = "\n\n".join(paragraphs)

      return {
        "title": title,
        "publish_date": publish_date,
        "content": full_news
    }
  
import re

def scrape_news_by_url(url):
    if "https://www.asianetnews.com/" in url:
        return Asianet(url)
    elif "https://www.manoramaonline.com/" in url:
        return Manorama(url)
    elif "https://www.mathrubhumi.com/" in url:
        return Mathrubhumi(url)
    elif "https://www.reporterlive.com/" in url:
        return Reporter(url)
    elif "https://truecopythink" in url:  # Replace with actual TrueCopy domain if available
        return TrueCopy(url)
    elif "https://jaihindtv.in/" in url:
        return JaiHind(url)
    elif "https://janayugomonline.com/" in url:
        return Janayugam(url)
    else:
        return {"error": "No matching parser for the provided URL \n This one only accepts Asianet, Manorama, Mathrubhumi, Reporter, TrueCopyThink, jaihindtv, janayugomonline"}
