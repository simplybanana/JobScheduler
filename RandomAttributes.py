import random
import string
import time
import json
import MachineDefine
import networkx as nx


class Job(object):
    def __init__(self, jobNum, productType, totalPages, totalRecords, collateral, matching, perf, colorsetup, insertType, rolls, roll_size,paperProfile, foldType=None, cover=None,):
        """
        groupings for jobs
        :param jobNum: list of jobNumbers
        :param productType: type either SS PB Letter
        :param totalPages: total number of pages
        :param totalRecords: total amount of pieces
        :param collateral: total number of collateral pieces
        :param matching: number of matching
        :param perf: Boolean if perf or not
        :param foldType: tri half flat
        :param cover: how many covers
        :param rolls: number of webs needed
        :param insertType: either poly or env or none
        :param colorsetup: is it color or not
        """
        self.jobNum = jobNum
        self.productType = productType
        self.totalPages = totalPages
        self.totalRecords = totalRecords
        self.collateral = collateral
        self.matching = matching
        self.perf = perf
        self.foldType = foldType
        self.cover = cover
        self.rolls = rolls
        self.roll_size = roll_size
        self.insertType = insertType
        self.colorsetup = colorsetup
        self.paperProfile = paperProfile


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
                                "PressProfile": "17in Letters",
                                "PaperProfile": "17in 50#",
                                "InputMethod": "12x18-60lb-CnC-Letter",
                                "ColorSetup": " ",
                                "FoldType": " ",
                                "InsertType": " ",
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
    job_attributes = {
      "destination": {
        "name": "{{organizationId}}"
      },
      "orderData": {
        "sourceOrderId": "613817_{{$randomInt}}",
        "customerName": "HEALTHPLAN SERVICES, INC",
        "purchaseOrderNumber": jobNum,
        "email": "Testing@onieldata.com",
        "items": [
          {
            "description": {"JobNumber":620574, "FileNumber":102637},
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
                  "Enclosure1": enclosures[0],
                  "Enclosure2": enclosures[1],
                  "Enclosure3": enclosures[2],
                  "Enclosure4": enclosures[3],
                  "Enclosure5": enclosures[4],
                  "Enclosure6": enclosures[5],
                  "Enclosure7": enclosures[6],
                  "Enclosure8": enclosures[7],
                  "Enclosure9": enclosures[8],
                  "Enclosure10": enclosures[9],
                  "Enclosure11": enclosures[10],
                  "Enclosure12": enclosures[11],
                  "Enclosure13": enclosures[12],
                  "Enclosure14": enclosures[13],
                  "Perforated": perf,
                  "Matching": str(match),
                  "FileNumber": "102637",
                  "Substrate": " ",
                  "BeginBarCode": "17377479878",
                  "EndBarCode": "17377480017",
                  "PDFPages": pages,
                  "BatchID": "620574-2",
                  "NumberRecords": records,
                  "PressProfile": "17in Letters",
                  "PaperProfile": "17in 50#",
                  "InputMethod": "12x18-60lb-CnC-Letter",
                  "ColorSetup": color_setup,
                  "FoldType": fold,
                  "InsertType":insertType,
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
            "slaDays": slaDays,
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
    #with open('D:\\Personal Projects\\JobSchedule\\JobFiles\\JobNumber'+str(job_attributes["orderData"]['purchaseOrderNumber'])+'.txt', 'w') as file:
        #file.write(json.dumps(job_attributes,indent=4))
    return job_attributes


def below_target(open_buckets,target,job,completed_jobs, key, i, j):
    diff = target - job['orderData']['items'][i]['components'][j]['attributes']['PDFPages']
    if key in open_buckets:
        if any(l <= diff for l in open_buckets[key].keys()):
            list_key = list(open_buckets[key].keys())
            list_key.sort(reverse=True)
            for k in list_key:
                if k > diff:
                    pass
                elif k == diff:
                    open_buckets[key][k].append(job)
                    completed_jobs.append(open_buckets[key][k])
                    open_buckets[key].pop(k)
                    break
                else:
                    ke = k + job['orderData']['items'][i]['components'][j]['attributes']['PDFPages']
                    open_buckets[key][k].append(job)
                    open_buckets[key][ke] = open_buckets[key][k]
                    open_buckets[key].pop(k)
                    break
        else:
            open_buckets[key][job['orderData']['items'][i]['components'][j]['attributes']['PDFPages']] = [job]
    else:
        open_buckets[key] = {job['orderData']['items'][i]['components'][j]['attributes']['PDFPages']: [job]}
    return open_buckets, completed_jobs


def find_matching_jobs(job, open_buckets=None, completed_jobs=None):
    if open_buckets is None:
        open_buckets = {}
    if completed_jobs is None:
        completed_jobs = []
    batchableAttributes = ['Perforated', 'Matching', 'ColorSetup', 'FoldType', 'PressProfile', 'InsertType']
    target = 180000
    for i in range(len(job['orderData']['items'])):
        # keys: Code,Perforated,Matching,Colorsetup,Foldtype, pressprofile, number of enclosures
        for j in range(len(job['orderData']['items'][i]['components'])):
            if job['orderData']['items'][i]['components'][j]['code'] == 'Collateral':
                continue
            keys = ''
            keyCheck = job['orderData']['items'][i]['components'][j]['code']
            keys += str(keyCheck) + ','
            for item in range(len(batchableAttributes)):
                keyCheck = job['orderData']['items'][i]['components'][j]['attributes'][batchableAttributes[item]]
                keys += str(keyCheck) + ','
            numEnclosures = 0
            k = 1
            while k < 15:
                keyCheck = job['orderData']['items'][i]['components'][j]['attributes']["Enclosure" + str(k)]
                if keyCheck:
                    numEnclosures += 1
                    k += 1
                else:
                    k = 15
            keys += str(numEnclosures)
            if job['orderData']['items'][i]['components'][j]['attributes']['PDFPages'] == target:
                completed_jobs.append([job])
            elif job['orderData']['items'][i]['components'][j]['attributes']['PDFPages'] > target:
                counter = 1
                while job['orderData']['items'][i]['components'][j]['attributes']['PDFPages'] > target:
                    tempjob = job
                    tempjob['orderData']['items'][i]["description"]["FileNumber"] = str(job['orderData']['items'][i]["description"]["FileNumber"]) + "-" + str(counter)
                    tempjob['orderData']['items'][i]['components'][j]['attributes']['PDFPages'] = 180000
                    completed_jobs.append([tempjob])
                    job['orderData']['items'][i]['components'][j]['attributes']['PDFPages'] -= target
                    counter += 1
                job['orderData']['items'][i]["description"]["FileNumber"] = str(job['orderData']['items'][i]["description"]["FileNumber"]) + "-" + str(counter)
                open_buckets, completed_jobs = below_target(open_buckets, target, job, completed_jobs, keys, i, j)
            else:
                open_buckets, completed_jobs = below_target(open_buckets, target, job, completed_jobs, keys, i, j)
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
                rolls = None
                roll_size = None
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
                cover = cover
                rolls = rolls
                roll_size = roll_size
                insertType = job['orderData']['items'][i]['components'][j]['attributes']['insertType']
                colorsetup = job['orderData']['items'][i]['components'][j]['attributes']['ColorSetup']
                paperProfile = job['orderData']['items'][i]['components'][j]['attributes']['PaperProfile']
            jns = Job(jobNum,productType,totalPages,totalRecords,collateral,matching,perf,colorsetup,insertType,rolls,roll_size,paperProfile,foldType,cover)
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
    print(completed_jobs)