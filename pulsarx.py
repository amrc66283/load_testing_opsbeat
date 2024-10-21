import pulsar

# Create a Pulsar client instance
client = pulsar.Client('pulsar://localhost:6650')

# Create a producer on the topic 'my-topic'
producer = client.create_producer('my-topic')

# Send a message
producer.send(('Hello Pulsar mai 150 huuuuuuuuu!').encode('utf-8'))

print("Message sent to Pulsar!")

# Close the client connection
client.close()
