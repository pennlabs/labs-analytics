# Labs Analytics Engine

## Motivation

As the premiere hub for student resources at Penn, Penn Labs is dedicated to maintaining high-quality products to better the lives of university students. From office hours on OHQ to laundry updates on Penn Mobile, students use our products on a day-to-day basis and depend on our features to help them navigate through their everyday lives. With an eye for innovation, Labs wants to develop products for _all_ university students, with the guarantee that their lives will be better for it.

That being said, with big traffic comes even bigger latency issues. As the popularity of our products and features increased, so too did the number of incoming requests and, as a consequence, I/O delay. A clear-cut example of this was identified on Penn Clubs (detailed in [this](https://pennlabs.org/blog/false-promises) article), where one moment of heavy traffic overwhelmed our compute power and brought down the product.

This, unfortunately, is not the only instance of performance concerns in Labs products. For instance, Penn Mobile is currently bottlenecked by its API calls to university servers, which has severely impacted response times to mobile users. This, in addition to Penn Mobile's plan to create analytic calls (ex. tracking user clicks on a particular tab), can easily drive up I/O costs and incur a non-trivial waste of clock cycles. While the team is trying to solve this issue by implementing a software layer cache, it remains unclear whether this is enough to significantly reduce the runtime along the backend's critical path. Similar problems have also occurred in other products, leading to several product downtimes.

The solution that we propose is an **asynchronous analytics engine** to help offload some of the work done by our web servers, thereby reducing response times for students. This engine is intended to handle background features, such as analytic data.

With this engine, we can collect a multitude of data points — click and view data for Penn Mobile posts, number of site visits per club for Penn Clubs, and most popular course searches for Penn Courses — all without harming the response times of our web servers. The engine's asynchronous nature allows us to completely circumvent I/O delay when sending back responses, thus enabling us to speed up the backend's critical path.

Collecting this background data will provide many affordances for students. For example, the data can enable Penn Labs to advocate for data-supported student demands during university associate meetings. Moreover, the data can be utilized as measurement points to help our developers further tailor our products toward student needs.

## Initial Planning

### Environment and Technologies
This will be a C++, performance-focused project. Since this application is not bottlenecked by I/O cost, unlike our other Django-based backends, we can now focus on CPU optimizations that will have a meaningful effect on response latency.

There are a few possible build tools that we can utilize, namely Bazel, CMake, SCons, and Ninja. For the sake of simplicity, we should choose Bazel as it seems to be the most user-friendly and the easiest to set up.

### Features
- [MVP] REST API that can handle incoming requests from product frontends
    - Implemented as a thread-pool
- [MVP] Functions that support asynchronous database operations
    - Supports bulk operations and atomic transactions
    - Implementation can have a `TransactionQueue` class to lazily forward transactions to the database during non-peak hours.
- [MVP] Proper Authentication and Encryption
    - Similar to B2B, only Labs products should be able to access the engine
    - Handles retrieving a Python user from the request to the C++ engine. This can be as simple as requiring requests to pass in a pennkey in the request body or a session-id in the request header.
- [MVP] Logs to record uncompleted, successful, and failed transactions
    - Important for debugging and fault tolerance against database crashes
    - Invariant: the server should still work even if the database doesn't!
- [Future] Programmer interface to enable existing products to interact with the engine
    - Written in DLA as an `AnalyticsClient` class

## Development

### Timeline
Ideally, the MVP for this project should be completed by the end of Summer 2023. Following this, further optimizations and functionality can be made in subsequent school semesters.

### Ticket System
We will be using the Issues feature on GitHub to keep track of tickets for this project. We can also use Shortcut if the majority prefer that option.

### Testing
This project is specifically designed for performance and availability. As such, the test cases should reflect this. The project will contain stress tests to properly test handling large workloads efficiently. For each stress test, there should be a corresponding timeout to ensure quick response times.

### Project Members and Roles
TBD
### Future Direction

This project will be the first of its kind in the Labs suite. It will serve as the model for future Labs products that are particularly sensitive to latency and throughput. As such, it is important to write maintainable code and adhere to proper C++ best practices.

While this project has gained the attention of many Labs members for its focus on performance and C++, we should be cautious when allocating resources to projects like these, especially in future semesters.

As important as analytics are, and as interesting as performance-based programming is, our goal as a club should still be to develop **products** for students. Speed and availability are important, but they should not be the primary focus for a social-good-oriented club like Labs. Club members should enjoy the work that they are doing! But a large part of developing for Labs is the greater good that comes out of it — giving back with features that benefit the Penn community. To that end, if it is between creating a new feature or reducing response times by a quarter of a second, efficiency can wait.

With that said, we should _not_ recruit new club members for solely C++ projects. Developing for social good is still the goal, and we want future classes to know this too! Labs newbies will have a primary product team to work with, where they can build front-facing features and learn first-class development practices. Moreover, if they are interested in performance-based projects like this, they are welcome to work on them in conjunction with their designated product.

# Setup

### Install Bazel
```
$ brew install bazel
```

### Install Make
```
$ brew install make
```

### Run Server
```
$ make all
```


### Recommendations
- Install the Bazel extension for syntax highlighting on BUILD files
- Read [this](https://bazel.build/start/cpp) documentation to get yourself familiar with Bazel project structure
