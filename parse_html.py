import os, glob
import json
from optparse import OptionParser

##################################
class ticket :
    ticket_type=''
    mileage=-0
    price=''
    nAvail=0

    def __init__ (self) :
        self.clear()

    def clear (self) :
        self.ticket_type=''
        self.mileage=-0
        self.price=''
        self.nAvail=0

##################################
class flight :
    ID=0
    date=0
    time_dep=''
    time_arr=''
    tickets={}

    def __init__ (self) :
        self.clear()

    def clear (self) :
        self.ID=0
        self.date=0
        self.time_dep=''
        self.time_arr=''
        self.tickets={}
    
##################################
def dumper(obj): #custom JSON dumper
    try:
        return obj.toJSON()
    except:
        return obj.__dict__
##################################
def getAttr(line,key) :
    tokens =  line.split('>')
    for it in range(0,len(tokens)):
        if key in tokens[it]: 
            return tokens[it+1].split('<')[0]

def getPriceBlock(line,key) :
    for block in line.split('#'):
        if key in block: 
            return block

def getPrice(block) :
    tokens =  block.split('>')
    for it in range(0,len(tokens)):
        if 'hoverInfo visuallyHidden' in tokens[it]: 
            return tokens[it+3].split('<')[0].rstrip('円')

def getFlightID(line) :
    line = line.replace('class="availabilityResultFlightDetail"><span>ANA','class="availabilityResultFlightDetail"><span class="anaWings">ANA')
    return getAttr(line, 'anaWings')

########################################
def parse_day(inFileName) :

    f = open(inFileName,'r')
    lines = f.readlines()

    flights={}
    for line in lines:
        #    time=line.split('>')[3].split('<')[0]
        #    print(time)

        this_flight = flight()    
        this_flight.ID = getFlightID(line)
        this_flight.date = inFileName.split('_')[-2]

        time = getAttr(line, 'availabilityResultFlightTime')
        this_flight.time_dep = time.split(' ')[0].replace(' ','')
        this_flight.time_arr = time.split(' ')[2].replace(' ','')

        blocks = line.replace('<td class=\"showResult\"','#<td class=\"showResult\"').split('#')
        for ib in range(1,len(blocks)) :        
            #        print(blocks[ib])

            t = ticket()
            t.ticket_type = getAttr(blocks[ib], 'hoverInfo visuallyHidden').split(':')[0]\
                .replace('プレミアム運賃','prem')\
                .replace('バリュープレミアム3A','val3A')\
                .replace('バリュープレミアム3B','val3B')\
                .replace('スーパーバリュープレミアム28','superVal28')\
                .replace('プレミアムビジネスきっぷ','premBus')\
                .replace('プレミアム障がい者割引','premDisab')\
                .replace('プレミアム株主優待割引','premStock')

            t.price = int(getPrice(blocks[ib]).replace(',',''))
            t.mileage = int(getAttr(blocks[ib], 'hoverInfo visuallyHidden').split(':')[1].split('/')[0].replace('マイル','').replace(',',''))
            nAvail = getAttr(blocks[ib], 'hasSeatCount')
            t.nAvail = 0 if nAvail==None else nAvail
            
            this_flight.tickets[t.ticket_type] = t


#        print('----------------------')
#        print(this_flight.ID, this_flight.date, this_flight.time_dep, this_flight.time_arr)
#        print(this_flight.tickets)

        flights[str(this_flight.date)+'_'+this_flight.ID] = this_flight

    return flights


######################################
parser = OptionParser(usage="usage : python parse_html.py -O [origin] -D [destination]")
parser.add_option("-O", dest="origin", type="string", default="haneda", help="Origin (all small capitals)")
parser.add_option("-D", dest="destination", type="string", default="naha", help="Destination (all small captals)")

(options, args) = parser.parse_args()

######################################

ls_key='output/*'+options.origin+'_'+options.destination+'*_event.html'
print("parse_html  INFO  Going over: ", ls_key)

dict_day={}
for f in sorted(glob.glob(os.path.join(ls_key))) : 
    date = f.split('_')[-2]
    dict_day[date] = parse_day(f)

jsonString = json.dumps(dict_day, default=dumper, indent=2)


outFile = 'output/parsed_'+options.origin+'_'+options.destination+'.json'
print('parse_html  INFO  Generated '+outFile)
with open(outFile, 'w') as f:  f.write(jsonString)
