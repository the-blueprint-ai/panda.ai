from langchain.tools.base import BaseTool
from typing import Any, List, Optional, Sequence, Type, Union, Dict
from config import settings
import logging
import random
import requests
from requests.exceptions import JSONDecodeError
from urllib.parse import quote
from datetime import date, datetime, timedelta

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# TOOLS
class NewsSearchTool(BaseTool):
    name = "News"
    description = "Use this when you want to get information about the top headlines of current news stories. The input should be a question in natural language that this API can answer."

    def _run(self, query: str) -> Dict:
        # URL-encode the query parameter
        encoded_query = quote(query)

        # Calculate the date range for the last week
        today = datetime.today()
        last_week = today - timedelta(days=5)
        from_date = last_week.strftime('%Y-%m-%d')
        to_date = today.strftime('%Y-%m-%d')

        url = ('https://newsapi.org/v2/everything?'
            f'q={encoded_query}&'
            f'from={from_date}&'
            f'to={to_date}&'
            'language=en&'
            'sortBy=popularity&'
            'apiKey=27161a2559d247abb02c031f5e065837')
        
        response = requests.get(url)
        json_response = response.json()

        # Limit the results to the top 5 articles
        top_5_articles = json_response['articles'][:5]
        json_response['articles'] = top_5_articles

        # Generate an HTML ordered list
        html_list_items = []
        for i, article in enumerate(top_5_articles):
            source_name = article['source'].get('name') or article['source'].get('Name') or "Unknown"
            html_list_items.append(f"<li><a class='text-primary' href='{article['url']}' target='_blank' style='text-decoration: none'>{article['title']} ({source_name})</a></li>")
        html_list = f"<div class='card text-bg-light text-center'><div class='card-header text-uppercase pt-3 pb-2 px-3'><h2 class='text-uppercase'>{query}</h2></div><div class='card-body text-start pt-2 pb-1 px-2'><ol>" + "".join(html_list_items) + "</ol></div></div>"
        
        return html_list

    async def _arun(self, query: str) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("News API does not support async")


class WikipediaSearchTool(BaseTool):
    name = "Wikipedia"
    description = "Use this when you want to search wikipedia about things you have no knowledge of. The input to this should be a single search term."

    def get_wiki_image(self, query, response):
        data = response.json()

        if data.get('originalimage') and data['originalimage'].get('source'):
            return data['originalimage']['source']

        url = f'https://en.wikipedia.org/api/rest_v1/page/media-list/{query}'
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            # Parse the data and return the desired value
            return data['items'][0]['srcset'][0]['src']
        else:
            # Handle the error or return a default value
            return None

    def _run(self, query: str) -> str:
        queryUnderscored = query.replace(" ", "_")
        url = ('https://en.wikipedia.org/api/rest_v1/page/summary/'
            f'{queryUnderscored}?redirect=false')

        response = requests.get(url)

        if response.status_code == 200:
            try:
                data = response.json()
            except JSONDecodeError:
                return f"🐼 I'm so sorry! The Wikipedia entry on {query} is unavailable at the moment. Please try again later."

            # Parse the data and return the desired value
            wikiTitle = data.get('title', 'No title available')
            wikiURL = data['content_urls']['desktop']['page']
            wikiExtract = data.get('extract', 'No summary available')
            wikiImage = self.get_wiki_image(queryUnderscored, response)

            html = f"""
    <div class='card text-bg-light text-center'>
        <a href="{wikiURL}" target="_blank"><img class="card-img-top" src="{wikiImage}" /></a>
        <div class='card-body pt-2 pb-1 px-2'>
            <h2 class="text-primary text-uppercase mt-2"><a class='text-primary' href="{wikiURL}" target="_blank" style='text-decoration: none'>{wikiTitle}</a></h2>
            <p class="card-text">{wikiExtract}</p>
        </div>
        <div class="card-footer pt-2 pb-2 px-2">
             <a href="{wikiURL}" target="_blank"><button class="btn btn-secondary btn-lg text-center" style='width: 80%'>SEE MORE...</button></a>
        </div>
    </div>
        """
            return html
        else:
            # Handle the error or return a default value
            return f"🐼 I'm so sorry! The Wikipedia entry on {query} is unavailable at the moment. Please try again later."

    async def _arun(self, query: str) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("Wikipedia API does not support async")
    

class YouTubeSearchTool(BaseTool):
    name = "YouTube"
    description = "Use this when you want to search for videos. The input to this should be a single search term."

    def _run(self, query: str) -> str:
        # URL-encode the query parameter
        encoded_query = quote(query)
        url = ('https://www.googleapis.com/youtube/v3/search?maxResults=5&q='
            f'{encoded_query}&key={settings.YOUTUBE_API_KEY}&type=video&part=snippet')

        response = requests.get(url)

        if response.status_code == 200:
            try:
                data = response.json()
                # Parse the data and return the desired value
                ytVideoId = None
                for item in data['items']:
                    if 'videoId' in item['id']:
                        ytVideoId = item['id']['videoId']
                        break

                if ytVideoId:
                    html = f"""
    <div class="card text-bg-light text-center">
        <div class='card-header text-uppercase pt-3 pb-2 px-3'>
            <a href="https://www.youtube.com/watch?v={ytVideoId}" target="_blank" style='text-decoration: none'><h2 class='text-primary text-uppercase'>{query}</h2></a>
        </div>
        <div class='card-body pt-2 pb-1 px-2' style='max-width: 100%'>
            <iframe width="100%" height="280" src="https://www.youtube-nocookie.com/embed/{ytVideoId}" title="" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
        </div>
        <div class="card-footer pt-2 pb-2 px-2">
            <a href="https://www.youtube.com/watch?v={ytVideoId}" target="_blank"><button class="btn btn-secondary btn-lg text-center" style='width: 80%'>SEE MORE...</button></a>
        </div>
    </div>
                    """
                    return html
                else:
                    # Handle the error or return a default value
                    return "🐼 I'm so sorry! I couldn't find a YouTube video about that unfortunately."
            except JSONDecodeError:
                return "🐼 I'm so sorry! I can't find that YouTube video at the moment. Please try again later."
            
    async def _arun(self, query: str) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("YouTube API does not support async")


class GoogleMapsSearchTool(BaseTool):
    name = "Google Maps"
    description = "Use this when you want to search for a location or get a map. The input to this should be a single search term."

    def _run(self, query: str) -> str:
        # URL-encode the query parameter
        encoded_query = quote(query)
        url = "https://www.google.com/maps/embed/v1/place?"f"key={settings.GOOGLE_MAPS_API_KEY}&q={encoded_query}"

        return f"""
            <div class="card text-bg-light text-center">
                <div class='card-header text-uppercase pt-3 pb-2 px-3'>
                    <a href="https://www.google.com/maps/search/{encoded_query}" target="_blank" style='text-decoration: none'><h2 class='text-primary text-uppercase'>{query}</h2></a>
                </div>
                <div class='card-body pt-2 pb-1 px-2' style='width: 100%'>
                    <iframe width="100%" height="315" frameborder="0" style="border:0" referrerpolicy="no-referrer-when-downgrade" src={url} allowfullscreen></iframe>
                </div>
                <div class="card-footer pt-2 pb-2 px-2">
                    <a href="https://www.google.com/maps/search/{encoded_query}" target="_blank"><button class="btn btn-secondary btn-lg text-center" style='width: 80%'>SEE MORE...</button></a>
                </div>
            </div>
                """
            
    async def _arun(self, query: str) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("YouTube API does not support async")


class GoogleImageSearchTool(BaseTool):
    name = "Google Images"
    description = "Use this when you want to search for images. The input to this should be a single search term."

    def _run(self, query: str) -> str:
        # URL-encode the query parameter
        encoded_query = quote(query)

        url = 'https://customsearch.googleapis.com/customsearch/v1'
        params = {
            'key': settings.GOOGLE_SEARCH_API_KEY,
            'cx': settings.GOOGLE_SEARCH_ENGINE_ID,
            'q': encoded_query,
            'searchType': 'image'
        }

        response = requests.get(url, params=params)

        if response.status_code == 200:
            try:
                data = response.json()
                # Parse the data and return the desired value
                results = data['items']

                # Get a random sample of 6 items
                random_items = random.sample(results, 6)

                # Generate HTML for 5 random items
                html_items = ''
                for idx, item in enumerate(random_items):
                    html_items += f'<a href="{item["image"]["contextLink"]}" target="_blank"><img class="img-thumbnail mb-2" src="{item["link"]}" alt="{item["title"]}" /></a>'

                html = f"""
        <div class="card text-bg-light text-center">
            <div class="card-header text-uppercase pt-3 pb-2 px-3">
                <a href="https://www.google.com/search?q={encoded_query}&tbm=isch" target="_blank" style='text-decoration: none'><h2 class='text-primary'>{query} IMAGES</h2></a>
            </div>
            <div class="card-body pt-2 pb-2 px-2">
                {html_items}
            </div>
            <div class="card-footer pt-2 pb-2 px-2">
                <a href="https://www.google.com/search?q={encoded_query}&tbm=isch" target="_blank"><button class="btn btn-secondary btn-lg text-center" style='width: 80%'>SEE MORE...</button></a>
            </div>
        </div>
                        """
                return html

            except JSONDecodeError:
                return "🐼 I'm so sorry! I can't find respond to that image search at the moment. Please try again later."
            
    async def _arun(self, query: str) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("Google search API does not support async")


class GoogleSearchTool(BaseTool):
    name = "Google Search"
    description = "Use this when you want to search the internet to answer questions about things you have no knowledge of. The input to this should be a single search term."

    def _run(self, query: str) -> str:
        # URL-encode the query parameter
        encoded_query = quote(query)

        url = 'https://customsearch.googleapis.com/customsearch/v1'
        params = {
            'key': settings.GOOGLE_SEARCH_API_KEY,
            'cx': settings.GOOGLE_SEARCH_ENGINE_ID,
            'q': encoded_query,
            'dateRestrict': 'm1',
            'safe': 'active'
        }

        response = requests.get(url, params=params)

        if response.status_code == 200:
            try:
                data = response.json()
                # Parse the data and return the desired value
                results = data['items']

                # Iterate through the array and collect up to 5 items that don't contain more than 2 %20 in the snippet
                html_items = ''
                count = 0
                for item in results:
                    if item['snippet'].count('%20') <= 2:
                        if "pagemap" in item:
                            image_src = item["pagemap"]["cse_image"][0]["src"] if "cse_image" in item["pagemap"] and item["pagemap"]["cse_image"] else None
                        else:
                            image_src = None

                        html_items += f'<li class="list-group-item"><a class="text-primary" href="{item["link"]}" target="_blank" style="text-decoration: none"><h4 class="text-uppercase mt-2">{item["title"]}</h4></a><div class="googleSearchItemContent d-flex flex-row align-items-center">'
                        if image_src:
                            html_items += f'<a class="me-3" href="{item["link"]}" target="_blank" style="width: 50%"><img class="img-thumbnail" src="{image_src}" alt="{item["title"]}" /></a>'
                        html_items += f'<p class="card-text">{item["snippet"]}</p></div></li>'
                        count += 1

                    if count == 5:
                        break

                # Fill in remaining slots with default message or blank content if there are fewer than 5 items
                while count < 5:
                    html_items += '<div class="googleSearchItem"><div class="googleSearchItemTitle"><h2>No result found</h2></div><div class="googleSearchItemContent"><p></p></div></div>'
                    count += 1

                html = f"""
        <div class="card text-bg-light text-center">
            <div class="card-header text-uppercase pt-3 pb-2 px-3">
                <a href="https://www.google.com/search?q={encoded_query}&dateRestrict=m1&safe=active" target="_blank" style='text-decoration: none'><h2 class='text-primary'>{query} SEARCH RESULTS</h2></a>
            </div>
            <div class="card-body text-start pt-0 pb-0 px-0">
                <ul class="list-group list-group-flush">
                    {html_items}
                </ul>
            </div>
            <div class="card-footer pt-2 pb-2 px-2">
                <a href="https://www.google.com/search?q={encoded_query}&dateRestrict=m1&safe=active" target="_blank"><button class="btn btn-secondary btn-lg text-center" style="width: 80%">SEE MORE...</button></a>
            </div>
        </div>
                        """
                return html

            except JSONDecodeError:
                return "🐼 I'm so sorry! I can't find respond to that search at the moment. Please try again later."
            
    async def _arun(self, query: str) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("Google search API does not support async")

class SpotifySearchTool(BaseTool):
    name = "Spotify Search"
    description = "Use this when you want to search for music. The input to this should be a single search term."

    def get_spotify_access_token(self):
        data = {
            "grant_type": "client_credentials",
            "client_id": settings.SPOTIFY_CLIENT_ID,
            "client_secret": settings.SPOTIFY_CLIENT_SECRET,
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        response = requests.post(settings.SPOTIFY_TOKEN_URL, data=data, headers=headers)
        response.raise_for_status()
        return response.json()["access_token"]


    def get_playlist_url(self, query: str, access_token: str):
        # URL-encode the query parameter
        encoded_query = quote(query)
        headers = {
            "Authorization": f"Bearer {access_token}",
        }
        params = {
            "q": encoded_query,
            "type": "playlist",
        }
        response = requests.get(settings.SPOTIFY_SEARCH_URL, headers=headers, params=params)
        response.raise_for_status()
        items = response.json()["playlists"]["items"]
        for item in items:
            if item["owner"]["display_name"] == "Spotify":
                return item["external_urls"]["spotify"]
        return None

    def _run(self, query: str) -> str:
        # URL-encode the query parameter
        access_token = self.get_spotify_access_token()
        playlist_url = self.get_playlist_url(query, access_token)

        if not playlist_url:
            return f"I'm sorry! I couldn't find any music when I searched for {query} 🐼"

        params = {
            "url": playlist_url,
        }
        response = requests.get(settings.SPOTIFY_EMBED_URL, params=params)
        response.raise_for_status()
        html_data = response.json()["html"]

        # Remove escape characters by loading the string as a JSON object
        unescaped_html_data = html_data.replace('\\', '')

        html_content = f"""<div class="spotifyMusicAnswer">{unescaped_html_data}</div>"""
        return html_content
    
    async def _arun(self, query: str) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("Spotify search API does not support async")
            

class TMDBSearchTool(BaseTool):
    name = "Movie & TV Search"
    description = "Use this when you want to search for movies, tv shows or actors. The input to this should be a single search term."

    def generate_known_for_images(self, known_for):
        images = []
        for item in known_for:
            title = item.get("title", item.get("name", "Unknown"))
            img_tag = f'<img class="img-thumbnail" src="https://image.tmdb.org/t/p/w600_and_h900_bestv2/{item["poster_path"]}" alt="{title}" style="width: 30%"/>'
            images.append(img_tag)
        return "".join(images)

    def _run(self, query: str) -> str:
        url = 'https://api.themoviedb.org/3/search/multi?'
        params = {
            'query': query,
            'api_key': settings.TMDB_API_KEY
            
        }

        response = requests.get(url, params=params)


        if response.status_code == 200:
            try:
                data = response.json()
                # Parse the data and return the desired value
                results = data['results']
                logging.info("Results: " + str(results))

                if not results:
                    return "I'm so sorry! I can't find that at the moment. Please try again later 🐼"

                first_item = results[0]

                if first_item["media_type"] == "person":
                    id = first_item["id"]
                    name = first_item["name"]
                    image = first_item["profile_path"]
                    known_for = first_item["known_for"]
                    known_for_images = self.generate_known_for_images(known_for)

                    html = f"""
        <div class="card text-bg-light text-center">
            <a href="https://www.themoviedb.org/person/{id}-{name}" target="_blank"><img class="card-img-top" src="https://image.tmdb.org/t/p/w600_and_h900_bestv2/{image}" alt="{name}" /></a>
            <div class="card-body pt-2 pb-1 px-2 text-center">
                <a href="https://www.themoviedb.org/person/{id}-{name}" target="_blank" style="text-decoration: none"><h2 class="text-primary text-uppercase">{name}</h2></a>

                <div class="tmdbAnswerContentDetails">
                    <h2>KNOWN FOR:</h2>
                    <div class="tmdbAnswerContentDetailsKnownFor d-flex justify-content-between">
                        {known_for_images}
                    </div>
                </div>
            </div>
            <div class="card-footer pt-2 pb-2 px-2">
                <a href="https://www.themoviedb.org/movie/{id}-{name}" target="_blank"><button class="btn btn-secondary btn-lg text-center" style="width: 80%">SEE MORE...</button></a>
            </div>
        </div>
                        """
                        
                elif first_item["media_type"] == "movie":
                    id = first_item["id"]
                    name = first_item["title"]
                    overview = first_item["overview"]
                    image = first_item["poster_path"]
                    release_date = first_item["release_date"]
                    date_obj = datetime.strptime(release_date, "%Y-%m-%d")
                    formatted_date = date_obj.strftime("%-dth %B %Y")
                    rating = first_item["vote_average"]
                    formatted_rating = "{:.1f}".format(round(rating, 1))

                    html = f"""
        <div class="card text-bg-light text-center">
            <a href="https://www.themoviedb.org/movie/{id}-{name}" target="_blank"><img class="card-img-top" src="https://image.tmdb.org/t/p/w600_and_h900_bestv2/{image}" alt="{name}" /></a>
            <div class="card-body pt-2 pb-1 px-2 text-start">
                <a href="https://www.themoviedb.org/movie/{id}-{name}" target="_blank" style="text-decoration: none"><h2 class="text-primary text-uppercase">{name}</h2></a>
                <div class="movieSubtitle d-flex">
                    <div class="movieReleaseDate me-5">
                        <h6 class="card-subtitle text-muted">RELEASE DATE:</h6>
                        <p class="card-subtitle text-muted">{formatted_date}</p>
                    </div>
                    <div class="movieRating">
                        <h6 class="card-subtitle text-muted">TMDB RATING:</h6>
                        <p class="card-subtitle text-muted">{formatted_rating}</p>
                    </div>
                </div>
                <p class="card-text mt-1 mb-3">{overview}</p>
            </div>
            <div class="card-footer pt-2 pb-2 px-2">
                <a href="https://www.themoviedb.org/movie/{id}-{name}" target="_blank"><button class="btn btn-secondary btn-lg text-center" style="width: 80%">SEE MORE...</button></a>
            </div>
        </div>
                        """

                elif first_item["media_type"] == "tv":
                    id = first_item["id"]
                    name = first_item["name"]
                    overview = first_item["overview"]
                    image = first_item["poster_path"]
                    release_date = first_item["first_air_date"]
                    date_obj = datetime.strptime(release_date, "%Y-%m-%d")
                    formatted_date = date_obj.strftime("%-dth %B %Y")
                    rating = results[0]["vote_average"]
                    formatted_rating = "{:.1f}".format(round(rating, 1))

                    html = f"""
        <div class="card text-bg-light text-center">
            <a href="https://www.themoviedb.org/tv/{id}-{name}" target="_blank"><img class="card-img-top" src="https://image.tmdb.org/t/p/w600_and_h900_bestv2/{image}" alt="{name}" /></a>
            <div class="card-body pt-2 pb-1 px-2 text-start">
                <a href="https://www.themoviedb.org/tv/{id}-{name}" target="_blank" style="text-decoration: none"><h2 class="text-primary text-uppercase">{name}</h2></a>
                <div class="movieSubtitle d-flex">
                    <div class="movieReleaseDate me-5">
                        <h6 class="card-subtitle text-muted">RELEASE DATE:</h6>
                        <p class="card-subtitle text-muted">{formatted_date}</p>
                    </div>
                    <div class="movieRating">
                        <h6 class="card-subtitle text-muted">TMDB RATING:</h6>
                        <p class="card-subtitle text-muted">{formatted_rating}</p>
                    </div>
                </div>
                <p class="card-text mt-1 mb-3">{overview}</p>
            </div>
            <div class="card-footer pt-2 pb-2 px-2">
                <a href="https://www.themoviedb.org/tv/{id}-{name}" target="_blank"><button class="btn btn-secondary btn-lg text-center" style="width: 80%">SEE MORE...</button></a>
            </div>
        </div>
                        """
                
                return html

            except JSONDecodeError:
                return "I'm so sorry! I can't find that at the moment. Please try again later 🐼"
            
    async def _arun(self, query: str) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("Google search API does not support async")