import requests


def test_generate_mc_question_api():
    try:
        response = requests.post('http://192.168.169.77:5000/generateMCQuestionAPI?context="Jack walked to the shop"&numberOptions=4')
        assert (response.status_code == 200)
        response.raise_for_status()
        # Code here will only run if the request is successful
    except requests.exceptions.HTTPError as errh:
        print(errh)
    except requests.exceptions.ConnectionError as errc:
        print(errc)
    except requests.exceptions.Timeout as errt:
        print(errt)
    except requests.exceptions.RequestException as err:
        print(err)


def test_generate_tf_question_api():
    try:
        response = requests.post(
            'http://192.168.169.77:5000/generateTFQuestionAPI?context="Jack walked to the shop"')
        assert (response.status_code == 200)
        response.raise_for_status()
        # Code here will only run if the request is successful
    except requests.exceptions.HTTPError as errh:
        print(errh)
    except requests.exceptions.ConnectionError as errc:
        print(errc)
    except requests.exceptions.Timeout as errt:
        print(errt)
    except requests.exceptions.RequestException as err:
        print(err)
