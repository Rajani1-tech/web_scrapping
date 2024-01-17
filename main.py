import tabula
import pandas as pd

def scraping_table_from_pdf(data_file_path):
    for i in range(1,6,1):
        invoice_data_list = tabula.read_pdf(data_file_path,pages=i)
        invoice_data_df = invoice_data_list[0]
        invoice_data_df = invoice_data_df.fillna(0)
        invoice_data_df = invoice_data_df.astype(str)
        new_headers = invoice_data_df.columns +"||"+ invoice_data_df.iloc[0] + '|| ' + invoice_data_df.iloc[1]
        invoice_data_df.columns = new_headers
        invoice_data_df = invoice_data_df.iloc[2:]
        new_invoice_data_df = pd.DataFrame(
            {
                col: invoice_data_df.iloc[i:i+3][col].str.cat(sep=' | ') for col in invoice_data_df.columns
            } for i in range(0, len(invoice_data_df), 3))
        if i == 1:
            new_invoice_data_df.to_csv(file_output_path, mode="w", index=False, header=True)
        else:
             new_invoice_data_df.to_csv(file_output_path, mode="a", index=False, header=False)
    return

def cleaned_function(new_invoice_data_df,file_output_path):
    new_invoice_data_df['property'] = new_invoice_data_df['Block/Lot/Qual||Cert Num Type|| Property Location'].str.split('|').str[1:]
    new_invoice_data_df['property'] = new_invoice_data_df['property'].apply(lambda x: ' '.join(x))
    new_invoice_data_df['property'] = new_invoice_data_df['property'].str.strip().str[9:]

    new_invoice_data_df['premium_price'] = new_invoice_data_df['Unnamed: 0||Check Cleared Date|| Premium/Percent'].str.split('|').str[2]
    new_invoice_data_df.loc[new_invoice_data_df['premium_price'].str[-1] == "%", 'premium_price'] = 0
    new_invoice_data_df['premium_price'] = new_invoice_data_df['premium_price'].str.replace(',', '')
    new_invoice_data_df['premium_price'] = new_invoice_data_df['premium_price'].astype(float)

    new_invoice_data_df['certificate'] = new_invoice_data_df['Prev Bal||Certificate|| Record Fee'].str.split('|').str[1]
    new_invoice_data_df['certificate'] = new_invoice_data_df['certificate'].str.replace(',', '')
    new_invoice_data_df['certificate'] = new_invoice_data_df['certificate'].astype(float)

    new_invoice_data_df['other_fee'] = new_invoice_data_df['Mun Transfer||Mun Adjust|| Other Fee'].str.split('|').str[2]
    new_invoice_data_df['other_fee'] = new_invoice_data_df['other_fee'].str.replace(',', '0')
    new_invoice_data_df['other_fee'] = new_invoice_data_df['other_fee'].str.replace(' ', '')
    new_invoice_data_df['other_fee'] = new_invoice_data_df['other_fee'].astype(float)

    new_invoice_data_df['subsq_fee'] = new_invoice_data_df['Unnamed: 1||Outside Subsq|| Assign Fee Foreclose Fee'].str.split('|').str[1]
    new_invoice_data_df['subsq_fee'] = new_invoice_data_df['subsq_fee'].str.replace(',', '')
    new_invoice_data_df['subsq_fee'] = new_invoice_data_df['subsq_fee'].astype(float)

    new_invoice_data_df['balance'] = new_invoice_data_df['Unnamed: 2||Balance|| 0'].str.split('|').str[1]
    new_invoice_data_df['balance'] = new_invoice_data_df['balance'].str.replace(',', '')
    new_invoice_data_df['balance'] = new_invoice_data_df['balance'].astype(float)

    new_invoice_data_df = new_invoice_data_df[["property","premium_price", "certificate","other_fee", "subsq_fee", "balance" ]]
    new_invoice_data_df.to_csv(file_output_path, mode="w", index=False, header=True)
    return

if __name__ == "__main__" :
    data_file_path = "input_data/10.23.23.pdf"
    file_output_path = "output_data/invoice_data.csv"
    df = scraping_table_from_pdf(data_file_path)
    df = pd.read_csv(file_output_path)
    file_output_path = "output_data/invoice_data_required.csv"
    cleaned_function(df,file_output_path)
