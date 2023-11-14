import unittest

# Import hàm extract_data_get_row từ module của bạn ở đây
def extract_data_get_row(item, is_detect_voice):
    common_data = [
        item.get('url', None),
        item.get('title', None),
        item.get('platform', None),
        item.get('statistics', {}).get('view_count', 0),
        item.get('statistics', {}).get('like_count', 0),
        item.get('statistics', {}).get('share_count', 0),
        item.get('statistics', {}).get('comment_count', 0),
        item.get('statistics', {}).get('save_count', 0),
        item.get('created_at', None),
    ]

    if is_detect_voice:
        common_data.insert(2, item.get('transcript', None))
        common_data.insert(3, item.get('keywords', None))

    return common_data


class TestExtractDataGetRow(unittest.TestCase):

    def test_with_detect_voice(self):
        item = {
            'url': 'https://example.com',
            'title': 'Sample Title',
            'transcript': 'Sample transcript',
            'keywords': ['keyword1', 'keyword2'],
            'platform': 'YouTube',
            'statistics': {
                'view_count': 1000,
                'like_count': 200,
                'share_count': 50,
                'comment_count': 30,
                'save_count': 10
            },
            'created_at': '2023-10-21'
        }

        result = extract_data_get_row(item, is_detect_voice=True)
        expected_result = [
            'https://example.com',
            'Sample Title',
            'Sample transcript',
            ['keyword1', 'keyword2'],
            'YouTube',
            1000,
            200,
            50,
            30,
            10,
            '2023-10-21'
        ]
        self.assertEqual(result, expected_result)

    def test_without_detect_voice(self):
        item = {
            'url': 'https://example.com',
            'title': 'Sample Title',
            'platform': 'YouTube',
            'statistics': {
                'view_count': 1000,
                'like_count': 200,
                'share_count': 50,
                'comment_count': 30,
                'save_count': 10
            },
            'created_at': '2023-10-21'
        }

        result = extract_data_get_row(item, is_detect_voice=False)
        expected_result = [
            'https://example.com',
            'Sample Title',
            'YouTube',
            1000,
            200,
            50,
            30,
            10,
            '2023-10-21'
        ]
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()
