from spilo.redis_pubsub import RedisPubSub


def test_singleton_class():
    cls1 = RedisPubSub(url="redis://localhost:6379/0")
    cls2 = RedisPubSub(url="redis://localhost:6379/0")
    assert cls1 is cls2

