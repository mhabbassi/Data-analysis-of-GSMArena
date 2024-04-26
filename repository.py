from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from model import (
    Base,
    Brand,
    OS,
    Battery,
    DeviceMemoryPrice,
    Device,
    LinkStatus,
    RawContent,
)


class BaseDAL:
    def __init__(self):
        # database_url = "sqlite:///example.db"
        database_url = "mysql+mysqlconnector://root:rahshiri@localhost/gsm"
        self.engine = create_engine(database_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def execute_query(self, query_func):
        session = self.Session()
        try:
            result = query_func(session)
            return result
        except Exception as e:
            raise e


class BrandDAL(BaseDAL):
    def get_or_create_brand(self, name):
        def query_func(session):
            session = self.Session()
            try:
                item = session.query(Brand).filter(Brand.name == name).first()
                if not item:
                    item = Brand(name=name)
                    item = session.add(item)
                    session.commit()
                    item = session.query(Brand).filter(Brand.name == name).first()
                return item
            except Exception as e:
                session.rollback()
                raise e
            finally:
                session.close()

        return self.execute_query(query_func)


class OSDAL(BaseDAL):
    def get_or_create_os(self, type, version):
        def query_func(session):
            session = self.Session()
            try:
                item = (
                    session.query(OS)
                    .filter(OS.type == type, OS.version == version)
                    .first()
                )
                if not item:
                    item = OS(type=type, version=version)
                    item = session.add(item)
                    session.commit()
                    item = (
                        session.query(OS)
                        .filter(OS.type == type, OS.version == version)
                        .first()
                    )
                return item
            except Exception as e:
                session.rollback()
                raise e
            finally:
                session.close()

        return self.execute_query(query_func)


class BatteryDAL(BaseDAL):
    def get_or_create_battery(self, type, capacity):
        def query_func(session):
            session = self.Session()
            try:
                item = (
                    session.query(Battery)
                    .filter(Battery.type == type, Battery.capacity == capacity)
                    .first()
                )
                if not item:
                    item = Battery(type=type, capacity=capacity)
                    item = session.add(item)
                    session.commit()
                    item = (
                        session.query(Battery)
                        .filter(Battery.type == type, Battery.capacity == capacity)
                        .first()
                    )
                return item
            except Exception as e:
                session.rollback()
                raise e
            finally:
                session.close()

        return self.execute_query(query_func)


class DeviceMemoryPriceDAL(BaseDAL):
    def create_device_memory_price(self, item):
        def query_func(session):
            session = self.Session()
            try:
                device_memory_price = session.add(item)
                session.commit()
                return device_memory_price
            except Exception as e:
                session.rollback()
                raise e
            finally:
                session.close()

        return self.execute_query(query_func)


class DeviceDAL(BaseDAL):
    def create_device(self, item_obj):
        def query_func(session):
            session = self.Session()
            try:
                url = item_obj.url
                session.add(item_obj)
                session.commit()
                item = session.query(Device).filter(Device.url == url).first()
                return item
            except Exception as e:
                session.rollback()
                raise e
            finally:
                session.close()

        return self.execute_query(query_func)


class LinkStatusDAL(BaseDAL):
    def create_link(self, brand, type, url, status):
        def query_func(session):
            item = session.query(LinkStatus).filter(LinkStatus.url == url).first()
            if not item:
                item = LinkStatus(brand=brand, type=type, url=url, status=status)
                item = session.add(item)
                session.commit()
            return item

        return self.execute_query(query_func)

    def update_link_status(self, url, status):
        def query_func(session):
            item = session.query(LinkStatus).filter(LinkStatus.url == url).first()
            item.status = status
            session.commit()
            return item

        return self.execute_query(query_func)

    def find_all_link(self, status, type):
        def query_func(session):
            items = (
                session.query(LinkStatus)
                .filter(LinkStatus.status.in_(status), LinkStatus.type == type)
                .all()
            )
            return items

        return self.execute_query(query_func)


class RawContentDAL(BaseDAL):
    def create_raw_content(self, brand, url, type, content, status):
        def query_func(session):
            item = session.query(RawContent).filter(RawContent.url == url).first()
            if not item:
                item = RawContent(
                    brand=brand, url=url, type=type, content=content, status=status
                )
                item = session.add(item)
                session.commit()
            return item

        return self.execute_query(query_func)

    def update_raw_content(self, url, status):
        def query_func(session):
            item = session.query(RawContent).filter(RawContent.url == url).first()
            item.status = status
            session.commit()
            return item

        return self.execute_query(query_func)

    def find_all_content(self, status, type):
        def query_func(session):
            items = (
                session.query(RawContent)
                .filter(RawContent.status.in_(status), RawContent.type == type)
                .all()
            )
            return items

        return self.execute_query(query_func)
