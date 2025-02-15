"""
@Author         : Ailitonia
@Date           : 2022/02/21 11:10
@FileName       : table.py
@Project        : nonebot2_miya 
@Description    : omega database tables metadata
@GitHub         : https://github.com/Ailitonia
@Software       : PyCharm 
"""

from sqlalchemy import Sequence, ForeignKey
from sqlalchemy import Column, Integer, BigInteger, Float, String, Date, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from .config import database_config


# 创建数据表基类
Base = declarative_base()


class SystemSettingOrm(Base):
    """系统参数表, 存放运行时配置"""
    __tablename__ = f'{database_config.db_prefix}system_setting'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4'}

    # 表结构
    id = Column(Integer, Sequence('system_setting_id_seq'), primary_key=True, nullable=False, index=True, unique=True)
    setting_name = Column(String(64), nullable=False, index=True, unique=True, comment='参数名称')
    setting_value = Column(String(128), nullable=False, index=True, comment='参数值')
    info = Column(String(128), nullable=True, comment='参数说明')
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<SystemSettingOrm(setting_name='{self.setting_name}', setting_value='{self.setting_value}', " \
               f"info='{self.info}', created_at='{self.created_at}', updated_at='{self.updated_at}')>"


class PluginOrm(Base):
    """插件表, 存放插件信息"""
    __tablename__ = f'{database_config.db_prefix}plugin'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4'}

    # 表结构
    id = Column(Integer, Sequence('plugin_id_seq'), primary_key=True, nullable=False, index=True, unique=True)
    plugin_name = Column(String(64), nullable=False, index=True, unique=True, comment='插件名称')
    module_name = Column(String(128), nullable=False, index=True, unique=True, comment='插件模块名称')
    enabled = Column(Integer, nullable=False, index=True, comment='启用状态, 1: 启用, 0: 禁用, -1: 失效或未安装')
    info = Column(String(256), nullable=True, comment='附加说明')
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<PluginOrm(plugin_name='{self.plugin_name}', module_name='{self.module_name}', " \
               f"enabled='{self.enabled}', info='{self.info}', " \
               f"created_at='{self.created_at}', updated_at='{self.updated_at}')>"


class StatisticOrm(Base):
    """统计信息表, 存放插件运行统计"""
    __tablename__ = f'{database_config.db_prefix}statistic'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4'}

    # 表结构
    id = Column(BigInteger, Sequence('Statistic_id_seq'), primary_key=True, nullable=False, index=True, unique=True)
    module_name = Column(String(64), nullable=False, index=True, comment='插件模块名称')
    plugin_name = Column(String(64), nullable=False, index=True, comment='插件显示名称')
    bot_self_id = Column(String(64), nullable=False, index=True, comment='对应的Bot')
    call_id = Column(String(64), nullable=False, index=True, comment='调用id, 对应调用用户对象信息')
    call_time = Column(DateTime, nullable=False, index=True, comment='调用时间')
    call_info = Column(String(4096), nullable=True, index=False, comment='调用信息')
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<StatisticOrm(module_name='{self.module_name}', plugin_name='{self.plugin_name}', " \
               f"bot_self_id='{self.bot_self_id}', call_id='{self.call_id}', call_time='{self.call_time}', " \
               f"call_info='{self.call_info}', created_at='{self.created_at}', updated_at='{self.updated_at}')>"


class HistoryOrm(Base):
    """记录表"""
    __tablename__ = f'{database_config.db_prefix}history'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4'}

    # 表结构
    id = Column(BigInteger, Sequence('history_id_seq'), primary_key=True, nullable=False, index=True, unique=True)
    time = Column(BigInteger, nullable=False, comment='事件发生的时间戳')
    self_id = Column(String(64), nullable=False, index=True, comment='收到事件的机器人id')
    event_type = Column(String(64), nullable=False, index=True, comment='事件类型')
    event_id = Column(String(64), nullable=False, index=True, comment='事件id')
    raw_data = Column(String(4096), nullable=False, comment='原始事件内容')
    msg_data = Column(String(4096), nullable=True, comment='经处理的事件内容')
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<HistoryOrm(time='{self.time}', self_id='{self.self_id}', " \
               f"event_type='{self.event_type}', event_id='{self.event_id}', " \
               f"raw_data='{self.raw_data}', msg_data='{self.msg_data}', " \
               f"created_at='{self.created_at}', updated_at='{self.updated_at}')>"


class BotSelfOrm(Base):
    """Bot表 对应不同机器人协议端"""
    __tablename__ = f'{database_config.db_prefix}bots'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4'}

    # 表结构
    id = Column(Integer, Sequence('bots_id_seq'), primary_key=True, nullable=False, index=True, unique=True)
    self_id = Column(String(64), nullable=False, index=True, unique=True, comment='bot身份id, 用于识别bot, qq号等')
    bot_type = Column(String(64), nullable=False, index=True, comment='Bot类型, 具体使用的协议')
    bot_status = Column(Integer, nullable=False, comment='Bot在线状态')
    bot_info = Column(String(512), nullable=True, comment='Bot描述信息')
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)

    # 设置级联和关系加载
    bots_related_entity = relationship('RelatedEntityOrm', back_populates='related_entity_back_bots',
                                       cascade='all, delete-orphan', passive_deletes=True)

    def __repr__(self):
        return f"<BotSelfOrm(self_id={self.self_id!r}', bot_type={self.bot_type!r}, bot_status={self.bot_status!r}, " \
               f"bot_info={self.bot_info!r}, created_at={self.created_at!r}, updated_at={self.updated_at!r})>"


class EntityOrm(Base):
    """实体表, 存放用户/群组/频道等所有需要交互的对象"""
    __tablename__ = f'{database_config.db_prefix}entity'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4'}

    # 表结构
    id = Column(Integer, Sequence('entity_id_seq'), primary_key=True, nullable=False, index=True, unique=True)
    entity_id = Column(String(64), nullable=False, index=True, comment='实体身份id, 不同类型实体可能相同, qq号/群号等')
    entity_type = Column(String(64), nullable=False, index=True, comment='实体类型')
    entity_name = Column(String(64), nullable=False, index=True, comment='实体名称')
    entity_info = Column(String(512), nullable=True, comment='实体描述信息')
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)

    # 设置级联和关系加载
    entity_related_entity = relationship('RelatedEntityOrm', back_populates='related_entity_back_entity',
                                         foreign_keys='RelatedEntityOrm.entity_id',
                                         cascade='all, delete-orphan', passive_deletes=True)
    entity_related_parent_entity = relationship('RelatedEntityOrm', back_populates='related_entity_parent_back_entity',
                                                foreign_keys='RelatedEntityOrm.parent_entity_id',
                                                cascade='all, delete-orphan', passive_deletes=True)

    def __repr__(self):
        return f"<EntityOrm(unique_id={self.entity_id!r}', entity_type={self.entity_type!r}, " \
               f"entity_name={self.entity_name!r}, entity_info={self.entity_info!r} " \
               f"created_at={self.created_at!r}, updated_at={self.updated_at!r})>"


class RelatedEntityOrm(Base):
    """实体关联表, 标注群成员等实体关联信息, 所有属性/好感度/权限/订阅等操作实例对象均以此为基准"""
    __tablename__ = f'{database_config.db_prefix}related_entity'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4'}

    id = Column(Integer, Sequence('related_entity_id_seq'), primary_key=True, nullable=False, index=True, unique=True)
    bot_id = Column(Integer, ForeignKey(BotSelfOrm.id, ondelete='CASCADE'), nullable=False, comment='所属bot')
    entity_id = Column(Integer, ForeignKey(EntityOrm.id, ondelete='CASCADE'), nullable=False, comment='本身的实体id')
    parent_entity_id = Column(Integer, ForeignKey(EntityOrm.id, ondelete='CASCADE'), nullable=False, comment='父实体id')
    relation_type = Column(String(64), nullable=False, index=True, comment='关联实体类型')
    entity_name = Column(String(64), nullable=False, index=True, comment='关联实体名称')
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)

    # 设置级联和关系加载
    related_entity_back_bots = relationship(BotSelfOrm, back_populates='bots_related_entity',
                                            lazy='joined', innerjoin=True)
    related_entity_back_entity = relationship(EntityOrm, back_populates='entity_related_entity',
                                              foreign_keys=entity_id,
                                              lazy='joined', innerjoin=True)
    related_entity_parent_back_entity = relationship(EntityOrm, back_populates='entity_related_parent_entity',
                                                     foreign_keys=parent_entity_id,
                                                     lazy='joined', innerjoin=True)

    related_entity_friend_ship = relationship('FriendshipOrm', back_populates='friend_ship_back_related_entity',
                                              cascade='all, delete-orphan', passive_deletes=True)
    related_entity_sign_in = relationship('SignInOrm', back_populates='sign_in_back_related_entity',
                                          cascade='all, delete-orphan', passive_deletes=True)
    related_entity_auth_setting = relationship('AuthSettingOrm', back_populates='auth_setting_back_related_entity',
                                               cascade='all, delete-orphan', passive_deletes=True)
    related_entity_cool_down = relationship('CoolDownOrm', back_populates='cool_down_back_related_entity',
                                            cascade='all, delete-orphan', passive_deletes=True)
    related_entity_email_box_bind = relationship('EmailBoxBindOrm', back_populates='email_box_bind_back_related_entity',
                                                 cascade='all, delete-orphan', passive_deletes=True)
    related_entity_subscription = relationship('SubscriptionOrm', back_populates='subscription_back_related_entity',
                                               cascade='all, delete-orphan', passive_deletes=True)

    def __repr__(self):
        return f"<RelatedEntityOrm(bot_id={self.bot_id!r}, entity_id={self.entity_id!r}, " \
               f"parent_entity_id={self.parent_entity_id!r}, relation_type={self.relation_type!r}, " \
               f"created_at={self.created_at!r}, updated_at={self.updated_at!r})>"


class FriendshipOrm(Base):
    """好感度及状态表, 养成系统基础表单"""
    __tablename__ = f'{database_config.db_prefix}friendship'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4'}

    id = Column(Integer, Sequence('friend_ship_id_seq'), primary_key=True, nullable=False, index=True, unique=True)
    entity_id = Column(Integer, ForeignKey(RelatedEntityOrm.id, ondelete='CASCADE'), nullable=False)
    status = Column(String(64), nullable=False, comment='当前状态')
    mood = Column(Float, nullable=False, comment='情绪值, 大于0: 好心情, 小于零: 坏心情')
    friend_ship = Column(Float, nullable=False, comment='好感度/亲密度, 大于0: 友好, 小于0: 厌恶')
    energy = Column(Float, nullable=False, comment='能量值')
    currency = Column(Float, nullable=False, comment='持有货币')
    response_threshold = Column(Float, nullable=False, comment='响应阈值, 控制对交互做出响应的概率或频率, 根据具体插件使用数值')
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)

    # 设置级联和关系加载
    friend_ship_back_related_entity = relationship(RelatedEntityOrm, back_populates='related_entity_friend_ship',
                                                   lazy='joined', innerjoin=True)

    def __repr__(self):
        return f"<FriendshipOrm(entity_id='{self.entity_id}', status='{self.status}', mood='{self.mood}', " \
               f"friend_ship='{self.friend_ship}', energy='{self.energy}', currency='{self.currency}', " \
               f"response_threshold='{self.response_threshold}', " \
               f"created_at='{self.created_at}', updated_at='{self.updated_at}')>"


class SignInOrm(Base):
    """签到表, 养成系统基础表单"""
    __tablename__ = f'{database_config.db_prefix}sign_in'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4'}

    id = Column(BigInteger, Sequence('user_sign_in_id_seq'), primary_key=True, nullable=False, index=True, unique=True)
    entity_id = Column(Integer, ForeignKey(RelatedEntityOrm.id, ondelete='CASCADE'), nullable=False)
    sign_in_date = Column(Date, nullable=False, index=True, comment='签到日期')
    sign_in_info = Column(String(64), nullable=True, comment='签到信息')
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)

    # 设置级联和关系加载
    sign_in_back_related_entity = relationship(RelatedEntityOrm, back_populates='related_entity_sign_in',
                                               lazy='joined', innerjoin=True)

    def __repr__(self):
        return f"<SignInOrm(entity_id='{self.entity_id}', sign_in_date='{self.sign_in_date}', " \
               f"sign_in_info='{self.sign_in_info}', " \
               f"created_at='{self.created_at}', updated_at='{self.updated_at}')>"


class AuthSettingOrm(Base):
    """授权配置表, 主要用于权限管理, 同时兼用于存放使用插件时需要持久化的配置"""
    __tablename__ = f'{database_config.db_prefix}auth_setting'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4'}

    id = Column(Integer, Sequence('auth_setting_id_seq'), primary_key=True, nullable=False, index=True, unique=True)
    entity_id = Column(Integer, ForeignKey(RelatedEntityOrm.id, ondelete='CASCADE'), nullable=False)
    module = Column(String(64), nullable=False, index=True, comment='模块名')
    plugin = Column(String(64), nullable=False, index=True, comment='插件名')
    node = Column(String(64), nullable=False, index=True, comment='权限节点/配置名')
    available = Column(Integer, nullable=False, index=True, comment='需求值, 0=deny/disable, 1=allow/enable, 1<=level')
    value = Column(String(8192), nullable=True, comment='若为插件配置项且对象具有的配置信息')
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)

    # 设置级联和关系加载
    auth_setting_back_related_entity = relationship(RelatedEntityOrm, back_populates='related_entity_auth_setting',
                                                    lazy='joined', innerjoin=True)

    def __repr__(self):
        return f"<AuthSettingOrm(entity_id='{self.entity_id}', module='{self.module}', plugin='{self.plugin}', " \
               f"node='{self.node}', available='{self.available}', value='{self.value}', " \
               f"created_at='{self.created_at}', updated_at='{self.updated_at}')>"


class CoolDownOrm(Base):
    """冷却事件表"""
    __tablename__ = f'{database_config.db_prefix}cool_down'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4'}

    # 表结构
    id = Column(Integer, Sequence('cool_down_id_seq'), primary_key=True, nullable=False, index=True, unique=True)
    entity_id = Column(Integer, ForeignKey(RelatedEntityOrm.id, ondelete='CASCADE'), nullable=False)
    event = Column(String(64), nullable=False, index=True, comment='冷却事件, 用于唯一标识某个/类冷却')
    stop_at = Column(DateTime, nullable=False, index=True, comment='冷却结束时间')
    description = Column(String(128), nullable=True, comment='事件描述')
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)

    # 设置级联和关系加载
    cool_down_back_related_entity = relationship(RelatedEntityOrm, back_populates='related_entity_cool_down',
                                                 lazy='joined', innerjoin=True)

    def __repr__(self):
        return f"<CoolDownOrm(entity_id='{self.entity_id}', event='{self.event}', stop_at='{self.stop_at}'," \
               f"description='{self.description}', created_at='{self.created_at}', updated_at='{self.updated_at}')>"


class EmailBoxOrm(Base):
    """邮箱表"""
    __tablename__ = f'{database_config.db_prefix}email_box'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4'}

    id = Column(Integer, Sequence('email_box_id_seq'), primary_key=True, nullable=False, index=True, unique=True)
    address = Column(String(128), nullable=False, index=True, unique=True, comment='邮箱地址')
    server_host = Column(String(128), nullable=False, comment='IMAP/POP3服务器地址')
    protocol = Column(String(16), nullable=False, comment='协议')
    port = Column(Integer, nullable=False, comment='服务器端口')
    password = Column(String(256), nullable=False, comment='密码')
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)

    # 设置级联和关系加载
    email_box_email_box_bind = relationship('EmailBoxBindOrm', back_populates='email_box_bind_back_email_box',
                                            cascade='all, delete-orphan', passive_deletes=True)

    def __repr__(self):
        return f"<EmailBoxOrm(address='{self.address}', server_host='{self.server_host}', " \
               f"protocol='{self.protocol}', port='{self.port}', " \
               f"created_at='{self.created_at}', updated_at='{self.updated_at}')>"


class EmailBoxBindOrm(Base):
    """邮箱绑定表"""
    __tablename__ = f'{database_config.db_prefix}email_box_bind'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4'}

    id = Column(Integer, Sequence('email_box_bind_id_seq'), primary_key=True, nullable=False, index=True, unique=True)
    email_box_id = Column(Integer, ForeignKey(EmailBoxOrm.id, ondelete='CASCADE'), nullable=False)
    entity_id = Column(Integer, ForeignKey(RelatedEntityOrm.id, ondelete='CASCADE'), nullable=False)
    bind_info = Column(String(64), nullable=True, comment='邮箱绑定信息')
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)

    # 设置级联和关系加载
    email_box_bind_back_email_box = relationship(EmailBoxOrm, back_populates='email_box_email_box_bind',
                                                 lazy='joined', innerjoin=True)
    email_box_bind_back_related_entity = relationship(RelatedEntityOrm, back_populates='related_entity_email_box_bind',
                                                      lazy='joined', innerjoin=True)

    def __repr__(self):
        return f"<EmailBoxBindOrm(email_box_id='{self.email_box_id}', entity_id='{self.entity_id}', " \
               f"bind_info='{self.bind_info}', created_at='{self.created_at}', updated_at='{self.updated_at}')>"


class SubscriptionSourceOrm(Base):
    """订阅源表"""
    __tablename__ = f'{database_config.db_prefix}subscription_source'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4'}

    id = Column(Integer, Sequence('sub_source_id_seq'), primary_key=True, nullable=False, index=True, unique=True)
    sub_type = Column(String(64), nullable=False, index=True, comment='订阅类型')
    sub_id = Column(String(64), nullable=False, index=True, comment='订阅id，直播间房间号/用户uid等')
    sub_user_name = Column(String(64), nullable=False, comment='订阅用户的名称')
    sub_info = Column(String(64), nullable=True, comment='订阅源信息')
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)

    # 设置级联和关系加载
    subscription_source_subscription = relationship('SubscriptionOrm',
                                                    back_populates='subscription_back_subscription_source',
                                                    cascade='all, delete-orphan', passive_deletes=True)

    def __repr__(self):
        return f"<SubscriptionSourceOrm(sub_type='{self.sub_type}', sub_id='{self.sub_id}', " \
               f"sub_user_name='{self.sub_user_name}', sub_info='{self.sub_info}', " \
               f"created_at='{self.created_at}', updated_at='{self.updated_at}')>"


class SubscriptionOrm(Base):
    """订阅表"""
    __tablename__ = f'{database_config.db_prefix}subscription'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4'}

    id = Column(Integer, Sequence('subscription_id_seq'), primary_key=True, nullable=False, index=True, unique=True)
    sub_source_id = Column(Integer, ForeignKey(SubscriptionSourceOrm.id, ondelete='CASCADE'), nullable=False)
    entity_id = Column(Integer, ForeignKey(RelatedEntityOrm.id, ondelete='CASCADE'), nullable=False)
    sub_info = Column(String(64), nullable=True, comment='订阅信息')
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)

    # 设置级联和关系加载
    subscription_back_subscription_source = relationship(SubscriptionSourceOrm,
                                                         back_populates='subscription_source_subscription',
                                                         lazy='joined', innerjoin=True)
    subscription_back_related_entity = relationship(RelatedEntityOrm, back_populates='related_entity_subscription',
                                                    lazy='joined', innerjoin=True)

    def __repr__(self):
        return f"<SubscriptionOrm(sub_source_id='{self.sub_source_id}', entity_id='{self.entity_id}', " \
               f"sub_info='{self.sub_info}', created_at='{self.created_at}', updated_at='{self.updated_at}')>"


class BiliDynamicOrm(Base):
    """B站动态表"""
    __tablename__ = f'{database_config.db_prefix}bili_dynamic'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4'}

    # 表结构
    id = Column(BigInteger, Sequence('bili_dynamic_id_seq'), primary_key=True, nullable=False, index=True, unique=True)
    dynamic_id = Column(BigInteger, nullable=False, index=True, unique=True, comment='动态id')
    dynamic_type = Column(Integer, nullable=False, index=True, comment='动态类型')
    uid = Column(Integer, nullable=False, index=True, comment='用户uid')
    content = Column(String(4096), nullable=False, comment='动态内容')
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<BiliDynamicOrm(dynamic_id='{self.dynamic_id}', dynamic_type='{self.dynamic_type}', " \
               f"uid='{self.uid}', content='{self.content}', " \
               f"created_at='{self.created_at}', updated_at='{self.updated_at}')>"


class PixivArtworkOrm(Base):
    """Pixiv 作品表"""
    __tablename__ = f'{database_config.db_prefix}pixiv_artwork'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4'}

    # 表结构
    id = Column(BigInteger, Sequence('pixiv_artwork_id_seq'), primary_key=True, nullable=False, index=True, unique=True)
    pid = Column(BigInteger, nullable=False, index=True, unique=True, comment='作品pid')
    uid = Column(BigInteger, nullable=False, index=True, comment='作者uid')
    title = Column(String(128), nullable=False, index=True, comment='作品标题title')
    uname = Column(String(128), nullable=False, index=True, comment='作者名')
    classified = Column(Integer, nullable=False, index=True, comment='标记标签, 0=未标记, 1=已人工标记或从可信已标记来源获取')
    nsfw_tag = Column(Integer, nullable=False, index=True, comment='nsfw标签, -1=未标记, 0=safe, 1=setu. 2=r18')
    width = Column(Integer, nullable=False, comment='原始图片宽度')
    height = Column(Integer, nullable=False, comment='原始图片高度')
    tags = Column(String(1024), nullable=False, comment='作品标签')
    url = Column(String(1024), nullable=False, comment='url')
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)

    # 设置级联和关系加载
    pixiv_artwork_pixiv_artwork_page = relationship('PixivArtworkPageOrm',
                                                    back_populates='pixiv_artwork_page_back_pixiv_artwork',
                                                    cascade='all, delete-orphan', passive_deletes=True)

    def __repr__(self):
        return f"<PixivArtworkOrm(pid='{self.pid}', uid='{self.uid}', title='{self.title}', uname='{self.uname}', " \
               f"classified='{self.classified}', nsfw_tag='{self.nsfw_tag}', " \
               f"width='{self.width}', height='{self.height}', tags='{self.tags}', url='{self.url}', " \
               f"created_at='{self.created_at}', updated_at='{self.updated_at}')>"


class PixivArtworkPageOrm(Base):
    """Pixiv 作品图片链接表"""
    __tablename__ = f'{database_config.db_prefix}pixiv_artwork_page'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4'}

    id = Column(BigInteger, Sequence('pixiv_page_id_seq'), primary_key=True, nullable=False, index=True, unique=True)
    artwork_id = Column(BigInteger, ForeignKey(PixivArtworkOrm.id, ondelete='CASCADE'), nullable=False)
    page = Column(Integer, nullable=False, index=True, comment='页码')
    original = Column(String(1024), nullable=False, comment='original image url')
    regular = Column(String(1024), nullable=False, comment='regular image url')
    small = Column(String(1024), nullable=False, comment='small image url')
    thumb_mini = Column(String(1024), nullable=False, comment='thumb_mini image url')
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)

    # 设置级联和关系加载
    pixiv_artwork_page_back_pixiv_artwork = relationship(PixivArtworkOrm,
                                                         back_populates='pixiv_artwork_pixiv_artwork_page',
                                                         lazy='joined', innerjoin=True)

    def __repr__(self):
        return f"<PixivPage(artwork_id='{self.artwork_id}', page='{self.page}', original='{self.original}', " \
               f"regular='{self.regular}', small='{self.small}', thumb_mini='{self.thumb_mini}', " \
               f"created_at='{self.created_at}', updated_at='{self.updated_at}')>"


class PixivisionArticleOrm(Base):
    """Pixivision 表"""
    __tablename__ = f'{database_config.db_prefix}pixivision_article'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4'}

    # 表结构
    id = Column(Integer, Sequence('pixivision_article_id_seq'),
                primary_key=True, nullable=False, index=True, unique=True)
    aid = Column(Integer, nullable=False, index=True, unique=True, comment='aid')
    title = Column(String(256), nullable=False, comment='title')
    description = Column(String(1024), nullable=False, comment='description')
    tags = Column(String(1024), nullable=False, comment='tags')
    artworks_id = Column(String(1024), nullable=False, comment='article artwork_id')
    url = Column(String(1024), nullable=False, comment='url')
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<PixivisionArticleOrm(aid='{self.aid}', title='{self.title}', description='{self.description}', " \
               f"tags='{self.tags}', artworks_id='{self.artworks_id}', url='{self.url}', " \
               f"created_at='{self.created_at}', updated_at='{self.updated_at}')>"


class WordBankOrm(Base):
    """问答语料词句表"""
    __tablename__ = f'{database_config.db_prefix}word_bank'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4'}

    # 表结构
    id = Column(Integer, Sequence('word_bank_id_seq'), primary_key=True, nullable=False, index=True, unique=True)
    key_word = Column(String(128), nullable=False, index=True, comment='匹配目标')
    reply_entity = Column(String(64), nullable=False, index=True, comment='响应对象, 可为群号/用户qq/频道id等标识')
    result_word = Column(String(8192), nullable=False, comment='结果文本')
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<WordBankOrm(key_word='{self.key_word}', reply_entity='{self.reply_entity}', " \
               f"result_word='{self.result_word}', created_at='{self.created_at}', updated_at='{self.updated_at}')>"


__all__ = [
    'Base',
    'SystemSettingOrm',
    'PluginOrm',
    'StatisticOrm',
    'HistoryOrm',
    'BotSelfOrm',
    'EntityOrm',
    'RelatedEntityOrm',
    'FriendshipOrm',
    'SignInOrm',
    'AuthSettingOrm',
    'CoolDownOrm',
    'EmailBoxOrm',
    'EmailBoxBindOrm',
    'SubscriptionSourceOrm',
    'SubscriptionOrm',
    'BiliDynamicOrm',
    'PixivArtworkOrm',
    'PixivArtworkPageOrm',
    'PixivisionArticleOrm',
    'WordBankOrm'
]
