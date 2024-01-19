import csv
from playwright.sync_api import sync_playwright
import time, requests
from bs4 import BeautifulSoup

class CodeCompilance:
    def __init__(self, record_type):
        columns = [
            "Date",
            "Record Numbers",
            "Record Type",
            "Address",
            "status"
        ]
        # Open the CSV file and create the csv_writer once in the constructor
     

        self.root_url = "https://aca-oregon.accela.com"
        self.base_url = f"{self.root_url}/LANE_CO/Default.aspx"

        with sync_playwright() as p:
            self.browser = p.chromium.launch()
            self.page = self.browser.new_page()
            self.start_process(record_type)

    def start_process(self, record_type):
        url = self.root_url + "/LANE_CO/Cap/CapHome.aspx?module=CodeCompliance&TabName=CodeCompliance"
        self.page.goto(url)
        time.sleep(2)

        self.page.select_option(
            "select#ctl00_PlaceHolderMain_generalSearchForm_ddlGSPermitType",
            label=record_type
        )
        time.sleep(2)

        search = self.page.query_selector("//a[contains(@id, 'ctl00_PlaceHolderMain_btnNewSearch')]")
        search.click()

        while True:
            self.page.screenshot(path="result.png", full_page=True)
            tr_rows = self.page.query_selector_all("//table[contains(@id,'ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList')]//tr")[3:-2]

            for each in tr_rows:
                try:
                    data = {}
                    details = each.query_selector_all("td")[1:]

                    first_page_data = []
                    data["date"] = details[0].inner_text().strip()
                    data["record_number"] = details[1].inner_text().strip()
                    data["record_type"] = details[2].inner_text().strip()
                    data["status"] = details[4].inner_text().strip()
                    data["address"] = details[6].inner_text().strip()

                    link = details[1].query_selector("a").get_attribute("href")
                    first_page_data.append(data['date'])
                    first_page_data.append(data['record_number'])
                    first_page_data.append(data['record_type'])
                    first_page_data.append(data['status'])
                    first_page_data.append(data['address'])

                    #print(first_page_data)
                    with open('required_data.csv', mode='a', newline='') as file:  # 'a' to append to the file
                     csv_writer = csv.writer(file)
                    csv_writer.writerow(first_page_data)
                    file.close()


                    

                    response = requests.get("https://aca-prod.accela.com" + link)
                    #print("https://aca-prod.accela.com" + link)

                    soup = BeautifulSoup(response.content, "lxml")
                    

                except:
                    print("Error")
                pass

if __name__ == "__main__":
    c = CodeCompilance("Complaint")
