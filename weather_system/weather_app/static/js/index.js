// 绑定控件时间
document.getElementById('date_slider').addEventListener('input', update);

var dom = document.getElementById('chart-container');
var myChart = echarts.init(dom, null, {
    renderer: 'canvas', useDirtyRect: false
});
var app = {};
var ROOT_PATH = 'http://127.0.0.1:8000/';

var option;

let date_list;
let province_id;

//            定义方法
//   获得时间
async function get_date() {
    try {
        const userData = await $.ajax({
            url: ROOT_PATH + 'get_date', type: 'GET', dataType: 'json'
        });
        return userData.data;
    } catch (error) {
        console.log(error)
        return null;
    }
}


// 设置允许时间
function update_date(date_list) {
    var date = document.getElementById('date_slider');
    $('#r-value').text(date_list[date.value - 1]['date']);
    var now_date = date_list[date.value - 1]['date'];
    console.log(date_list[date.value - 1]['date']);
    return now_date;
}


// 获得各个省份ID
async function get_province_id() {
    try {
        const res = await $.ajax({
            url: ROOT_PATH + 'province_ID', type: 'GET', dataType: 'json'
        });
        return res.data;
    } catch (error) {
        console.error("error", error);
        return [];
    }
}

// 通过省份ID和时间获得省份天气数据
async function get_weather(province_id, date) {
    const weather_data = await $.ajax({
        url: ROOT_PATH + 'province_weather', data: {province: province_id, date: date}, type: 'GET', dataType: 'json',
    });
    return weather_data.data;
}

// 获得最大和最小气温
async function get_max_and_min_temperature() {
    const max_temperature = await $.ajax({
        url: ROOT_PATH + 'max_temperature', type: 'GET', dataType: 'json'
    })

    const min_temperature = await $.ajax({
        url: ROOT_PATH + 'min_temperature', type: 'GET', dataType: 'json'
    })
    return [max_temperature.data, min_temperature.data];
}


// 更新地图数据
function updateMapData(data) {
    myChart.setOption({
        series: [{"data": data}]
    });
}

// 更新地图天气数据
function updateMapTemperature(max_temperature, min_temperature) {
    myChart.setOption([{
        visualMap: {min: min_temperature, max: max_temperature}
    }])
}

async function update() {
    var now_date = update_date(date_list);

    // 获得data数据
    const promises = Object.values(province_id).map(id => get_weather(id, now_date));
    var data = await Promise.all(promises);

    console.log(data);
    // 更新地图数据
    updateMapData(data);
}


(async () => {
    // 获得时间列表
    date_list = await get_date();
    // 获得省份列表
    province_id = await get_province_id();
    // 当前时间
    var now_date = date_list[0]['date'];

    console.log(date_list);
    console.log(province_id);

    // 设置地图最低和最高温度
    const temperature = await get_max_and_min_temperature();
    var max_temperature = temperature[0][0], min_temperature = temperature[1][0];
    updateMapTemperature(max_temperature, min_temperature);
    console.log(max_temperature, min_temperature);

    // 获得data数据
    const promises = Object.values(province_id).map(id => get_weather(id, now_date));
    var data = await Promise.all(promises);

    console.log(data);
    // 更新地图数据
    updateMapData(data);
})();


myChart.showLoading();
$.get(ROOT_PATH + 'china.json', function (chinaJson) {
    myChart.hideLoading();

    echarts.registerMap('China', chinaJson);

    option = {
        title: {
            text: '中国天气信息', subtext: '数据来源中国气象局', left: 'right'
        }, tooltip: {
            trigger: 'item', formatter: function (params) {
                if (params.value && !isNaN(params.value)) {
                    return ['<div style="font-weight:bold;color:#333;padding-bottom:4px;border-bottom:1px solid #eee">' + params.name + '</div>', '人口: ' + params.value + ' 人',].join('<br/>');
                } else {
                    return params.name + ': 数据暂缺';
                }
            }
        }, visualMap: {
            left: 'right', min: -30, max: 40, inRange: {
                color: ['#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', '#ffffbf', '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026']
            }, text: ['高气温', '低气温'], calculable: true
        }, toolbox: {
            show: true, left: 'left', top: 'top', feature: {
                dataView: {readOnly: false}, restore: {}, saveAsImage: {}
            }
        }, series: [{
            name: '中国人口', type: 'map', roam: true, // 允许缩放和平移
            map: 'China', emphasis: {
                label: {
                    show: true // 高亮时显示省份名称
                }
            }, data: []
        }]
    };
    myChart.setOption(option);
});


window.addEventListener('resize', myChart.resize);