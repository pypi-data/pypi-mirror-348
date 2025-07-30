from dotenv import load_dotenv

load_dotenv()

import autumn
from autumn import AttachParams


def main():

    params = AttachParams(
        customer_id="123",
        product_id="lite",
    )

    result = autumn.attach(params)

    print("Result: ", result)


if __name__ == "__main__":
    main()
