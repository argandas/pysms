# pysms
![Python package](https://github.com/argandas/pysms/workflows/Python%20package/badge.svg)

Python Code for sensing SMS using SIM900 modem

## Dependencies

In order to get all necessary Python modules, please execute the following command inside the repo folder:
```
$ pip install --upgrade pip
$ pip install -r requirements.txt
```

## Usage

To send an SMS execute `send_sms.py` with the following syntax:
```
$ python .\send_sms.py -a "your_phone_number" -m "message"
```

Optional argument `d` allows the user to debug the AT command traffic of the SIM module:
 ```
$ python .\send_sms.py -d -a "your_phone_number" -m "message"
```


