import autumn

autumn.api_key = "am_sk_test_MHFnpArNlruvDKa7mNScBJdVljWvMTCTDF41Xg0Zfi"

CUS_ID = "123"


def test_delete_customer():
    params = autumn.CancelParams(
        customer_id=CUS_ID,
        product_id="1234567890",
        entity_id="1234567890",
    )
    result = autumn.cancel(params)


def test_create_customer():
    params = autumn.AttachParams(
        customer_id="1234567890",
        product_id="1234567890",
        entity_id="1234567890",
    )

    result = autumn.attach(params)
    print("Result: ", result)
