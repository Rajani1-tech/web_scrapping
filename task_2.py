import csv
from playwright.sync_api import sync_playwright
import time
import requests
from bs4 import BeautifulSoup

class Crawler:
    def __init__(self, record_type):
        columns = [
            "date",
            "record_number",
            "record_type",
            # "application_name",
            "status",
         
            "address",
            # "action",
            
            # "parcel_number",
            "violation_date",
            "code_section",
            'category',
            "description"
        ]
        with open('aca-prod.csv', mode='w', newline='') as file:
            self.csv_writer = csv.writer(file)
            self.csv_writer.writerow(columns)


        self.base_url = "https://aca-prod.accela.com/COSPRINGS/Cap/CapHome.aspx?module=Enforcement&TabName=Enforcement&TabList=Home%7C0%7CPolice%7C1%7CPlanning%7C2%7CPublicWorks%7C3%7CEnforcement%7C4%7CLicensing%7C5%7CStormWater%7C6%7CCurrentTabIndex%7C4"

        with sync_playwright() as p:
            self.browser = p.chromium.launch()
            self.page = self.browser.new_page()
            self.start_process(record_type)

    def start_process(self, record_type):
        self.page.goto(self.base_url)
        self.page.select_option(
            "select[name='ctl00$PlaceHolderMain$generalSearchForm$ddlGSPermitType']",
            value=record_type
        )
        time.sleep(2)

        search_button = self.page.query_selector("//a[contains(@id,'ctl00_PlaceHolderMain_btnNewSearch')]")
        search_button.click()
        time.sleep(3)
        
        while True:
            
      
            self.page.screenshot(path="result.png", full_page=True)
            tr_rows = self.page.query_selector_all("//table[contains(@class,'ACA_GridView ACA_Grid_Caption')]//tr")[3:-2]
            compare={0:"A",1:"B",2:"C",3:"D",4:"E",5:"F",6:"G",7:"H"}
          
            for each in tr_rows:
                try:
                    inner_data=0
                    data = {}
                    additional_data_final = []
                    details = each.query_selector_all("td")[1:]
        
                    first_page_data=[]
                    data["date"] = details[0].inner_text().strip()
                
                    data["record_number"] = details[1].inner_text().strip()
                    data["record_type"] = details[2].inner_text().strip()
                    # data["application_name"] = details[3].inner_text().strip()
                    # print(data['application_name'])
                    data["status"] = details[4].inner_text().strip()
                    # data["description"] = details[5].inner_text().strip()
                    data["address"] = details[6].inner_text().strip()
                    # data["action"] = details[7].inner_text().strip()
                 
                    link = details[1].query_selector("a").get_attribute("href")
                    first_page_data.append(data['date']) 
                    first_page_data.append(data['record_number'])
                    first_page_data.append(data['record_type'])
                    # first_page_data.append(data['application_name'] )
                    first_page_data.append(data['status'] )
                    # first_page_data.append(data['description'])
                    first_page_data.append(data['address'] )
                    # first_page_data.append(data['action'])
                 
                    print(first_page_data)
               
                    response = requests.get("https://aca-prod.accela.com" + link)
                
                    print("https://aca-prod.accela.com" + link)
                    soup = BeautifulSoup(response.content, "lxml")
                    data_div = soup.find('div', {'class': 'ACA_OC_PHPlumbingGroup'})
                    element_violation=soup.find_all('span', {'id': 'ctl00_PlaceHolderMain_PermitDetailList1_palParceList'})
                    row=[]
                    print(element_violation)               
                    if len(element_violation)==1:
                 
                        inner_data=1
                        labels = data_div.find_all('span', {'class': 'ACA_SmLabelBolder font11px'})

                        values = data_div.find_all('span', {'class': 'ACA_SmLabel ACA_SmLabel_FontSize'})
                        
                        violation_rows = soup.find_all('tr', {'id': 'trASITList'})
                        violation_status = soup.find('div', {'class': 'MoreDetail_ItemCol1'}, text='Violation Status:').find_next_sibling('div').string.strip()
                        violation_date = soup.find('div', {'class': 'MoreDetail_ItemCol1'}, text='Violation Date:').find_next_sibling('div').string.strip()
                        category = soup.find('div', {'class': 'MoreDetail_ItemCol1'}, text='Category:').find_next_sibling('div').string.strip()
                        code_section = soup.find('div', {'class': 'MoreDetail_ItemCol1'}, text='Code Section:').find_next_sibling('div').string.strip()
                        code_description = soup.find('div', {'class': 'MoreDetail_ItemCol1'}, text='Code Description:').find_next_sibling('div').string.strip()
                        appeal_section  = soup.find('div', {'class': 'MoreDetail_ItemCol1'}, text='Appeal Provisions:').find_next_sibling('div').string.strip()

                        if violation_status==None:
                            violation_status=" "
                        if violation_date is None:
                            violation_date=" "
                        if category is None:
                            violation_date=" "
                        if code_section is None:
                            code_section=" "
                        if code_description is None:
                            code_description=' '
                        if appeal_section is None:
                            appeal_section=' '
                        row.extend([violation_status, violation_date,category,code_description, code_section,appeal_section])

                        for row in violation_rows:
                            
                            violation_data = {}
                        
                    
                            violation_id=[]
                            violation_date=[]
                            category=[]
                            code_description=[]
                            elements = row.find_all('div', {'class': 'MoreDetail_ItemCol'})
                            
                            for j in range(0, len(elements), 2):
                                label = elements[j].find('span', {'class': 'ACA_SmLabelBolder font11px'}).text.strip()
                                value = elements[j + 1].find('span', {'class': 'ACA_SmLabel_FontSize'}).text.strip()
                            


                                if label=="Code Section:":
                                    violation_id.append(value)
                                if label=="Violation Date:":
                                    violation_date.append(value)
                                
                                if label=="Category:":
                                    category.append(value)
                                
                                if label=="Code Description:":
                                    code_description.append(value)
                          
                            
                            length=len(violation_id)
                            
                        
                            for i in range(0, length):
                            
                                additional_data=[]
                                additional_data.append(data['date']) 
                                additional_data.append(data['record_number'] +"-"+ compare[i])
                                additional_data.append(data['record_type'])
                        
                                additional_data.append(data['status'] )
                                additional_data.append(data['address'])
                                # additional_data.append(data['action'])
                              
                               
                                additional_data.append(violation_date[i])
                                additional_data.append(violation_id[i])
                                additional_data.append(category[i])
                                additional_data.append(code_description[i])
                                additional_data_final.append(additional_data)
                         
                         
                    # try:
                    #     data["parcel_number"] = soup.select_one(
                    #         "div.MoreDetail_ItemCol.MoreDetail_ItemCol1 div"
                    #     ).text
                    # except Exception:
                    #     data["parcel_number"] = None
                    
                    if inner_data==0:
                        with open(".csv", mode='a', newline='') as file:
                          
                            self.csv_writer = csv.writer(file)
                            self.csv_writer.writerow(first_page_data)
                    elif inner_data==1:
                        with open("aca-prod.csv", mode='a', newline='') as file:
                            self.csv_writer = csv.writer(file)
                      
                            for data_row in additional_data_final:
                              
                                self.csv_writer.writerow(data_row)
                    
                except:
                    print("Error")
                    pass

            pagination_elements = self.page.query_selector_all("//td[contains(@class,'aca_pagination_td aca_pagination_PrevNext')]")
            
            if len(pagination_elements) > 1:
                next_button = pagination_elements[1].query_selector("a")
            else:
                next_button = None

            if not next_button:
                break

            next_button.click()
            time.sleep(2)

if __name__ == "__main__":
    cw = Crawler("Enforcement Case")
