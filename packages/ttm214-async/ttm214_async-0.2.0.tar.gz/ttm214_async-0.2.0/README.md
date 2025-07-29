# TTM214 Async


An asynchronous library for controlling TTM214 devices.
<br />
Communication uses the TOHO protocol


## Example

``` python
import asyncio

from ttm214_async import TTM214, ReadRequest, WriteRequest


async def main() -> None:
    comport = "COM3"
    address = 1

    # Initialize client
    client = TTM214(address, use_bcc=True)
    await client.open_port(comport)

    # Write request
    print(await client.query(WriteRequest("SV1", 100)))

    # Read request
    print(await client.query(ReadRequest("PV1")))
    print(await client.query(ReadRequest("SV1")))


if __name__ == "__main__":
    asyncio.run(main())


```