

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



body="" #empty body for the email

# Retrieve email credentials from environment variables
email_user = "Enter your sender email"
email_pass = "password"

# Define the recipient and subject
to_email = "Enter your reciever email"
subject = 'Your subject'


#########scraper#################

import requests
from bs4 import BeautifulSoup


# URL of the website to scrape
url = "https://www.australiancomputertraders.com.au/laptop-computers/laptops/?sort%5B0%5D%5Bfield%5D=price&sort%5B0%5D%5Border%5D=asc&pgnum=2"

# Send a GET request to the website
response = requests.get(url)
# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content of the webpage
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the container that holds the laptop information
    # This will vary depending on the website's structure, adjust the selectors accordingly
    #laptops = soup.find_all('div',class_='gaec-product')
    
    divs_with_data_listname = soup.find_all('div', attrs={'data-name': True,'data-price': True,'data-url': True})

    data_list = []
    
    for div in divs_with_data_listname:
  
        data_listname_value = div['data-name']
        data_price = float(div['data-price'])
        url = div['data-url']
        div_content = div.text.strip()
        
        data_list.append({
        'data_listname': data_listname_value,
        'data_price': data_price,
        'url': url,

        })
        
    sorted_data_list = sorted(data_list, key=lambda x: x['data_price'])
   
    # Print the sorted data
    
    for item in sorted_data_list:
        
        body+=f"\nProduct: {item['data_listname']} \n"
        body+=f"Price: {item['data_price']} AUD  \n"
        body+=f"Link: {item['url']}  \n"
        body+='-' * 120
        
        #print(f'Product: {data_listname_value}')
        #print(f'Price: {data_price}')
        #print('-' * 80)
    
    #print(body)
 
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")


##########email################



# Create the email content
msg = MIMEMultipart()
msg['From'] = email_user
msg['To'] = to_email
msg['Subject'] = subject


msg.attach(MIMEText(body, 'plain'))

# Set up the SMTP server and send the email
try:
    server = smtplib.SMTP('smtp.office365.com', 587)
    server.starttls()
    server.login(email_user, email_pass)
    text = msg.as_string()
    server.sendmail(email_user, to_email, text)
    print("Email sent successfully!")
except Exception as e:
    print(f"Failed to send email: {e}")
finally:
    server.quit()

    
