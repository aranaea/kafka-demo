## Kafka Demo ##

This repo contains a pretty simple demo of Kafka's pub/sub capabilities.  Inside
you'll find a small handful of goodies.

* `docker-compose.yml`
  * This is the base composition.  It should allow you to bring up the stack 
  with just `docker-compose up`
* `docker-compose.dev.yml`
  * The same as `docker-compose.yml` except that it mounts the producer and 
  consumer src directories to make the dev/test cycle easier.  You can start it with 
  `docker-compose -f docker-compose.dev.yml up`
* producer
  * The source and `Dockerfile` for the producer application.
* consumer
  * Same thing but for the consumer
* tester  
  * Some tests to exercise the stack once it's up and running.  You might expect
  these to be unit tests but they're actually integration tests.  The applications
  are very simple so the meat of the testing was really in the component 
  interactions.
  
### Dependencies ###
Other versions may work but this build has been tested with the following:

Python 2.7.13
docker-compose version 1.15.0
Docker version 17.05.0-ce

You should also run:
```bash
pip install -r requirements.txt
```
is the `tester` directory to make sure you have the packages needed.

### Example Usage ###

You'll always need to start it manually

```bash
docker-compose up
```

It'll take a few seconds to come up.  Usually the producer and consumer
seem to start before kafka is ready and there's a point where it looks 
like it's good to go, but it's not.

```
consumer_1   | Running app in debug mode!
consumer_1   |  * Running on http://0.0.0.0:80/ (Press CTRL+C to quit)
consumer_1   |  * Restarting with stat
producer_1   |  * Running on http://0.0.0.0:80/ (Press CTRL+C to quit)
producer_1   |  * Restarting with stat
consumer_1   |  * Debugger is active!
consumer_1   |  * Debugger PIN: 325-703-385
producer_1   |  * Debugger is active!
producer_1   |  * Debugger PIN: 111-020-208
```

You shoud wait a few more seconds until you see this message in the 
console:

```
kafka_1      | creating topics: stats:1:1
```

#### Manual Testing ####
In another terminal you can then run:
```bash
curl -X POST -H "Content-Type: application/json" localhost:8282/events -d '{"event" : "a test event"}'
```
output
```bash
{"status": "success"}
```

Then, to read the message from the queue:
```bash
curl localhost:8283/events
```

#### Scripted Testing ####

After starting the stack wich `docker-compose` go into the `tester` directory and run:

```bash
python tests.py
```
output
```bash
.....
----------------------------------------------------------------------
Ran 5 tests in 0.668s

OK
```

#### Kafkacat ####

If you want to test using `kafkacat` you'll need to jump through some minor hoops.
The issue is that Kafka advertises it's broker through Zookeeper using it's hostname
and in the docker composition the Kafka host is 'kafka'.  But you'll likely be trying
to run kafkacat locally against the exported 'localhost' port, which can't resolve the
advertised hostname of 'kafka'.  To fix this just add an entry to your `/etc/hosts` file
(or equivalent for windows).  eg:

```bash
127.0.0.1       localhost kafka
```

### Dev Mode ###

A quick note about starting with the `docker-compose.dev.yml` file.  This one will
mount the local directories to the containers to make dev easier, but if you've
already started the containers with the `docker-compose.yml` file there will be
a conflict.  

*Make sure you run `docker-compose down` before switching to dev mode.*

### Known Issues and Other things to worry about ###
There currently seems to be a bug in the python kafka consumer. It may be related to 
https://github.com/dpkp/kafka-python/issues/601 because I see the behavior described
there when I try to `seek_to_beginning`.  Right now, the consumer can't read the first
2 messages so the tests fail the first time but pass the second time they're run.

This is just a quick demo of kafka's pub sub using Python.  It's missing _a lot_ of 
stuff you would want if you were going to use this in a production environment.  Including:
* payload validation
* authentication and authorization
* improved error handling
* connection retries for kafka brokers
* managing partitions
* probably other things

