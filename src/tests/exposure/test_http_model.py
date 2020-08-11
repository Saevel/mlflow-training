from python_http_client import Client


def test_model_via_http():

    # NOTE: Change this if you chose to expose the model on a different port
    client = Client(host='http://localhost:5050', request_headers={})

    request_headers = {"Content-Type": "application/json"}

    data = {"data": [
        [6.0, 2.2, 5.0, 1.5],
        [5.7, 2.9, 4.2, 1.3]
    ]}

    print("\nInput Data: " + repr(data))

    response = client.invocations.call.post(request_body=data,request_headers=request_headers)

    print(response.body)

    assert response.status_code == 200, "The request should be correctly processed by the model"

    # TODO: ADD ASSERTION FOR RESPONSE BODY
