## Edwin Garcia
### Lewis University
### Distributed Computing Systems
### Week 6 Assignment 1 – Distributed Processing Using Messages

### CPSC-55500-02-FA16
### Manoj Bhat

#### Description

This is a brief narrative of the steps performed to integrate an Apache Avro application and perform messaging patterns based on ZeroMQ. 
This project is a derivative of Week 2 Assignment where an AVRO client/server application was created. This project expands into 2 Linux (Ubuntu 16.x) VM nodes where nodes perform either publish/subscribe and request/reply patterns (1.1). 

##### Files
1.	avro-gradeserver.py – Contains a publish socket and a request socket
2.	avro-gradeclient.py – Contains a subscribe socket
3.	student_write.py – Contains the AVRO application
4.	student_schema.avsc – AVRO schema file

##### Ports/Sockets
1.	Port 5560 – Publishes to subscribers when a new student is added.
2.	Port 5570 – Requests data when a student is created from student_write.py application.

Avro-gradeclient.py contains a subscribe socket listening on port 5560.

Operation
To operate the messaging patterns, all applications must be executed in the shell. This is done by using ssh to the 2 nodes (2.1). student_write.py and avro-gradeserver.py resides in node with IP address 10.0.0.12. avro-gradeclient.py resides in 10.0.0.17:
1.	python ./app/py/student_write.py – runs the AVRO application
2.	python ./app/py/avro-gradeserver.py {2} – runs the PUB and REQ sockets. An optional argument sets the sleep interval in seconds.
3.	python ./app/py/avro-gradeclient.py {Math} - runs the SUB socket. An optional argument sets the filter for the PUB/SUB pattern.

#### Conclusion

ZeroMQ is an eye opener for me. I ran into some errors that took me sometime to figure out. The key is to understand the basic concepts, particularly the way the patterns work. There are details in how the patterns work and you have to follow these concepts for it to work. Unfortunately, I did not find a viable debugger tool for the purpose. It is something I will need to explore.
I have also installed Apache ActiveMQ. It comes with a functional example that runs on node server. I elected to experiment with ZeroMQ as I feel it allows me to fully understand the concepts of how it works. ActiveMQ seems to wrap things into easier concepts but I prefer learning it the harder way. However, ZeroMQ is not a complicated concept. It is just something I am not familiar with and requires a little bit of learning curve.
I can see a few practical applications to ZeroMQ down the line. In the interim, I will continue to evaluate ZeroMQ and keep this in my toolbox.
