this is my in house library for interacting with Zimra's FDMS system 
# Fiscal Device Gateway API Client

This repository provides a Python client for interacting with the Fiscal Device Gateway API provided by ZIMRA. The client can be used to manage various operations related to fiscal devices, such as registering a device, fetching configurations, issuing certificates, and handling fiscal day operations.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Class Methods](#class-methods)
- [Contributing](#contributing)
- [License](#license)

## Installation

To use this client, clone the repository and install the necessary dependencies:

```bash
git clone https://github.com/lordskyzw/zimra.git
cd zimra
pip install -r requirements.txt
```

## Usage

You can use the `Device` class to interact with the Fiscal Device Gateway API. Below is an example of how to initialize the class and perform some operations.

### Example

```python
from zimra import Device

# Initialize the device in test mode
device = Device(
    device_id: str, 
    serialNo: str, 
    activationKey: str, 
    cert_path: str, 
    private_key_path:str, 
    test_mode:bool =True, 
    deviceModelName: str='Model123', 
    deviceModelVersion:str = '1.0',
    company_name:str ="Nexus"
)

# Open a fiscal day
fiscal_day_status = device.openDay(fiscalDayNo=102)
print(fiscal_day_status)
```


```python
# Submit a receipt
example_invoice = {
  "deviceID": 12345,
  "receiptType": "FISCALINVOICE",
  "receiptCurrency": "USD",
  "receiptCounter": 1,
  "receiptGlobalNo": 1,
  "invoiceNo": "mz-1",
  "receiptDate": datetime.now().strftime('%Y-%m-%dT%H:%M:%S'), #example: "2021-09-30T12:00:00",
  "receiptLines": [
    {"item_name": "0percent_item",
      "tax_percent": 0.00,
      "quantity": 1,
      "unit_price": 10.00
    },
    {"item_name": "15percent_item2",
      "tax_percent": 15.00,
      "quantity": 1,
      "unit_price": 20.00
    }
  ],
  "receiptPayments":[{
    "moneyTypeCode": 0,
    "paymentAmount": 30.00
    }]
}

receipt = device.prepareReceipt(example_invoice) # this method does all the heavy lifting for you

receipt_status = device.submitReceipt(receipt_data) # this method submits the receipt to the fiscal device management system
print(receipt_status)
```

## Class Methods

### `__init__(self, test_mode=False, *args)`

Initializes the Device class. 

- `test_mode`: Boolean to specify whether to use the test environment or production environment.

### `register(self)`

Registers the device.

### `verifyTaxpayerInformation(self)`

Verifies the taxpayer information associated with the device.

### `getConfig(self)`

Fetches the device configuration and updates the device attributes.

### `issueCertificate(self)`

Issues a certificate for the device.

### `getStatus(self)`

Gets the current status of the device.

### `openDay(self, fiscalDayNo, fiscalDayOpened=None)`

Opens a fiscal day.

### `prepareReceipt(self, receiptData)`

Prepares a receipt to be submitted to the fiscal device management system.
It calculates the taxes and formats them in the required format
It signs the receipt as well using the private key provided

### `submitReceipt(self, receiptData)`

Submits a receipt to the fiscal device gateway.

### `closeDay(self)`

Closes the fiscal day.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any changes.
This project is still in development and there are many features that can be added to make work simpler for front end developers

## License

This project is licensed under the MIT License. See the LICENSE file for details.
