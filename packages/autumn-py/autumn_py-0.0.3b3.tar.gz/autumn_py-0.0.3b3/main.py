from dotenv import load_dotenv

from autumn.customers import CreateCustomerParams

load_dotenv()
import os

import autumn

autumn.secret_key = "am_sk_test_MHFnpArNlruvDKa7mNScBJdVljWvMTCTDF41Xg0Zfi"


def main():

    # response = autumn.customers.create({
    #     "id": "123",
    #     "name": "John Doe",
    # })

    # print(response)

    # print(autumn.attach({
    #     "customer_id": "123",
    #     "product_id": "pro-example",
    # }))

    # print(autumn.customers.get(id="123"))
    # params = UpdateCustomerParams(name="John Yeo", email="john@example.com")
    # response = autumn.customers.update(
    #     id="123",
    #     params=params,
    # )

    # print(response)
    autumn.customers.create(CreateCustomerParams(
        id="123",
        name="John Doe",
    ))

    response = autumn.customers.delete(id="123")

    print(response)

    # response = autumn.customers.get(id="cus_123")
    # print(response)


if __name__ == "__main__":
    main()
