from pytrends.request import TrendReq
import pandas as pd
import matplotlib.pyplot as plt

# Initialize pytrends
pytrends = TrendReq(hl='en-US', tz=360)

# Define a broad initial list of websites to compare
websites_batches = [
    ["google.com", "youtube.com", "facebook.com", "tokopedia.com", "shopee.co.id"],
    ["instagram.com", "detik.com", "kompas.com", "tribunnews.com", "liputan6.com"],
    ["bukalapak.com", "whatsapp.com", "netflix.com"]
]

# Define the years you want to analyze
years = ['2021', '2022', '2023']

# Initialize an empty DataFrame to store results
all_data = pd.DataFrame()

# Fetch data for each batch of websites by year
for year in years:
    for websites in websites_batches:
        timeframe = f'{year}-01-01 {year}-12-31'
        pytrends.build_payload(websites, cat=0, timeframe=timeframe, geo='ID', gprop='')
        data = pytrends.interest_over_time()

        # Drop the 'isPartial' column if it exists
        if 'isPartial' in data.columns:
            data = data.drop(columns=['isPartial'])

        # Add a 'Year' column to the data
        data['Year'] = year
        
        # Append the data to the all_data DataFrame
        all_data = pd.concat([all_data, data], axis=0)

# Remove duplicate columns if they exist
all_data = all_data.loc[:, ~all_data.columns.duplicated()]

# Sum up the search interest by year for each website
yearly_data = all_data.groupby(['Year']).sum()

# Find the top 10 websites overall based on the sum over all years
top_10_websites = yearly_data.sum().sort_values(ascending=False).head(10).index

# Filter the yearly data to only include the top 10 websites
top_10_yearly_data = yearly_data[top_10_websites]

# Plot the data as a bar chart
top_10_yearly_data.plot(kind='bar', figsize=(14, 7))

plt.title('Relative Search Interest for Top 10 Websites in Indonesia (2021-2023)')
plt.xlabel('Year')
plt.ylabel('Search Interest')
plt.legend(title='Websites', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
plt.show()

