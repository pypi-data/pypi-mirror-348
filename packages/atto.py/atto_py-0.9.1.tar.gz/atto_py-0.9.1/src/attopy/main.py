from attopy import AttoClient
import httpx # for httpx.ReadTimeout

ADDRESS = 'atto://ad7z3jdoeqwayzpaiafizb5su6zc2fyvbeg2wq5t3yfj3q5iuprx23z437juk'
HASH = '8E99403D1FF449D8B523B5ECE7B35F917F0CD8FCE3B09195855F0F2A69BD164A'

with AttoClient('http://h:8080') as node:
    # ====================================================================
    #  Check how far behind or ahead our clock is compared to the server
    # ====================================================================
    print(f'The client is {node.instants()}.')
    print()

    # ====================================================================
    #             Get account details (balance, height, etc.)
    # ====================================================================
    #
    # AttoClient.account(account) returns an Account object.
    # Here, an atto:// address is passed, but a public key or Account object
    # would also be fine.
    print('Account {ADDRESS} summary:')
    account = node.account(ADDRESS)
    print(account)
    print()

    # ====================================================================
    #                        Stream account updates
    # ====================================================================
    # 
    # account.get() returns an up to date version of an account.
    #
    # account.stream() continuously yields account updates upon changes to the
    # balance or representative
    print('Waiting for account updates...')

    try:
        for update in account.stream(timeout=3):
        # Alternatively:
        #for update in node.account(ADDRESS, stream=True)
            account = update
            print(account)
    except httpx.ReadTimeout:
        print('No updates received within the last three seconds')
    print()

    # ====================================================================
    #             Stream an account's receivable transactions
    # ====================================================================
    #
    print('Waiting for account receivables...')

    try:
        for receivable in account.receivables(min_amount=10, timeout=3):
        # Alternatively:
#for update in node.receivables(ADDRESS, stream=True)
            print(receivable)
    except httpx.ReadTimeout:
        print('No more new receivables found within the last three seconds')
    print()

    # ====================================================================
    #  Stream an account's transaction entries in a certain height range
    # ====================================================================
    #
    # Account.entries() returns a generator that yields transaction entries.
    # from_ specifies the starting height, and to specifies the ending height.
    # from_ defaults to 1 and to defaults to effectively infinity.
    #
    # Here, next() returns the first yielded entry (the one matching the
    # starting height).
    print('The account\'s last transaction entry is:')

    latest_entry = next(account.entries(from_=account.height))
    ## Alternatively:
    ## latest_entry = next(node.entries(ADDRESS, from_=account.height)

    print(latest_entry)
    print()

    # ====================================================================
    #                             Transactions
    # ====================================================================
    #
    print('The corresponding signed transaction block is:')
    print(next(node.transaction(latest_entry.hash_, stream=True)))
    print()

    # ====================================================================
    #     Streaming the latest transactions and entries on the network
    # ====================================================================
    #
    print('Waiting for new transactions on the network...')
    try:
        for tx in node.transactions(timeout=15):
        # Alternatively:
        #for update in node.receivables(ADDRESS, stream=True)
            print(receivable)
    except httpx.ReadTimeout:
        print('No new transactions were published within the last fifteen '
              'seconds')
    print()

    print('Waiting for new entries on the network...')
    try:
        for entry in node.entries(timeout=15):
        # Alternatively:
        #for update in node.receivables(ADDRESS, stream=True)
            print(receivable)
    except httpx.ReadTimeout:
        print('No new entries were recorded within the last fifteen seconds')
    print()

    # ====================================================================
    #                      Summary and other methods
    # ====================================================================
    #
    # AttoClient.instants()
    # Get an object containing the time difference between the client and the
    # server; useful for calculating accurate timestamps when publishing
    # blocks.
    #
    # AttoClient.account(account)
    # Account.get()
    # Get an up to date version of an account.
    #
    # AttoClient.account(account, stream=True)
    # Account.stream()
    # Get every new version of an account.
    #
    # AttoClient.entry(hash, stream=True)
    # Entry.get()
    # Get a transaction entry by its hash. Will hang until the entry has been
    # confirmed by the network.
    #
    # AttoClient.transaction(hash, stream=True)
    # Transaction.get()
    # Get a transaction by its hash. Transactions lack some useful information
    # contained in entries.
    #
    # AttoClient.receivables(account, min_amount=1)
    # Account.receivables(min_amount=1)
    # Stream receivable transactions for an account.
    #
    # AttoClient.entries(account, from_, to_, stream=True)
    # Account.entries(from_, to_, stream=True)
    # Stream transaction entries for an account in a certain height range.
    # Additional arguments can be passed to httpx.Client.stream().iter_lines(),
    # such as a timeout in seconds.
    #
    # AttoClient.transactions(account, from_, to_, stream=True)
    # Account.transactions(from_, to_, stream=True)
    # Stream transactions for an account in a certain height range. Additional
    # arguments can be passed to httpx.Client.stream().iter_lines(), such as a
    # timeout in seconds.
    #
    # AttoClient.receivables(min_amount=1)
    # Stream receivable transactions for an account.
    #
    # AttoClient.entries(from_, to_, stream=True)
    # Stream transaction entries for an account in a certain height range.
    # Additional arguments can be passed to httpx.Client.stream().iter_lines(),
    # such as a timeout in seconds.
    #
    # AttoClient.transactions(from_, to_, stream=True)
    # Stream transactions for an account in a certain height range. Additional
    # arguments can be passed to httpx.Client.stream().iter_lines(), such as a
    # timeout in seconds.
