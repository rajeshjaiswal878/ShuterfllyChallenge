"""
Shutterflly challenge to Calculate Life time value of given customers to predict his future purchase power index
In this part of code we are generating Fake date to build our model to Calculate Life Time Value of Customer
Author: Rajesh Jaiswal
Dated: 10th June 2017
"""
import random
import string
from datetime import datetime
from faker import Faker

# We are using Faker Package to generate dummy data for all data structures.
# Faker packaged replaced old dummy data creation package Factory


# This function will create Fake timestamp for a given purchase entry in(YY:MM:DD Hh:MM:SS) format
def date_gen(date_one):
    return date_one.strftime("%Y-%m-%d %H:%M:%S")


# This Function will generate random Cutomer ID for purchase entry
def customer_id_gen(n):
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in xrange(n))


# This Function will generate data as per the sample given in challenge n customers
def data_genaration(n_customers, n_events, filepath):
    fake = Faker()
    iteration_one = True
    list_all_event = ['CUSTOMER', 'SITE_VISIT', 'IMAGE', 'ORDER']

    with open(filepath, 'w') as f:
        # this for loop will create one customer entry    
        for _ in xrange(n_customers):
            cutomerid = customer_id_gen(12)
            n_cutomer_date = fake.date_time_this_decade()
            custmer_entry = { 'type': 'CUSTOMER', 'verb': 'NEW', 'key': cutomerid, 'last_name': fake.last_name(),
                'event_time': date_gen(n_cutomer_date), 'adr_city': fake.city(), 'adr_state': fake.state()}

            # Write customer entry into data set
            if iteration_one:
                f.write('[' + str(custmer_entry))
                iteration_one = False
            else:
                f.write(',\n' + str(custmer_entry))

            print "Customer entry #{}:\n{}".format(_, custmer_entry)

            # Create events
            for i in xrange(random.randint(0,n_events)):
                event_timestamp = fake.date_time_this_decade()
                type_of_event = list_all_event[random.randint(0, len(list_all_event)-1)]
                # create site visit data for given event
                if type_of_event == 'SITE_VISIT':
                    event = { 'type': type_of_event, 'verb': 'NEW', 'key': customer_id_gen(12),
                              'event_time': date_gen(event_timestamp), 'customer_id': cutomerid }
                # create image fake data of a given event
                elif type_of_event == 'IMAGE':
                    event = { 'type': type_of_event, 'verb': 'UPLOAD', 'key': customer_id_gen(12),
                              'event_time': date_gen(event_timestamp), 'customer_id': cutomerid }
                # create order fake data of given event
                elif type_of_event == 'ORDER':
                    order_id = customer_id_gen(8)
                    event = { 'type': type_of_event, 'verb': 'NEW', 'key': order_id,
                              'event_time': date_gen(event_timestamp), 'customer_id': cutomerid,
                              'total_amount': "{:.2f} USD".format(random.uniform(4, 500))}
                    f.write(',\n' + str(event))
                    print "\tEvent #{}:\n\t{}".format(i, event)
                    
                    # Randomly updated_order orders 0-2 times
                    for updated_order in xrange(random.randint(0, 2)):
                        event = {'type':type_of_event, 'verb':'UPDATE', 'key':order_id, 'customer_id':cutomerid,
                                 'event_time':  date_gen(fake.date_time_between_dates(event_timestamp, datetime.now())),
                                 'total_amount':"{:.2f} USD".format(random.uniform(4, 500))}
                        f.write(',\n' + str(event))
                        print "\t > Update #{}:\n\t   {}".format(updated_order, event)

                elif type_of_event == 'CUSTOMER':
                    event = { 'type': type_of_event, 'verb': 'UPDATE', 'key': cutomerid, 'adr_state': fake.state(),
                              'event_time': date_gen(fake.date_time_between_dates(n_cutomer_date, datetime.now()))}

                print "\tEvent #{}:\n\t{}".format(i, event)
                if type_of_event != 'ORDER':
                    f.write(',\n' + str(event))

        f.write(']')
        print "\n-------------Cutomer Purchase Entries--------------".format(n_customers, filepath)

# main function to load a program step by step
if __name__ == '__main__':
    # this number will decide number of entries in input dataset
    newCustomersCount = 1000
    # Random parameter to pick entry
    maxRandomEvent = 15
    # To store generated fake data to use in main program
    inputData = "../input/input.txt"
    # data_genaration function to write data in input text file
    data_genaration(newCustomersCount, maxRandomEvent, inputData)