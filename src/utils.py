from import_pack import *

def get_loc(result):
    try:
        return result.find('div', {'class': 'location'}).text
    except:
        return 'NA'

def get_comp(result):
    try:
        return result.find ('a', {'data-tn-element': 'companyName'}).text.replace("\n", "")
    except:
        return 'NA'

def get_job(result):
    try:
        return result.find('a', {'data-tn-element':'jobTitle'}).text.replace("\n","")
    except:
        return 'NA'

def get_sal(result):
    try:
        return result.find('span', {'class':'salaryText'}).text.replace("\n","")
    except:
        return 'NA'

def get_desc(result):
    try:
        return result.find('div', {'class':'summary'}).text.replace("\n","")
    except:
        return 'NA'

def get_skill(job_URLS):
    print("inside get skill")
    job_descriptions = []
    doc_frequency = Counter()  # This will create a full counter of our terms.

    for j in range(0, len(job_URLS)):
        html = requests.get(job_URLS[j])
        final_description = BeautifulSoup(html.text, 'html.parser')
        final_description = final_description.findAll("div", {"class": "jobsearch-jobDescriptionText"})
        #if final_description:  # So that we only append when the website was accessed correctly
        job_descriptions.append(final_description)
        sleep(1)
    description_str = " ".join(str(x) for x in job_descriptions)
    description_str = description_str.split()

    ttemp = []
    for item in description_str:
        temp = str(item).split()
        for items in temp:
            items = items.replace("</br>", "")
            items = items.replace("</div>", "")
            items = items.replace("<li>", "")
            items = items.replace("<ul>", "")
            items = items.replace(",", "")
            items = items.replace(".", "")
            items = items.lower()
            ttemp.append(items)

    doc_frequency.update(ttemp)
    prog_lang_dict = Counter({'Python': doc_frequency['python'], 'R': doc_frequency['r'],
                              'Java': doc_frequency['java'], 'C++': doc_frequency['c++'],
                              'Ruby': doc_frequency['ruby'],
                              'Perl': doc_frequency['perl'], 'Matlab': doc_frequency['matlab'],
                              'JavaScript': doc_frequency['javascript'], 'Scala': doc_frequency['scala']})

    analysis_tool_dict = Counter({'Excel': doc_frequency['excel'], 'Tableau': doc_frequency['tableau'],
                                  'D3.js': doc_frequency['d3.js'], 'SAS': doc_frequency['sas'],
                                  'SPSS': doc_frequency['spss'], 'D3': doc_frequency['d3']})

    hadoop_dict = Counter({'Hadoop': doc_frequency['hadoop'], 'MapReduce': doc_frequency['mapreduce'],
                           'Spark': doc_frequency['spark'], 'Pig': doc_frequency['pig'],
                           'Hive': doc_frequency['hive'], 'Shark': doc_frequency['shark'],
                           'Oozie': doc_frequency['oozie'], 'ZooKeeper': doc_frequency['zookeeper'],
                           'Flume': doc_frequency['flume'], 'Mahout': doc_frequency['mahout']})

    database_dict = Counter({'SQL': doc_frequency['sql'], 'NoSQL': doc_frequency['nosql'],
                             'HBase': doc_frequency['hbase'], 'Cassandra': doc_frequency['cassandra'],
                             'MongoDB': doc_frequency['mongoDb']})

    overall_total_skills = prog_lang_dict + analysis_tool_dict + hadoop_dict + database_dict  # Combine our Counter objects

    final_frame = pd.DataFrame(overall_total_skills.items(),
                               columns=['Term', 'NumPostings'])  # Convert these terms to a
    #final_frame.NumPostings = (final_frame.NumPostings) * 100 / len(job_descriptions)  # Gives percentage of job postings
    return final_frame


