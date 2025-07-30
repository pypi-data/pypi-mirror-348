from dotenv import load_dotenv

load_dotenv()

from src.autumn.client import AttachParams
import src.autumn as autumn


def main():

    params = AttachParams(
        customer_id="123",
        product_id="lite",
    )

    result = autumn.attach(params)
    print("Result: ", result)

    # print("Checkout URL: ", result.checkout_url)


if __name__ == "__main__":
    main()
