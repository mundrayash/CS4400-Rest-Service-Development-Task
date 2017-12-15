# CS4400-Rest-Service-Development-Task
Yash Mundra
Student No.: 16338461

This project computes the average cyclomatic complexity of all the python files in a GitHub repository. To calculate it     efficiently, a master and number of workers nodes are created. The code is written in python 3.0. Radon library is used.

Working: When the worker starts up, it requests work from the master. The master replies to the worker with an sha key. Then the worker computes the cyclomatic complexity of the python files and returns the average to the master. It again asks for more work. If no more work is left, the master replies with a work completed message and shuts down the workers node.

Result: The time to calculate the cyclomatic complexity was computed with different number of worker nodes (from 1 to 10). It was the highest with 1 worker and decreased gradually but after 5-6 worker nodes, the change was not much.

To start the program run the run.sh script.



