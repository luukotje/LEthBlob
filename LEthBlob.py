import typer
import functions.date as date
import functions.extract as extract
import functions.addresses as addresses
from web3 import Web3
from web3.middleware import geth_poa_middleware
from colorama import init as colorama_init
from colorama import Fore
from pyfiglet import figlet_format

app = typer.Typer()

def initialise_w3(host, port):
    w3 = Web3(Web3.HTTPProvider(host + ':' + str(port)))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    if (not w3.is_connected()):
        print(f'{Fore.RED}Failed to connect to server please check your host and port{Fore.RESET}')
        exit()

    return w3


@app.command()
def get_date_of_block(
        block: int,
        host: str = typer.Option('http://localhost', help='Set the host of the web3 provider'),
        port: int = typer.Option(8545, help='Set the host of the web3 provider')
):
    w = initialise_w3(host, port)
    try:
        print('date: ' + str(date.get_block_date(w, block)))
    except:
        print(f'{Fore.RED}Unable to find the provided block{Fore.RESET}')


@app.command()
def get_last_block(
        host: str = typer.Option('http://localhost', help='Set the host of the web3 provider'),
        port: int = typer.Option(8545, help='Set the host of the web3 provider')
):
    w = initialise_w3(host, port)

    last_block, str_date = date.get_last_block(w)
    print(f'last_block: {last_block}, published at: {str_date} ')


@app.command()
def search_block_by_timestamp(
        timestamp: int,
        after: bool = typer.Option(False,
                                   help='If set it will search for the closest timestamp after the given timestamp'),
        host: str = typer.Option('http://localhost', help='Set the host of the web3 provider'),
        port: int = typer.Option(8545, help='Set the host of the web3 provider')
):
    w = initialise_w3(host, port)

    try:
        block_number, found_date, timestamp = date.search_block_by_timestamp(w, timestamp, after)
        print(f'block number: {block_number}, date: {found_date}, timestamp: {timestamp} ')
    except:
        print(f'{Fore.RED}Unable to find a block for the given timestamp{Fore.RESET}')


@app.command()
def search_block_by_date(
        input_date: str = typer.Argument(default="", help='Date format: yyyy/mm/dd-hh:mm:ss'),
        after: bool = typer.Option(False,
                                   help='If set it will search for the closest timestamp after the given timestamp'),
        host: str = typer.Option('http://localhost', help='Set the host of the web3 provider'),
        port: int = typer.Option(8545, help='Set the host of the web3 provider')
):
    w = initialise_w3(host, port)

    try:
        block_number, found_date, timestamp = date.search_block_by_date(w, input_date, after)
        print(f'block number: {block_number}, date: {found_date}, timestamp: {timestamp} ')
    except:
        print(f'{Fore.RED}Unable to find a block for the given date{Fore.RESET}')


@app.command()
def extract_block(
        block: int,
        address: str = typer.Option('', help='If set it will only search for files sent by the given address'),
        archive: bool = typer.Option(False, help='If set the program will extract archives'),
        host: str = typer.Option('http://localhost', help='Set the host of the web3 provider'),
        port: int = typer.Option(8545, help='Set the host of the web3 provider')
):
    w = initialise_w3(host, port)

    last_block, _ = date.get_last_block(w)
    check_address = False

    if block > last_block:
        print(f'{Fore.RED}The provided block does not exist{Fore.RESET}')
        return

    if address != "":
        check_address = True
        if len(address) != 42:
            print(f'{Fore.RED}An incorrect address is provided{Fore.RESET}')
            return

    try:
        found = extract.extract_from_block(w, block, address, check_address, archive)
        if found:
            print(f'{Fore.GREEN}Files are located in the extracted folder{Fore.RESET}')
        else:
            print(f'{Fore.GREEN}No files are found during the scan{Fore.RESET}')
    except:
        print(f'{Fore.RED}Something went wrong during extraction{Fore.RESET}')


@app.command()
def extract_block_range(
        begin: int,
        end: int,
        address: str = typer.Option('', help='If set it will only search for files sent by the given address'),
        stop_at_found: bool = typer.Option(False, help='If set the program will stop after it found one block containing data'),
        archive: bool = typer.Option(False, help='If set the program will extract archives'),
        host: str = typer.Option('http://localhost', help='Set the host of the web3 provider'),
        port: int = typer.Option(8545, help='Set the host of the web3 provider')
):
    w = initialise_w3(host, port)

    last_block, _ = date.get_last_block(w)
    check_address = False

    if end > last_block:
        print(f'{Fore.RED}The ending block does not exist{Fore.RESET}')
        return

    if address != "":
        check_address = True
        if len(address) != 42:
            print(f'{Fore.RED}An incorrect address is provided{Fore.RESET}')
            return

    if begin >= end:
        print(f'{Fore.RED}The ending block must be larger than the beginning block{Fore.RESET}')
        return
    try:
        found = extract.extract_block_range(w, begin, end, stop_at_found, address, check_address, archive)
        if found:
            print(f'{Fore.GREEN}Files are located in the extracted folder{Fore.RESET}')
        else:
            print(f'{Fore.GREEN}No files are found during the scan{Fore.RESET}')
    except:
        print(f'{Fore.RED}Something went wrong during extraction{Fore.RESET}')


@app.command()
def get_address_by_transaction(
        transaction: str,
        host: str = typer.Option('http://localhost', help='Set the host of the web3 provider'),
        port: int = typer.Option(8545, help='Set the host of the web3 provider')
):
    w = initialise_w3(host, port)

    if len(transaction) != 66:
        print(f'{Fore.RED}An incorrect transaction is provided{Fore.RESET}')
        return

    try:
        addres = addresses.get_address_by_transaction(w, transaction)
        print('address: ' + addres)
    except:
        print(f'{Fore.RED}Unable to process transaction{Fore.RESET}')


@app.command()
def get_transactions_by_address(
        address: str,
        host: str = typer.Option('http://localhost', help='Set the host of the web3 provider'),
        port: int = typer.Option(8545, help='Set the host of the web3 provider')
):
    w = initialise_w3(host, port)

    if len(address) != 42:
        print(f'{Fore.RED}An incorrect address is provided{Fore.RESET}')
        return

    try:
        transactions = addresses.get_transactions_by_address(w, address)
        print('transactions: ' + str(transactions))
    except:
        print(f'{Fore.RED}Unable to process address{Fore.RESET}')


@app.command()
def extract_date_range(
        begin_date: str = typer.Argument(default="", help='Date format: yyyy/mm/dd-hh:mm:ss'),
        end_date: str = typer.Argument(default="", help='Date format: yyyy/mm/dd-hh:mm:ss'),
        address: str = typer.Option('', help='If set it will only search for files sent by the given address'),
        stop_at_found: bool = typer.Option(False, help='If set the program will stop after it found one block containing data'),
        archive: bool = typer.Option(False, help='If set the program will extract archives'),
        host: str = typer.Option('http://localhost', help='Set the host of the web3 provider'),
        port: int = typer.Option(8545, help='Set the host of the web3 provider')
):
    w = initialise_w3(host, port)

    last_block, _ = date.get_last_block(w)
    check_address = False

    try:
        begin, _, _ = date.search_block_by_date(w, begin_date, False)
    except:
        print(f'{Fore.RED}Unable to find a block for the begin date{Fore.RESET}')
        return

    try:
        end, _, _ = date.search_block_by_date(w, end_date, False)
    except:
        print(f'{Fore.RED}Unable to find a block for the end date{Fore.RESET}')
        return

    if end > last_block:
        print(f'{Fore.RED}The ending block does not exist{Fore.RESET}')
        return

    if address != "":
        check_address = True
        if len(address) != 42:
            print(f'{Fore.RED}An incorrect address is provided{Fore.RESET}')
            return

    if begin >= end:
        print(f'{Fore.RED}The ending block must be larger than the beginning block{Fore.RESET}')
        return
    try:
        found = extract.extract_block_range(w, begin, end, stop_at_found, address, check_address, archive)
        if found:
            print(f'{Fore.GREEN}Files are located in the extracted folder{Fore.RESET}')
        else:
            print(f'{Fore.GREEN}No files are found during the scan{Fore.RESET}')
    except:
        print(f'{Fore.RED}Something went wrong during extraction{Fore.RESET}')


@app.command()
def extract_timestamp_range(
        begin_timestamp: int,
        end_timestamp: int,
        address: str = typer.Option('', help='If set it will only search for files sent by the given address'),
        stop_at_found: bool = typer.Option(False, help='If set the program will stop after it found one block containing data'),
        archive: bool = typer.Option(False, help='If set the program will extract archives'),
        host: str = typer.Option('http://localhost', help='Set the host of the web3 provider'),
        port: int = typer.Option(8545, help='Set the host of the web3 provider')
):
    w = initialise_w3(host, port)

    check_address = False

    try:
        begin, _, _ = date.search_block_by_timestamp(w, begin_timestamp, False)
    except:
        print(f'{Fore.RED}Unable to find a block for the begin timestamp{Fore.RESET}')
        return

    try:
        end, _, _ = date.search_block_by_timestamp(w, end_timestamp, False)
    except:
        print(f'{Fore.RED}Unable to find a block for the end timestamp{Fore.RESET}')
        return

    if address != "":
        check_address = True
        if len(address) != 42:
            print(f'{Fore.RED}An incorrect address is provided{Fore.RESET}')
            return

    if begin >= end:
        print(f'{Fore.RED}The ending block must be larger than the beginning block{Fore.RESET}')
        return
    try:
        found = extract.extract_block_range(w, begin, end, stop_at_found, address, check_address, archive)
        if found:
            print(f'{Fore.GREEN}Files are located in the extracted folder{Fore.RESET}')
        else:
            print(f'{Fore.GREEN}No files are found during the scan{Fore.RESET}')
    except:
        print(f'{Fore.RED}Something went wrong during extraction{Fore.RESET}')


@app.command()
def search_transactions(
        begin: int,
        end: int,
        address: str,
        host: str = typer.Option('http://localhost', help='Set the host of the web3 provider'),
        port: int = typer.Option(8545, help='Set the host of the web3 provider')
):
    w = initialise_w3(host, port)

    last_block, _ = date.get_last_block(w)

    if end > last_block:
        print(f'{Fore.RED}The ending block does not exist{Fore.RESET}')
        return

    if len(address) != 42:
        print(f'{Fore.RED}An incorrect address is provided{Fore.RESET}')
        return

    if begin >= end:
        print(f'{Fore.RED}The ending block must be larger than the beginning block{Fore.RESET}')
        return
    try:
        found = addresses.search_transactions_by_address(w, begin, end, address)
        if found:
            print(f'{Fore.GREEN}Completed search{Fore.RESET}')
        else:
            print(f'{Fore.GREEN}No transactions found{Fore.RESET}')
    except:
        print(f'{Fore.RED}Something went wrong during search{Fore.RESET}')

@app.command()
def search_transactions_date(
        begin_date: str,
        end_date: str,
        address: str,
        host: str = typer.Option('http://localhost', help='Set the host of the web3 provider'),
        port: int = typer.Option(8545, help='Set the host of the web3 provider')
):
    w = initialise_w3(host, port)

    try:
        begin, _, _ = date.search_block_by_date(w, begin_date, False)
    except:
        print(f'{Fore.RED}Unable to find a block for the begin date{Fore.RESET}')
        return

    try:
        end, _, _ = date.search_block_by_date(w, end_date, False)
    except:
        print(f'{Fore.RED}Unable to find a block for the end date{Fore.RESET}')
        return


    if len(address) != 42:
        print(f'{Fore.RED}An incorrect address is provided{Fore.RESET}')
        return

    if (begin >= end):
        print(f'{Fore.RED}The ending block must be larger than the beginning block{Fore.RESET}')
        return
    try:
        found = addresses.search_transactions_by_address(w, begin, end, address)
        if found:
            print(f'{Fore.GREEN}Completed search{Fore.RESET}')
        else:
            print(f'{Fore.GREEN}No transactions found{Fore.RESET}')
    except:
        print(f'{Fore.RED}Something went wrong during search{Fore.RESET}')

@app.command()
def search_transactions_timestamp(
        begin_timestamp: int,
        end_timestamp: int,
        address: str,
        host: str = typer.Option('http://localhost', help='Set the host of the web3 provider'),
        port: int = typer.Option(8545, help='Set the host of the web3 provider')
):
    w = initialise_w3(host, port)

    last_block, _ = date.get_last_block(w)

    try:
        begin, _, _ = date.search_block_by_timestamp(w, begin_timestamp, False)
    except:
        print(f'{Fore.RED}Unable to find a block for the begin timestamp{Fore.RESET}')
        return

    try:
        end, _, _ = date.search_block_by_timestamp(w, end_timestamp, False)
    except:
        print(f'{Fore.RED}Unable to find a block for the end timestamp{Fore.RESET}')
        return

    if len(address) != 42:
        print(f'{Fore.RED}An incorrect address is provided{Fore.RESET}')
        return

    if (begin >= end):
        print(f'{Fore.RED}The ending block must be larger than the beginning block{Fore.RESET}')
        return
    try:
        found = addresses.search_transactions_by_address(w, begin, end, address)
        if found:
            print(f'{Fore.GREEN}Completed search{Fore.RESET}')
        else:
            print(f'{Fore.GREEN}No transactions found{Fore.RESET}')
    except:
        print(f'{Fore.RED}Something went wrong during search{Fore.RESET}')

@app.command()
def extract_transaction(
        transaction: str,
        host: str = typer.Option('http://localhost', help='Set the host of the web3 provider'),
        port: int = typer.Option(8545, help='Set the host of the web3 provider')
):
    w = initialise_w3(host, port)

    if len(transaction) != 66:
        print(f'{Fore.RED}An incorrect transaction is provided{Fore.RESET}')
        return

    try:
        found = extract.extract_transaction(w, transaction)
        if found:
            print(f'{Fore.GREEN}Completed extraction{Fore.RESET}')
        else:
            print(f'{Fore.GREEN}No files found{Fore.RESET}')
    except:
        print(f'{Fore.RED}Unable to process transaction{Fore.RESET}')

@app.command()
def show_transaction(
        transaction: str,
        host: str = typer.Option('http://localhost', help='Set the host of the web3 provider'),
        port: int = typer.Option(8545, help='Set the host of the web3 provider')
):
    w = initialise_w3(host, port)

    if len(transaction) != 66:
        print(f'{Fore.RED}An incorrect transaction is provided{Fore.RESET}')
        return

    try:
        print(extract.get_transaction(w, transaction))
    except:
        print(f'{Fore.RED}Unable to process transaction{Fore.RESET}')

if __name__ == "__main__":
    colorama_init()
    print(Fore.BLUE + figlet_format('LEthBL<>b', font='slant') + Fore.RESET)
    app()
