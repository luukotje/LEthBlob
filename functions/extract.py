import binwalk
import os

def extract_from_block(w3, block_number, address, check_address, archive):
    block = w3.eth.get_block(block_number)
    files_found = False
    for tx_hash in block.transactions:
        tx = w3.eth.get_transaction(tx_hash)
        if (not archive) or ('504b0304' in tx.input[2:]):
            if (not check_address) or (address == tx['from']):
                input_data = bytes.fromhex(tx.input[2:])
                file_name = str(block_number) + '_' + tx_hash.hex()
                f = open(file_name, 'wb')
                f.write(input_data)
                f.close()
                results = binwalk.scan(file_name, signature=True, quiet=True, dd='.*', extract=True, directory='extracted/')

                for module in results:
                    for result in module.results:
                        if result.file.path in module.extractor.output:
                            if result.offset in module.extractor.output[result.file.path].extracted:
                                file_count = len(module.extractor.output[result.file.path].extracted[result.offset].files)
                                if file_count > 0:
                                    print("Found %d file(s) in block %d, transaction %s" % (file_count, block_number, tx_hash.hex()))
                                    files_found =  True
                os.remove(file_name)
    return files_found



def extract_block_range(w3, begin, end, stop_when_found, address, check_address, archive):
    all_found = False
    for i in range(begin, end+1):
        found = extract_from_block(w3, i, address, check_address, archive)
        if found:
            all_found = True
            if stop_when_found:
                return all_found
    return all_found

def extract_transaction(w3, tx_hash):
    files_found = False
    tx = w3.eth.get_transaction(tx_hash)
    block_number = tx.blockNumber
    input_data = bytes.fromhex(tx.input[2:])
    file_name = str(block_number) + '_' + tx_hash
    f = open(file_name, 'wb')
    f.write(input_data)
    f.close()
    results = binwalk.scan(file_name, signature=True, quiet=True, dd='.*', extract=True, directory='extracted/')

    for module in results:
        for result in module.results:
            if result.file.path in module.extractor.output:
                if result.offset in module.extractor.output[result.file.path].extracted:
                    file_count = len(module.extractor.output[result.file.path].extracted[result.offset].files)
                    if file_count > 0:
                        print("Found %d file(s) in block %d, transaction %s" % (file_count, block_number, tx_hash))
                        files_found = True
    os.remove(file_name)
    return files_found

def get_transaction(w3, tx_hash):
    return w3.eth.get_transaction(tx_hash)