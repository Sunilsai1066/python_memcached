from pymemcache.client import base
from pymemcache import fallback


def do_some_query():
    # Replace with actual querying code to a database,
    # a remote REST API, etc.
    return 42


# The ignore_exc=True parameter ensures that if the old cache server is down,
# it won’t throw an error—it will just continue execution.
old_cache = base.Client(('localhost', 11211), ignore_exc=True)
new_cache = base.Client(('localhost', 11212))

client = fallback.FallbackClient((new_cache, old_cache))

result = client.get('some_key')

if result is None:
    # The cache is empty, need to get the value
    # from the canonical source:
    result = do_some_query()

    # Cache the result for next time:
    client.set('some_key', result)

print(result)
