# Demonstrate DIY hashing implmenentation

import json
from collections import namedtuple
import time

TABLE_SIZE = 1009


# One bucket in a hash table
class Bucket:

    def __init__(self, key_str, val_str):
        self.key = key_str
        self.val = val_str

    def print_me(self):
        print("key=" + self.key + "," + "val=" + self.val)


# holds all the buckets
class Hash_table():

    def __init__(self, n_items):
        self.name = "My Hash Table"
        self.n_buckets = n_items
        self.bucket_list = [Bucket("", "") for i in range(self.n_buckets)]
        self.collisions = 0
        self.num_items = 0  # Track the number of items in the hash table

    def print_hash_table(self, start, limit):

        for i in range(start, start + limit):
            self.bucket_list[i].print_me()

    # This is the actual hashing function
    def compute_hash_bucket(self, key_str):
        hash_value = 0
        for char in key_str:
            hash_value = (hash_value * 31 + ord(char)) % self.n_buckets
        return hash_value

    def load_factor(self):
        return self.num_items / self.n_buckets

    # Resize the hash table
    def resize(self, new_size):
        old_buckets = self.bucket_list
        old_size = self.n_buckets

        self.n_buckets = new_size
        self.bucket_list = [Bucket("", "") for _ in range(self.n_buckets)]
        self.num_items = 0  # Reset the number of items

        # Re-insert items into the resized hash table
        for bucket in old_buckets:
            if bucket.key != "":
                self.insert(bucket.key, bucket.val)

    def insert(self, key_str, val_str):
        if self.load_factor() > 0.5:
            # Resize the hash table to double its current size
            new_size = self.n_buckets * 2
            self.resize(new_size)

            # Insert the key-value pair
        index = self.compute_hash_bucket(key_str)
        original_index = index

        while self.bucket_list[index].key != "":
            # If the key already exists, update the value
            if self.bucket_list[index].key == key_str:
                self.bucket_list[index].val = val_str
                return True

            # Move to the next index using linear probing
            index = (index + 1) % self.n_buckets

            # If we've looped back to the original index, the table is full
            if index == original_index:
                return False

            self.collisions += 1

        # Found an empty bucket, insert the key-value pair
        self.bucket_list[index] = Bucket(key_str, val_str)
        self.num_items += 1  # Increment the number of items
        return True

    def search_linear(self, key_str):
        index = self.compute_hash_bucket(key_str)
        original_index = index

        while self.bucket_list[index].key != "":
            if self.bucket_list[index].key == key_str:
                return self.bucket_list[index].val

            # Move to the next index using linear probing
            index = (index + 1) % self.n_buckets

            # If we've looped back to the original index or found an empty bucket,
            # the key is not in the table
            if index == original_index or self.bucket_list[index].key == "":
                return None

        # Key not found
        return None


# Convert json dictionary into a list of objects
def custom_json_decoder(c_name, inDict):
    createdClass = namedtuple(c_name, inDict.keys())(*inDict.values())
    return createdClass


# Load and parse the JSON files
# create a list of objects from the specified JSON file
def load_lynx_json(c_name, f_name):
    with open(f_name, 'r') as fp:
        # Load the JSON
        json_dict = json.load(fp)
        object_list = []
        for i in range(len(json_dict)):
            tmp = custom_json_decoder(c_name, json_dict[i])
            object_list.append(tmp)
        return object_list


def load_data_into_dictionary(file_name):
    with open(file_name, 'r') as fp:
        json_dict = json.load(fp)
        data_dict = {}
        for item in json_dict:
            key = item['code']  # Assuming 'code' is the key
            value = item['name']  # Assuming 'name' is the value
            data_dict[key] = value
        return data_dict


#
# main starts here
#
def main():
    # Load the stops from json
    # assuming you are using Lynx stops
    master_stops_list = load_lynx_json('Stops', "stops.json")

    # create the (initial) hash table
    the_hash_table = Hash_table(TABLE_SIZE)

    # hash the stops using stop_code as key and stop__name as the stored value
    successful_inserts = 0
    stops_processed = 0

    # get time in nanoseconds -- maybe OS-specific?
    t0 = time.perf_counter_ns()

    for this_stop in master_stops_list:
        stops_processed = stops_processed + 1
        if the_hash_table.insert(this_stop.code, this_stop.name) == True:
            successful_inserts = successful_inserts + 1

        if the_hash_table.load_factor() > 0.5:
            print("Hash table is more than 50% full. Resizing...")
            print("Old table size:", the_hash_table.n_buckets)
            the_hash_table.resize(the_hash_table.n_buckets * 2)
            print("New table size:", the_hash_table.n_buckets)
    t1 = time.perf_counter_ns() - t0
    print("elapsed ns = " + str(t1))

    print("stops_processed = " + str(stops_processed))
    print("successful_inserts = " + str(successful_inserts))
    print("collisions = " + str(the_hash_table.collisions))


    # Test search
    print("\nTesting Search:")
    search_keys = ["1277", "3456", "3051", "2248", "6483"]  # Example keys to search
    for key in search_keys:
        stop_name = the_hash_table.search_linear(key)
        if stop_name:
            print(f"Stop with code '{key}' found: {stop_name}")
        else:
            print(f"Stop with code '{key}' not found.")

        # Test loading data into dictionary
    start_time_dict = time.perf_counter()
    data_dictionary = load_data_into_dictionary("stops.json")
    end_time_dict = time.perf_counter()
    print("Time taken to load data into dictionary:", end_time_dict - start_time_dict)
    print("Number of items in the dictionary:", len(data_dictionary))
    print("First 5 items in the dictionary:", dict(list(data_dictionary.items())[:5]))


if __name__ == "__main__":
    main()
