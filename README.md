## Verified environment
- MacOS: 10.15.7
- Chrome: 96.0.4664.93 (Official Build) (x86_64)
- Selenium: 4.1.0
- Python: 3.9.1

## Pre-requisites
- Google Chrome
- Python3
- (Optional) [Selenium IDE](https://chrome.google.com/webstore/detail/selenium-ide/mooikfkahbdckldjjndioackbalphokd) for debugging

## Install
Setting up a virtual env:
<pre>
python -m venv venv_ANAPremQuery/
source venv_ANAPremQuery/bin/activate
</pre>
Install `Selenium` and `chrome driver`:
<pre>
pip install selenium
pip install chromedriver-binary==96.*   # specify the version of your chome browser  
</pre>

## Next time you log in
<pre>
source venv_ANAPremQuery/bin/activate
</pre>

## Run web queries
<pre>
# Query Haneda->Naha on 15 Feb 2022
python ANAPremQuery.py -y 2022 -m 2 -d 15 -O haneda -D naha

## Query Haneda->Naha for the whole month of Feb 2022
python ANAPremQuery.py -y 2022 -m 2 -O haneda -D naha

## Parallelise (appending `&`)
for month in 1 2 3; do
    python ANAPremQuery.py -y 2022 -m $month -O haneda -D naha & 
done

## Print out the options
python ANAPremQuery.py -h
</pre>
The output files are generated in `output/` created at the location the script is run.  
An example of batch queries can be found in [`ANAPremQuery.sh`](https://github.com/HiggsIsBoson/ANAPremScraper/blob/master/ANAPremQuery.sh).  

**NOTE:** The parser is in progress. To be added at some point.  

## When you finish
Type
<pre>
deactivate
</pre>
to exit the virtual env.
