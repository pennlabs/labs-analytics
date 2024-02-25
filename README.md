# Labs Analytics Engine

Labs Analytics Engine is an unified **asynchronous analytics engine** to track, monitor and store live analytics data across all Penn Labs products.

## Getting Started

### Dev Environment Setup

1. We maintain our `Python` packages and version using `Pipenv`. You can install it by:

```bash
pip install pipenv --user
```

2. Clone the Labs Analytics Engine repository

```bash
git clone git@github.com:pennlabs/labs-analytics.git
```

3. Install dependencies using `Pipenv`

```bash
pipenv install
```

### Setting up for local development

This guide details the steps to set up `Redis`, `Redis Insight`, `postgres` and `pgweb` instances using Docker, making it easy for development.

<<<<<<< HEAD
> [!NOTE]  
=======
> [NOTE]  
>>>>>>> origin/master
> Docker installed on your system. If Docker and Docker Compose is not installed, please follow the installation guide at [Docker's official documentation](https://docs.docker.com/get-docker/).

Run all the services by:

```bash
docker-compose up -d
```

Here's where you can find the services:

1. `postgres` can be found on it's default port `5432` with
   - username: `labs`
   - password: `analytics`
   - db: `lab-analytics`
2. `pgweb` is a web GUI to visualize the database, it can be accessed at `http://localhost:8002`
3. `redis` is exposed at it's default port `6379`
4. `Redis Insight` is the web GUI to visualize `redis`, it can be found at `http://localhost:8001`

<<<<<<< HEAD
=======
After ensuring that your .env file is properly configured, you can create the local database by running the following command:

```bash
pipenv run python src/database.py
```

>>>>>>> origin/master
😎 Happy Hacking!

### Development Guide

The structure of this project is setup based on [FastAPI Best Practices](https://github.com/zhanymkanov/fastapi-best-practices). We will try to adhere to it as much as possible, here are the most important conventions to follow. PRs that violate these rules may not be merged.

1. Excessively use `Pydantic` for data validation, validators stored in `schema.py`

   - The consistency of the schema is of utmost importance since the analytics engine must accommodate all labs products

   ```python
       from datetime import datetime
       from typing import Tuple

       from pydantic import BaseModel


       class Delivery(BaseModel):
           timestamp: datetime
           dimensions: Tuple[int, int]


       m = Delivery(timestamp='2020-01-02T03:04:05Z', dimensions=['10', '20'])
       print(repr(m.timestamp))
       #> datetime.datetime(2020, 1, 2, 3, 4, 5, tzinfo=TzInfo(UTC))
       print(m.dimensions)
       #> (10, 20)
   ```

2. Use `dependencies.py` to validate server side data
   - `Pydantic` can only validate the values from client input. Use dependencies to validate data against database constraints like email already exists, user not found, etc.
3. Migrations done through `Alembic`
   - Migration file name template `*date*_*slug*.py`, e.g. `2022-08-24_post_content_idx.py`
4. Follow the `REST`
   - Follow the REST API framework for naming routes and endpoints
5. Do not use `async` without `await`

   ```python
   #####################
   ### GOOD EXAMPLES ###
   #####################
   @router.get("/thread-ping")
   def good_ping():
       time.sleep(10) # I/O blocking operation for 10 seconds, but in another thread
       pong = service.get_pong()  # I/O blocking operation to get pong from DB, but in another thread

       return {"pong": pong}

   @router.get("/async-ping")
   async def ping():
       await asyncio.sleep(10) # non-blocking I/O operation
       pong = await service.async_get_pong()  # non-blocking I/O db call

       return {"pong": pong}


   #####################
   #### BAD EXAMPLE ####
   #####################
   @router.get("/terrible-ping")
   async def terrible_catastrophic_ping():
       time.sleep(10) # I/O blocking operation for 10 seconds
       pong = service.get_pong()  # I/O blocking operation to get pong from DB

       return {"pong": pong}
   ```

## Motivation

As the premiere hub for student resources at Penn, Penn Labs is dedicated to maintaining high-quality products to better the lives of university students. From office hours on OHQ to laundry updates on Penn Mobile, students use our products on a day-to-day basis and depend on our features to help them navigate through their everyday lives. With an eye for innovation, Labs wants to develop products for _all_ university students, with the guarantee that their lives will be better for it.

That being said, with big traffic comes even bigger latency issues. As the popularity of our products and features increased, so too did the number of incoming requests and, as a consequence, I/O delay. A clear-cut example of this was identified on Penn Clubs (detailed in [this](https://pennlabs.org/blog/false-promises) article), where one moment of heavy traffic overwhelmed our compute power and brought down the product.

This, unfortunately, is not the only instance of performance concerns in Labs products. For instance, Penn Mobile is currently bottlenecked by its API calls to university servers, which has severely impacted response times to mobile users. This, in addition to Penn Mobile's plan to create analytic calls (ex. tracking user clicks on a particular tab), can easily drive up I/O costs and incur a non-trivial waste of clock cycles. While the team is trying to solve this issue by implementing a software layer cache, it remains unclear whether this is enough to significantly reduce the runtime along the backend's critical path. Similar problems have also occurred in other products, leading to several product downtimes.

The solution that we propose is an **asynchronous analytics engine** to help offload some of the work done by our web servers, thereby reducing response times for students. This engine is intended to handle background features, such as analytic data.

With this engine, we can collect a multitude of data points — click and view data for Penn Mobile posts, number of site visits per club for Penn Clubs, and most popular course searches for Penn Courses — all without harming the response times of our web servers. The engine's asynchronous nature allows us to completely circumvent I/O delay when sending back responses, thus enabling us to speed up the backend's critical path.

Collecting this background data will provide many affordances for students. For example, the data can enable Penn Labs to advocate for data-supported student demands during university associate meetings. Moreover, the data can be utilized as measurement points to help our developers further tailor our products toward student needs.

## Features

- [MVP] REST API that can handle incoming requests from product frontends
  - Implemented as a thread-pool
- [MVP] Functions that support asynchronous database operations
  - Supports bulk operations and atomic transactions
  - Implementation can have a `TransactionQueue` class to lazily forward transactions to the database during non-peak hours.
- [MVP] Proper Authentication and Encryption
  - Similar to B2B, only Labs products should be able to access the engine
  - Handles retrieving a Python user from the request to the engine. This can be as simple as requiring requests to pass in a pennkey in the request body or a session-id in the request header.
- [MVP] Logs to record uncompleted, successful, and failed transactions
  - Important for debugging and fault tolerance against database crashes
  - Invariant: the server should still work even if the database doesn't!
- [Future] Programmer interface to enable existing products to interact with the engine
  - Written in DLA as an `AnalyticsClient` class

### Timeline

Ideally, the project should be completed by the end of Spring 2024 in preperation for `Labs Wrapped`. Following this, further optimizations and functionality can be made in subsequent school semesters.

### Ticket System

We will be using the Issues feature on GitHub to keep track of tickets for this project. We can also use Shortcut if the majority prefer that option.

### Testing

This project is specifically designed for performance and availability. As such, the test cases should reflect this. The project will contain stress tests to properly test handling large workloads efficiently. For each stress test, there should be a corresponding timeout to ensure quick response times.

### Project Members and Roles

Justin Zhang

Vincent Cai

Jefferson Ding

Jesse Zong

### Future Direction

This project will be the first of its kind in the Labs suite that unifies analytics accross all products. It will serve as the model for future Labs products that are particularly sensitive to latency and throughput.

As important as analytics are, and as interesting as performance-based programming is, our goal as a club should still be to develop **products** for students. Speed and availability are important, but they should not be the primary focus for a social-good-oriented club like Labs. Club members should enjoy the work that they are doing! But a large part of developing for Labs is the greater good that comes out of it — giving back with features that benefit the Penn community. To that end, if it is between creating a new feature or reducing response times by a quarter of a second, efficiency can wait.
