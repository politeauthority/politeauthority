$(function() {

    Morris.Area({
        element: 'quote-area-chart',
        data: [
            {%for q in quotes%}
                {%if q[7] and q[3] and q[4] and q[5]%}
                    {
                        period: '{{q[7]}}',
                        price: {{q[3]}},
                        high: {{q[4]}},
                        low: {{q[5]}}
                    },
                {%endif%}
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
