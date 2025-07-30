import pytest
import strawberry
from gredisql.core import Server, KeyVal, ScoreMember
import requests
import json

@pytest.fixture
def server():
    return Server(debug=True)

@pytest.fixture
def graphql_url():
    return "http://localhost:5055/graphql"

def test_string_operations(server, graphql_url):
    # Test SET and GET
    query = """
    query {
        set(name: "test_key", value: "test_value")
        get(name: "test_key")
    }
    """
    response = requests.post(graphql_url, json={"query": query})
    data = response.json()
    assert data["data"]["set"]["response"] == "OK"
    assert data["data"]["get"]["response"] == "test_value"

    # Test MSET and MGET
    query = """
    query {
        mset(mappings: [
            {key: "key1", value: "value1"},
            {key: "key2", value: "value2"}
        ])
        mget(keys: ["key1", "key2"])
    }
    """
    response = requests.post(graphql_url, json={"query": query})
    data = response.json()
    assert data["data"]["mset"]["response"] == "True"
    assert data["data"]["mget"]["response"] == ["value1", "value2"]

    # Test INCRBY and DECRBY
    query = """
    query {
        set(name: "counter", value: "10")
        incrby(name: "counter", amount: 5)
        decrby(name: "counter", amount: 3)
    }
    """
    response = requests.post(graphql_url, json={"query": query})
    data = response.json()
    assert data["data"]["incrby"]["response"] == "15"
    assert data["data"]["decrby"]["response"] == "12"

def test_list_operations(server, graphql_url):
    # Test LPUSH and LRANGE
    query = """
    query {
        lpush(name: "mylist", values: ["one", "two", "three"])
        lrange(name: "mylist", start: 0, end: -1)
    }
    """
    response = requests.post(graphql_url, json={"query": query})
    data = response.json()
    assert data["data"]["lpush"]["response"] == "3"
    assert data["data"]["lrange"]["response"] == ["three", "two", "one"]

    # Test RPUSH and LPOP
    query = """
    query {
        rpush(name: "mylist2", values: ["a", "b", "c"])
        lpop(name: "mylist2")
    }
    """
    response = requests.post(graphql_url, json={"query": query})
    data = response.json()
    assert data["data"]["rpush"]["response"] == "3"
    assert data["data"]["lpop"]["response"] == "a"

def test_set_operations(server, graphql_url):
    # Test SADD and SMEMBERS
    query = """
    query {
        sadd(name: "myset", values: ["one", "two", "three"])
        smembers(name: "myset")
    }
    """
    response = requests.post(graphql_url, json={"query": query})
    data = response.json()
    assert data["data"]["sadd"]["response"] == "3"
    assert set(data["data"]["smembers"]["response"]) == {"one", "two", "three"}

    # Test SISMEMBER
    query = """
    query {
        sismember(name: "myset", value: "one")
    }
    """
    response = requests.post(graphql_url, json={"query": query})
    data = response.json()
    assert data["data"]["sismember"]["response"] == "1"

def test_hash_operations(server, graphql_url):
    # Test HSET and HGET
    query = """
    query {
        hset(name: "myhash", key: "field1", value: "value1")
        hget(name: "myhash", key: "field1")
    }
    """
    response = requests.post(graphql_url, json={"query": query})
    data = response.json()
    assert data["data"]["hset"]["response"] == "1"
    assert data["data"]["hget"]["response"] == "value1"

    # Test HGETALL
    query = """
    query {
        hset(name: "myhash", key: "field2", value: "value2")
        hgetall(name: "myhash")
    }
    """
    response = requests.post(graphql_url, json={"query": query})
    data = response.json()
    response_dict = {item["key"]: item["value"] for item in data["data"]["hgetall"]["response"]}
    assert response_dict == {"field1": "value1", "field2": "value2"}

def test_sorted_set_operations(server, graphql_url):
    # Test ZADD and ZRANGE
    query = """
    query {
        zadd(name: "mysortedset", members: [
            {score: 1.0, member: "one"},
            {score: 2.0, member: "two"},
            {score: 3.0, member: "three"}
        ])
        zrange(name: "mysortedset", start: 0, end: -1, withscores: true)
    }
    """
    response = requests.post(graphql_url, json={"query": query})
    data = response.json()
    assert data["data"]["zadd"]["response"] == "3"
    assert len(data["data"]["zrange"]["response"]) == 3

    # Test ZSCORE
    query = """
    query {
        zscore(name: "mysortedset", value: "one")
    }
    """
    response = requests.post(graphql_url, json={"query": query})
    data = response.json()
    assert float(data["data"]["zscore"]["response"]) == 1.0

def test_key_operations(server, graphql_url):
    # Test KEYS and EXISTS
    query = """
    query {
        set(name: "test_key1", value: "value1")
        set(name: "test_key2", value: "value2")
        keys(pattern: "test_*")
        exists(names: ["test_key1", "test_key2"])
    }
    """
    response = requests.post(graphql_url, json={"query": query})
    data = response.json()
    assert set(data["data"]["keys"]["response"]) == {"test_key1", "test_key2"}
    assert data["data"]["exists"]["response"] == "2"

    # Test DELETE
    query = """
    query {
        delete(names: ["test_key1", "test_key2"])
    }
    """
    response = requests.post(graphql_url, json={"query": query})
    data = response.json()
    assert data["data"]["delete"]["response"] == "2"

def test_expiration_operations(server, graphql_url):
    # Test EXPIRE
    query = """
    query {
        set(name: "expire_key", value: "value")
        expire(name: "expire_key", time: 10)
    }
    """
    response = requests.post(graphql_url, json={"query": query})
    data = response.json()
    assert data["data"]["expire"]["response"] == "1"

if __name__ == "__main__":
    pytest.main([__file__]) 