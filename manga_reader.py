import streamlit as st
import requests
from urllib.parse import quote
import random
from bs4 import BeautifulSoup


greetings = [
    "Konnichiwa!", "Ohayou gozaimasu!", "Konbanwa!", "Sayonara!", 
    "Arigatou gozaimasu!", "Ittekimasu!", "Tadaima!", "Okaerinasai!", 
    "Itadakimasu!", "Gochisousama deshita!"
]


songs = [
    {"title": "Shape of You - Ed Sheeran", "video_id": "JGwWNGJdvx8"},
    {"title": "Blinding Lights - The Weeknd", "video_id": "4NRXx6U8ABQ"},
    {"title": "Uptown Funk - Mark Ronson ft. Bruno Mars", "video_id": "OPf0YbXqDm0"},
    {"title": "Bad Guy - Billie Eilish", "video_id": "DyDfgMOUjCI"},
    {"title": "Rolling in the Deep - Adele", "video_id": "U0CGsw6h60k"},
    {"title": "Pretender - Official Hige Dandism", "video_id": "TQ8WlA2GXbk"},
    {"title": "Lemon - Kenshi Yonezu", "video_id": "S9qB7s5j5F4"},
    {"title": "Gurenge - LiSA", "video_id": "8hOpJ9CprqA"},
    {"title": "Koi - Gen Hoshino", "video_id": "W2dYQh36Y7E"},
    {"title": "Zenzenzense - RADWIMPS", "video_id": "PDSkFeMVNFs"},
    {"title": "Dynamite - BTS", "video_id": "gdZLi9oWNZg"},
    {"title": "Gangnam Style - PSY", "video_id": "9bZkp7q19f0"},
    {"title": "Boy With Luv - BTS ft. Halsey", "video_id": "XsX3ATc3FbA"},
    {"title": "How You Like That - BLACKPINK", "video_id": "ioNng23DkIM"},
    {"title": "Kill This Love - BLACKPINK", "video_id": "2S24-y0Ij3Y"},
]

def get_manga_info(manga_name):
    url = f"https://api.mangadex.org/manga?title={quote(manga_name)}&includes[]=cover_art&limit=10"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        manga_list = []
        for manga in data.get('data', []):
            manga_id = manga['id']
            title = manga['attributes']['title'].get('en', list(manga['attributes']['title'].values())[0] if manga['attributes']['title'] else 'Unknown Title')
            cover_art = next((rel for rel in manga['relationships'] if rel['type'] == 'cover_art'), None)
            cover_url = (f"https://mangadex.org/covers/{manga_id}/{cover_art['attributes']['fileName']}" 
                         if cover_art and 'fileName' in cover_art['attributes'] else 'No cover available.')
            manga_list.append({
                'id': manga_id,
                'title': title,
                'cover_url': cover_url
            })
        return manga_list if manga_list else [{"error": "No manga found."}]
    except requests.exceptions.RequestException as e:
        return [{"error": f"Error fetching manga: {e}"}]

def get_chapters(manga_id):
    url = f"https://api.mangadex.org/manga/{manga_id}/feed?translatedLanguage[]=en&order[chapter]=desc&limit=100"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        chapters = []
        for chapter in data.get('data', []):
            if chapter['attributes']['chapter']:
                chapters.append({
                    'id': chapter['id'],
                    'chapter_number': chapter['attributes']['chapter'],
                    'title': chapter['attributes']['title'] or f"Chapter {chapter['attributes']['chapter']}"
                })
        return sorted(chapters, key=lambda x: float(x['chapter_number']), reverse=True)
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching chapters: {e}")
        return []

def get_chapter_pages(chapter_id):
    url = f"https://api.mangadex.org/at-home/server/{chapter_id}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        base_url = data.get('baseUrl')
        chapter_hash = data['chapter'].get('hash')
        pages = data['chapter'].get('data', [])
        if not (base_url and chapter_hash and pages):
            return []
        return [f"https://uploads.mangadex.org/data/{chapter_hash}/{page}" for page in pages]
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching pages: {e}")
        return []

@st.cache_data
def get_gifs(manga_name):
    search_url = f"https://tenor.com/search/{quote(manga_name)}-gifs"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    try:
        response = requests.get(search_url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        img_tags = soup.find_all('img', src=True)
        gif_urls = [img['src'] for img in img_tags if img['src'].endswith('.gif')]
        return gif_urls[:3]
    except Exception as e:
        st.error(f"Error fetching GIFs: {e}")
        return []

# Streamlit app
def main():
    st.set_page_config(page_title="Manga Reader", layout="wide")
    st.title("Manga Reader App")

    # Sidebar
    with st.sidebar:
        st.header("Search Manga")
        st.write(random.choice(greetings))
        manga_name = st.text_input("Enter a manga name (e.g., One Piece):")
        if st.button("Search"):
            if manga_name:
                with st.spinner("Searching for manga..."):
                    st.session_state['manga_list'] = get_manga_info(manga_name)
                    st.session_state['selected_manga'] = None
                    st.session_state['manga_info'] = None
                    st.session_state['chapter_id'] = None
                    st.session_state['page_index'] = 0
            else:
                st.warning("Please enter a manga name.")

        # Manga selection
        if 'manga_list' in st.session_state and st.session_state['manga_list']:
            if "error" not in st.session_state['manga_list'][0]:
                manga_options = [manga['title'] for manga in st.session_state['manga_list']]
                selected_manga = st.selectbox("Choose a manga:", manga_options, key="manga_select")
                if selected_manga != st.session_state.get('selected_manga'):
                    st.session_state['selected_manga'] = selected_manga
                    selected_manga_index = manga_options.index(selected_manga)
                    st.session_state['manga_info'] = st.session_state['manga_list'][selected_manga_index]
                    st.session_state['chapter_id'] = None
                    st.session_state['page_index'] = 0

    # Main content
    if 'manga_info' in st.session_state and st.session_state['manga_info']:
        manga_info = st.session_state['manga_info']
        col1, col2 = st.columns([2, 1])

        with col1:
            st.header(manga_info['title'])
            if manga_info['cover_url'] != 'No cover available.':
                st.image(manga_info['cover_url'], caption=f"Cover of {manga_info['title']}", width=300)
            else:
                st.write("No cover image available.")

            # Chapter selection
            st.subheader("Chapters")
            with st.spinner("Loading chapters..."):
                chapters = get_chapters(manga_info['id'])
            if chapters:
                chapter_options = [f"{chapter['chapter_number']} - {chapter['title']}" for chapter in chapters]
                selected_chapter = st.selectbox("Select a chapter to read:", chapter_options, key=f"chapter_select_{manga_info['id']}")
                selected_chapter_index = chapter_options.index(selected_chapter)
                selected_chapter_id = chapters[selected_chapter_index]['id']
                
                
                if st.session_state.get('chapter_id') != selected_chapter_id:
                    st.session_state['chapter_id'] = selected_chapter_id
                    st.session_state['page_index'] = 0

                if st.session_state['chapter_id']:
                    with st.spinner("Loading pages..."):
                        pages = get_chapter_pages(st.session_state['chapter_id'])
                    if pages:
                        st.subheader(f"Reading {selected_chapter}")
                       
                        if 'page_index' not in st.session_state:
                            st.session_state['page_index'] = 0
                        col_nav1, col_nav2, col_nav3 = st.columns([1, 3, 1])
                        with col_nav1:
                            if st.button("Previous Page", disabled=st.session_state['page_index'] == 0):
                                st.session_state['page_index'] = max(0, st.session_state['page_index'] - 1)
                        with col_nav3:
                            if st.button("Next Page", disabled=st.session_state['page_index'] == len(pages) - 1):
                                st.session_state['page_index'] = min(len(pages) - 1, st.session_state['page_index'] + 1)
                        
                        try:
                            st.image(pages[st.session_state['page_index']], caption=f"Page {st.session_state['page_index'] + 1}", use_column_width=True)
                        except:
                            st.error(f"Failed to load page: {pages[st.session_state['page_index']]}")

                        # Next Chapter button
                        if selected_chapter_index > 0: 
                            if st.button("Next Chapter"):
                                st.session_state['chapter_id'] = chapters[selected_chapter_index - 1]['id']
                                st.session_state['page_index'] = 0
                                st.rerun()
                    else:
                        st.write("No pages available for this chapter.")
            else:
                st.write("No chapters found.")

        with col2:
            with st.expander("Related GIFs"):
                gif_urls = get_gifs(manga_name)
                if gif_urls:
                    for url in gif_urls:
                        st.image(url, caption=f"GIF related to {manga_info['title']}", width=200)
                else:
                    st.write("No GIFs found.")

            # Random song in an expander
            with st.expander("Random Famous Song"):
                random_song = random.choice(songs)
                video_id = random_song["video_id"]
                embed_url = f"https://www.youtube.com/embed/{video_id}?autoplay=0"
                st.components.v1.html(
                    f'<iframe width="100%" height="315" src="{embed_url}" frameborder="0" allowfullscreen></iframe>',
                    width=300, height=315
                )
                st.write(f"Song: {random_song['title']}")
                st.write("Note: This song is a random famous song in English, Japanese, or Korean, and is not related to the manga.")

        st.markdown("---")
        st.write("Manga data and images sourced from [MangaDex](https://mangadex.org).")

if __name__ == "__main__":
    main()