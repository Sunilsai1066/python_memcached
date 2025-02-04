import time
from pymemcache.client.base import Client

# Connect to Memcached server (Make sure Memcached is running)
client = Client(('localhost', 11211))

# Reset counter for demonstration
client.set('counter', b'10')  # Store as bytes


def cas_success_case():
    """Simulates a successful CAS operation."""
    print("\n=== CAS SUCCESS CASE ===")

    # Process A gets the value and CAS token
    value, cas_token = client.gets('counter')

    if value is not None:
        value = int(value.decode())  # Decode bytes to string and convert to int

    print(f"Process A - Initial Value: {value}, CAS Token: {cas_token}")

    # Process A increments the value
    new_value = str(value + 1).encode()  # Convert int to string, then to bytes

    # Process A updates the value using CAS
    success = client.cas('counter', new_value, cas_token)

    if success:
        print(f"Process A - CAS Success: Updated counter to {new_value.decode()}")
    else:
        print("Process A - CAS Failed")


def cas_failure_case():
    """Simulates a CAS failure due to concurrent modification."""
    print("\n=== CAS FAILURE CASE ===")

    # Process A retrieves the value and CAS token
    value_A, cas_token_A = client.gets('counter')

    if value_A is not None:
        value_A = int(value_A.decode())  # Decode bytes to string and convert to int

    print(f"Process A - Value: {value_A}, CAS Token: {cas_token_A}")

    # Simulate Process B modifying the value before Process A updates
    client.set('counter', b'20')  # Directly setting new value in bytes
    print("Process B - Directly set counter to 20")

    # Process A tries to update with old CAS token
    new_value_A = str(value_A + 1).encode()  # Convert int to bytes
    success_A = client.cas('counter', new_value_A, cas_token_A)

    if success_A:
        print(f"Process A - CAS Success: Updated counter to {new_value_A.decode()}")
    else:
        print("Process A - CAS Failed: Value was modified by another process")


# Run both cases
cas_success_case()
time.sleep(1)  # Just to differentiate cases in output
cas_failure_case()
