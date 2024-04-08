from DrissionPage import ChromiumPage
from constants import CAPTCHA_TARGET_NAME_QUESTION_ID_MAPPING
import requests
import base64
from request import request_captcha, construct_task_data


def process_captcha():
    url = "https://www.google.com/recaptcha/api2/demo"
    page = ChromiumPage()
    page.get(url)  # get the page
    captcha_button = page.ele("x://div[@class='rc-anchor-content']")
    captcha_button.click()
    page.wait(1)
    # get the captcha iframe
    iframe = page.ele("x://*[contains(@title,'challenge')]")
    if iframe:
        print("captcha iframe found")
        # get the question  id
        question = iframe.ele("tag:strong").text
        question_id = CAPTCHA_TARGET_NAME_QUESTION_ID_MAPPING.get(question)
        # get the captcha img
        img = iframe.ele("tag:img").attr("src")
        img_base64 = convertImg(img)
        # get the pending click elements
        pending_click_elements = iframe.eles("tag:td")  # get the 9 element of imgs
        # create task data
        task_data = construct_task_data(img_base64, question_id)
        # request the capsolver
        res = request_captcha(task_data)
        if res and res.get("errorId") == 0:
            data_click = res["solution"]["objects"]
            # click elements
            if len(data_click) != 0:
                for i in range(len(data_click)):
                    click = data_click[i]
                    pending_click_elements[click].click()
                # verify button
                iframe.ele("x://*[contains(@class,'rc-button-default')]").click()

    else:
        print("captcha iframe not found")


def convertImg(img_url):
    response = requests.get(img_url)
    base64_image_string = base64.b64encode(response.content).decode("utf-8")
    return base64_image_string


if __name__ == "__main__":
    process_captcha()
