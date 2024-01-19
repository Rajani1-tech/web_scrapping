from playwright.sync import sync_playwright

url = "https://aca-oregon.accela.com/LANE_CO/Cap/CapHome.aspx?module=CodeCompliance&TabName=CodeCompliance&TabList=Home%7C0%7CPlanning%7C1%7CBuilding%7C2%7CCodeCompliance%7C3%7CCurrentTabIndex%7C3"
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = self.browser.newpage()
    start_process('Complaint')

def start_process(record_type):
    page.goto(url)
    page.select_option("select#ctl00_PlaceHolderMain_generalSearchForm_ddlGSPermitType", label=record_type)
    search_button = page.query_selector("//a[contains(@id,'ctl00_PlaceHolderMain_btnNewSearch')]")
    search_button.click()
    tr_rows = page.query_selector_all("//table[contains(@class,'ACA_GridView ACA_Grid_Caption')]//tr")[3:-2]
    print(tr_rows)
    
    
