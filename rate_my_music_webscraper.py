import traceback
import requests
import time
import os
import re
import pandas as pd
import numpy as np

from bs4 import SoupStrainer, BeautifulSoup


def loop_through_pages():
    albums = []
    artists = []
    genres = []
    sec_genres = []
    album_descriptors = []
    page_num = 1
    cleaner = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')

    try:
        running = True

        while running == True:
            print(page_num)
            page = get_page(page_num)

            item_boxes = has_item_boxes(page)

            if item_boxes != False:
                for item_box in item_boxes:
                    for lines in item_box:
                        for line in lines:
                            line = str(line)

                            if 'topcharts_item_title' in line:
                                title = re.sub(cleaner, '', line)
                                albums.append(title)

                            if 'topcharts_item_artist_newmusicpage topcharts_item_artist' in line:
                                artist = re.sub(cleaner, '', line)
                                artists.append(artist)

                            if 'genre topcharts_item_genres' in line:
                                genre = re.sub(cleaner, '', line)
                                genres.append(genre)

                            if 'genre topcharts_item_secondarygenres' in line:
                                sec_genre = re.sub(cleaner, '', line)
                                sec_genres.append(sec_genre)

                            if 'topcharts_item_descriptors' in line:
                                if len(genres) != len(sec_genres):
                                    sec_genres.append(False)
                                album_descriptor = re.sub(cleaner, '', line)
                                album_descriptors.append(album_descriptor)
            

            else:
                running = False

            page_num += 1
            time.sleep(45)

        df = pd.DataFrame({'Album': albums,
                            'Artist': artists,
                            'Genres': genres,
                            'Secondary_Genres': sec_genres,
                            'Album_Descriptors': album_descriptors})

        return df

    except Exception:
        traceback.print_exc()
        print("getAndParseHtmlTitles() Catch")


def has_item_boxes(page):
    item_bodies_filter = SoupStrainer('div', attrs={'class': 'topcharts_itembox chart_item_release'})
    soup_bodies = BeautifulSoup(page.content, 'html.parser', parse_only=item_bodies_filter)
    item_bodies = soup_bodies.find_all('div', attrs={'class': 'topcharts_itembox chart_item_release'})

    if item_bodies:
        return item_bodies
    
    return False


def get_page(page_num):
    if page_num == 1:
        url = 'http://webcache.googleusercontent.com/search?q=cache:https://rateyourmusic.com/charts/top/album/all-time/#results&strip=0&vwsrc=0'
    else:
        url = 'http://webcache.googleusercontent.com/search?q=cache:https://rateyourmusic.com/charts/top/album/all-time/{}/#results&strip=0&vwsrc=0'.format(page_num)
    requests_session = requests.Session()
    page = requests_session.get(url)

    return page



df = loop_through_pages()

df.to_csv('albums4.csv')