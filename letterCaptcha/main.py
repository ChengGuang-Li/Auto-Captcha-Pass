from DrissionPage import ChromiumPage
import requests
import base64
import ddddocr


def convertImg(img_url):
    response = requests.get(img_url)
    base64_image_string = base64.b64encode(response.content).decode("utf-8")
    return base64_image_string


def process_letter_captcha(img_url):
    ocr = ddddocr.DdddOcr(beta=True)
    res = ocr.classification(img_url)
    return res


def process_captcha():
    url = "https://www.examtopics.com/exams/amazon/aws-certified-solutions-architect-associate-saa-c03/view/3/"
    page = ChromiumPage()
    page.wait(4)
    page.get(url)  # get the page
    # scroll page
    ele = page.ele("x://div[@class='col-12 text-center mb-50']")
    page.scroll.to_see(ele)
    page.wait(2)
    # get the captcha img
    img_url = page.ele("x://img[@class='captcha']").attr("src")
    img_base64 = convertImg(img_url)
    captcha_res = process_letter_captcha(img_base64)  # get the results
    if captcha_res:
        # get the input area
        input_area = page.ele("x://input[@name='captcha_1']")
        input_area.input(captcha_res)
        submit_button = page.ele("x://button[@class='btn btn-primary']")
        submit_button.click()
        # check new page after successful captcha verification
        page.wait(2)
        page.scroll.to_half()


if __name__ == "__main__":
    process_captcha()
