from crawler import Crawler

base_url = "https://www.gsmarena.com"
brand_list = [
    "samsung",
    "apple",
    "huawei",
    "nokia",
    "sony",
    "htc",
    "lg",
    "lenovo",
    "xiaomi",
    "asus",
    "alcatel",
    "blu",
    "infinix",
    "zte",
]
crawler = Crawler(base_url, brand_list)
crawler.run()
