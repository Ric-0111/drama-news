import requests
import os
from feedgen.feed import FeedGenerator
from datetime import datetime, timezone

# GitHubのSecretsからキーを読み込む設定
TMDB_API_KEY = os.environ.get('TMDB_API_KEY')

def get_trending_tv_shows():
    url = f"https://api.themoviedb.org/3/trending/tv/day?api_key={TMDB_API_KEY}&language=ja-JP"
    response = requests.get(url)
    data = response.json()
    all_shows = data.get('results', [])
    return [s for s in all_shows if s.get('original_language') != 'ja'][:5]

def generate_rss():
    shows = get_trending_tv_shows()
    fg = FeedGenerator()
    fg.id('https://www.themoviedb.org/')
    fg.title('最新海外ドラマトレンド')
    fg.author({'name': 'Drama Bot'})
    fg.link(href='https://www.themoviedb.org/', rel='alternate')
    fg.description('TMDBから取得した最新の話題作リストです')
    fg.language('ja')

    for show in shows:
        fe = fg.add_entry()
        fe.id(str(show.get('id')))
        fe.title(show.get('name'))
        fe.link(href=f"https://www.themoviedb.org/tv/{show.get('id')}")
        fe.description(show.get('overview'))
        fe.pubDate(datetime.now(timezone.utc))

    # rss.xmlとして保存
    fg.rss_file('rss.xml')

if __name__ == "__main__":
    generate_rss()
