import time
from pymemcache.client.base import Client

# Connect to Memcached server (Ensure Memcached is running)
client = Client(('localhost', 11211))


def read_database():
    """Simulates fetching data from a database."""
    print("Fetching value from database...")
    return 42  # Example value


def get_value():
    """Retrieve value from cache, if not found, get from DB and update cache."""
    result = client.get('my_key')

    if result is None:
        # Cache miss or expired, call database
        result = read_database()

        # Store in cache with TTL of 10 seconds
        client.set('my_key', str(result), expire=10)

        print(f"Cache updated with value: {result}")
    else:
        print(f"Cache hit: {result.decode()}")

    return int(result)  # Convert from bytes to int


# First call: Fetches from DB and stores in cache
print("First call result:", get_value())

# Second call within 10 seconds: Fetches from cache
time.sleep(5)  # Wait 5 seconds
print("Second call result:", get_value())

# Third call after TTL expires: Fetches from DB again
time.sleep(6)  # Wait another 6 seconds (Total > 10 seconds)
print("Third call result:", get_value())
