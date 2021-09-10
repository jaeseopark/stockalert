![icon](icon/icon128.png "icon")

# stockalert

stockalert polls retailer APIs and/or scrapes their websites to detect product availabilities.

Currently supported:
* [Bestbuy Canada](https://bestbuy.ca)
* [MemoryExpress](https://memoryexpress.com)
* [CalDigit](https://shop.caldigit.com/us)

## Development

```bash
sam build
sam local invoke StockAlertFunction # TODO: mock SNS
```
