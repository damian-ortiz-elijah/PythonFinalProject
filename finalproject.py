
#I had to pip installa beautifulsoup libary through the termianl after i created a virtual enviroment 
from bs4 import BeautifulSoup
#In order to scrape websistes i neede to download the requests libary that allows us to pull the url that is entered by the user 
import requests
#this will help me schedule the web scraper  
import time
#still figuring out the saved file or data but this helps get accuarte time stamps for the file 
from datetime import datetime

# Function 1 srapes and returns keywords that match from the given url
def scrape_website(url, keywords):
    response = requests.get(url) # This pulls the url that was given using the requsts libary 
    soup = BeautifulSoup(response.text, 'html.parser')# This return the text from the url 
    # Extract all text from the page but cleans out of white space making it easier to read logs 
    text = soup.get_text(separator=' ', strip=True).lower()


    # Match keywords if any 
    found = []
    for word in keywords:# keeps looking for words until there isnt any more 
        if word.lower() in text:# If the word is in uppercase it converts it to lowercase 
            found.append(word)# If a keyword is found this will add it to the found list

    return found, text  # This function will return the matches from the keywords put in and the the full text 


# Function 2 this function will aks for the inputs regarding wait time how many times to scrape and the time it will wait to scrape again
def get_user_input ():
    print("Lets build your scraper:")
    name = input("Whats your name? ")  # personalization using inputs 
    url = input("Enter the URL you want to scrape: ") # Asking for the website you want to scrape 
    count = int(input("How many times should I scrape this site? "))
    wait_time = int(input("How many seconds do you want to wait in between scrapes"))
    
    # Asking for optional keywords to be put in a list 
    # This will ask for the key words in order to create a list of keywords
    keyword_input = input("Enter keywords to search use a comma to seperate or press enter to skip:")
    # If the user does input keywords sepertaed by commas it will automatically be put into list if skipped it will read as a emtpy list 
    keywords = keyword_input.split(",") if keyword_input else []
    
    print(f"Alright {name}, scraping will begin shortly...\n")
    return name, url, count, wait_time, keywords

# Function 3 this function logs the results of each web scrape into a text file
def log_results(scrape_num, url, matches, keywords, scraped_text):
    # Open or creates a file
    with open("scrape_results.txt", "a", encoding="utf-8") as file:
        
        #  This helps print the number of scrappes and the timetsamps of when it was scraped to track whne the crapes happen 
        file.write(f"\nScrape #{scrape_num} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # This logs the url that was scraped 
        file.write(f"URL: {url}\n")

        # This then checks for the keywords that the user put in if any 
        if keywords:
            # If any of the keywords were found in the page content strore them 
            if matches:
                file.write(f"Keywords found: {matches}\n")
            else:
                # If keywords were provided but not found this prints out to let the user know 
                file.write("No keywords found.\n")
        else:
            # If no keywords were provided it will notify the user
            file.write("No keywords were given.\n")

        # Add a preview of the scraped page content so the user knows what what scraped 
        file.write("Scraped Text Snippet:\n")
        file.write(scraped_text[:500] + "\n")  # Limits to only 500 characters 

        # Seperates using a visual line to seperate the scrape from the next one 
        file.write("-" * 40 + "\n")


# Main program 
def main():
    name, url, count, wait_time, keywords = get_user_input()
   # Starts a counter for how many times to scrape 
    i = 0
    # loop until we rach the amount of scrapes the user asked for
    while i < count:
        # Prints the amount of scrapes were on it will start at 1 instead of 0
        print(f"Scrape #{i+1}...")
        # Calls the function in order to scrape the website and url 
        matches = scrape_website(url, keywords)
        
        # Print results to the terminal 
        if keywords:
            if matches: # If the user eneterned keywods and they were found thgis will print out 
                print(f" Found these keywords: {matches}")
            else:    # If keywords were found and they were given this will print out 
                print(" No keywords found this time.")
        else:      # If no keyWords were given this will print out 
            print("No keywords given, just scraping the page...")

        # Log results to file
        log_results(i + 1, url, matches, keywords)

        i += 1 # Increases scrape count while also keeping track of scrape count 
        if i < count: # If more scrapes are sceheduled it will wait the time given before doing the next one 
            print(f"Waiting {wait_time} seconds before the next scrape...\n")
            time.sleep(wait_time) #Counter for the program to wait before it executes the program 

    print(f"\nThanks for using the scraper {name} Done scraping {count} time(s)")

# Actually runs the program its a special way/easier  way to execute the program 
if __name__ == "__main__":
    main()
