import requests
import time
import random
import re
from utils import is_not_none_or_empty


def get_network_technology(info):
    try:
        if is_not_none_or_empty(info["network_5g"]):
            return "5G"
        elif is_not_none_or_empty(info["network_4g"]):
            return "4G"
        elif is_not_none_or_empty(info["network_3g"]):
            return "3G"
        elif is_not_none_or_empty(info["network_2g"]):
            return "2G"
        else:
            return None
    except Exception as e:
        print(f"Error in get_network_technology {info['url']} - {e}")
        return None


def get_body_dimensions(info):
    try:
        body_dimensions = info["body_dimensions"]
        if not is_not_none_or_empty(body_dimensions):
            return (None, None, None)

        pattern = re.compile(
            r"(\d+(?:\.\d+)?)\s?[xX]\s?(\d+(?:\.\d+)?)\s?[xX]\s?(\d+(?:\.\d+)?)\s?mm"
        )
        match = re.search(pattern, body_dimensions)
        if match:
            length = match.group(1)
            width = match.group(2)
            height = match.group(3)
            return length, width, height
        else:
            return (None, None, None)

    except Exception as e:
        print(f"Error in get_body_dimensions {info['url']} - {e}")
        return (None, None, None)


def get_display_dimensions(info):
    try:
        display_resolution = info["display_resolution"]
        if not is_not_none_or_empty(display_resolution):
            return (None, None, None)

        pattern = r"(\d+.*x.*\d+).*pixels.*(~\d+ ppi).*"
        match = re.search(pattern, display_resolution)
        if match:
            width, height = match.group(1).strip().lower().split("x")
            ppi = match.group(2).lower().replace("ppi", "").replace("~", "").strip()
            return width, height, ppi
        else:
            return (None, None, None)

    except Exception as e:
        print(f"Error in get_display_dimensions {info['url']} - {e}")
        return (None, None, None)


def get_display_details(info):
    try:
        display_size = info["display_size"]
        if not is_not_none_or_empty(display_size):
            return (None, None)

        pattern = re.compile(
            r"([\d.]+) inches, ([\d.]+) cm2 \(~([\d.]+)% screen-to-body ratio\)"
        )
        match = re.search(pattern, display_size)
        if match:
            screen_size = match.group(1)
            screen_body_ratio = match.group(3)
            return screen_size, screen_body_ratio
        else:
            return (None, None)

    except Exception as e:
        print(f"Error in get_display_details {info['url']} - {e}")
        return (None, None)


def get_battery(info):
    try:
        batery_type = info["batery_type"]
        if not is_not_none_or_empty(batery_type):
            return (None, None)

        pattern_type = re.compile(r"Li-Ion|Li-Po")
        pattern_capacity = re.compile(r"(\d+)\s*mAh")
        type_match = pattern_type.search(batery_type)
        capacity_match = pattern_capacity.search(batery_type)
        if type_match or capacity_match:
            battery_type = (
                type_match.group() if type_match and type_match.group() else None
            )
            capacity = (
                capacity_match.group(1)
                if capacity_match and capacity_match.group(1)
                else None
            )
            return battery_type, capacity
        else:
            return None, None

    except Exception as e:
        print(f"Error in get_battery {info['url']} - {e}")
        return (None, None)


def get_sim(info):
    try:
        body_sim = info["body_sim"]
        if not is_not_none_or_empty(body_sim):
            return (None, None)
        body_sim = str(body_sim).lower()
        sim_type = None
        sim_count = None

        if body_sim.find("quad") != -1:
            sim_count = 4
        elif body_sim.find("triple") != -1:
            sim_count = 3
        elif body_sim.find("dual") != -1:
            sim_count = 2
        elif body_sim.find("no") != -1:
            sim_count = 0
        else:
            sim_count = 1

        pattern = re.search(r"\b(nano|mini|micro)-sim\b", body_sim, flags=re.IGNORECASE)
        if pattern:
            sim_type = pattern.group(1)
        return sim_type, sim_count

    except Exception as e:
        print(f"Error in get_sim {info['url']} - {e}")
        return (None, None)


def get_os(info):
    try:
        platform_os = info["platform_os"]
        if not is_not_none_or_empty(platform_os):
            return (None, None)

        os_pattern = re.compile(r"([a-zA-Z\s]+)\s*([\d.]+).*")
        match = os_pattern.search(platform_os)
        if match:
            os_name, os_version = match.groups()
            return os_name.strip(), os_version.strip()
        else:
            return None, None

    except Exception as e:
        print(f"Error in get_os {info['url']} - {e}")
        return (None, None)


def get_sensory(info):
    try:
        features_sensors = info["features_sensors"]
        if not is_not_none_or_empty(features_sensors):
            return (None, None)

        features_sensors = re.sub(r"\([^)]*\)", "", features_sensors)
        features_sensors = features_sensors.lower()
        features_sensors = features_sensors.split(",")

        return len(features_sensors), "/".join(features_sensors)

    except Exception as e:
        print(f"Error in get_sensory {info['url']} - {e}")
        return (None, None)


def convert_price(base_amount, base_symbol, year):
    # https://www.macrotrends.net/2548/euro-dollar-exchange-rate-historical-chart
    u_s_dollars_convert_rate = {
        2024: 1.065,
        2023: 1.08,
        2023: 1.08,
        2022: 1.05,
        2021: 1.18,
        2020: 1.14,
        2019: 1.12,
        2018: 1.18,
        2017: 1.13,
        2016: 1.11,
        2015: 1.11,
        2014: 1.33,
        2013: 1.33,
        2012: 1.29,
        2011: 1.39,
        2010: 1.33,
        2009: 1.39,
        2008: 1.47,
        2007: 1.37,
        2006: 1.26,
        2005: 1.24,
        2004: 1.24,
        2003: 1.13,
        2002: 0.95,
        2001: 0.9,
        2000: 0.92,
    }
    # https://www.macrotrends.net/2553/euro-british-pound-exchange-rate-historical-chart
    british_pounds_convert_rate = {
        2024: 0.86,
        2023: 0.87,
        2022: 0.85,
        2021: 0.86,
        2020: 0.89,
        2019: 0.88,
        2018: 0.88,
        2017: 0.88,
        2016: 0.82,
        2015: 0.73,
        2014: 0.81,
        2013: 0.85,
        2012: 0.81,
        2011: 0.87,
        2010: 0.86,
        2009: 0.89,
        2008: 0.8,
        2007: 0.68,
        2006: 0.68,
        2005: 0.68,
        2004: 0.68,
        2003: 0.69,
        2002: 0.63,
        2001: 0.62,
        2000: 0.61,
    }
    # https://www.kaggle.com/datasets/lsind18/euro-exchange-daily-rates-19992020?resource=download
    indian_rupees_convert_rate = {
        2024: 85.96,
        2023: 89.23,
        2022: 82.69,
        2021: 87.44,
        2020: 84.64,
        2019: 78.84,
        2018: 80.73,
        2017: 73.53,
        2016: 74.37,
        2015: 71.2,
        2014: 81.04,
        2013: 77.93,
        2012: 68.6,
        2011: 64.89,
        2010: 60.59,
        2009: 67.36,
        2008: 63.61,
        2007: 56.42,
        2006: 56.84,
        2005: 54.81,
        2004: 56.3,
        2003: 52.61,
        2002: 45.92,
        2001: 42.25,
        2000: 41.36,
    }
    if (
        not str(base_symbol).lower().find("€") == -1
        or not str(base_symbol).lower().find("eur") == -1
    ):
        return base_amount
    elif (
        not str(base_symbol).lower().find("$") == -1
        or not str(base_symbol).lower().find("dollar") == -1
    ):
        return float(base_amount) / u_s_dollars_convert_rate.get(year, 0)
    elif not str(base_symbol).lower().find("£") == -1:
        return float(base_amount) / british_pounds_convert_rate.get(year, 0)
    elif not str(base_symbol).lower().find("₹") == -1:
        return float(base_amount) / indian_rupees_convert_rate.get(year, 0)
    else:
        return 0


def get_price(info):
    try:
        misc_price = info["misc_price"]
        if not is_not_none_or_empty(misc_price):
            return None

        misc_price = str(misc_price).lower()
        base_amount = None
        base_symbol = None
        if misc_price.find("eur") != -1:
            base_symbol = "eur"
            base_amount = re.findall(r"\b\d+\b", misc_price)[0]
        if not base_amount:
            euro_match = re.search(r"€\s*(\d+(\.\d{1,2})?)", misc_price)
            if euro_match:
                base_symbol = "€"
                base_amount = float(euro_match.group(1))
            else:
                match = re.search(r"(\D+)\s*([\d,]+)", misc_price)
                if match:
                    base_symbol = match.group(1).strip()
                    base_amount = match.group(2).replace(",", "")

        return convert_price(
            base_amount=base_amount, base_symbol=base_symbol, year=get_year(info=info)
        )

    except Exception as e:
        print(f"Error in get_price {info['url']} - {e}")
        return None


def get_year(info):
    try:
        launch_announced = info["launch_announced"]
        if not is_not_none_or_empty(launch_announced):
            return None

        match = re.search(r"(\d{4})", launch_announced)
        if match:
            year = int(match.group(1))
            return year
        else:
            return None

    except Exception as e:
        print(f"Error in get_year {info['url']} - {e}")
        return None


def get_cpu(info):
    try:
        platform_cpu = info["platform_cpu"]
        if not is_not_none_or_empty(platform_cpu):
            return None

        match = re.search(r"(\S*?-core)", platform_cpu, re.IGNORECASE)
        if match:
            core_info = str(match.group(1))
            core_info = core_info.lower()
            if core_info.find("8") != -1 or core_info.find("octa") != -1:
                return 8
            elif core_info.find("quad") != -1:
                return 4
            elif core_info.find("dual") != -1:
                return 2
            elif core_info.find("triple") != -1:
                return 3
            else:
                return 1
        else:
            return 1

    except Exception as e:
        print(f"Error in get_cpu {info['url']} - {e}")
        return None


def get_memories_prices(info):
    try:
        mem_price_info = info["memories_version"]
        ret_obj = None
        if mem_price_info:
            ret_obj = []
            for item in mem_price_info:
                mem = str(item[0]).strip()
                match = re.match(r"(\d+GB)\s+((\d+GB) RAM).*", mem)
                internal_storage = (
                    match.group(1) if match and len(match.groups()) >= 1 else None
                )
                ram = match.group(3) if match and len(match.groups()) >= 3 else None
                price = str(item[1]).strip().replace(",", "")
                match = re.search(r"(\D+)\s*([\d,]+)", price)
                if match:
                    base_symbol = (
                        match.group(1).strip() if len(match.groups()) >= 1 else None
                    )
                    base_amount = (
                        match.group(2).replace(",", "")
                        if len(match.groups()) >= 2
                        else None
                    )
                price = convert_price(
                    base_symbol=base_symbol,
                    base_amount=base_amount,
                    year=get_year(info=info),
                )
                ret_obj.append(
                    {"price": price, "ram": ram, "internal_storage": internal_storage}
                )
        elif is_not_none_or_empty(info["memory_internal"]):
            ret_obj = []
            memory_internal = info["memory_internal"]
            match = re.match(r"(\d+GB)\s+((\d+GB) RAM).*", memory_internal)
            internal_storage = (
                match.group(1) if match and len(match.groups()) >= 1 else None
            )
            ram = match.group(3) if match and len(match.groups()) >= 3 else None
            price = get_price(info=info)
            ret_obj.append(
                {"price": price, "ram": ram, "internal_storage": internal_storage}
            )
        return ret_obj

    except Exception as e:
        print(f"Error in get_memories_prices {info['url']} - {e}")
        return None


def get_weight(info):
    try:
        body_weight = info["body_weight"]
        if not is_not_none_or_empty(body_weight):
            return None

        pattern = r"(\d+) g"
        match = re.search(pattern, body_weight)
        if match:
            return float(match.group(1))
        else:
            return None

    except Exception as e:
        print(f"Error in body_weight {info['url']} - {e}")
        return None


def get_popularity(info):
    try:
        fan_count = info["fan"]
        view_count = info["hits"]
        if not is_not_none_or_empty(fan_count):
            fan_count = None
        if not is_not_none_or_empty(view_count):
            view_count = None

        pattern = r"(\d+).*"
        match = re.search(pattern, view_count)
        if match:
            view_count = int(match.group(1))

        match = re.search(pattern, fan_count)
        if match:
            fan_count = int(match.group(1))
        return (fan_count, view_count)

    except Exception as e:
        print(f"Error in get_popularity {info['url']} - {e}")
        return (None, None)


def get_device_type(info):

    try:
        type = "phone"
        name = str(info["name"]).lower()
        screen_size, screen_body_ratio = get_display_details(info=info)
        if name.find("watch") != -1:
            type = "watch"
        elif (
            name.find("tablet") != -1
            or name.find("ipad") != -1
            or name.find("phab") != -1
            or (screen_size and float(screen_size) >= 7)
        ):
            type = "tablet"
        return type

    except Exception as e:
        print(f"Error in get_device_type {info['url']} - {e}")
        return None
