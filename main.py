import sys
import os
import pprint

import praw
import curses
import webbrowser
import configparser
import math


from termcolor import colored, cprint

import functions
import config
import search
import dump
import constants
import formatString
import scroll

if(config.client_id == "" or config.client_secret == "" or config.user_agent == ""):
    print("Either the client id, client secret, or user agent are not specified. Please enter these values in config.py")
    exit()

# Read-only instance
reddit_read_only = praw.Reddit(client_id=config.client_id,         # your client id
                               client_secret=config.client_secret,      # your client secret
                               user_agent=config.user_agent)        # your user agent

subs = config.subReddits
searchesPath = config.searches_file
numPostsPerSub = 5

desiredFlair = config.desiredFlair # Posts with at least one of these flairs will be kept
desiredTitle = config.desiredTitle # Posts with at least one of these titles will be kept
posts = []

postAgeLimit = 86400 * 2 # 2 days old

lowerAgeBound = 18
upperAgeBound = 23

numScraped = 0


# Gets the matching posts from the search
"""
for sub in subs:
    #print(f"{sub}:")
    subreddit = reddit_read_only.subreddit(sub)
    #pprint.pprint(vars(subreddit)) #prints all possible variables for subreddit


    currentTime = functions.currentTimestamp()
    for post in subreddit.new(limit = numPostsPerSub):
        numScraped += 1
        #print(post.subreddit_name_prefixed)
        needToSearchFlair = True;

        title = post.title
        for t in desiredTitle:
            if(title != None and t.lower() in title.lower()):
                # print(f"{colored(t,'red')} found in {title}")
                posts.append(post)
                needToSearchFlair = False;
                break

        if(needToSearchFlair):
            flair = post.link_flair_text
            for f in desiredFlair:
                if(flair != None and f.lower() in flair.lower()):
                    # print(f"{f} found in {flair}")
                    posts.append(post)
                    break


# Displays how many posts were searched through, and how many matched the criteria
print(f"Scraped {numScraped} post(s). Found {len(posts)} post(s) matching the criteria")

if (not posts): # If no posts were found matching the criteria
    
    # Lists all the flairs in desiredFlairs
    flairs = ""
    for flair in desiredFlair:
        flairs += flair + ", "
    flairs = flairs.removesuffix(", ")
    
    # Lists all the titles in desiredTitles
    titles = ""
    for title in desiredTitle:
        titles += title + ", "
    titles = titles.removesuffix(", ")

    # Prints information
    print(f"No posts were found containing the flairs: {flairs} or containing: {titles} in the title")
else:
    print()
    cprint("Posts matching filters:","yellow")
    
    currentSubreddit = ""
    ticker = 0
    for post in posts:
        if(post.subreddit_name_prefixed != currentSubreddit):
            currentSubreddit = post.subreddit_name_prefixed
            print()
            cprint(currentSubreddit,"green")
            print()
        ticker += 1
        print(f"{ticker}.")
        age = int(currentTime-post.created_utc)
        print(functions.enbox([post.title,post.link_flair_text,post.author.name,f"Created: {functions.formatAge(age)} ago"],80))
        # pprint.pprint(vars(post)) #prints all possible variables for post

"""

"""
while(True):
    response = input("Enter the number of a post above for more options: ")
    if(response.lower() == 'r'):
        print("Refresh command")
    else:
        try:
            response = int(response)
        except ValueError:
            print("Invalid input")
            continue

        if(response <= 0 or response > len(posts)):
            print("The value entered is out of bounds.")
            continue

        while(True):
            print("menu")
            menu = functions.getInput("Would you like to:\n1. Display post\n2. Copy post URL\n3. Display post URL\n4. Copy URL to message user",1,4,3)
            if(menu == -1):
                continue

            if(menu == 1):
                print(functions.enbox([posts[response-1].title,"%separator%",posts[response-1].selftext],80))
            elif(menu == 2):
                functions.copyToClipboard(posts[response-1].url)
            elif(menu == 3):
                print(posts[response-1].url)
            elif(menu == 4):
                print("Function to copy chat url")
            break

    break
"""




# Beginning of the curses window


#"""
# Initialization work
screen = curses.initscr()
curses.noecho() # Does not display what user types
curses.cbreak() # User does not have to press enter for the input buffer to be read
screen.keypad(True) # Converts keys like arrow keys to a specific value

minTermLines = 24
minTermCols = 80
if(curses.LINES < minTermLines or curses.COLS < minTermCols):
    curses.nocbreak(); screen.keypad(0); curses.echo()
    curses.endwin()
    print(f"The current terminal size {curses.LINES}x{curses.COLS} is too small. The minimum size supported is {minTermLines}x{minTermCols}")
    exit()

searches = []
try:
    searches = functions.getSearches(searchesPath)
except FileNotFoundError:
    searches = []

numPosts = len(posts)
postNum = 0
lineNum = 0
browseMode = True
choosingSearches = True
searchIndex = 0


page = scroll.ScrollingList(screen,[""])
toolTip = scroll.ToolTip(formatString.combineStrings("<-- Line 1 -- >","(press q to quit)",curses.COLS,0,curses.COLS-18))




      

try:
    
    

    while True:
        screen.clear()

        if(choosingSearches):
            if(searches):
                searchIndex = functions.getSearchNum(screen, searches)
                if(searchIndex == -1):
                    break
                choosingSearches = False
                
                currentTime = functions.currentTimestamp()
                searchTime = searches[searchIndex].lastSearchTime

                # If search has never been performed
                if(searchTime == None):
                    screen.clear()
                    screen.addstr(0,0,"This search has never been performed. Gathering posts from the last week.")
                    screen.addstr(1,0,"Press q to quit or any other key to continue")
                    screen.refresh()
                    char = screen.getch()  
                    if char == ord('q'):
                        break
                    searches[searchIndex].lastSearchTime = math.floor(functions.currentTimestamp() - constants.DAY * 7)

                # If search was last performed over a week ago
                elif(currentTime - searchTime > constants.DAY * 7):
                    screen.clear()
                    screen.addstr(0,0,f"This search was last performed {formatString.formatAge(currentTime-searchTime)} ago.")
                    screen.addstr(1,0,"Press q to quit,")
                    screen.addstr(2,0,"y to perform the search any ways,")
                    screen.addstr(3,0,"or n to perform search on posts from the last week")
                    screen.refresh()

                    char = screen.getch()  
                    if char == ord('q'):
                        break
                    elif not char == ord('y'):
                        searches[searchIndex].lastSearchTime = math.floor(functions.currentTimestamp() - constants.DAY * 7)
                
                time = math.floor(functions.currentTimestamp())
                posts = functions.performSearch(reddit_read_only,searches[searchIndex])
                headers = functions.getHeaders(posts)
                numPosts = len(posts)
                page.updateStrings(screen,headers,0,toolTip)
                searches[searchIndex].lastSearchTime = time
                dump.saveSearches(searches,searchesPath)

                #end of need to change
            else:
                screen.addstr(0,0,"No searches found. Press e to create a new search.")
                screen.addstr(1,0,"Alternatively, press q to exit, and edit the searches file")
                screen.addstr(2,0,f"The current searches file is {searchesPath}. Is this correct?")
                screen.addstr(3,0,"If not, edit the value of searches_file in config.py")

                char = screen.getch()  
                if char == ord('q'):
                    break

            # Clears screen after search choosing process
            screen.clear()
            screen.refresh()

        
        
        elif(not browseMode):
            functions.viewPost(posts[postNum],screen)
            browseMode = True

        else:
            ticker = 0

            toolTip.replace([formatString.combineStrings(f"<-- Line {lineNum + 1} -- >","(press q to quit)",80,0,curses.COLS-18)])
            for item in page.getLines():
                screen.addstr(ticker,0,f"{item}")
                ticker = ticker + 1
            
            
            screen.refresh()
            char = screen.getch()

            
            if char == ord('q'):
                break

            elif(char == curses.KEY_UP or char == ord('w')):
                lineNum = page.scrollUp()
            
            elif(char == curses.KEY_DOWN or char == ord('s')):
                lineNum = page.scrollDown()
     
            elif char == ord('e'):
                screen.addstr(curses.LINES-1,curses.COLS-18,"(press q to exit)")
                screen.addstr(curses.LINES-1,0,f"Enter a post number, then press enter: ")
                c = screen.getch() # Allows immediate exit if they press q
                if c == ord('q'):
                    continue

                # Otherwise update prompt
                screen.addstr(curses.LINES-1,0,"")
                screen.clrtoeol()
                screen.refresh()
                screen.addstr(curses.LINES-1,curses.COLS-18,"(enter q to exit)")
                screen.addstr(curses.LINES-1,0,f"Enter a post number, then press enter: ")

                # Display what they type, and require they press enter
                curses.echo()
                curses.nocbreak()
                curses.ungetch(c) # Adds the first character back to the buffer
                string = screen.getstr()

                # Undo displaying input and requiring enter be pressed
                curses.noecho()
                curses.cbreak()

                val = 0
                try:
                    val = int(string)
                except ValueError:
                    continue

                val -= 1
                if(val >= 0 and val < numPosts):
                    browseMode = False
                    postNum = val

            

finally:
    curses.nocbreak(); screen.keypad(0); curses.echo()
    curses.endwin()

#"""