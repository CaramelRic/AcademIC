#!/user/bin/env python
# -*- coding: utf-8 -*-

import requests
import pandas as pd
from bs4 import BeautifulSoup

def bug(user_name,password):
    login_data = {"email": user_name, "userPwd": password}
    headers = {"Content-Type": "application/x-www-form-urlencoded", "Referer": "http://ams.bhsfic.com/system/login",
               "Host": "ams.bhsfic.com"}
    url = "http://ams.bhsfic.com/system/login/doLogin"
    s = requests.session()
    r_login = s.post(url=url, data=login_data, headers=headers)
    #r_sem = s.post(url = "http://ams.bhsfic.com/system/setSystemsSemsterIds", data = {"semsIds": 17})
    r_system = s.get("http://ams.bhsfic.com/student/behavior/studentGpa", headers=headers)
    r_reference = s.get("http://ams.bhsfic.com")
    reference = r_reference.content.decode("utf8")
    html = r_system.content.decode("utf8")
    if reference == html:
        a = "invalid login"
        return a
    else:
        AcademicReport = BeautifulSoup(html, "html.parser")
        AcademicReport.text
        Overall = pd.read_html(html)[0]
        global GPACourse
        GPACourse = []
        GPACoursenum = []
        for x in range(0, len(Overall) - 1):
            if Overall.loc[x, "科目"].find("考查课") == -1:
                GPACourse.append(Overall.loc[x, "科目"])
                GPACoursenum.append(x)
        GPACourseGrade = []
        GPACourseLevel = []
        for x in GPACoursenum:
            GPACourseGrade.append(Overall.loc[x, "Total总评成绩"])
            #GPACourseGrade.append(int(Overall.loc[x, "Total总评成绩"]))
            #since the course grade is NaN when scores are not updated, and NaN can't be convert to Int, we removed int()
        i = 0
        for x in GPACourseGrade:
            if Overall.loc[i, "类型"].find("AP") != -1:
                if 92.5 <= x <= 100:
                    GPACourseLevel.append(5.00)
                elif 89.5 <= x < 92.5:
                    GPACourseLevel.append(4.67)
                elif 86.5 <= x < 89.5:
                    GPACourseLevel.append(4.33)
                elif 82.5 <= x < 86.5:
                    GPACourseLevel.append(4.00)
                elif 79.5 <= x < 82.5:
                    GPACourseLevel.append(3.67)
                elif 76.5 <= x < 79.5:
                    GPACourseLevel.append(3.33)
                elif 72.5 < x < 76.5:
                    GPACourseLevel.append(3.00)
                elif 69.5 <= x < 72.5:
                    GPACourseLevel.append(2.67)
                elif 67 <= x < 69.5:
                    GPACourseLevel.append(2.33)
                elif 63 <= x < 67:
                    GPACourseLevel.append(2.00)
                elif 60 <= x < 63:
                    GPACourseLevel.append(1.67)
                elif x < 60:
                    GPACourseLevel.append(0.00)
            elif Overall.loc[i, "科目"].find("Honors") != -1:
                if 92.5 <= x <= 100:
                    GPACourseLevel.append(4.50)
                elif 89.5 <= x < 92.5:
                    GPACourseLevel.append(4.17)
                elif 86.5 <= x < 89.5:
                    GPACourseLevel.append(3.83)
                elif 82.5 <= x < 86.5:
                    GPACourseLevel.append(3.50)
                elif 79.5 <= x < 82.5:
                    GPACourseLevel.append(3.17)
                elif 76.5 <= x < 79.5:
                    GPACourseLevel.append(2.83)
                elif 72.5 <= x < 76.5:
                    GPACourseLevel.append(2.50)
                elif 69.5 <= x < 72.5:
                    GPACourseLevel.append(2.17)
                elif 67 <= x < 69.5:
                    GPACourseLevel.append(1.83)
                elif 63 <= x < 67:
                    GPACourseLevel.append(1.50)
                elif 60 <= x < 63:
                    GPACourseLevel.append(1.17)
                elif x < 60:
                    GPACourseLevel.append(0.00)
            else:
                if 92.5 <= x <= 100:
                    GPACourseLevel.append(4.00)
                elif 89.5 <= x < 92.5:
                    GPACourseLevel.append(3.67)
                elif 86.5 <= x < 89.5:
                    GPACourseLevel.append(3.33)
                elif 82.5 <= x < 86.5:
                    GPACourseLevel.append(3.00)
                elif 79.5 <= x < 82.5:
                    GPACourseLevel.append(2.67)
                elif 76.5 <= x < 79.5:
                    GPACourseLevel.append(2.33)
                elif 72.5 <= x < 76.5:
                    GPACourseLevel.append(2.00)
                elif 69.5 <= x < 72.5:
                    GPACourseLevel.append(1.67)
                elif 67 <= x < 69.5:
                    GPACourseLevel.append(1.33)
                elif 63 <= x < 67:
                    GPACourseLevel.append(1.00)
                elif 60 <= x < 63:
                    GPACourseLevel.append(0.67)
                elif x < 60:
                    GPACourseLevel.append(0.00)
            i = i + 1
        total = 0
        Credits = []
        totalcredit = 0
        for i in GPACoursenum:
            Credits.append(Overall["Credit学分"][i])
        global GPA
        if len(GPACourseLevel) != 0:
            for x in range(0, len(GPACourseLevel)):
                total += GPACourseLevel[x] * Credits[x]
                totalcredit += Credits[x]
            GPA = total / totalcredit
        else:
            GPA = "nan"
        GPAsql = pd.DataFrame([GPACourse, GPACourseGrade, GPACourseLevel, [], []],
                              index=["GPACourse", "GPACourseGrade", "GPACourseLevel", "GPA_GradeDetail_Links",
                                     "GPACourse_Details"], columns=GPACoursenum)
        CourselistPage_r = s.get("http://ams.bhsfic.com/student/courseclass/studentCourseLists")
        CourselistPage_Html = CourselistPage_r.content.decode("utf8")
        CourselistPage = BeautifulSoup(CourselistPage_Html, "html.parser")
        Courselist = pd.read_html(CourselistPage_Html)[0]
        GPA_Courselistnum = []
        for x in range(0, Courselist.shape[0]):
            for y in GPACourse:
                if y == Courselist.loc[x, "班课"]:
                    GPA_Courselistnum.append(x)
        medium = []
        for x in range(0, len(GPACourse)):
            for y in range(0, len(GPA_Courselistnum)):
                if Courselist.loc[GPA_Courselistnum[y], "班课"] == GPACourse[x]:
                    medium.append(GPA_Courselistnum[y])
        GPA_Courselistnum = medium
        links = []
        for link in CourselistPage.table.find_all("a"):
            links.append(link.get("href"))
        GradeDetail_Links = []
        for link in links:
            if type(link) == str:
                if link.find("gradeDetailPage") != -1:
                    GradeDetail_Links.append("http://ams.bhsfic.com" + link)
        GPA_GradeDetail_Links = []
        for x in GPA_Courselistnum:
            GPA_GradeDetail_Links.append(GradeDetail_Links[x])
        for x in range(0, GPAsql.shape[1]):
            GPAsql.loc["GPA_GradeDetail_Links", x] = GPA_GradeDetail_Links[x]
        global GPACourse_Details
        GPACourse_Details = []
        for x in GPACoursenum:
            if type(GPAsql.loc["GPACourseLevel", x]) == float:
                GPACourse_Details.append(pd.read_html(s.get(url=GPA_GradeDetail_Links[x]).content.decode("utf8")))
            else:
                GPACourse_Details.append("None")
        Details = []
        for x in range(0, len(GPACourse)):
            course = []
            for y in GPACourse_Details[x]:
                if type(y) == str:
                    one = 1
                else:
                    a = []
                    title = y.columns[0]
                    a.append(title)
                    for z in y.values.tolist():
                        detail_name = z[0]
                        detail_grade = z[2].replace(u'\xa0', u' ')
                        b = [detail_name, detail_grade]
                        a.append(b)
                    course.append(a)
            Details.append(course)
        return [len(GPACourse), round(GPA,3), GPACourse, GPACourseGrade, Details]
