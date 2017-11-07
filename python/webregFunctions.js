console.log(timeConvSE(17,0,17,50))
//console.log(dayConvNum2Str(4))

function dayConvNum2Str(dayCode)
{
    var dayStr = "";
    if (/1/.test(dayCode))
    {
        dayStr = dayStr
            + "M";
    }
    if (/2/.test(dayCode))
    {
        dayStr = dayStr
            + "Tu";
    }
    if (/3/.test(dayCode))
    {
        dayStr = dayStr
            + "W";
    }
    if (/4/.test(dayCode))
    {
        dayStr = dayStr
            + "Th";
    }
    if (/5/.test(dayCode))
    {
        dayStr = dayStr
            + "F";
    }
    if (/6/.test(dayCode))
    {
        dayStr = dayStr
            + "Sa";
    }
    if (/7/.test(dayCode))
    {
        dayStr = dayStr
            + "Su";
    }
    return dayStr;
}

function timeConvSE(beginHH, beginMM, endHH, endMM)
{
    var timeStr = "TBA";
    var beginHM = beginHH
        + ":"
        + beginMM;
    var endHM = endHH
        + ":"
        + endMM;

    beginHM = timeConv24To12(beginHM);
    endHM = timeConv24To12(endHM);

    if (beginHH == 0
        && beginMM == 0
        && endHH == 0
        && endMM == 0)
    {
        timeStr = "TBA";
    }
    else
    {
        timeStr = beginHM
            + "-"
            + endHM;
    }
    return timeStr;
}

function timeConv24To12(timeMH)
{
    // 08:35 => 08:35a
    // 0835 => 08:35a
    // dateNum 901315 Sun 01:15PM

    if (undefined == timeMH)
    {
        return "TBA";
    }

    var hour = "";
    var min = "";
    if (-1 == timeMH.indexOf(':'))
    {
        hour = timeMH.substring(0, 2);
        min = String("0"
            + timeMH.substring(2)).slice(-2);
    }
    else
    {
        var arr = timeMH.split(":");
        hour = arr[0];
        min = String("0"
            + arr[1]).slice(-2);
    }

    var ampm = "a";
    var timeStr = "";

    if (hour > 12)
    {
        ampm = "p";
        hour = hour - 12;
    }
    else if (hour == 12)
    {
        ampm = "p";
    }
    timeStr = hour
        + ":"
        + min
        + ampm;
    return timeStr;
}
