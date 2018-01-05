# figshare-recommender-etl
A Python script that ingests Figshare's API data and transforms it into data suitable for loading into a recommendation engine.
In our case, we save the recommendation data in Kafka but you can easily change this in ingest.py.

## Installation

First make sure you have your Python dependencies:

pip3 install kafka-python

Change your Kafka connection settings under kafka_output.py.  You may also want to change your app token in api.py.

## Running

Simply run the ingest.py file:

python3 ingest.py

You'll need to give the script access to write a small local file "bookmark.json" to keep track of ingestion over multiple runs.  Delete this file if you'd like to start again from scratch.
