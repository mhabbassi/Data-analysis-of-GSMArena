from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Brand(Base):
    __tablename__ = "brand"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(16))


class OS(Base):
    __tablename__ = "os"
    id = Column(Integer, autoincrement=True, primary_key=True)
    type = Column(String(128))
    version = Column(String(16))


class Battery(Base):
    __tablename__ = "battery"
    id = Column(Integer, autoincrement=True, primary_key=True)
    type = Column(String(32))
    capacity = Column(String(16))


class DeviceMemoryPrice(Base):
    __tablename__ = "device_memory_price"
    id = Column(Integer, autoincrement=True, primary_key=True)
    device_id = Column(Integer, ForeignKey(name="fk_dmp_device_id", column="device.id"))
    ram = Column(String(16))
    internal_storage = Column(String(16))
    price = Column(String(128))


class Device(Base):
    __tablename__ = "device"
    id = Column(Integer, autoincrement=True, primary_key=True)

    brand_id = Column(Integer, ForeignKey(name="fk_device_brand_id", column="brand.id"))
    os_id = Column(Integer, ForeignKey(name="fk_device_os_id", column="os.id"))
    battery_id = Column(
        Integer, ForeignKey(name="fk_device_battery_id", column="battery.id")
    )

    name = Column(String(256))
    url = Column(String(512))
    type = Column(String(8))
    network_technology = Column(String(8))
    network_types = Column(String(256))
    sensors_count = Column(String(8))
    sensors_types = Column(String(512))
    length = Column(String(16))
    width = Column(String(16))
    height = Column(String(16))
    weight = Column(String(16))
    resolution_l = Column(String(16))
    resolution_w = Column(String(16))
    screen_body_ratio = Column(String(16))
    screen_size = Column(String(16))
    ppi = Column(String(16))
    sim_type = Column(String(16))
    sim_count = Column(Integer)
    released_date = Column(String(16))
    cpu_core = Column(String(16))
    fan_count = Column(String(16))
    view_count = Column(String(16))

    def __str__(self):
        return f"id:{self.id},brand:{self.brand},name:{self.name},type:{self.type},network_technology:{self.network_technology},length:{self.length},width:{self.width},height:{self.height},weight:{self.weight},resolution_l:{self.resolution_l},resolution_w:{self.resolution_w},screen_body_ratio:{self.screen_body_ratio},screen_size:{self.screen_size},ppi:{self.ppi},battery_type:{self.battery_type},battery_capacity:{self.battery_capacity},sim_type:{self.sim_type},sim_count:{self.sim_count},os_type:{self.os_type},os_version:{self.os_version},price:{self.price},released_date:{self.released_date},cpu_core:{self.cpu_core},ram:{self.ram},internal_storage:{self.internal_storage},fan_count:{self.fan_count},view_count:{self.view_count}"


class LinkStatus(Base):
    __tablename__ = "link_status"
    id = Column(Integer, autoincrement=True, primary_key=True)
    brand = Column(String(128))
    type = Column(String(16))
    url = Column(String(256), index=True, unique=True)
    status = Column(Integer)


class RawContent(Base):
    __tablename__ = "raw_content"
    id = Column(Integer, autoincrement=True, primary_key=True)
    brand = Column(String(128))
    type = Column(String(16))
    url = Column(String(256), index=True, unique=True)
    content = Column(LONGTEXT)
    status = Column(Integer)
