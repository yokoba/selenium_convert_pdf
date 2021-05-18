import json

from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time

DRIVER = "/home/admin/convert/venv/lib/python3.6/site-packages/chromedriver_binary/chromedriver"


def main():
    display = Display(visible=0, size=(1920 * 2, 1200 * 2))
    display.start()

    options = Options()

    appState = {
        "recentDestinations": [{"id": "Save as PDF", "origin": "local", "account": ""}],
        "selectedDestinationId": "Save as PDF",
        "version": 2,
        "isLandscapeEnabled": False,
        "pageSize": "A4",
        "isHeaderFooterEnabled": False,
        "isCssBackgroundEnabled": True,
    }

    prefs = {
        "printing.print_preview_sticky_settings.appState": json.dumps(appState),
        "savefile.default_directory": "/tmp",
    }

    options.add_experimental_option("prefs", prefs)
    options.add_argument("--kiosk-printing")

    driver = webdriver.Chrome(executable_path=DRIVER, options=options)

    driver.get("https://www.google.com/")

    try:
        WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located)
        print("PDF出力を開始")
        driver.save_screenshot("./screen_shot.png")
        driver.execute_script("window.print()")
        print("PDF変換完了")
    except Exception as e:
        print(e)
    finally:
        print("PDFのダウンロードを待機")
        time.sleep(10)
        print("ダウンロード完了、Seleniumを終了")
        driver.quit()


if __name__ == "__main__":
    main()
