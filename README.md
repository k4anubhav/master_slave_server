# Master Server

Master server has job queue and slave client will pull jobs from the queue and execute them. and send the result back to
the master server. So, you can have multiple slave clients and one master server. The job queue will be shared between
all the slave clients.

So far, only REST API call is supported. The slave client will make a REST API call with the specified method, url and
body. The response will be sent back to the master server.

You can configure **webhook** url in the master server. To receive the result of the job in your application.

Currently, slave client also needed to be trusted, the project may be updated in the future to support untrusted slave
client.

### Use Cases

- You are limited by the number of API calls from your IP address. You can use this to make
  more API calls. Utilizing multiple IP addresses.

### [Slave Client](https://github.com/k4anubhav/slave_client)

### Supported Job

- [x] REST API call

### Platform Support

- [ ] Linux
- [ ] Windows
- [ ] Mac
- [x] Android
- [ ] iOS // Not tested

### TODO

- [ ] Add logs in client, so client user can see what jobs are being executed.
- [ ] Add support for untrusted slave client
- [ ] Add support for more job types
- [ ] Add support for more platforms