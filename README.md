## Raspberry PI System Information -> RabbitMQ
The scripts included connect to a RabbitMQ server and submit (some) system information. This could be scheduled through a system task (cron, Task Scheduler, etc.) in order to periodically report data to the message queue.

While simple, the intention is also such, to simply collect relevant information from a series of Raspberry Pis that I have and then store them into some data tool for later analysis (or a dashboard if I ever find time to get around to it).

Two primary files are included:

- `client.py` is the main purpose of the project and that's to publish data to a known MQ server 
- `server.py` is really just here as a placeholder for an eventual consumer