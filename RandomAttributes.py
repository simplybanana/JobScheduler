import random
import string
import time
import json
import MachineDefine
import networkx as nx
import math

class Order(object):
    def __init__(self, jobNum, productType, totalPages, totalRecords, collateral, matching, perf, foldType, cover, insertType, colorsetup, paperProfile):
        self.jobNum = jobNum
        self.productType = productType
        self.totalPages = totalPages
        self.totalRecords = totalRecords
        self.pagesPerRecord = totalPages/totalRecords
        self.collateral = collateral
        self.matching = matching
        self.perf = perf
        self.foldType = foldType
        self.cover = cover
        self.insertType = insertType
        self.colorsetup = colorsetup
        self.paperProfile = paperProfile
        self.insertGroup = []

    def other_attribute(self):
        inserters = MachineDefine.inserter_define()
        for item in inserters:
            if self.collateral < item.num_pockets and self.matching < item.match and self.insertType == "Envelope":
                self.insertGroup.append(item.name)

    def batchable_attributes(self):
        batchable = str(self.productType) + ',' + str(self.insertGroup) + ',' + \
                    str(self.perf) + ',' + str(self.foldType) + ',' + \
                    str(self.colorsetup) + ',' + str(self.paperProfile)
        return batchable


class Bucket(Order):
    def __init__(self, jobNum, productType, totalPages, totalRecords, collateral, matching, perf, foldType, cover, insertType, colorsetup, paperProfile):
        super().__init__(jobNum, productType, totalPages, totalRecords, collateral, matching, perf, foldType, cover, insertType, colorsetup, paperProfile)
        self.rolls = 0
        self.roll_size = " "

    def decide_rolls(self):
        pass


def create_json_template():
    job_attributes = {
        "destination": {
            "name": "{{organizationId}}"
        },
        "orderData": {
            "sourceOrderId": "613817_{{$randomInt}}",
            "customerName": "HEALTHPLAN SERVICES, INC",
            "purchaseOrderNumber": "",
            "email": "Testing@onieldata.com",
            "items": [
                {
                    "description": {"JobNumber": " ", "FileNumber": " "},
                    "sku": "Letter",
                    "sourceItemId": "BillsPerf_Remit_NC_PG4",
                    "barcode": "{{$randomInt}}",
                    "quantity": 1,
                    "extraData": {
                        "Plant": "Texas"
                    },
                    "components": [
                        {
                            "code": "Letter",
                            "fetch": False,
                            "localFile": True,
                            "attributes": {
                                "Enclosure1": " ",
                                "Enclosure2": " ",
                                "Enclosure3": " ",
                                "Enclosure4": " ",
                                "Enclosure5": " ",
                                "Enclosure6": " ",
                                "Enclosure7": " ",
                                "Enclosure8": " ",
                                "Enclosure9": " ",
                                "Enclosure10": " ",
                                "Enclosure11": " ",
                                "Enclosure12": " ",
                                "Enclosure13": " ",
                                "Enclosure14": " ",
                                "Perforated": " ",
                                "Matching": " ",
                                "FileNumber": "102637",
                                "Substrate": " ",
                                "BeginBarCode": "17377479878",
                                "EndBarCode": "17377480017",
                                "PDFPages": " ",
                                "BatchID": "620574-2",
                                "NumberRecords": " ",
                                "MinReosource": " ",
                                "MaxResource": " ",
                                "PressProfile": "17in Letters",
                                "PaperProfile": "17in 50#",
                                "InputMethod": "12x18-60lb-CnC-Letter",
                                "ColorSetup": " ",
                                "FoldType": " ",
                                "insertType": " ",
                                "ImpositionLocation": "8.5x11_Slit-n-merge_34in_Dual_roll_in YURI SPECIAL"
                            },
                            "path": "613817\\LT_Slit-Merge\\613817-101969-BillsPerf-Remit-NC-PG4-LT_Slit-Merge-PG-001.PDF"
                        },
                        {
                            "code": "Collateral",
                            "fetch": False,
                            "localFile": True,
                            "path": "test"
                        }
                    ]
                }
            ],
            "stockItems": [],
            "shipments": [
                {
                    "shipByDate": "2020-06-26",
                    "slaDays": " ",
                    "canShipEarly": True,
                    "shipTo": {
                        "name": "Test",
                        "companyName": "Test",
                        "address1": "Test",
                        "state": "Test",
                        "town": "Test",
                        "postcode": "Test",
                        "isoCountry": "Test"
                    },
                    "carrier": {
                        "code": "customer",
                        "service": "delivery"
                    }
                }
            ]
        }
    }
    with open('D:\\Personal Projects\\JobSchedule\\JSONTemplate.txt', 'w') as file:
        file.write(json.dumps(job_attributes, indent=4))
    return job_attributes


def random_job(jobNum,perf=None,match=None, color_setup=None, fold=None, records=None, pages=None):
    if perf is None:
        perf = random.choice(['True','False'])
    if match is None:
        match = random.choice([0,2,3])
    if records is None:
        records = random.randint(0,5000)
    if pages is None:
        pages = records * random.randint(2,100)
    jobNum = jobNum
    if color_setup is None:
        color_setup = random.choice(["MONO90_V2_1","Color1"])
    if fold is None:
        fold = random.choice(["Flat","Tri","Half"])
    slaDays = random.choice([1,2,3,4,5])
    insertType = "Envelope"
    enclosures = []
    i = 0
    fillerDone = True
    while i < 14:
        if i > 3:
            fillerDone = False
        if random.randint(0,1) == 0 and fillerDone:
            letters = string.ascii_lowercase
            s = ''.join(random.choice(letters) for j in range(6))
        else:
            s = ''
            fillerDone = False
        enclosures.append(s)
        i += 1
    listed_attributes = [perf,match,records,pages,insertType,fold,color_setup]
    with open('D:\\Personal Projects\\JobSchedule\\JSONTemplate.txt') as json_file:
        data = json.load(json_file)
        attributes = ['Perforated', 'Matching', 'NumberRecords', 'PDFPages', 'insertType', 'FoldType','ColorSetup']
        for i in range(1,15):
            data['orderData']['items'][0]['components'][0]['attributes']['Enclosure'+str(i)] = enclosures[i-1]
        j = 0
        for item in attributes:
            data['orderData']['items'][0]['components'][0]['attributes'][item] = listed_attributes[j]
            j += 1
        data['orderData']['items'][0]['description']['JobNumber'] = jobNum
        data['orderData']['shipments'][0]['slaDays'] = slaDays
    return data


def below_target(order,key,target,open_buckets,completed_jobs):
    diff = target - order.totalPages
    if key in open_buckets:
        if any(l <= diff for l in open_buckets[key].keys()):
            list_key = list(open_buckets[key].keys())
            list_key.sort(reverse=True)
            for k in list_key:
                if k == diff:
                    open_buckets[key][k].append(order)
                    completed_jobs.append(open_buckets[key][k])
                    open_buckets[key].pop(k)
                    break
                elif k < diff:
                    ke = k + order.totalPages
                    open_buckets[key][k].append(order)
                    open_buckets[key][ke] = open_buckets[key][k]
                    open_buckets[key].pop(k)
                    break
        else:
            open_buckets[key][order.totalPages] = [order]
    else:
        open_buckets[key] = {order.totalPages: [order]}

    return open_buckets,completed_jobs


def find_matching_jobs(order,target=180000, open_buckets=None, completed_jobs=None):
    if open_buckets is None:
        open_buckets = {}
    if completed_jobs is None:
        completed_jobs = []
    keys = order.batchable_attributes()
    if order.totalPages == target:
        completed_jobs.append(order)
    elif order.totalPages > target:
        counter = 1
        while order.totalPages > target:
            temporder = order
            temporder.jobNum = str(order.jobNum) + "-" + str(counter)
            if target % temporder.pagesPerRecord == 0:
                temporder.totalPages = target
                temporder.totalRecords = target/temporder.pagesPerRecord
                completed_jobs.append(temporder)
                order.totalPages -= target
                order.totalRecords -= target/order.pagesPerRecord
            else:
                records = math.floor(target/temporder.pagesPerRecord)
                temporder.totalPages = records*temporder.pagesPerRecord
                temporder.totalRecords = records
                completed_jobs.append(temporder)
                order.totalPages -= temporder.totalPages
                order.totalRecords -= temporder.totalRecords
            counter += 1
        order.jobNum = str(order.jobNum) + "-" + str(counter)
        open_buckets,completed_jobs = below_target(order, keys, target, open_buckets, completed_jobs)
    else:
        open_buckets, completed_jobs = below_target(order, keys, target, open_buckets, completed_jobs)
    return open_buckets, completed_jobs


def json_to_class(job):
    jobs = []
    for i in range(len(job['orderData']['items'])):
        for j in range(len(job['orderData']['items'][i]['componenets'])):
            jobNum = job['orderData']["purchaseOrderNumber"]
            productType = job['orderData']['items'][i]['components'][j]['code']
            if productType == 'Collateral':
                totalPages = 0
                totalRecords = job['orderData']['items'][i]['components'][j-1]['attributes']['NumberRecords']
                collateral = None
                matching = None
                perf = None
                foldType = None
                cover = None
                insertType = None
                colorsetup = None
                paperProfile = None
            else:
                totalPages = job['orderData']['items'][i]['components'][j]['attributes']['PDFPages']
                totalRecords = job['orderData']['items'][i]['components'][j]['attributes']['NumberRecords']
                k = 1
                numEnclosures = 0
                while k < 15:
                    keyCheck = job['orderData']['items'][i]['components'][j]['attributes']["Enclosure" + str(k)]
                    if keyCheck:
                        numEnclosures += 1
                        k += 1
                    else:
                        k = 15
                collateral = numEnclosures
                matching = job['orderData']['items'][i]['components'][j]['attributes']['Matching']
                perf = job['orderData']['items'][i]['components'][j]['attributes']['Perforated']
                foldType = job['orderData']['items'][i]['components'][j]['attributes']['FoldType']
                cover = None
                insertType = job['orderData']['items'][i]['components'][j]['attributes']['insertType']
                colorsetup = job['orderData']['items'][i]['components'][j]['attributes']['ColorSetup']
                paperProfile = job['orderData']['items'][i]['components'][j]['attributes']['PaperProfile']
            jns = Order(jobNum, productType, totalPages, totalRecords, collateral, matching, perf, foldType, cover, insertType, colorsetup, paperProfile)
            jns.other_attribute()
            jobs.append(jns)
    return jobs


def job_path(graph, j):
    MachineDefine.update_weights(graph, j)
    path = nx.dijkstra_path(graph, 'start', 'shipping')
    time = nx.dijkstra_path_length(graph, 'start', 'shipping')
    for i in path:
        if type(i) != str:
            i.queue.append(j.jobNum)
            if type(i) == MachineDefine.Printing:
                i.wait_time += (j.totalPages / i.run_speed) * 60
                i.current_roll = j.roll_size
                i.current_color = j.colorsetup
            elif type(i) == MachineDefine.Inserter:
                i.wait_time += (j.totalRecords / i.run_speed) * 60
                i.current_foldtype = j.foldType
    return graph, path, time


if __name__ == '__main__':
    """
    g = MachineDefine.create_graph()
    #j = Job(111111,"Letter", 180000, 36000,4,0,False,"Color","Env",2, 36, foldType="Tri")
    jn = 100000
    open_buckets = {}
    completed_jobs = []
    for i in range(5):
        job = random_job(jn,color_setup="Color1",fold="Tri")
        jn += 1
        open_buckets, completed_jobs = find_matching_jobs(job,open_buckets,completed_jobs)
    print(open_buckets)
    print(completed_jobs)"""
    #create_json_template()
    #random_job(100000)
    print(math.floor(4/3))