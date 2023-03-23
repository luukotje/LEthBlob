from datetime import datetime
import pytz

def get_block_date(w3, block_number):
    block = w3.eth.get_block(block_number)
    timestamp = block.timestamp
    return datetime.fromtimestamp(timestamp)

def get_last_block(w3):
    block = w3.eth.get_block('latest')
    number = block.number
    timestamp = block.timestamp
    return number, str(datetime.fromtimestamp(timestamp))


def search_block_by_timestamp(w3, target_timestamp, after):
    average_block_time = 15
    block = w3.eth.get_block('latest')
    number = block.number
    timestamp = block.timestamp

    if after:
        lower_limit = target_timestamp
        higher_limit = target_timestamp + 50
    else:
        lower_limit = target_timestamp - 50
        higher_limit = target_timestamp

    while timestamp > target_timestamp:
        decrease_blocks = int((timestamp - target_timestamp) / average_block_time)
        if decrease_blocks < 1:
            break

        number -= decrease_blocks
        block = w3.eth.get_block(number)

        timestamp = block.timestamp

    if timestamp < lower_limit:
        while timestamp < lower_limit:
            number += 1

            block = w3.eth.get_block(number)
            timestamp = block.timestamp

    if timestamp > higher_limit:
        while timestamp > lower_limit:
            number -= 1

            block = w3.eth.get_block(number)
            timestamp = block.timestamp

    return number, datetime.utcfromtimestamp(timestamp), timestamp


def search_block_by_date(w3, date, after):
    date = datetime.strptime(date, '%Y/%m/%d-%H:%M:%S')
    utc_date = date.replace(tzinfo=pytz.UTC)
    timestamp = utc_date.timestamp()
    return search_block_by_timestamp(w3, timestamp, after)

