from ticketapp.db.redis import redis



# Fetch all messages from the "completed_order" stream
stream_messages = redis.xread({'completed_order': '0'})

# Iterate over the messages and parse the order data
for _, messages in stream_messages:
    for message in messages:
        order_data = message[1]
        print(order_data)
