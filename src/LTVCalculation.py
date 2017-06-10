"""
Shutterflly challenge to Calculate Life time value of given customers to predict his future purchase power index
In this part of code we are gCalculate Life Time Value of Customer
Author: Rajesh Jaiswal
Dated: 10th June 2017
"""

from dateutil.parser import parse as date_parser
from dateutil import rrule

date_key_value = 'event_time'
order_key = 'ORDER'
visit_key_value = 'SITE_VISIT'
customer_key_value = 'CUSTOMER'
total_amount_kvalue = 'total_amount'


# This function will calculate number of weeks
def number_of_weeks(start, last):
    weeks_count = rrule.rrule(rrule.WEEKLY, dtstart=start, until=last)
    return weeks_count.count()


# This function create required data from input data
def create_datalist(file_path, events_data):
    loop_one = True
    with open(file_path) as f:
        for line in f.readlines():
            if loop_one:
                loop_one = False
                line_eval = line.strip()[1:-1]
            else:
                line_eval = line.strip()[:-1]
            ingest(line_eval, events_data)


# This function will create output file from result of ltv
def genarate_output(filename, fulldata):
    with open(filename, 'w') as f:
        for x in fulldata:
            f.write(x[0] + ', ' + str(x[1]) + '\n')


# This function will ingest data in to data list
def ingest(e, D):
    checkdata = eval(e)
    if date_key_value in checkdata:
        checkdata[date_key_value] = date_parser(checkdata[date_key_value])

    customer_id = checkdata['customer_id'] if checkdata['type'] != customer_key_value \
                  else checkdata['key']

    if customer_id not in D:
        # Generate new cutomer id vale
        D[customer_id] = [checkdata]
    else:
        # Addition of new customer
        D[customer_id].append(checkdata)


def topXSimpleLTVCustomers(x, D, display_details=False):
    """
     A simple LTV can be calculated using the following equation: 52(a) x t.
    Where a is the average customer value per week (customer expenditures per
    visit (USD) x number of site visits per week) and t is the average customer lifespan.
    The average lifespan for Shutterfly is 10 years.
    LTV = 52(a) x t
    """
    LTVs = []
    for customer_id in D:

        # Weekly visits      
        visitkey = visit_key_value if visit_key_value in [r['type'] for r in D[customer_id]] else 'ORDER'
        visit_date_timestamp = [r[date_key_value] for r in D[customer_id] if r['type'] == visitkey]

        # This part check customer purchase and visit time stamp
        if visit_date_timestamp and 'ORDER' in [r['type'] for r in D[customer_id]]:
            active_weeks = number_of_weeks(min(visit_date_timestamp), max(visit_date_timestamp))

            # Customer bill for each week purchase
            order_data = [(r['key'], r['verb'], r['event_time'], float(r[total_amount_kvalue].split()[0]))
                           for r in D[customer_id] if r['type'] == order_key]
            order_amounts_by_id = {}
            
            # Check for order updates
            for k, verb, event_timestamp, amount in order_data:
                if k not in order_amounts_by_id:
                    order_amounts_by_id[k] = (event_timestamp, amount)
                else:
                    if event_timestamp > order_amounts_by_id[k][0]:
                        # Replace amount if newer update exists
                        order_amounts_by_id[k] = (event_timestamp, amount)
            total_order_amounts = sum([order_amounts_by_id[k][1] for k in order_amounts_by_id])
            avg_revenue_per_week = float(total_order_amounts) / active_weeks

            # LTv here ve calculate LTV of considering life span of 10
            customer_lifespan = 10
            LTVs.append((customer_id, 52 * avg_revenue_per_week * customer_lifespan))
        else:
            # No ORDER events
            LTVs.append((customer_id, 0))

    LTVs.sort(reverse=True, key=lambda y: y[1])
    
    # This part of code print top x value of LTV
    if display_details:
        print "\n-------------TOP X Entries of LTV list------------------------------------"
        for ltv in LTVs[:x]:
                print "{}".format(ltv)
    return LTVs[:x]

# Main Thread to handle programm step by step            
if __name__ == '__main__':
    # Customer details list
    customer_details = {}
    # Is cutsomer details are right
    display_details = True
    # generate cutomer data from input file
    create_datalist("../input/input1.txt", customer_details)
    # Create output file and save it
    topX=topXSimpleLTVCustomers(10, customer_details, display_details)
    output_filepath = "../output/output.txt"
    # print required number of top 10 cutomers value
    genarate_output(output_filepath, topX)
    print "\n-------------------Data saved -----------------------------"