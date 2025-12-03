var dom = document.getElementById('chart-container');
var myChart = echarts.init(dom, null, {
    renderer: 'canvas',
    useDirtyRect: false
});
var app = {};
var ROOT_PATH = 'http://127.0.0.1:8000/';

var option;

myChart.showLoading();
$.get(ROOT_PATH + 'china.json', function (chinaJson) {
    myChart.hideLoading();

    echarts.registerMap('China', chinaJson);

    option = {
        title: {
            text: '中国人口分布',
            subtext: '基于人口统计数据',
            left: 'center'
        },
        tooltip: {
            trigger: 'item',
            formatter: function (params) {
                // 检查value是否存在且为数字
                if (params.value && !isNaN(params.value)) {
                    // 格式化人口数量（例如：10000000 -> 1000万）
                    var value = params.value;
                    var formattedValue;
                    if (value >= 100000000) {
                        formattedValue = (value / 100000000).toFixed(2) + '亿';
                    } else if (value >= 10000) {
                        formattedValue = (value / 10000).toFixed(2) + '万';
                    } else {
                        formattedValue = value;
                    }
                    return params.name + ': ' + formattedValue;
                } else {
                    return params.name + ': 数据暂缺';
                }
            }
        },
        visualMap: {
            left: 'right',
            min: 1000000, // 最小人口数（可根据实际数据调整）
            max: 150000000, // 最大人口数（可根据实际数据调整）
            inRange: {
                color: [
                    '#313695',
                    '#4575b4',
                    '#74add1',
                    '#abd9e9',
                    '#e0f3f8',
                    '#ffffbf',
                    '#fee090',
                    '#fdae61',
                    '#f46d43',
                    '#d73027',
                    '#a50026'
                ]
            },
            text: ['高人口', '低人口'],
            calculable: true
        },
        toolbox: {
            show: true,
            left: 'left',
            top: 'top',
            feature: {
                dataView: {readOnly: false},
                restore: {},
                saveAsImage: {}
            }
        },
        series: [
            {
                name: '中国人口',
                type: 'map',
                roam: true, // 允许缩放和平移
                map: 'China',
                emphasis: {
                    label: {
                        show: true // 高亮时显示省份名称
                    }
                },
                data: [
                    {name: '北京市', value: 21880000},
                    {name: '天津市', value: 13870000},
                    {name: '河北', value: 74610000},
                    {name: '山西', value: 34920000},
                    {name: '内蒙古', value: 24050000},
                    {name: '辽宁', value: 42590000},
                    {name: '吉林', value: 23980000},
                    {name: '黑龙江', value: 31850000},
                    {name: '上海', value: 24890000},
                    {name: '江苏', value: 84750000},
                    {name: '浙江', value: 64570000},
                    {name: '安徽', value: 61030000},
                    {name: '福建', value: 41540000},
                    {name: '江西', value: 45190000},
                    {name: '山东', value: 101600000},
                    {name: '河南', value: 99410000},
                    {name: '湖北', value: 57750000},
                    {name: '湖南', value: 66440000},
                    {name: '广东', value: 126010000},
                    {name: '广西', value: 50130000},
                    {name: '海南', value: 10080000},
                    {name: '重庆', value: 32120000},
                    {name: '四川', value: 83710000},
                    {name: '贵州', value: 38560000},
                    {name: '云南', value: 47210000},
                    {name: '西藏', value: 3650000},
                    {name: '陕西', value: 39530000},
                    {name: '甘肃', value: 25020000},
                    {name: '青海', value: 5930000},
                    {name: '宁夏', value: 7200000},
                    {name: '新疆', value: 25850000},
                    {name: '台湾', value: 23310000},
                    {name: '香港', value: 7390000},
                    {name: '澳门', value: 680000}
                ]
            }
        ]
    };
    myChart.setOption(option);
});

if (option && typeof option === 'object') {
    myChart.setOption(option);
}

window.addEventListener('resize', myChart.resize);