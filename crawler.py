import concurrent.futures
from utils import get_url_data
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from repository import (
    LinkStatusDAL,
    RawContentDAL,
    DeviceDAL,
    BrandDAL,
    OSDAL,
    BatteryDAL,
    DeviceMemoryPriceDAL,
)
from model import Device, DeviceMemoryPrice
import re
import logging
from crawlerUtils import *

logger = logging.getLogger("gsmarena-scraper")


class Crawler:
    def __init__(self, base_url, brand_list):
        self.base_url = base_url
        self.brand_list = [item.upper() for item in brand_list]
        self.brand_info = {}
        self.linkStatusDAL = LinkStatusDAL()
        self.rawContentDAL = RawContentDAL()
        self.deviceDAL = DeviceDAL()
        self.brandDal = BrandDAL()
        self.osDAL = OSDAL()
        self.batteryDAL = BatteryDAL()
        self.deviceMemoryPriceDAL = DeviceMemoryPriceDAL()

    def run(self):
        self.fetch_brands_info(brand_url="makers.php3")
        print("fetch brands list")

        self.fetch_brands_pages_url()
        print("fetch brands pages url")

        self.save_brands_pages_content()
        print("save brands pages contents")

        self.save_devices_pages_url()
        print("fetch brands pages url")


        self.fetch_device_content()
        print("save devices pages contents")

        self.process_device_data()
        print("fetch brands devices data")

    def fetch_brands_info(self, brand_url):
        content = get_url_data(urljoin(self.base_url, brand_url))
        if not content:
            return None
        soup = BeautifulSoup(content, "html.parser")
        brands = (
            soup.find("div", attrs={"class": "st-text"}).find("table").find_all("a")
        )
        for item in brands:
            if item and item.text and item.get("href"):
                key = item.text.upper()
                key = re.sub(r"\d| DEVICES", "", key)
                key = key.strip()
                if key in self.brand_list:
                    self.brand_info[key] = {
                        "url": urljoin(self.base_url, item.get("href")),
                        "device_urls": [],
                    }
        return self.brand_info

    def fetch_brands_pages_url(self):
        for key, brand in self.brand_info.items():
            start_page = 1
            last_page = 1
            link_schema = ""
            content = get_url_data(brand["url"])
            soup = BeautifulSoup(content, "html.parser")
            page_section = soup.find(class_="nav-pages")
            if page_section:
                last_page_info = page_section.select("a")[-2]
                last_page = int(last_page_info.text)
                link_schema = last_page_info.get("href")

            brand_device_urls = [urljoin(self.base_url, brand["url"])]
            for page_num in range(start_page, last_page + 1):
                if start_page == last_page:
                    break
                url = urljoin(
                    self.base_url,
                    link_schema.replace(f"p{last_page}", f"p{page_num}"),
                )
                brand_device_urls.append(url)
                self.linkStatusDAL.create_link(
                    brand=key, url=url, status=0, type="BRAND_PAGE"
                )

            brand["device_urls"] = brand_device_urls

    def fetch_device_content(self):
        links = self.linkStatusDAL.find_all_link(status=[0, -1], type="DEVICE_PAGE")
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            device_future_list = {
                executor.submit(get_url_data, item.url): item for item in links
            }
            for future in concurrent.futures.as_completed(device_future_list):
                item = device_future_list[future]
                try:
                    data = future.result()
                    if not data:
                        print(f"Failed to fetch {item.url}")
                    else:
                        print(f"Fetched data {item.url}")
                        self.rawContentDAL.create_raw_content(
                            brand=item.brand,
                            url=item.url,
                            type="DEVICE_PAGE",
                            status=0,
                            content=data.encode("utf-8"),
                        )
                        self.linkStatusDAL.update_link_status(url=item.url, status=1)
                except Exception as e:
                    print(f"Failed to fetch {item}: {e}")

    def save_devices_pages_url(self):
        brand_page_contents_list = self.rawContentDAL.find_all_content(
            status=[0, -1], type="BRAND_PAGE"
        )
        for item in brand_page_contents_list:
            soup = BeautifulSoup(item.content, "html.parser")
            devices_link_info = soup.find("div", attrs={"class": "makers"}).find_all(
                "a"
            )
            for obj in devices_link_info:
                url = urljoin(self.base_url, obj.get("href"))
                brand = item.brand
                type = "DEVICE_PAGE"
                self.linkStatusDAL.create_link(
                    brand=brand, type=type, url=url, status=0
                )
                self.rawContentDAL.update_raw_content(item.url, status=1)

    def save_brands_pages_content(self):
        links = self.linkStatusDAL.find_all_link(status=[0, -1], type="BRAND_PAGE")
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            device_future_list = {
                executor.submit(get_url_data, item.url): item for item in links
            }
            for future in concurrent.futures.as_completed(device_future_list):
                item = device_future_list[future]
                try:
                    data = future.result()
                    if not data:
                        print(f"Failed to fetch {item.url}")
                    else:
                        print(f"Fetched data {item.url}")
                        self.rawContentDAL.create_raw_content(
                            brand=item.brand,
                            url=item.url,
                            type="BRAND_PAGE",
                            status=0,
                            content=data.encode("utf-8"),
                        )
                        self.linkStatusDAL.update_link_status(url=item.url, status=1)
                except Exception as e:
                    print(f"Failed to fetch {item}: {e}")

    def process_device_data(self):
        devices_list = self.rawContentDAL.find_all_content(
            status=[0, -1], type="DEVICE_PAGE"
        )
        # devices_list = devices_list[0:100]
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=3, thread_name_prefix="GSMARENA"
        ) as executor:
            device_future_list = {
                executor.submit(self.fetch_device_data, item): item
                for item in devices_list
            }
            for future in concurrent.futures.as_completed(device_future_list):
                item = device_future_list[future]
                try:
                    data = future.result()
                    if not data:
                        print(f"Failed to process device {item.url}")
                    else:
                        print(f"{data['name']}")
                        self.clean_save_device_data(info=data)
                except Exception as e:
                    print(f"Failed to fetch {item}: {e}")

    def fetch_device_data(self, device):
        # if str(device.content).find("Infinix Smart 7 (India)") == -1:
        #     return None

        device_soup = BeautifulSoup(device.content, "html.parser")
        result = {}
        # ===========================================================================
        result["brand"] = device.brand
        result["url"] = device.url
        result["name"] = device_soup.find("h1").text
        # ===========================================================================
        a1 = device_soup.find_all(attrs={"data-spec": "nettech"})
        result["network_technology"] = None
        if len(a1) == 1:
            result["network_technology"] = a1[0].text
        a2 = device_soup.find_all(attrs={"data-spec": "net2g"})
        result["network_2g"] = None
        if len(a2) == 1:
            result["network_2g"] = a2[0].text
        a3 = device_soup.find_all(attrs={"data-spec": "net3g"})
        result["network_3g"] = None
        if len(a3) == 1:
            result["network_3g"] = a3[0].text
        a4 = device_soup.find_all(attrs={"data-spec": "net4g"})
        result["network_4g"] = None
        if len(a4) == 1:
            result["network_4g"] = a4[0].text
        a5 = device_soup.find_all(attrs={"data-spec": "net5g"})
        result["network_5g"] = None
        if len(a5) == 1:
            result["network_5g"] = a5[0].text
        # ===========================================================================
        result["launch_announced"] = None
        a2 = device_soup.find_all(attrs={"data-spec": "year"})
        if len(a2) == 1:
            result["launch_announced"] = a2[0].text
        result["launch_status"] = None
        a6 = device_soup.find_all(attrs={"data-spec": "status"})
        if len(a6) == 1:
            result["launch_status"] = a6[0].text
        # ===========================================================================
        result["body_dimensions"] = None
        a7 = device_soup.find_all(attrs={"data-spec": "dimensions"})
        if len(a7) == 1:
            result["body_dimensions"] = a7[0].text
        result["body_weight"] = None
        a5 = device_soup.find_all(attrs={"data-spec": "weight"})
        if len(a5) == 1:
            result["body_weight"] = a5[0].text
        # ===========================================================================
        result["body_sim"] = None
        a6 = device_soup.find_all(attrs={"data-spec": "sim"})
        if len(a6) == 1:
            result["body_sim"] = a6[0].text
        # ===========================================================================
        result["display_type"] = None
        a7 = device_soup.find_all(attrs={"data-spec": "displaytype"})
        if len(a7) == 1:
            result["display_type"] = a7[0].text
        result["display_size"] = None
        a8 = device_soup.find_all(attrs={"data-spec": "displaysize"})
        if len(a8) == 1:
            result["display_size"] = a8[0].text
        result["display_resolution"] = None
        a9 = device_soup.find_all(attrs={"data-spec": "displayresolution"})
        if len(a9) == 1:
            result["display_resolution"] = a9[0].text
        result["display_resolution"] = None
        a10 = device_soup.find_all(attrs={"data-spec": "displayresolution"})
        if len(a10) == 1:
            result["display_resolution"] = a10[0].text
        # ===========================================================================
        result["platform_os"] = None
        a11 = device_soup.find_all(attrs={"data-spec": "os"})
        if len(a11) == 1:
            result["platform_os"] = a11[0].text
        # ===========================================================================
        result["platform_chipset"] = None
        a12 = device_soup.find_all(attrs={"data-spec": "chipset"})
        if len(a12) == 1:
            result["platform_chipset"] = a12[0].text
        result["platform_cpu"] = None
        a13 = device_soup.find_all(attrs={"data-spec": "cpu"})
        if len(a13) == 1:
            result["platform_cpu"] = a13[0].text
        result["platform_gpu"] = None
        a14 = device_soup.find_all(attrs={"data-spec": "gpu"})
        if len(a14) == 1:
            result["platform_gpu"] = a14[0].text
        # ===========================================================================
        result["memory_slot"] = None
        a15 = device_soup.find_all(attrs={"data-spec": "memoryslot"})
        if len(a15) == 1:
            result["memory_slot"] = a15[0].text
        result["memory_internal"] = None
        a16 = device_soup.find_all(attrs={"data-spec": "internalmemory"})
        if len(a16) == 1:
            result["memory_internal"] = a16[0].text
        result["memory_other"] = None
        a17 = device_soup.find_all(attrs={"data-spec": "memoryother"})
        if len(a17) == 1:
            result["memory_other"] = a17[0].text

        result["memories_version"] = None
        memories_version = device_soup.find(
            "table", attrs={"class": "pricing inline widget"}
        )
        if memories_version:
            result["memories_version"] = []
            memories_version = memories_version.find_all("tr")
            for item in memories_version:
                mem_inf = item.find_all("td")
                result["memories_version"].append((mem_inf[0].text, mem_inf[1].text))
        # ===========================================================================
        # result["cam1_num"] = None
        # a17 = device_soup.find_all(attrs={"href": "glossary.php3?term=camera"})
        # if len(a17) != 0:
        #     result["cam1_num"] = a17[0].text
        # result["cam1_modules"] = None
        # a18 = device_soup.find_all(attrs={"data-spec": "cam1modules"})
        # if len(a18) == 1:
        #     result["cam1_modules"] = a18[0].text
        # result["cam1_features"] = None
        # a19 = device_soup.find_all(attrs={"data-spec": "cam1features"})
        # if len(a19) == 1:
        #     result["cam1_features"] = a19[0].text
        # result["cam1_video"] = None
        # a20 = device_soup.find_all(attrs={"data-spec": "cam1video"})
        # if len(a20) == 1:
        #     result["cam1_video"] = a20[0].text
        # result["cam2_num"] = None
        # a20 = device_soup.find_all(
        #     attrs={"href": "glossary.php3?term=secondary-camera"}
        # )
        # if len(a20) != 0:
        #     result["cam2_num"] = a20[0].text
        # result["cam2_modules"] = None
        # a21 = device_soup.find_all(attrs={"data-spec": "cam2modules"})
        # if len(a21) == 1:
        #     result["cam2_modules"] = a21[0].text
        # result["cam2_features"] = None
        # a22 = device_soup.find_all(attrs={"data-spec": "cam2features"})
        # if len(a22) == 1:
        #     result["cam2_features"] = a22[0].text
        # result["cam2_video"] = None
        # a23 = device_soup.find_all(attrs={"data-spec": "cam2video"})
        # if len(a23) == 1:
        #     result["cam2_video"] = a23[0].text
        # ===========================================================================
        # result["sound_loudspeaker"] = None
        # a = device_soup.find_all(attrs={"href": "glossary.php3?term=loudspeaker"})
        # if len(a) == 1:
        #     result["sound_loudspeaker"] = a[0].find_next().text
        # result["sound_audio-jack"] = None
        # a = device_soup.find_all(attrs={"href": "glossary.php3?term=audio-jack"})
        # if len(a) == 1:
        #     result["sound_audio-jack"] = a[0].find_next().text
        # result["comm_wlan"] = None
        # a24 = device_soup.find_all(attrs={"data-spec": "wlan"})
        # if len(a24) == 1:
        #     result["comm_wlan"] = a24[0].text
        # result["comm_bluetooth"] = None
        # a25 = device_soup.find_all(attrs={"data-spec": "bluetooth"})
        # if len(a25) == 1:
        #     result["comm_bluetooth"] = a25[0].text
        # result["comm_positioning"] = None
        # a26 = device_soup.find_all(attrs={"data-spec": "gps"})
        # if len(a26) == 1:
        #     result["comm_positioning"] = a26[0].text
        # result["comm_nfc"] = None
        # a27 = device_soup.find_all(attrs={"data-spec": "nfc"})
        # if len(a27) == 1:
        #     result["comm_nfc"] = a27[0].text
        # result["comm_radio"] = None
        # a29 = device_soup.find_all(attrs={"data-spec": "radio"})
        # if len(a29) == 1:
        #     result["comm_radio"] = a29[0].text
        # result["comm_usb"] = None
        # a30 = device_soup.find_all(attrs={"data-spec": "usb"})
        # if len(a30) == 1:
        #     result["comm_usb"] = a30[0].text
        # result["features_other"] = None
        # a31 = device_soup.find_all(attrs={"data-spec": "featuresother"})
        # if len(a31) == 1:
        #     result["features_other"] = a31[0].text
        # ===========================================================================
        result["features_sensors"] = None
        a31 = device_soup.find_all(attrs={"data-spec": "sensors"})
        if len(a31) == 1:
            result["features_sensors"] = a31[0].text
        # ===========================================================================
        result["batery_type"] = None
        a32 = device_soup.find_all(attrs={"data-spec": "batdescription1"})
        if len(a32) == 1:
            result["batery_type"] = a32[0].text
        result["battery_charging"] = None
        a = device_soup.find_all(attrs={"href": "glossary.php3?term=battery-charging"})
        if len(a) == 1:
            result["battery_charging"] = a[0].find_next().text
        # ===========================================================================
        result["misc_colors"] = None
        a33 = device_soup.find_all(attrs={"data-spec": "colors"})
        if len(a33) == 1:
            result["misc_colors"] = a33[0].text
        result["misc_models"] = None
        a34 = device_soup.find_all(attrs={"data-spec": "models"})
        if len(a34) == 1:
            result["misc_models"] = a34[0].text
        result["misc_price"] = None
        a35 = device_soup.find_all(attrs={"data-spec": "price"})
        if len(a35) == 1:
            result["misc_price"] = a35[0].text
        # ===========================================================================
        result["fan"] = device_soup.find(class_="specs-fans").find("strong").text
        result["popularity"] = (
            device_soup.find(class_="light pattern help help-popularity")
            .find("strong")
            .text
        )
        result["hits"] = (
            device_soup.find(class_="light pattern help help-popularity")
            .find("span")
            .text
        )
        # ===========================================================================
        return result

    def clean_save_device_data(self, info):
        device_obj = Device()
        device_obj.url = info["url"]
        device_obj.name = info["name"]
        device_obj.network_types = str(info["network_technology"]).strip()
        device_obj.network_technology = get_network_technology(info=info)

        length, width, height = get_body_dimensions(info=info)
        device_obj.length = length
        device_obj.width = width
        device_obj.height = height

        device_obj.weight = get_weight(info=info)

        resolution_l, resolution_w, ppi = get_display_dimensions(info=info)
        device_obj.resolution_l = resolution_l
        device_obj.resolution_w = resolution_w
        device_obj.ppi = ppi

        screen_size, screen_body_ratio = get_display_details(info=info)
        device_obj.screen_body_ratio = screen_body_ratio
        device_obj.screen_size = screen_size

        sim_type, sim_count = get_sim(info=info)
        device_obj.sim_type = sim_type
        device_obj.sim_count = sim_count

        sensors_count, sensors_types = get_sensory(info=info)
        device_obj.sensors_count = sensors_count
        device_obj.sensors_types = sensors_types

        year = get_year(info=info)
        device_obj.released_date = year

        cpu_core = get_cpu(info=info)
        device_obj.cpu_core = cpu_core

        (fan_count, view_count) = get_popularity(info=info)
        device_obj.fan_count = fan_count
        device_obj.view_count = view_count

        device_obj.type = get_device_type(info=info)
        ##############################################################################
        brand = self.brandDal.get_or_create_brand(name=info["brand"])
        device_obj.brand_id = brand.id

        battery_type, battery_capacity = get_battery(info=info)
        battery = self.batteryDAL.get_or_create_battery(
            type=battery_type, capacity=battery_capacity
        )
        device_obj.battery_id = battery.id

        os_type, os_version = get_os(info=info)
        os = self.osDAL.get_or_create_os(type=os_type, version=os_version)
        device_obj.os_id = os.id

        device_obj = self.deviceDAL.create_device(item_obj=device_obj)

        memories_prices = get_memories_prices(info=info)
        if memories_prices and len(memories_prices) > 0:
            for obj in memories_prices:
                internal_storage = obj["internal_storage"]
                ram = obj["ram"]
                price = obj["price"]
                self.deviceMemoryPriceDAL.create_device_memory_price(
                    DeviceMemoryPrice(
                        device_id=device_obj.id,
                        ram=ram,
                        internal_storage=internal_storage,
                        price=price,
                    )
                )

        return device_obj
