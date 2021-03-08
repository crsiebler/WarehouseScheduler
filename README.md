# WarehouseScheduler
A mini Python application that determines when to schedule processing an order with some stipulations.

The application is Dockerized using amancevice/pandas:1.2.3. A Makefile is provided for easily building the image and running the container.

## Installation

Use our Makefile to assist building the application. Run the command below (You may need sudo priviledges):

    make build

## Testing

Unit tests compare the output to expected results. To run the tests, execute the command below:

    make test

## Execution

To run the package, execute the command below:

    make run