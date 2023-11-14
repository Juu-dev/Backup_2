import unittest

# Import hàm data_parse từ module của bạn ở đây
def data_parse(data, platform, url):
    result = {
        'url': url,
        'platform': platform,
        'thumb_url': '',
        'title': '',
        'created_at': '',
        'statistics': {
            'comment_count': '',
            'view_count': '',
            'share_count': '',
            'save_count': '',
            'like_count': '',
        },
    }

    if platform == 'tiktok' and data:
        aweme_detail = data.get('aweme_detail', None)
        if aweme_detail:
            result['thumb_url'] = aweme_detail['video']['ai_dynamic_cover']['url_list'][0] if 'video' in aweme_detail else ''
            result['file_url'] = aweme_detail.get('video', {}).get('play_addr', {}).get('url_list', [])[0] if 'video' in aweme_detail else ''
            result['title'] = aweme_detail['desc']
            result['created_at'] = aweme_detail['create_time']
            result['statistics']['comment_count'] = aweme_detail['statistics']['comment_count'] if 'statistics' in aweme_detail else ''
            result['statistics']['view_count'] = aweme_detail['statistics']['play_count'] if 'statistics' in aweme_detail else ''
            result['statistics']['share_count'] = aweme_detail['statistics']['share_count'] if 'statistics' in aweme_detail else ''
            result['statistics']['save_count'] = aweme_detail['statistics']['collect_count'] if 'statistics' in aweme_detail else ''
            result['statistics']['like_count'] = aweme_detail['statistics']['digg_count'] if 'statistics' in aweme_detail else ''
            result['failed'] = not bool(aweme_detail['video'])

    elif platform == 'youtube' and 'items' in data and len(data['items']) > 0:
        item = data['items'][0]
        result['thumb_url'] = item['snippet']['thumbnails']['default']['url']
        result['title'] = item['snippet']['title']
        result['created_at'] = item['snippet']['publishedAt']
        result['statistics']['comment_count'] = item['statistics'].get('commentCount', '')
        result['statistics']['view_count'] = item['statistics'].get('viewCount', '')
        result['statistics']['like_count'] = item['statistics'].get('likeCount', '')

    elif platform == 'instagram' and data:
        post_image = ''
        if 'image_versions2' in data:
            post_image = data['image_versions2']['candidates'][-1]['url'] if 'candidates' in data['image_versions2'] else ''
        elif 'carousel_media' in data and data['carousel_media'][0].get('image_versions2'):
            post_image = data['carousel_media'][0]['image_versions2']['candidates'][-1]['url'] if 'candidates' in data['carousel_media'][0]['image_versions2'] else ''

        result['thumb_url'] = post_image
        result['title'] = data['caption'].get('text', '')
        result['created_at'] = data['caption'].get('created_at', '')
        result['statistics']['comment_count'] = data.get('comment_count', '')
        result['statistics']['view_count'] = data.get('play_count', '0')
        result['statistics']['share_count'] = data.get('reshare_count', '')
        result['statistics']['like_count'] = data.get('like_count', '')

    return result


class TestDataParse(unittest.TestCase):

    def test_tiktok_data_parse(self):
        tiktok_data = {
            'aweme_detail': {
                'video': {
                    'ai_dynamic_cover': {
                        'url_list': ['thumbnail_url']
                    },
                    'play_addr': {
                        'url_list': ['video_url']
                    }
                },
                'desc': 'Video description',
                'create_time': '2023-10-21',
                'statistics': {
                    'comment_count': 100,
                    'play_count': 1000,
                    'share_count': 50,
                    'collect_count': 30,
                    'digg_count': 200
                }
            }
        }

        result = data_parse(tiktok_data, 'tiktok', 'https://tiktok.com')
        self.assertEqual(result['platform'], 'tiktok')
        self.assertEqual(result['thumb_url'], 'thumbnail_url')
        self.assertEqual(result['file_url'], 'video_url')
        self.assertEqual(result['title'], 'Video description')
        self.assertEqual(result['created_at'], '2023-10-21')
        self.assertEqual(result['statistics']['comment_count'], 100)
        self.assertEqual(result['statistics']['view_count'], 1000)
        self.assertEqual(result['statistics']['share_count'], 50)
        self.assertEqual(result['statistics']['save_count'], 30)
        self.assertEqual(result['statistics']['like_count'], 200)
        self.assertFalse(result['failed'])

    def test_youtube_data_parse(self):
        youtube_data = {
            'items': [
                {
                    'snippet': {
                        'thumbnails': {
                            'default': {
                                'url': 'thumbnail_url'
                            },
                        },
                        'title': 'YouTube Video Title',
                        'publishedAt': '2023-10-21'
                    },
                    'statistics': {
                        'commentCount': 200,
                        'viewCount': 3000,
                        'likeCount': 500
                    }
                }
            ]
        }

        result = data_parse(youtube_data, 'youtube', 'https://youtube.com')
        self.assertEqual(result['platform'], 'youtube')
        self.assertEqual(result['thumb_url'], 'thumbnail_url')
        self.assertEqual(result['title'], 'YouTube Video Title')
        self.assertEqual(result['created_at'], '2023-10-21')
        self.assertEqual(result['statistics']['comment_count'], 200)
        self.assertEqual(result['statistics']['view_count'], 3000)
        self.assertEqual(result['statistics']['like_count'], 500)

    def test_instagram_data_parse(self):
        instagram_data = {
            'image_versions2': {
                'candidates': [
                    {'url': 'image_url'}
                ]
            },
            'caption': {
                'text': 'Instagram Caption',
                'created_at': '2023-10-21'
            },
            'comment_count': 50,
            'play_count': 1000,
            'reshare_count': 20,
            'like_count': 150
        }

        result = data_parse(instagram_data, 'instagram', 'https://instagram.com')
        self.assertEqual(result['platform'], 'instagram')
        self.assertEqual(result['thumb_url'], 'image_url')
        self.assertEqual(result['title'], 'Instagram Caption')
        self.assertEqual(result['created_at'], '2023-10-21')
        self.assertEqual(result['statistics']['comment_count'], 50)
        self.assertEqual(result['statistics']['view_count'], 1000)
        self.assertEqual(result['statistics']['share_count'], 20)
        self.assertEqual(result['statistics']['like_count'], 150)

if __name__ == '__main__':
    unittest.main()
