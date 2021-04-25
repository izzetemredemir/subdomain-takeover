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