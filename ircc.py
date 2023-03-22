from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

import time
import csv
import pandas as pd

from bs4 import BeautifulSoup
import requests

import subprocess
import json

#Define Executable Path
options=Options()
options.chrome_executable_path= "/usr/local/bin/chromedriver"
driver=webdriver.Chrome(options=options)

def turnon(link):
    try:
        driver.get(link)
    except:
        print('no internet access')

title=""

def ircc():
    turnon('https://www.canlii.org/en/')
    time.sleep(5)
    list=["2018 FC 142", "2021 FC 534","2020 FC 500","2019 FCA 34","2018 FC 1207","2017 FC 1191","2016 FC 1033", "2015 FC 485","2014 FC 1019"]#"2012 FC 980"]
    #,#"2011 FC 172","2010 FC 850", "2009 FC 998","2008 FC 407","2007 FC 489","2021 FC 603"
    #,"2020 FC 202","2019 FC 1633","2018 FC 1218", "2017 FC 98", "2016 FC 1174", "2015 SCC 61", "2014 FC 704", "2013 FC 903",
	#"2012 FC 612","2011 FC 797","2010 FC 852","2009 FC 1193","2008 FC 1303","2007 FC 1088"]
    length= len(list)

    count=0
    while(count<length):
        location=""
        applicant=""
        respondent=""
        judgment=""
        present=""
        introduction=""
        analysis=""
        conclusion=""
    
        case=driver.find_element(By.XPATH, "//*[@id='idInput']")
        case.send_keys(list[count])
        case.send_keys(Keys.RETURN)
        time.sleep(5)
        driver.find_element(By.XPATH, "//*[@id='searchResults']/div[1]/ol/li[1]/div/div/div[2]/div[1]/div/span[1]/a").click()
        driver.maximize_window()
        time.sleep(5)
        title=list[count]

        #URL
        url=str(driver.current_url)

        #Date 
        date= driver.find_element(By.XPATH, "//*[@id='documentMeta']/div[1]/div[2]").text

        #Filenum
        filenum=driver.find_element(By.XPATH,"//*[@id='documentMeta']/div[2]/div[2]").text

        #Citation
        Boolean=driver.find_elements(By.XPATH,"//*[@id='documentMeta']/div[4]/div[2]")
        if len(Boolean)>0:
            citation= driver.find_element(By.XPATH,"//*[@id='documentMeta']/div[4]/div[2]").text
        else:
            citation= driver.find_element(By.XPATH,"//*[@id='documentMeta']/div[3]/div[2]").text
        
        #Location
        Boolean=driver.find_elements(By.XPATH,"//*[@id='originalDocument']/div/div/div[2]/p[5]")
        Boolean2=driver.find_elements(By.XPATH,"//*[@id='originalDocument']/div/div[2]/p[3]") 
        Boolean3=driver.find_elements(By.XPATH,"//*[@id='originalDocument']/div/div[2]/p[6]") 
        if len(Boolean)>0:
            location=driver.find_element(By.XPATH,"//*[@id='originalDocument']/div/div/div[2]/p[5]").text
        elif len(Boolean2)>0:
            location=driver.find_element(By.XPATH,"//*[@id='originalDocument']/div/div[2]/p[3]").text
        elif len(Boolean3)>0:
            location=driver.find_element(By.XPATH,"//*[@id='originalDocument']/div/div[2]/p[3]").text
        else:
            print("location not found")

        #Applicant
        Boolean2=driver.find_elements(By.XPATH,"//*[@id='originalDocument']/div/div/div[2]/table/tbody/tr[2]/td")
        Boolean2_1=driver.find_elements(By.XPATH,"//*[@id='originalDocument']/div/div[2]/table/tbody/tr[2]/td")
        if len(Boolean2)>0:
            applicant= driver.find_element(By.XPATH,"//*[@id='originalDocument']/div/div/div[2]/table/tbody/tr[2]/td").text
        elif len(Boolean2_1)>0:
            applicant= driver.find_element(By.XPATH,"//*[@id='originalDocument']/div/div[2]/table/tbody/tr[2]/td").text
        else:
            print("Applicant not found")
        
        #Respondent
        Boolean3=driver.find_elements(By.XPATH, "//*[@id='originalDocument']/div/div/div[2]/table/tbody/tr[5]/td")
        Boolean3_1=driver.find_elements(By.XPATH, "//*[@id='originalDocument']/div/div[2]/table/tbody/tr[5]/td")
        if len(Boolean3)>0:
            respondent= driver.find_element(By.XPATH, "//*[@id='originalDocument']/div/div/div[2]/table/tbody/tr[5]/td").text
        elif len(Boolean3_1)>0:
            respondent= driver.find_element(By.XPATH, "//*[@id='originalDocument']/div/div[2]/table/tbody/tr[5]/td").text
        else:
            print("Respondent not found")

        #Judgment
        WS3= driver.find_elements(By.CLASS_NAME,"WordSection3")
        S3= driver.find_elements(By.CLASS_NAME,"Section3")
        isthat=driver.find_elements(By.LINK_TEXT,"is that")
        if len(WS3)>0:
            Judgment=driver.find_element(By.CLASS_NAME,"WordSection3").text
            judgment_start=Judgment.find('is that')+8
            if judgment_start !=7:
                judgment=Judgment[judgment_start:]
            else:
                print("")
        elif len(S3)>0:
            Judgment=driver.find_element(By.CLASS_NAME,"Section3").text
            judgment_start=Judgment.find('is that')+8
            if judgment_start !=7:
                judgment=Judgment[judgment_start:]
            else:
                print("")
        elif len(isthat)==1:
            body=driver.find_element(By.CLASS_NAME,"Section2").text
            isthat=body.find("is that")
            judgment_End= body.find("FEDERAL COURT")
            judgment=body[isthat:judgment_End]
        else:
            print("Judgment not found")
        


        WS2 =driver.find_elements(By.CLASS_NAME, "WordSection2")
        S2=driver.find_elements(By.CLASS_NAME, "Section2")
        if len(WS2)>0:
            body=driver.find_element(By.CLASS_NAME, "WordSection2").text
            #Present
            present_start=body.find('PRESENT')
            present_end=body.find('BETWEEN')
            present=body[present_start:present_end]
            
            Introduction_start=body.find('JUDGMENT AND REASONS')+20
            Introduction_start2=body.find('REASONS FOR JUDGMENT AND JUDGMENT')+ 33
            Introduction_end=body.find('Analysis')
            Introduction_end2=body.find('ANALYSIS')

            analysis_start= body.find('Analysis')+8
            analysis_start2=body.find('ANALYSIS')+8
            analysis_end=body.find('Conclusion')
            analysis_end2=body.find('CONCLUSION')

            conclusion_start=body.find('Conclusion')+9
            conclusion_start2=body.find('CONCLUSION')+9

            #Write Introduction
            if Introduction_start !=19:
                if Introduction_end !=-1:
                    introduction= body[Introduction_start:Introduction_end]
                elif Introduction_end2 != -1:
                    introduction= body[Introduction_start:Introduction_end2]
            elif Introduction_start2!=32:
                if Introduction_end !=-1:
                    introduction= body[Introduction_start2:Introduction_end]
                elif Introduction_end2 != -1:
                    introduction= body[Introduction_start2:Introduction_end2] 
            #Write Analysis
            if analysis_start!=7:
                analysis=body[analysis_start:analysis_end]
            elif analysis_start2!=7:
                analysis=body[analysis_start2:analysis_end2]
            #Write Conclusion
            if conclusion_start != 8:
                conclusion=body[conclusion_start:]
            elif conclusion_start2 != 8:
                conclusion=body[conclusion_start:]

        elif len(S2)>0:
            body=driver.find_element(By.CLASS_NAME, "Section2").text
            #Present
            present=body.find('PRESENT')
            present_end=body.find('BETWEEN')
            present=body[present_start:present_end]
            
            Introduction_start=body.find('JUDGMENT AND REASONS')+20
            Introduction_start2=body.find('REASONS FOR JUDGMENT AND JUDGMENT')+ 33
            Introduction_end=body.find('Analysis')
            Introduction_end2=body.find('ANALYSIS')

            analysis_start= body.find('Analysis')+8
            analysis_start2=body.find('ANALYSIS')+8
            analysis_end=body.find('Conclusion')
            analysis_end2=body.find('CONCLUSION')

            conclusion_start=body.find('Conclusion')+9
            conclusion_start2=body.find('CONCLUSION')+9

            #Write Introduction
            if Introduction_start !=19:
                if Introduction_end !=-1:
                    introduction= body[Introduction_start:Introduction_end]
                elif Introduction_end2 != -1:
                    introduction= body[Introduction_start:Introduction_end2]
            elif Introduction_start2!=32:
                if Introduction_end !=-1:
                    introduction= body[Introduction_start2:Introduction_end]
                elif Introduction_end2 != -1:
                    introduction= body[Introduction_start2:Introduction_end2] 
            #Write Analysis
            if analysis_start!=7:
                analysis=body[analysis_start:analysis_end]
            elif analysis_start2!=7:
                analysis=body[analysis_start2:analysis_end2]
            #Write Conclusion
            if conclusion_start != 8:
                conclusion=body[conclusion_start:]
            elif conclusion_start2 != 8:
                conclusion=body[conclusion_start:]
        

        else:
            print("Section2 not found")
            #import No_Section_2
        
        file=open(title +'.json','w')
        
        #Extract Paragraph

        soup= BeautifulSoup(driver.page_source, 'html.parser')
        content= soup.find('div', class_= 'WordSection2')
        
        if content!=None:
            elements= content.find_all(['h1', 'h2','div','li','h3','blockquote'])
            paragraphs=[]
            for element in elements:
                html=str(element)
                text = element.get_text(strip=True)
                if text:
                    paragraphs.append({"p":text,"o":html})
        else: 

            content_s=driver.find_element(By.XPATH,"//*[@id='originalDocument']/div/div/p[50]")
            content_e=driver.find_element(By.XPATH,"//*[@id='originalDocument']/div/div/p[87]")

            htmls=""
            for element in content_s.find_elements(By.XPATH, "./following-sibling::*"):
                if element == content_e:
                    break
                htmls+=element.get_attribute("outerHTML")
            soup= BeautifulSoup(htmls,"html.parser")
            paragraphs=[]
            for element in soup.find_all(['p']):
                html=str(element)
                text = element.get_text(strip=True)
                if text:
                    paragraphs.append({"p":text,"o":html})


        data={'url':url,'date': date, 'filenum': filenum, 'citation': citation, 'location':location,'applicant':applicant,'respondent':respondent,
        'judgment':judgment,'present':present,'introduction':introduction,'analysis':analysis,'conclusion':conclusion,'paragraphs':paragraphs}
        json.dump(data,file)
               
        
        driver.get('https://www.canlii.org/en/')
        time.sleep(5)
        count+=1
    else:
        print("completed")
        

ircc()
driver.close()
