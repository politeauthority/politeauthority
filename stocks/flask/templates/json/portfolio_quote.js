
//Flot Multiple Axes Line Chart
$(function() {
    var oilprices = [
        {%for q in quotes%}
            [
                new Date({{q.date.year}}, {{q.date.month}}, {{q.date.day}}).getTime(), 
                {{q.close|round(2)}}
            ],
        {%endfor%}
    ];

    function euroFormatter(v, axis) {
        return v.toFixed(axis.tickDecimals) + "€";
    }

    function doPlot(position) {
        $.plot($("#flot-line-chart-multi"), [{
            data: oilprices,
            label: "Company Price ($)",
            // points: 'triangle'
        }], {
            xaxes: [{
                mode: 'time',
                tickSize: [1, "month"],
                tickLength: 0,
                axisLabel: "2012",
                axisLabelUseCanvas: true,
                axisLabelFontSizePixels: 12,
                axisLabelFontFamily: 'Verdana, Arial',
                axisLabelPadding: 10
            }],
            yaxes: [{
                min: 0
            }, {
                // align if we are to the right
                alignTicksWithAxis: position == "right" ? 1 : null,
                position: position,
                tickFormatter: euroFormatter
            }],
            legend: {
                position: 'nw'
            },
            grid: {
                hoverable: true //IMPORTANT! this is needed for tooltip to work
            },
            tooltip: true,
            tooltipOpts: {
                content: "%s for %x was %y",
                xDateFormat: "%m %d",

                onHover: function(flotItem, $tooltipEl) {
                    // console.log(flotItem, $tooltipEl);
                }
            },
            colors: ["#5cb85c", "#0022FF"]

        });
    }

    doPlot("right");

    $("button").click(function() {
        doPlot($(this).text());
    });
});