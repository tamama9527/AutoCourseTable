
function isAvailable(v) {
    const course = ["106_1", "106_2"];
    return course.indexOf(v) != -1;
}

function parseClassInfo() {
    const param = parseParam();
    let filename;
    let header;
    if (param && isAvailable(param)) {
        filename = param + "_course.json";
        header = param.substr(0, 3)+ "學年度第" + param.substr(4, 1) + "學期課程資訊(課表)";
    } else {
        const today=new Date();
        const month = today.getMonth();
        const year = today.getFullYear();
        if (month+1>=2 && month+1 <= 7) {
            filename = (year-1911-1) + "_2_course.json";
            header = (year-1911-1) + "學年度第2學期課程資訊(課表)";
        } else {
            if (month < 2) {
                filename = (year-1911-1) + "_1_course.json";
                header = (year-1911-1);
            } else {
                filename = (year-1911) + "_1_course.json";
                header = (year-1911);
            }
            header +="學年度第1學期課程資訊(課表)";
        }
    }
    $('#header').text(header);
    $.getJSON('static/json/'+filename, function (lessonData) {
        const TimeData = lessonData["Time"], CourseData = lessonData["Course"];
        setTimeData(TimeData);
        setCourseData(CourseData);
    });
}

function getSyle(statusCode) {
    const statusTable = JSON.parse('{"-99": "unsure", "-1": "club", "0": "student", "1": "ta"}');
    return (statusCode in statusTable)  ? (statusTable[statusCode]) : "Error";
}

function getStatus(status) {
    const statusTable = JSON.parse('{"-99": "未確認", "-1": "社團課程", "0": "學生", "1": "教學助理"}');
    return status in statusTable ? statusTable[status] : "Error";
}

function getFor(forCode) {
    const forCodeTable = JSON.parse('{"-1": "未知", "-1": "課外", "0": "學士", "1": "碩士", "2": "博士"}');
    return forCode in forCodeTable ? forCodeTable[forCode] : "Error";
}

function setTimeData(TimeData) {
    for (let key in TimeData) {
        $("td#t"+key).html("第"+key+"節<br/>"+TimeData[key]);
    }
}

function setCourseData(CourseData) {
    let noTimeCourse = 0;
    for (let key in CourseData) {
        if (CourseData.hasOwnProperty(key)) {
            const Course = CourseData[key];
            const TimeData = Course["time"];
            if ($.isEmptyObject(TimeData)) {
                $('ul#Other').append('<li>'+Course["name"]+'</li>');
                noTimeCourse += 1;
            } else {
                for (let time in TimeData) {
                    if (TimeData.hasOwnProperty(time)) {
                        let target = $("td#"+time);
                        if (target.html() != "") {
                            target.html("<i class=\"warning sign icon\"></i>衝突<i class=\"warning sign icon\"></i>");
                            target.addClass("Error");
                        } else {
                            target.html(Course["name"] + "<br>" + TimeData[time] + "<br>" + Course["teacher"]);
                            target.addClass(getSyle(Course["status"]));
                            let popupContent = "";
                            /*
                            if (Course.hasOwnProperty("for")) {
                                popupContent += getFor(Course["for"]) + "課程 / " + getStatus(Course["status"]) + "<br>";
                            }
                            */
                            popupContent += "選課代號：" + key + "<br>";
                            if (Course.hasOwnProperty("point")) {
                                popupContent += "學分數：" + Course["point"];
                            }
                            if (popupContent) {
                                target.attr("data-html", popupContent);
                                target.attr("data-variation", "inverted");
                                target.addClass("popup inver");
                                target.popup();
                            }
                        }
                    }
                }
            }
        }
    }
    if (noTimeCourse === 0) {
        $('div#noTime').hide();
    }
}

function parseParam() {
    let strUrl = location.search;
    let getPara, ParaVal;
    let aryPara = [];
    if (strUrl.indexOf("?") != -1) {
        let getSearch = strUrl.split("?");
        getPara = getSearch[1].split("&");
        for (let i = 0; i < getPara.length; i++) {
            ParaVal = getPara[i].split("=");
            aryPara.push(ParaVal[0]);
            aryPara[ParaVal[0]] = decodeURI(ParaVal[1]);
        }
    }
    if ("v" in aryPara) {
        return aryPara["v"];
    } else {
        return false;
    }
}
