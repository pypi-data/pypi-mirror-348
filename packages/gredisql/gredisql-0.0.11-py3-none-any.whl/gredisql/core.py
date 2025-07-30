# -*- coding: utf-8 -*-

"""
author: S.M. Sabbir Amin
date: 30 Aug 2023
email: sabbir.amin@goava.com, sabbiramin.cse11ruet@gmail.com

"""
import typing
import redis
import strawberry
from flask import Flask
from strawberry.flask.views import GraphQLView


@strawberry.type
class CommonString:
    response: typing.Optional[str]


@strawberry.type
class CommonInt:
    response: int


@strawberry.type
class CommonList:
    response: typing.List[str]


@strawberry.type
class KeyValuePair:
    key: str
    value: str


@strawberry.type
class CommonDict:
    response: typing.List[KeyValuePair]


@strawberry.input
class KeyVal:
    key: str
    value: str


@strawberry.input
class ScoreMember:
    score: float
    member: str


class Server:
    def __init__(self,
                 host: str = 'localhost',
                 port: int = 5055,
                 debug=True,
                 REDIS_HOST: str = 'localhost',
                 REDIS_PORT: int = 6379,
                 REDIS_DB: int = 0,
                 REDIS_PASSWORD: str = '',
                 REDIS_DECODE_RESPONSE: bool = True
                 ):
        self.app = Flask(__name__)
        self.host = host
        self.port = port
        self.debug = debug
        self.REDIS_HOST = REDIS_HOST if REDIS_HOST else 'localhost'
        self.REDIS_PORT = REDIS_PORT if REDIS_PORT else 6379
        self.REDIS_DB = REDIS_DB if REDIS_DB else 0
        self.REDIS_PASSWORD = REDIS_PASSWORD if REDIS_PASSWORD else ''
        self.REDIS_DECODE_RESPONSE = REDIS_DECODE_RESPONSE if REDIS_DECODE_RESPONSE else True
        print('Connecting Redis, host:', self.REDIS_HOST, ', port:', self.REDIS_PORT)
        rr = redis.StrictRedis(host=self.REDIS_HOST,
                               port=self.REDIS_PORT,
                               db=self.REDIS_DB,
                               password=self.REDIS_PASSWORD,
                               decode_responses=self.REDIS_DECODE_RESPONSE)

        @strawberry.type
        class Query:
            @strawberry.field
            def set(self,
                    name: str,
                    value: str,
                    ex: typing.Optional[int] = None,
                    px: typing.Optional[int] = None,
                    nx: typing.Optional[bool] = False,
                    xx: typing.Optional[bool] = False,
                    keepttl: typing.Optional[bool] = False,
                    get: typing.Optional[bool] = False,
                    exat: typing.Optional[int] = None,
                    pxat: typing.Optional[int] = None
                    ) -> CommonString:
                resp = rr.set(
                    name=name,
                    value=value,
                    ex=ex,
                    px=px,
                    nx=nx,
                    xx=xx,
                    keepttl=keepttl,
                    get=get,
                    exat=exat,
                    pxat=pxat
                )
                return CommonString(response=str(resp))

            @strawberry.field
            def get(self, name: str) -> CommonString:
                resp = rr.get(name=name)
                return CommonString(response=resp)

            @strawberry.field
            def getex(self,
                      name: str,
                      ex: typing.Optional[int] = None,
                      px: typing.Optional[int] = None,
                      exat: typing.Optional[int] = None,
                      pxat: typing.Optional[int] = None,
                      persist: bool = False
                      ) -> CommonString:
                resp = rr.getex(name=name, ex=ex, px=px, exat=exat, pxat=pxat, persist=persist)
                return CommonString(response=resp)

            @strawberry.field
            def info(self) -> CommonString:
                info_dict = rr.info()
                return CommonString(response=str(info_dict))

            @strawberry.field
            def mset(self, mappings: typing.List[KeyVal]) -> CommonString:
                mappings = {m.key: m.value for m in mappings}
                resp = rr.mset(mappings)
                return CommonString(response=str(resp))

            @strawberry.field
            def mget(self, keys: typing.List[str]) -> CommonList:
                resp = rr.mget(keys=keys)
                return CommonList(response=resp)

            @strawberry.field
            def incrby(self, name: str, amount: int = 1) -> CommonString:
                return CommonString(response=str(rr.incrby(name=name, amount=amount)))

            @strawberry.field
            def decrby(self, name: str, amount: int = 1) -> CommonString:
                return CommonString(response=str(rr.decrby(name=name, amount=amount)))

            @strawberry.field
            def incrbyfloat(self, name: str, amount: float = 1.0) -> CommonString:
                return CommonString(response=str(rr.incrbyfloat(name=name, amount=amount)))

            @strawberry.field
            def keys(self, pattern: str) -> CommonList:
                return CommonList(response=rr.keys(pattern=pattern))

            @strawberry.field
            def delete(self, names: typing.List[str]) -> CommonString:
                return CommonString(response=str(rr.delete(*names)))

            @strawberry.field
            def exists(self, names: typing.List[str]) -> CommonString:
                return CommonString(response=str(rr.exists(*names)))

            @strawberry.field
            def append(self, key: str, value: str) -> CommonString:
                return CommonString(response=str(rr.append(key=key, value=value)))

            @strawberry.field
            def expire(
                    self,
                    name: str,
                    time: int,
                    nx: typing.Optional[bool] = False,
                    xx: typing.Optional[bool] = False,
                    gt: typing.Optional[bool] = False,
                    lt: typing.Optional[bool] = False) -> CommonString:
                return CommonString(response=str(rr.expire(
                    name=name,
                    time=time,
                    nx=nx,
                    xx=xx,
                    gt=gt,
                    lt=lt
                )))

            @strawberry.field
            def expireat(
                    self,
                    name: str,
                    when: int,
                    nx: typing.Optional[bool] = False,
                    xx: typing.Optional[bool] = False,
                    gt: typing.Optional[bool] = False,
                    lt: typing.Optional[bool] = False) -> CommonString:
                return CommonString(response=str(rr.expireat(
                    name=name,
                    when=when,
                    nx=nx,
                    xx=xx,
                    gt=gt,
                    lt=lt
                )))

            @strawberry.field
            def getdel(self, name: str) -> CommonString:
                return CommonString(response=rr.getdel(name=name))

            @strawberry.field
            def sadd(self, name: str, values: typing.List[str]) -> CommonString:
                return CommonString(response=str(rr.sadd(name, *values)))

            @strawberry.field
            def scard(self, name: str) -> CommonString:
                return CommonString(response=str(rr.scard(name=name)))

            @strawberry.field
            def sdiff(self, keys: typing.List[str]) -> CommonList:
                return CommonList(response=rr.sdiff(keys))

            @strawberry.field
            def sdiffstore(self, keys: typing.List[str], dest: str) -> CommonString:
                return CommonString(response=str(rr.sdiffstore(dest=dest, keys=keys)))

            @strawberry.field
            def sinter(self, keys: typing.List[str]) -> CommonList:
                return CommonList(response=rr.sinter(keys))

            @strawberry.field
            def sinterstore(self, keys: typing.List[str], dest: str) -> CommonString:
                return CommonString(response=str(rr.sinterstore(dest=dest, keys=keys)))

            @strawberry.field
            def sismember(self, name: str, value: str) -> CommonString:
                return CommonString(response=str(rr.sismember(name=name, value=value)))

            @strawberry.field
            def smembers(self, name: str) -> CommonList:
                return CommonList(response=rr.smembers(name=name))

            @strawberry.field
            def smove(self, src: str, dst: str, value: str) -> CommonString:
                return CommonString(response=str(rr.smove(src=src, dst=dst, value=value)))

            @strawberry.field
            def spop(self, name: str, count: typing.Optional[int] = None) -> CommonString:
                result = rr.spop(name=name, count=count)
                if isinstance(result, list):
                    return CommonString(response=str(result))
                return CommonString(response=str(result))

            @strawberry.field
            def lpush(self, name: str, values: typing.List[str]) -> CommonString:
                return CommonString(response=str(rr.lpush(name, *values)))

            @strawberry.field
            def rpush(self, name: str, values: typing.List[str]) -> CommonString:
                return CommonString(response=str(rr.rpush(name, *values)))

            @strawberry.field
            def lpop(self, name: str, count: typing.Optional[int] = None) -> CommonString:
                result = rr.lpop(name, count)
                if isinstance(result, list):
                    return CommonString(response=str(result))
                return CommonString(response=str(result))

            @strawberry.field
            def rpop(self, name: str, count: typing.Optional[int] = None) -> CommonString:
                result = rr.rpop(name, count)
                if isinstance(result, list):
                    return CommonString(response=str(result))
                return CommonString(response=str(result))

            @strawberry.field
            def lrange(self, name: str, start: int, end: int) -> CommonList:
                return CommonList(response=rr.lrange(name, start, end))

            @strawberry.field
            def llen(self, name: str) -> CommonString:
                return CommonString(response=str(rr.llen(name)))

            @strawberry.field
            def hset(self, name: str, key: str, value: str) -> CommonString:
                return CommonString(response=str(rr.hset(name, key, value)))

            @strawberry.field
            def hget(self, name: str, key: str) -> CommonString:
                return CommonString(response=rr.hget(name, key))

            @strawberry.field
            def hgetall(self, name: str) -> CommonDict:
                result = rr.hgetall(name)
                return CommonDict(response=[KeyValuePair(key=k, value=v) for k, v in result.items()])

            @strawberry.field
            def hdel(self, name: str, keys: typing.List[str]) -> CommonString:
                return CommonString(response=str(rr.hdel(name, *keys)))

            @strawberry.field
            def hlen(self, name: str) -> CommonString:
                return CommonString(response=str(rr.hlen(name)))

            @strawberry.field
            def hkeys(self, name: str) -> CommonList:
                return CommonList(response=rr.hkeys(name))

            @strawberry.field
            def hvals(self, name: str) -> CommonList:
                return CommonList(response=rr.hvals(name))

            @strawberry.field
            def zadd(self, name: str, members: typing.List[ScoreMember]) -> CommonString:
                mapping = {m.member: m.score for m in members}
                return CommonString(response=str(rr.zadd(name, mapping)))

            @strawberry.field
            def zrange(self, name: str, start: int, end: int, withscores: bool = False) -> CommonList:
                return CommonList(response=rr.zrange(name, start, end, withscores=withscores))

            @strawberry.field
            def zrevrange(self, name: str, start: int, end: int, withscores: bool = False) -> CommonList:
                return CommonList(response=rr.zrevrange(name, start, end, withscores=withscores))

            @strawberry.field
            def zcard(self, name: str) -> CommonString:
                return CommonString(response=str(rr.zcard(name)))

            @strawberry.field
            def zscore(self, name: str, value: str) -> CommonString:
                return CommonString(response=str(rr.zscore(name, value)))

            @strawberry.field
            def zrem(self, name: str, values: typing.List[str]) -> CommonString:
                return CommonString(response=str(rr.zrem(name, *values)))

            @strawberry.field
            def zcount(self, name: str, min_score: float, max_score: float) -> CommonString:
                return CommonString(response=str(rr.zcount(name, min_score, max_score)))

        self.schema = strawberry.Schema(Query)
        self.app.add_url_rule(
            "/graphql",
            view_func=GraphQLView.as_view("graphql_view", schema=self.schema),
        )

    def run(self):
        self.app.run(
            host=self.host,
            port=self.port,
            debug=self.debug
        )
