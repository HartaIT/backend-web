import scrapy, json
from w3lib.html import replace_escape_chars
from ..utils import cookie_parse


class InstagramSpider(scrapy.Spider):
    name = "InstagramSpider"
    allowed_domains = ["www.instagram.com"]
    start_urls = ["https://www.instagram.com/"]

    headers = {
        "x-asbd-id": 0,
        "x-csrftoken": "",
        "x-ig-app-id": 0,
        "X-Ig-Www-Claim": "",
        "x-requested-with": ""
    }
    username = 'netrom_software'

    def start_requests(self):
        yield scrapy.Request(
            url=f'https://www.instagram.com/api/v1/users/web_profile_info/?username={self.username}',
            cookies=cookie_parse(),
            headers=self.headers,
            callback=self.parse
        )

    def parse(self, response):
        resp = json.loads(response.body)
        user_data = resp['data']['user']
        full_name = user_data['full_name']
        bio = user_data['biography']

        yield {
            "id": user_data['id'],
            "username": user_data['username'],
            "full_name": full_name,
            "recent_post": user_data['edge_owner_to_timeline_media']['edges'][0]['node']['edge_media_to_caption']['edges'][0]['node'],
            "profile_picture": user_data['profile_pic_url_hd'],
            "bio": replace_escape_chars(bio, replace_by=" "),
        }

