def test_api_get_1(playwright):
    request = playwright.request.new_context()
    response = request.get("https://jsonplaceholder.typicode.com/posts/1")

    assert response.status == 200
    json_response = response.json()
    print(json_response)
    assert json_response['id'] == 1

    request.dispose()
    print('Test completed')

