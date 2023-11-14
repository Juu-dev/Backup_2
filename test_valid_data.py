import unittest

# Import the valid_data function here
# def valid_data(data, platform):
#     if(platform == "youtube"):
#         return data.get("items",None)
#     if (platform == "tiktok"):
#         return data.get("error", None) == None
#     return True

def valid_data(data, platform):
    if platform == "youtube":
        return "items" in data
    if platform == "tiktok":
        return "error" not in data
    return True


class TestValidDataFunction(unittest.TestCase):

    def test_valid_data_youtube(self):
        # Test the function with YouTube data
        data = {"items": ["item1", "item2"]}
        self.assertTrue(valid_data(data, "youtube"))

    def test_valid_data_tiktok(self):
        # Test the function with TikTok data
        data = {"error": None}
        self.assertTrue(valid_data(data, "tiktok"))

    def test_valid_data_other_platform(self):
        # Test the function with data from another platform
        data = {"key": "value"}
        self.assertTrue(valid_data(data, "instagram"))

    def test_invalid_data_youtube(self):
        # Test the function with invalid YouTube data
        data = {"other_key": "value"}
        self.assertFalse(valid_data(data, "youtube"))

    def test_invalid_data_tiktok(self):
        # Test the function with invalid TikTok data
        data = {"error": "Some error message"}
        self.assertFalse(valid_data(data, "tiktok"))

if __name__ == '__main__':
    unittest.main()
