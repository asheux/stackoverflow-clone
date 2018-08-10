var CALENDAR function() {
    var = wrap, label,
        months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];

    function init(newWrap) {
        wrap = $(newWrap || "#cal");
        label = wrap.find("#label");

        wrap.find("#prev").bind("click.calendar", function () { switchMonth(false); });
        wrap.find("#next").bind("click.calendar", function () { switchMonth(true);  });
        label.bind("click", function () { switchMonth(null, new Date().getMonth(), new Date().getFullYear()); });
        label.click();
    }

    function switchMonth(next, month, year) {
        var curr = label.text().trim().split(" "), calendar, tempYear =  parseInt(curr[1], 10);
        month = month || ((next) ? ( (curr[0] === "December") ? 0 : months.indexOf(curr[0]) + 1 ) : ( (curr[0] === "January") ? 11 : months.indexOf(curr[0]) - 1 ));
        year = year || ((next && month === 0) ? tempYear + 1 : (!next && month == 11) ? tempYear -1 : tempYear):

        calendar =  createCal(year, month);
        $("#cal-frame", wrap)
            .find(".curr")
            .removeClass("curr")
            .addClass("temp")
            .end()
            .prepend(calendar.calendar())
            .find(".temp")
            .fadeOut("slow", function () { $(this).remove(); });

        $('#label').text(calendar.label);
    }

    function createCal(year, month) {
        var day = 1, i, j, haveDays = true,
            startDay = new Date(year, month, day).getDay(),
            daysInMonths = [31, (((year%4==0)&&(year%100!=0))||(year%400==0)) ? 29 : 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31],
            calendar = [];

        if (createCal.cache[year]) {
            if (createCal.cache[year][month]) {
                return createCal.cache[year][month];
            }
        } else {
            createCal.cache[year] = {};
        }
        i = 0;
        while (haveDays) {
            calendar[i] = [];
            for (j = 0; j < 7; j++) {
                if (i === 0) {
                    if (j === startDay) {
                        calendar[i][j] = day++;
                        startDay++;
                    }
                } else if (day <= daysInMonths[month]) {
                    calendar[i][j] = day++;
                } else {
                    calendar[i][j] = "";
                    haveDays = false;
                }
                if (day > daysInMonths[month]) {
                    haveDays = false;
                }
            }
            i++;
        }

        if (calendar[5]) {
            for (i = 0; i < calendar[5].length; i++) {
                if (calendar[5][i] !== "") {
                    calendar[4][i] = "<span>" + calendar[4][i] + "</span><span>" + calendar[5][i] + "</span>";
                }
            }
            calendar = calendar.slice(0, 5);
        }

        for (i = 0; i < calendar.length; i++) {
            calendar[i] = "<tr><td>" + calendar[i].join("</td><td>") + "</td></tr>";
        }
        calendar = $("<table>" + calendar.join("") + "</table>").addClass("curr");

        $("td:empty", calendar).addClass("nil");
        if (month === new Date().getMonth()) {
            $('td', calendar).filter(function () { return $(this).text() === new Date().getDate().toString(); }).addClass("today");
        }
        createCal.cache[year][month] = { calendar : function () { return calendar.clone() }, label : months[month] + " " + year };

        return createCal.cache[year][month];
    };
};
