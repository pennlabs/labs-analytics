# Labs Analytics Engine

## Motivation

As the premiere hub for student resources at Penn, Penn Labs is dedicated to maintaining high-quality products to better the lives of university students. From office hours on OHQ to laundry updates on Penn Mobile, students use our products on a day-to-day basis and depend on our features to help navigate through their everyday lives. With an eye for innovation, Labs wants to develop products for _all_ university students, with the guarantee that their lives will be better for it.

That being said, with big traffic comes even bigger latency issues. As the popularity of our products and features increased, so too did the number of incoming requests and, as a consequence, I/O delay. A clear-cut example of this was identified on Penn Clubs (detailed in [this](https://pennlabs.org/blog/false-promises) article), where one moment of heavy traffic overwhelmed our compute power and brought down the product.

This, unfortunately, is not the only instance of performance concerns in Labs products. For instance, Penn Mobile is currently bottlenecked by its API calls to university servers, which has severely impacted response times to mobile users. This, in addition to Penn Mobile's plan to create analytic calls (ex. tracking user clicks on a particular tab), can easily drive up I/O costs and incur a non-trivial waste of clock cycles. While the team is trying to solve this issue by implementing a software layer cache, it remains unclear whether this is enough to significantly reduce the runtime along the backend's critical path. Similar problems have also occurred in other products, leading to several product downtimes.

The solution that we propose is an **asynchronous analytics engine** to help offload some of the work done by our web servers, thereby reducing response times for students. This engine is intended to handle background features, such as analytic data.

With this engine, we can collect a multitude of data points — click and view data for Penn Mobile posts, number of site visits per club for Penn Clubs, and most popular course searches for Penn Courses — all without harming the response times of our web servers. The engine's asynchronous nature allows us to completely circumvent I/O delay when sending back responses, thus enabling us to speed up the backend's critical path.

Collecting this background data will provide many affordances for students. For example, the data can enable Penn Labs to advocate for data-supported student demands during university associate meetings. Moreover, the data can be utilized as measurement points to help our developers further tailor our products toward student needs.

## Initial Planning

## Development

