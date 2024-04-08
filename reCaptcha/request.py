import requests
import os


def construct_task_data(image_url, question_id):
    task_data = {
        "type": "ReCaptchaV2Classification",
        "image": image_url,
        "question": question_id,
    }
    return task_data


# read env properties
def load_dotenv(dotenv_path=".env"):
    with open(dotenv_path) as f:
        for line in f:
            if line.strip() and not line.startswith("#"):
                key, value = line.strip().split("=", 1)
                os.environ[key] = value


def request_captcha(task):
    load_dotenv()
    data = {"clientKey": os.getenv("CLIENT_KEY")}
    data["task"] = task

    url = "https://api.capsolver.com/createTask"
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        # print response
        print("response content >>>:", response.json())
        return response.json()
    else:
        # print error msg
        print("Failed, error code >>> :", response.status_code)
        print("error msg >>> :", response.text)
        return None
