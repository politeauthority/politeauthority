$(function() {

    Morris.Area({
        element: 'quote-area-chart',
        data: [
            {%for q in quotes%}
                {
                    period: '{{q.date}}',
                    price: {{q.close}},
                    high: {{q.high}},
                    low: {{q.low}}
                },
            {%endfor%}
        ],
        xkey: 'period',
        ykeys: ['price', 'high', 'low'],
        labels: ['Close', 'High', 'Low'],
        pointSize: 2,
        hideHover: 'auto',
        resize: true
    });
});
