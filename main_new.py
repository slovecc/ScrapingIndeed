from import_pack import *
from utils import *
from param import *

results = []
total_skills = pd.DataFrame()
url_base = "https://www.indeed.es/ofertas?q=data+scientist"
base_url = 'http://www.indeed.es'

#jobs0 = pd.DataFrame(columns=['location', 'title', 'company', 'salary', 'summary'])
total_jobs = pd.DataFrame(columns=['location', 'title', 'company', 'salary', 'summary'])

for city in indeed_cities:
    print(city)
    url = url_base+"&l="+city
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'html.parser')

    num_jobs_area = soup.find(id='searchCountPages').string  # Now extract the total number of jobs found
    job_numbers = re.findall('\d+', num_jobs_area)  # Extract the total jobs found from the search result
    tot_job_numbers = int(job_numbers[1])
    print('There were', tot_job_numbers, 'jobs found')  # Display how many jobs were found

    num_pages = tot_job_numbers / 10  # This will be how we know the number of times we need to iterate over each new
    # search result page

    for i in range(0, int(round(num_pages))):  # Loop through all of our search result pages
        print('Getting page', i)
        start_num = str(i * 10)  # Assign the multiplier of 10 to view the pages we want
        current_page = ''.join([url, '&start=', start_num])
        # Now that we can view the correct 10 job returns, start collecting the text samples from each
        html_page = requests.get(current_page)
        page_obj = BeautifulSoup(html_page.text, 'html.parser')  # Locate all of the job links

        tt = page_obj.findAll("div", {"class": "title"})
        uu = [subclass.find('a') for subclass in tt]

        job_URLS = [base_url + x.get("href") for x in uu]  # Get the URLS for the jobs

        skills=get_skill(job_URLS) #to add here in the data frame also the city
        if i == 0:
            total_skills = pd.DataFrame(skills)
        else:
           # total_skills= pd.concat([total_skills, pd.DataFrame(skills)], ignore_index=False)
            total_skills = total_skills.append(pd.DataFrame(skills), ignore_index=False)

        for result in page_obj.find_all('div', {'class': 'jobsearch-SerpJobCard'}):
            results.append(result)
        #print(results)
        jobs1=pd.DataFrame()
        for entry in results:
            location = get_loc(entry)
            title = get_job(entry)
            company = get_comp(entry)
            salary = get_sal(entry)
            desc = get_desc(entry)
            jobs0 = pd.DataFrame({'location': [location],
                                  'title': [title],
                                  'company': [company],
                                  'salary': [salary],
                                  'summary': [desc]})
            jobs1=jobs1.append(jobs0)


            #jobs0 = jobs0.drop_duplicates()
        #total_jobs = pd.concat([total_jobs, pd.DataFrame(jobs0)], ignore_index=False)
        total_jobs = total_jobs.append(jobs1, ignore_index=False)

        #results.to_csv('./csv/indeed-results.csv', index=False, encoding='utf-8')

        #clean salaries, adding year experience, see if more city, spain ?
    total_jobs=total_jobs.drop_duplicates()
    total_skills_grouped = total_skills.groupby("Term").sum()/tot_job_numbers * 100

#total_skills_grouped.plot.bar( y='NumPostings', rot=45,legend=False)
