# Subdomain Takeover Automation
I made a simple subdomain takeover bot and run it for 1 month. It sent many notifications for a month, but all of them were invalid.
But it can still be improved and made really functional. <br />
In summary, I built a bot that searches for subdomain takeover vulnerabilities on all websites that are in bug bounty programs. <br />
I wrote a crontab command to run every 6 hours and it sends the domains it finds into the telegram channel.

![Subdomain Takeover](https://raw.githubusercontent.com/izzetemredemir/subdomain-takeover/main/ss.png)

## What is Subdomain Takeover?
> A subdomain takeover occurs when an attacker gains control over a subdomain of a target domain.
Simply, We somehow take over a forgotten subdomain.

[Subdomain Takeover: Basic](https://0xpatrik.com/subdomain-takeover-basics/)

#### Subdomain Takeover Steps
                
1. Find Target Domains
2. Find All Subdomains (Subdomain Enumeration)
3. Check The Each Subdomains for Takeover

#### 1.Find Target Domains:
 We need to find a list of all the target domains from all the public bug bounty programs.<br />
 This repo provides us with all this data<br />
 [bounty-targets-data](https://github.com/arkadiyt/bounty-targets-data)<br />
 
#### 2. Subdomain Enumeration 
Subdomain Enumeration is a deep and multi-layered field. <br />
Since the process takes a long time, tools written in go work more efficiently than those written with python.
So I used [subfinder](https://github.com/projectdiscovery/subfinder) subdomain enumaration tool.
> "Fast passive subdomain enumeration tool."

#### 3. Subdomain Takeover
I used [subjack](https://github.com/haccer/subjack) for subdomain takeover.
I use Subjack instead of [SubOver](https://github.com/Ice3man543/SubOver) because Subjack is more up to date.<br />
But it still finds outdated vulnerabilities, We should filter them.
> "Subjack is a Subdomain Takeover tool written in Go designed to scan a list of subdomains concurrently and identify ones that are able to be hijacked."

## test.sh
```
rm /home/ubuntu/results.txt;
cd ~/subdomain_takeover/bounty-targets-data/;
git pull;
cd ~/subdomain_takeover;
cp ~/subdomain_takeover/bounty-targets-data/data/wildcards.txt ./;
echo "*.example.com" >> ~/subdomain_takeover/bounty-targets-data/data/wildcards.txt # You can add extra domains to your target list
cat wildcards.txt | sed 's/^*.//g' | grep -v '*' > wildcards_without_stars.txt;
while read host;
   do file=$host && file+="_subfinder.out";
   ~/go/bin/subfinder -t 100 -o $file -d $host;
done < ./wildcards_without_stars.txt;
cat ./*.out > all_subdomains.lst;
~/go/bin/subjack -c /home/ubuntu/src/github.com/haccer/subjack/fingerprints.json -w ./all_subdomains.lst -t 300 -timeout 5 -o /home/ubuntu/results.txt;
python3 /home/ubuntu/main.py;
```

## main.py (telegram bot)
```
import telebot
import datetime
import os

from tempfile import mkstemp
from shutil import move, copymode
from os import fdopen, remove
def replace(file_path):
    #Create temp file
    fh, abs_path = mkstemp()
    some_list = ["[SHOPIFY]","[FASTLY]","[TUMBLR]"]
    with fdopen(fh,'w') as new_file:
        with open(file_path) as old_file:
            for line in old_file:

                list6 = []
                list6.append(line)
                durum =[x for x in some_list if any(x in item for item in list6)]
                if len(durum)==0:
                    new_file.write(line)
    copymode(file_path, abs_path)
    #Remove original file
    remove(file_path)
    #Move new file
    move(abs_path, file_path)
replace("/home/ubuntu/results.txt")

def tele( ):
    now =datetime.datetime.now().strftime("%m/%d/%Y, %H:%M")
    token = "YOUR-BOT-TOKEn"
    bot = telebot.TeleBot(token)
    #message = "{} \n {}".format(title, url)
    file= open("/home/ubuntu/results.txt","rb")
    bot.send_document(chat_id="YOUR-CHAT-ID", caption=now,data=file)

if os.stat("/home/ubuntu/results.txt").st_size > 0:
    tele()

```
## Crontab Command (Runs every 6 hours)
```
0 */6 * * *  /home/ubuntu/test.sh
```

You can check [this list](https://github.com/EdOverflow/can-i-take-over-xyz) for available vulnerability
#### References
Main inspiration: [How To Setup an Automated Sub-domain Takeover Scanner for All Bug Bounty Programs in 5 Minutes](https://hakluke.medium.com/how-to-setup-an-automated-sub-domain-takeover-scanner-for-all-bug-bounty-programs-in-5-minutes-3562eb621db3)<br />
[The Best Source Patrik Hudak](https://0xpatrik.com/)<br />
[Link1](https://www.youtube.com/watch?v=q_A8aXLO1gA)<br />
[Link2](https://wikihak.com/bug-bounty-automation-subdomain-enumeration/)<br />
[Link3](https://developer.mozilla.org/en-US/docs/Web/Security/Subdomain_takeovers)<br />
[Link4](https://www.hackerone.com/blog/Guide-Subdomain-Takeovers)<br />
[Link5](https://labs.detectify.com/2014/10/21/hostile-subdomain-takeover-using-herokugithubdesk-more/)

