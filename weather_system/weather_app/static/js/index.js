var dom = document.getElementById('chart-container');
var myChart = echarts.init(dom, null, {
    renderer: 'canvas',
    useDirtyRect: false
});
var app = {};
var ROOT_PATH = 'http://127.0.0.1:8000/';

var option;

var weather_data, date;

$.ajax(
    {
        url: ROOT_PATH + 'get_date',
        type: 'GET',
        dataType: 'json',
        success: function (res) {
            date = res.data;
            console.log(date);
        },
        error: function (res) {
            console.log(res);
        }
    }
)

myChart.showLoading();
$.get(ROOT_PATH + 'china.json', function (chinaJson) {
    myChart.hideLoading();

    echarts.registerMap('China', chinaJson);

    option = {
        title: {
            text: '中国人口分布',
            subtext: '基于人口统计数据',
            left: 'right'
        },
        tooltip: {
            trigger: 'item',
            formatter: function (params) {
                if (params.value && !isNaN(params.value)) {
                    // 安全检查value是否为有效数字
                    return [
                        '<div style="font-weight:bold;color:#333;padding-bottom:4px;border-bottom:1px solid #eee">' + params.name + '</div>',
                        '人口: ' + params.value+ ' 人',

                    ].join('<br/>');
                } else {
                    return params.name + ': 数据暂缺';
                }
            }
        },
        visualMap: {
            left: 'right',
            min: 1000000,
            max: 150000000,
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
                    {name: '河北省', value: 74610000},
                    {name: '山西省', value: 34920000},
                    {name: '内蒙古自治区', value: 24050000},
                    {name: '辽宁省', value: 42590000},
                    {name: '吉林省', value: 23980000},
                    {name: '黑龙江省', value: 31850000},
                    {name: '上海市', value: 24890000},
                    {name: '江苏省', value: 84750000},
                    {name: '浙江省', value: 64570000},
                    {name: '安徽省', value: 61030000},
                    {name: '福建省', value: 41540000},
                    {name: '江西省', value: 45190000},
                    {name: '山东省', value: 101600000},
                    {name: '河南省', value: 99410000},
                    {name: '湖北省', value: 57750000},
                    {name: '湖南省', value: 66440000},
                    {name: '广东省', value: 126010000},
                    {name: '广西壮族自治区', value: 50130000},
                    {name: '海南省', value: 10080000},
                    {name: '重庆市', value: 32120000},
                    {name: '四川省', value: 83710000},
                    {name: '贵州省', value: 38560000},
                    {name: '云南省', value: 47210000},
                    {name: '西藏自治区', value: 3650000},
                    {name: '陕西省', value: 39530000},
                    {name: '甘肃省', value: 25020000},
                    {name: '青海省', value: 5930000},
                    {name: '宁夏回族自治区', value: 7200000},
                    {name: '新疆维吾尔自治区', value: 25850000},
                    {name: '台湾省', value: 23310000},
                    {name: '香港特别行政区', value: 7390000},
                    {name: '澳门特别行政区', value: 680000}
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