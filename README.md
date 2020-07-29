# density-dpus

# Density API Homework Assignment

## Goal

The goal here is to create an API that can handle both historical and real-time people count requests from consumers.

## Context

Density DPUs (depth processing units) are mounted above doorways. The DPU sends a request to the API when a person passes underneath (+1 when towards the DPU, -1 when walking away from the DPU).

You are provided with a CSV file of raw events from a handful of DPUs, and a floorplan indicating DPUs, doorways, and spaces.

![space diagram](https://raw.githubusercontent.com/DensityCo/api-hw/trunk/space-diagram.png)


## Assignment

The task was to accomplish the following:

- Scaffold a database structure that includes spaces, doorways, and count data.

**I've included a logical data model diagram in doc/data_model. The SQL DDL file can be found under resources/sql/ddl.sql**

- Document how you would store and return real-time count for spaces.
- Document how you would store and return historical count for spaces.

**The REST endpoint for active counts would simply write a tuple of the form (space_positive, space_pos_count, space_negative, space_neg_count, timestamp)
to the Kafka queue. This queue would/could be partitioned by location_id to better serve some locations that had higher foot traffic
than others. The readers at the other end of the queue would re-sequence the messages arriving as much as possible 
(see: https://www.enterpriseintegrationpatterns.com/patterns/messaging/Resequencer.html) for each space_id (based on timestsamp) 
to mitigate out-of-orderness.** 

**Note that since DPU messages can in theory be delayed for as long as possible, in the interests of timely reporting it might not 
be possible to get a 100% accurate count at every point in time.**

**Once the messages are re-sequenced, they are written to another Kafka queue, and the readers from this queue read messages
up to a certain defined limit, and write them out to the SpacePersonCount time series database. This has the benefit of 
being able to write to the database in batches which should be more performant than writing individual rows. 
(I'm assuming one is available, such as TimeScaleDB). There may be other alternatives to this, such as Cassandra which has a 
notion of ordered keys. In that case we could explore encoding keys as tuples of the form (space_id, timestamp) with values as 
the counts, which would automatically give us ordered counts by time and space.**

**At the same time, the REST endpoint would update the current known counts for the related spaces on each side of the DPU
in a key-value store of some kind, such as Redis. Note that because of DPU messages arriving out of order, and no effort
being made at this stage to re-sequence them, these counts are at best a rough approximation of the true count.**

**Basically we're trying to strike a balance between accuracy vs timeliness of useful information.**

- Prototype an API endpoint that yields the current count of a given space at a given point in time.

**The REST API endpoints are in main.py. I used Flask to build it and added comments 
(but I should've used docstrings instead!) documenting each endpoint. I didn't flesh out each and every metadata endpoint 
but the general form should be the same for adding doorways, DPUs etc.**

- Describe the technologies you would use in production to handle this workload at scale (100,000 DPUs).

**Kafka for queueing, TimeScaleDB (an extension to PostGres) or Cassandra for historical counts for each space, 
PostGres or some other DB to store the metadata, Flask or Django or any Web framework to build the REST endpoints.** 

**Deployment could be on-prem or on the cloud, using Docker to containerize the individual components and perhaps something 
like Kubernetes to wire them all together.**

**If the load is heavy, we could probably have multiple instances of the web app being served behind a load balancer.**

Items to take into consideration:

- DPUs are sometimes moved from one doorway to another.
- DPUs sometimes send events out of order.
- DPUs don't always send data up in real-time. Network downtime and other events can cause delayed events.

## Deliverables

For delivery of this assignment:

- Database schema / SQL file.

The logical data model is in doc/data_model. SQL DDL files are in resources/sql/ddl.sql

- Prototype a Python application that yields the current count of a given space at a given point in time. For example, "what was the count at 3:34pm yesterday?"

**I've included some unimplemented REST endpoints for counts in main.py.**

- Focus on prototyping database query / API implementation and don't worry about best-practices with app structure.

**I've included an architecture diagram under doc/architecture.**

- Documentation on real-time and historical use-cases.

**See above.**

- Documentation on production technologies.

**See above.**

## Submission
Create a new repo using your Github account with a unique name and send us the final product (please do not fork or submit a PR to this repo).

