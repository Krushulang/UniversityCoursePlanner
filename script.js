(async function () {
    var major = document.getElementById('major');
    var courses = document.getElementById('courselist');
    var department = document.getElementById('coursepick');
    var depts;
    var campusSelected;
    var curriculum = document.getElementById('curriculum')

    var checkedValues = [];
    var checkedOff;

    var bothell = {};
    fetch('/bothload')
        .then(function (response) {
            return response.json();
        }).then(function (data) {
            bothellResult = data;
            for (key in bothellResult) {
                bothell[key] = bothellResult[key];
            }
        });

    var bothellDep = {};
    fetch('/bdepartmentload')
        .then(function (response) {
            return response.json();
        }).then(function (data) {
            bothellResult = data;
            for (key in bothellResult) {
                bothellDep[key] = bothellResult[key];
            }
        });

    var bothellCir = {};
    fetch('/bcurriculumload')
        .then(function (response) {
            return response.json();
        }).then(function (data) {
            bothellResult = data;
            for (key in bothellResult) {
                bothellCir[key] = bothellResult[key];
            }
        });

    var majors;
    var departments = "";

    await new Promise(r => setTimeout(r, 1000));
    campusSelected = "bothell";
    for (key in bothell) {
        temp = bothell[key].split(" ", 3)  
        if(temp[2] == "your"){
            majors += '<option value="' + key + '">' + bothell[key] + '</option>';
        }
        else if(temp[2] == "Arts"){
            tempres = bothell[key].split("Bachelor of Arts ")[1]
            majors += '<option value="' + key + '">' + "B.A. " + tempres + '</option>';
        }
        else if(temp[2] == "Science"){
            tempres = bothell[key].split("Bachelor of Science ")[1]
            console.log(tempres)
            majors += '<option value="' + key + '">' + "B.S. " + tempres + '</option>';
        }
        else{
            majors += '<option value="' + key + '">' + bothell[key] + '</option>';
        }
    }
    major.innerHTML = majors;
    var j = 0;
    for (key in bothellDep) {
        var space = 12 - key.length;
        var actSpace = "";
        for (var i = 0; i < space; i++) {
            actSpace += "&nbsp"
        }
        departments += '<input class="depbox" type="checkbox" name="department" value="' + key + '">' + bothellDep[key] + actSpace;
        j++;
        if (j % 8 == 0) {
            departments += '<br />'
        }
    }
    department.innerHTML = departments;
    depts = document.forms["initform"].elements["department"];

    checkedValues = document.getElementsByClassName("depbox");
    if (depts) {
        for (dep in depts) {
            depts[dep].onclick = async function () {
                var courseslisted = {};
                var time = 0;
                courses.innerHTML = "";
                checkedOff = []
                checkedOff.push(campusSelected);
                for (key in checkedValues) {
                    if (checkedValues[key].checked) {
                        checkedOff.push(checkedValues[key].value);
                    }
                }
                await fetch('/courseSelection', {
                    method: "POST",
                    body: checkedOff
                })
                    .then(function (response) {
                        return response.json();
                    }).then(function (data) {
                        depResult = data;
                        for (key in depResult) {
                            time++;
                            courseslisted[key] = depResult[key];
                        }
                    });
                var courseResult = 'Please select courses from this list that you have taken <select class="form-select text-center" size="20" name="courses" multiple="multiple" id="courses" required>';
                for (key in courseslisted) {
                    courseResult += '<option class="courseList" value="' + key + '">' + courseslisted[key] + '</option>'
                }
                courseResult += '</select>'
                courses.innerHTML = courseResult;
                $('.courseList').mousedown(function (e) {
                    e.preventDefault();
                    $(this).prop('selected', !$(this).prop('selected'));
                    return false;
                });
            };
        }

    }


    var cirResult = '<select class="form-select text-center" size="20" name="curriculum" multiple="multiple" id="curriculum">';
    for (key in bothellCir) {
        cirResult += '<option value="' + key + '">' + key + '</option>'
    }
    cirResult += '</select>'
    curriculum.innerHTML = cirResult;
    $('option').mousedown(function (e) {
        e.preventDefault();
        $(this).prop('selected', !$(this).prop('selected'));
        return false;
    });



    //when user changes the type of select box
    function majorDropdown() {
        // console.log(checkedValues);
        if (this.value === 'choose') {
            // courses.innerHTML = '<option>Please select a major first</option>';
            return;
        }
        var course = getCourses(this.value);

        //loop to get options in the object to create options
        var options = '<option>Please choose the classes you have taken</option>';
        for (var key in course) {
            options += '<option value="' + key + '">' + course[key] + '</option>';
        }
        // courses.innerHTML = options;
    };

    function getCourses(courseType) {
        if (courseType === 'csse') {
            return csse;
        }
        else if (courseType === 'temp3') {
            return temp3;
        }
    }

    major.addEventListener('change', majorDropdown, false);


}());

var mySlider = new rSlider({
    target: '#slider1',
    values: [600, 630, 700, 730, 800, 830, 900, 930, 1000, 1030, 1100, 1130, 1200, 1230, 1300, 1330, 1400, 1430, 1500, 1530, 1600, 1630, 1700, 1750, 1800, 1830, 1900, 1930, 2000, 2030, 2100, 2130, 2200, 2230, 2300],
    range: true, // range slider
    labels: false,
    scale:false
});

var mySlider = new rSlider({
    target: '#slider2',
    values: [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200],
    range: true, // range slider
    labels: false,
    scale:false
});