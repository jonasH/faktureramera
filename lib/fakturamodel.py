
# TODO: generate getters/setters
class Job():
#id  hours price   job
    price = 0
    number = 0
    text = ""
    def __init__(self, price, number,text ):
        self.price = price
        self.number = number
        self.text = text

class Customer():
# id name  address   zipcode
    id = 0
    name = ""
    address = ""
    zipcode = ""

    def __init__(self,id,name,address, zipcode):
        """"""
        self.id,self.name,self.address, self.zipcode = id,name,address, zipcode



# TODO: generate getters/setters
class Bill():
#  id  reference bill_date  payed  payed_date
    customer = None
    jobs = []
    id = 0
    reference = ""
    bill_date = ""
    payed = False
    payed_date = None
    
    def __init__(self,id,reference,bill_date,payed = False,payed_date = None):
        self.id,self.reference,self.bill_date,self.payed,self.payed_date = id,reference,bill_date,payed,payed_date

    
    def addJob(self,job):
        self.jobs.append(job)

    def removeJob(self, job):
        self.jobs.remove(job)

    def setCustomer(self, customer):
        """"""
        self.customer = customer

    def getCustomer(self):
        """"""
        return self.customer

# TODO: all settings here! Shortcut: hardcode
class Profile():
    def __init__(self):
        """"""
        # TODO fix this hack, it's just a quick hack right now
        import lib.profile as profile
        self.daysToPay    = profile.daysToPay    
        self.address      = profile.address      
        self.mail         = profile.mail         
        self.telephone    = profile.telephone    
        self.orgNr        = profile.orgNr        
        self.bankAccount  = profile.bankAccount  
        self.tax          = profile.tax          
        self.billLocation = profile.billLocation 
