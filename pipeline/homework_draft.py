'''
in terminal 1:
cd pipeline
docker-compose up

in terminal 2:
cd pipeline
docker build -t ny_taxi:homework .
docker run -it ny_taxi:homework

Question 1. What's the version of pip in the python:3.13 image?

Question 2. Given the docker-compose.yaml, what is the hostname and port that pgadmin should use to connect to the postgres database?

Question 3. For the trips in November 2025, how many trips had a trip_distance of less than or equal to 1 mile?

Question 4. Which was the pick up day with the longest trip distance? Only consider trips with trip_distance less than 100 miles.

Question 5. Which was the pickup zone with the largest total_amount (sum of all trips) on November 18th, 2025?

Question 6. For the passengers picked up in the zone named "East Harlem North" in November 2025, which was the drop off zone that had the largest tip?

Question 7. Which of the following sequences describes the Terraform workflow for: 1) Downloading plugins and setting up backend, 2) Generating and executing changes, 3) Removing all resources?
'''