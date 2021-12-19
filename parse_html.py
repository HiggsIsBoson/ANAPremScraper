import os, glob

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
    time=''
    tickets=[]

    def __init__ (self) :
        self.clear()

    def clear (self) :
        self.ID=0
        self.date=0
        self.time=''
        self.tickets=[]
    
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
def parse_day(inFileName, dict_flights) :

    f = open(inFileName,'r')
    lines = f.readlines()

    for line in lines:
        #    time=line.split('>')[3].split('<')[0]
        #    print(time)

        this_flight = flight()    
        this_flight.flightID = getFlightID(line)
        this_flight.date = inFileName.split('_')[-2]
        this_flight.time = getAttr(line, 'availabilityResultFlightTime')

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
            
            this_flight.tickets.append(t)


        print('----------------------')
        print(this_flight.flightID, this_flight.date, this_flight.time)
        for t in this_flight.tickets :
            print(t.ticket_type, t.mileage, t.price, t.nAvail)

        dict_flights.append(this_flight)

######################################
dict_flights=[]

for f in sorted(glob.glob(os.path.join('output/*_event.html'))) : 
    print(f)
#    parse_day('output/rawquery_haneda_naha_20220228_event.html',dict_flights)
    parse_day(f, dict_flights)

print(dict_flights)
