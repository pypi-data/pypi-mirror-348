## GredisQL

A GraphQL interface for Redis Database.

## Version Information

Current Version: 0.0.9

### Update History

#### Version 0.0.9 (Latest)

- Added support for Redis Sorted Sets operations
- Added support for Redis Hash operations
- Improved type handling for GraphQL responses
- Fixed GraphQL schema type definitions
- Added comprehensive test suite

#### Version 0.0.8

- Added support for Redis List operations
- Added support for Redis Set operations
- Improved error handling

#### Version 0.0.7

- Initial release with basic Redis operations
- Support for String operations
- Basic GraphQL interface implementation

## How To Install

```python
pip install gredisql
```

If you find this project interesting, you can always appreciate it by giving it a Star. :D

## A Background of `GredisQL`

![background_image](/img/gredisql-bg.png)

## Motivation

1. I was bored, been sick for a while, had to lie on the bed. So I needed to create something.
2. Redis has Web interface ( actually a REST interface), so I urged to build one in GraphQL.
3. There are some pretty amazing GraphQL libraries around python echo system, I wanted to try them.
4. Last but not least, jump into quick coding session, engage and nurture the human mind. LOL

## Design Philosophy

1. All the data `mutation` and `query` are not separated here by action and most probably all the actions are performed via `query` operation.
2. Technically `all` the requests sent to the GraphQL `server` was in `POST`, so I was initially okay with the implementation.
3. `Strawberry-Graphql` is kind of server agnostic so either you can use `ASGI` or `WSGI` counterpart.
4. Currently limiting the implementation with `WSGI` server, but I've plan to adopt `ASGI` in the journey, to support `subscription`.
5. Not `all` Redis commands are found in the implementation, I'll try to cover it in the process.

## Inspiration and Tools I used

1. `redis==5.0.0` is used to communicate with the Redis database.
2. `strawberry-graphql` is used to do the heavy lifting. Also, I tried `ariadne` which is also another cool tool to try with.

## Features and Future Plans

1. [x] String Commands

   - GET, SET, MSET, MGET
   - INCRBY, DECRBY, INCRBYFLOAT
   - APPEND, GETEX, GETDEL
   - EXPIRE, EXPIREAT
   - KEYS, EXISTS, DELETE

2. [x] List Commands

   - LPUSH, RPUSH
   - LPOP, RPOP
   - LRANGE
   - LLEN

3. [x] Set Commands

   - SADD, SCARD
   - SDIFF, SDIFFSTORE
   - SINTER, SINTERSTORE
   - SISMEMBER, SMEMBERS
   - SMOVE, SPOP

4. [x] Hash Commands

   - HSET, HGET
   - HGETALL
   - HDEL
   - HLEN
   - HKEYS, HVALS

5. [x] Sorted Set Commands
   - ZADD
   - ZRANGE, ZREVRANGE
   - ZCARD
   - ZSCORE
   - ZREM
   - ZCOUNT

And many more to come in the future iteration.

## Example GraphQL Queries

### String Operations

```graphql
query {
  set(name: "mykey", value: "myvalue")
  get(name: "mykey")
  mset(
    mappings: [
      { key: "key1", value: "value1" }
      { key: "key2", value: "value2" }
    ]
  )
  mget(keys: ["key1", "key2"])
}
```

### List Operations

```graphql
query {
  lpush(name: "mylist", values: ["one", "two", "three"])
  lrange(name: "mylist", start: 0, end: -1)
  llen(name: "mylist")
}
```

### Hash Operations

```graphql
query {
  hset(name: "myhash", key: "field1", value: "value1")
  hget(name: "myhash", key: "field1")
  hgetall(name: "myhash")
}
```

### Sorted Set Operations

```graphql
query {
  zadd(name: "myset", mapping: {"member1": 1.0, "member2": 2.0})
  zrange(name: "myset", start: 0, end: -1, withscores: true)
  zcard(name: "myset")
}
```

## Quick Starting the GraphQL Server

```python
if __name__ == "__main__":
    from gredisql.core import Server

    server = Server()
    server.run()
```

You can specify the `host`, `port` and `debug` mode in while instantiating the `GraphQL` server.
Simply write,

```python

if __name__ == "__main__":

    REDIS_HOST = 'redis-4343.c8.us-east-1-4.ec2.cloud.redislabs.com'
    REDIS_PORT = 16292
    REDIS_PASSWORD = 'your-secret-password'

    from gredisql.core import Server

    server = Server(
         REDIS_HOST=REDIS_HOST,
         REDIS_PORT=REDIS_PORT,
         REDIS_PASSWORD=REDIS_PASSWORD
    )
    server.run()

```

Now navigate to `http://localhost:5055/graphql` and voilà.
