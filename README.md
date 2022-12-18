# blockchain-transaction-status
This repository contains a Python script that uses the Blockcypher API to check the status of a Bitcoin transaction using a hash ID. The script can be used to monitor the progress of transactions and ensure that they are being processed correctly.

## Installation

`pip install -r requirements.txt`

## How to use
Edit blockchain_transaction_status.py:

```py
TOKEN = 'YOUR TOKEN'
```
This bot is made with reference to IST (UTC + 5:30). Change the following line according to your timezone:
```py
tzinfo=pytz.FixedOffset(-330)
```
eg: For New Zealand Standard Time (UTC + 12:00)
```py
tzinfo=pytz.FixedOffset(-720)
```

Run the program:

`python blockchain_transaction_status.py`

### Example
![Transaction Successful](https://user-images.githubusercontent.com/120903301/208303080-8ce38678-b82c-425c-989b-09cd801e0903.png)

![Confirmations < 6](https://user-images.githubusercontent.com/120903301/208303178-93093b59-acdf-4904-b5f5-97fff488b2fb.png)
