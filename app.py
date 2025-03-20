from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

app = Flask(__name__)

def get_instagram_video(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get(url)
        video_element = driver.find_element(By.TAG_NAME, "video")
        video_url = video_element.get_attribute("src")
        driver.quit()
        return video_url
    except Exception as e:
        driver.quit()
        return None

@app.route("/download", methods=["GET"])
def download_video():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    video_url = get_instagram_video(url)
    if video_url:
        return jsonify({"video_url": video_url})
    else:
        return jsonify({"error": "Could not fetch video"}), 500

if __name__ == "__main__":
    app.run(debug=True)
