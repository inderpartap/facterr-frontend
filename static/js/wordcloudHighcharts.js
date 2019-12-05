Highcharts.chart('container', {
    series: [{
        type: 'wordcloud',
        data: [{"test":20},{"test2":10}],
        name: 'Occurrences'
    }],
    title: {
        text: 'Wordcloud of words in real news'
    }
});