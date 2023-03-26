def get_address_by_transaction(w3, transaction):
    tx = w3.eth.get_transaction(transaction)
    return tx['from']

def get_transactions_by_address(w3, address):
    return w3.eth.get_transaction_count(address)

def search_transactions_by_address(w3, begin, end, address):
    transaction_found = False
    for i in range(begin, end + 1):
        block = w3.eth.get_block(i)
        for tx_hash in block.transactions:
            tx = w3.eth.get_transaction(tx_hash)

            if address == tx['from']:
                print('transaction:' + tx_hash.hex())
                transaction_found = True
    return transaction_found
