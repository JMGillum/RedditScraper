# RedditScraper
Scrapes subreddits and filters by flair or title


For pyperclip, if it doesn't work, run sudo apt-get install xclip. For more information see https://pypi.org/project/pyperclip/

Issues:

* scroll.py Tooltip class does not have proper spacing. It does not account for blank lines between rows
* Does not fully check that config is proper
* No command line options
* Doesn't handle banned, quarantined, private, or nonexistent subreddits
* Search creation UI is subpar
