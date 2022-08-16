var myChart = echarts.init(document.getElementById('K_line'), 'dark');
// , 'dark' 為暗色版
var option;

const upColor = '#00da3c';
const downColor = '#ec0000';

// 資料預處理函式建立
function splitData(rawData) {
    let categoryData = [];
    let values = [];
    let volumes = [];
    let name = [];
    for (let i = 0; i < rawData.length; i++) {
        name.push(rawData[i].splice(0, 1)[0]);
        categoryData.push(rawData[i].splice(0, 1)[0]);
        values.push(rawData[i]);
        volumes.push([i, rawData[i][4], rawData[i][0] > rawData[i][1] ? 1 : -1]);
    }
    return {
        categoryData: categoryData,
        values: values,
        volumes: volumes,
        name: name
    };
}

function splitData_MACD(rawData) {
    let name = [];
    let Data = [];
    let MACD_V = [];
    let MACDsignal = [];
    let MACDhist = [];
    for (let i = 0; i < rawData.length; i++) {
        name.push(rawData[i].splice(0, 1)[0]);
        Data.push(rawData[i].splice(0, 1)[0]);
        MACD_V.push(rawData[i].splice(0, 1)[0]);
        MACDsignal.push(rawData[i].splice(0, 1)[0]);
        MACDhist.push(rawData[i].splice(0, 1)[0]);
    }
    return {
      name: name,
      Data: Data,
      MACD_V: MACD_V,
      MACDsignal: MACDsignal,
      MACDhist: MACDhist,
    };
}

function splitData_Change_MK(rawData) {
    let name = [];
    let Data = [];
    let Change_MK = [];

    for (let i = 0; i < rawData.length; i++) {
        name.push(rawData[i].splice(0, 1)[0]);
        Data.push(rawData[i].splice(0, 1)[0]);
        Change_MK.push(rawData[i].splice(0, 1)[0]);
    }
    return {
      name: name,
      Data: Data,
      Change_MK: Change_MK,
    };
}

function splitData_BBAND(rawData) {
    let name = [];
    let categoryData = [];
    let values = [];
    let upper = [];
    let middle = [];
    let lower = [];
    for (let i = 0; i < rawData.length; i++) {
        name.push(rawData[i].splice(0, 1)[0]);
        categoryData.push(rawData[i].splice(0, 1)[0]);
        upper.push(rawData[i].splice(0, 1)[0]);
        middle.push(rawData[i].splice(0, 1)[0]);
        lower.push(rawData[i].splice(0, 1)[0]);
        values.push(rawData[i]);
    }
    return {
      name: name,
      categoryData: categoryData,
      values: values,
      upper: upper,
      middle: middle,
      lower: lower,
    };
}


// MA計算函式建立
function calculateMA(dayCount, data) {
    var result = [];
    for (var i = 0, len = data.values.length; i < len; i++) {
        if (i < dayCount) {
            result.push('-');
            continue;
        }
        var sum = 0;
        for (var j = 0; j < dayCount; j++) {
            sum += data.values[i - j][1];
        }
        result.push(+(sum / dayCount).toFixed(3));
    }
    return result;
}

// 搜尋時頁面: 將search_from取得的股票號碼連同post請求一起傳到後端，取得資料後進行繪圖
function check_search_from(){
  if (!search_from.q.value.length){
    alert('請填 股票資訊');
    return false;
  }
  // serialize()會將表單值序列化
  $.post('/K_line', $(search_from).serialize(), function(data){
    //成功取得資料後進行資料處理
    // console.log(typeof(data));
    // 因為這邊取得的資料型態為字串，所以需要透過eval()將其轉為js物件，才可正常執行splitData()
    var data = splitData(eval(data)); 
    // console.log(data.categoryData);
    // 開始繪圖
    myChart.setOption(
    (option = {
      animation: false,
      legend: {
        bottom: 10,
        left: 'center',
        data: [data.name[0], 'MA5', 'MA10', 'MA20', 'MA30']
      },
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'cross'
        },
        borderWidth: 1,
        borderColor: '#ccc',
        padding: 10,
        textStyle: {
          color: '#000'
        },
        position: function (pos, params, el, elRect, size) {
          const obj = {
            top: 10
          };
          obj[['left', 'right'][+(pos[0] < size.viewSize[0] / 2)]] = 30;
          return obj;
        }
        // extraCssText: 'width: 170px'
      },
      axisPointer: {
        link: [
          {
            xAxisIndex: 'all'
          }
        ],
        label: {
          backgroundColor: '#777'
        }
      },
      toolbox: {
        feature: {
          dataZoom: {
            yAxisIndex: false
          },
          brush: {
            type: ['lineX', 'clear']
          }
        }
      },
      brush: {
        xAxisIndex: 'all',
        brushLink: 'all',
        outOfBrush: {
          colorAlpha: 0.1
        }
      },
      visualMap: {
        show: false,
        seriesIndex: 5,
        dimension: 2,
        pieces: [
          {
            value: 1,
            color: downColor
          },
          {
            value: -1,
            color: upColor
          }
        ]
      },
      grid: [
        {
          left: '10%',
          right: '8%',
          height: '50%'
        },
        {
          left: '10%',
          right: '8%',
          top: '63%',
          height: '16%'
        }
      ],
      xAxis: [
        {
          type: 'category',
          data: data.categoryData,
          boundaryGap: false,
          axisLine: { onZero: false },
          splitLine: { show: false },
          min: 'dataMin',
          max: 'dataMax',
          axisPointer: {
            z: 100
          }
        },
        {
          type: 'category',
          gridIndex: 1,
          data: data.categoryData,
          boundaryGap: false,
          axisLine: { onZero: false },
          axisTick: { show: false },
          splitLine: { show: false },
          axisLabel: { show: false },
          min: 'dataMin',
          max: 'dataMax'
        }
      ],
      yAxis: [
        {
          scale: true,
          splitArea: {
            show: true
          }
        },
        {
          scale: true,
          gridIndex: 1,
          splitNumber: 2,
          axisLabel: { show: false },
          axisLine: { show: false },
          axisTick: { show: false },
          splitLine: { show: false }
        }
      ],
      // 下方橫條設定
      dataZoom: [
        {
          type: 'inside',
          xAxisIndex: [0, 1],
          start: 50,
          end: 100
        },
        {
          show: true,
          xAxisIndex: [0, 1],
          type: 'slider',
          top: '85%',
          start: 98,
          end: 100
        }
      ],
      // 滑鼠移過時顯示的資料設定
      series: [
        {
          name: data.name[0],
          type: 'candlestick',
          data: data.values,
          itemStyle: {
            color: upColor,
            color0: downColor,
            borderColor: undefined,
            borderColor0: undefined
          },
          tooltip: {
            formatter: function (param) {
              param = param[0];
              return [
                'Date: ' + param.name + '<hr size=1 style="margin: 3px 0">',
                'Open: ' + param.data[0] + '<br/>',
                'Close: ' + param.data[1] + '<br/>',
                'Lowest: ' + param.data[2] + '<br/>',
                'Highest: ' + param.data[3] + '<br/>'
              ].join('');
            }
          }
        },
        {
          name: 'MA5',
          type: 'line',
          data: calculateMA(5, data),
          smooth: true,
          lineStyle: {
            opacity: 0.5
          }
        },
        {
          name: 'MA10',
          type: 'line',
          data: calculateMA(10, data),
          smooth: true,
          lineStyle: {
            opacity: 0.5
          }
        },
        {
          name: 'MA20',
          type: 'line',
          data: calculateMA(20, data),
          smooth: true,
          lineStyle: {
            opacity: 0.5
          }
        },
        {
          name: 'MA30',
          type: 'line',
          data: calculateMA(30, data),
          smooth: true,
          lineStyle: {
            opacity: 0.5
          }
        },
        {
          name: 'Volume',
          type: 'bar',
          xAxisIndex: 1,
          yAxisIndex: 1,
          data: data.volumes
        }
      ]
    }),
    true
  )

  });
  
  $.post('/MACD', $(search_from).serialize(), function(data){
    var data = splitData_MACD(eval(data));
    MACD_lin(data);
  });
  
  $.post('/Change_MK', $(search_from).serialize(), function(data){
    var data = splitData_Change_MK(eval(data));
    Change_MK_lin(data);
  });
  
  $.post('/BBAND', $(search_from).serialize(), function(data){
    var data = splitData_BBAND(eval(data));
    BBAND_lin(data);
  });
  
  
  
  // 由於已用jquery.post的方式讓表格資料回傳，所以回傳false，阻止onsubmit提交
  return false;
}


// 預設頁面: 發送ajax請求，從後台獲取json數據
$(document).ready(function () {  
//   getData_BBAND();
//   getData_Change_MK();
//   getData_MACD();
  getData_Kline();
  // console.log(app.rawData);
});


// 以下為K_line

function getData_Kline() {
$.ajax({

url:'/K_line',
data:{},
type:'POST',
async:false,
dataType:'json',

success:function(data) {
// 成功取得資料後進行資料預處理
// console.log(typeof(data));
// console.log(data);
var data = splitData(data);
// console.log(data);
// 開始繪圖
myChart.setOption(
    (option = {
      
      animation: false,
      title: {
        text: 'K_line'
      },
      legend: {
        bottom: 10,
        left: 'center',
        data: [data.name[0], 'MA5', 'MA10', 'MA20', 'MA30']
      },
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'cross'
        },
        borderWidth: 1,
        borderColor: '#ccc',
        padding: 10,
        textStyle: {
          color: '#000'
        },
        position: function (pos, params, el, elRect, size) {
          const obj = {
            top: 10
          };
          obj[['left', 'right'][+(pos[0] < size.viewSize[0] / 2)]] = 30;
          return obj;
        }
        // extraCssText: 'width: 170px'
      },
      axisPointer: {
        link: [
          {
            xAxisIndex: 'all'
          }
        ],
        label: {
          backgroundColor: '#777'
        }
      },
      toolbox: {
        feature: {
          dataZoom: {
            yAxisIndex: false
          },
          brush: {
            type: ['lineX', 'clear']
          }
        }
      },
      brush: {
        xAxisIndex: 'all',
        brushLink: 'all',
        outOfBrush: {
          colorAlpha: 0.1
        }
      },
      visualMap: {
        show: false,
        seriesIndex: 5,
        dimension: 2,
        pieces: [
          {
            value: 1,
            color: downColor
          },
          {
            value: -1,
            color: upColor
          }
        ]
      },
      grid: [
        {
          left: '10%',
          right: '8%',
          height: '50%'
        },
        {
          left: '10%',
          right: '8%',
          top: '63%',
          height: '16%'
        }
      ],
      xAxis: [
        {
          type: 'category',
          data: data.categoryData,
          boundaryGap: false,
          axisLine: { onZero: false },
          splitLine: { show: false },
          min: 'dataMin',
          max: 'dataMax',
          axisPointer: {
            z: 100
          }
        },
        {
          type: 'category',
          gridIndex: 1,
          data: data.categoryData,
          boundaryGap: false,
          axisLine: { onZero: false },
          axisTick: { show: false },
          splitLine: { show: false },
          axisLabel: { show: false },
          min: 'dataMin',
          max: 'dataMax'
        }
      ],
      yAxis: [
        {
          scale: true,
          splitArea: {
            show: true
          }
        },
        {
          scale: true,
          gridIndex: 1,
          splitNumber: 2,
          axisLabel: { show: false },
          axisLine: { show: false },
          axisTick: { show: false },
          splitLine: { show: false }
        }
      ],
      // 下方橫條設定
      dataZoom: [
        {
          type: 'inside',
          xAxisIndex: [0, 1],
          start: 50,
          end: 100
        },
        {
          show: true,
          xAxisIndex: [0, 1],
          type: 'slider',
          top: '85%',
          start: 98,
          end: 100
        }
      ],
      // 滑鼠移過時顯示的資料設定
      series: [
        {
          name: data.name[0],
          type: 'candlestick',
          data: data.values,
          itemStyle: {
            color: upColor,
            color0: downColor,
            borderColor: undefined,
            borderColor0: undefined
          },
          tooltip: {
            formatter: function (param) {
              param = param[0];
              return [
                'Date: ' + param.name + '<hr size=1 style="margin: 3px 0">',
                'Open: ' + param.data[0] + '<br/>',
                'Close: ' + param.data[1] + '<br/>',
                'Lowest: ' + param.data[2] + '<br/>',
                'Highest: ' + param.data[3] + '<br/>'
              ].join('');
            }
          }
        },
        {
          name: 'MA5',
          type: 'line',
          data: calculateMA(5, data),
          smooth: true,
          lineStyle: {
            opacity: 0.5
          }
        },
        {
          name: 'MA10',
          type: 'line',
          data: calculateMA(10, data),
          smooth: true,
          lineStyle: {
            opacity: 0.5
          }
        },
        {
          name: 'MA20',
          type: 'line',
          data: calculateMA(20, data),
          smooth: true,
          lineStyle: {
            opacity: 0.5
          }
        },
        {
          name: 'MA30',
          type: 'line',
          data: calculateMA(30, data),
          smooth: true,
          lineStyle: {
            opacity: 0.5
          }
        },
        {
          name: 'Volume',
          type: 'bar',
          xAxisIndex: 1,
          yAxisIndex: 1,
          data: data.volumes
        }
      ]
    }),
    true
  )

},
error:function (msg) {
console.log(msg);
alert('系統發生錯誤');
}
})
};
// setInterval(getData,10000); //自動輪尋，10秒一次，動態刷新(先不要開，電腦撐不住)


// 以下為MACD

var chartDom = document.getElementById('MACD');
// var MACD = echarts.init(chartDom, 'dark');
var option;


function getData_MACD() {
$.ajax({

url:'/MACD',
data:{},
type:'POST',
async:false,
dataType:'json',

success:function(data) {
// 成功取得資料後進行資料預處理
var data = splitData_MACD(data);
// console.log(typeof(data));
// console.log(data.Data);
// console.log(data.MACD_V);
// console.log(data.MACDsignal);
// console.log(data.MACDhist);
// console.log(data);
// console.log(data);
// 開始繪圖
MACD_lin(data);

},
error:function (msg) {
console.log(msg);
alert('系統發生錯誤');
}


})
};

function MACD_lin(_rawData) {
  option = {
  title: {
    text: 'MACD'
  },
  tooltip: {
    trigger: 'axis'
  },
  legend: {
    data: ['MACD', 'MACDhist', 'MACDsignal']
  },
  grid: {
    left: '3%',
    right: '4%',
    bottom: '3%',
    containLabel: true
  },
  toolbox: {
    feature: {
      saveAsImage: {}
    }
  },
  xAxis: {
    type: 'category',
    boundaryGap: false,
    data: _rawData.Data,
    axisLine: { onZero: false },
    splitLine: { show: false },
    min: 'dataMin',
    max: 'dataMax',
    axisPointer: {
      z: 100
    }
  },
  yAxis: {
    type: 'value'
  },
  series: [
    {
      name: 'MACD',
      type: 'line',
      stack: 'Total',
      data: _rawData.MACD_V,
    },
    {
      name: 'MACDhist',
      type: 'line',
      stack: 'Total',
      data: _rawData.MACDhist,
    },
    {
      name: 'MACDsignal',
      type: 'line',
      stack: 'Total',
      data: _rawData.MACDsignal,
    }
  ],
  backgroundColor: '#191C24',
};
  MACD.setOption(option);
}
option && MACD.setOption(option);


// 以下為Change_MK

var chartDom = document.getElementById('Change_MK');
var Change_MK = echarts.init(chartDom, 'dark');
var option;


function getData_Change_MK() {
$.ajax({

url:'/Change_MK',
data:{},
type:'POST',
async:false,
dataType:'json',

success:function(data) {
// 成功取得資料後進行資料預處理
var data = splitData_Change_MK(data);
// console.log(typeof(data));
// console.log(data.Data);
// console.log(data.Change_MK);

// 開始繪圖
Change_MK_lin(data);
},
error:function (msg) {
console.log(msg);
alert('系統發生錯誤');
}


})
};

function Change_MK_lin(_rawData) {
  option = {
  title: {
    text: 'Change_MK'
  },
  tooltip: {
    trigger: 'axis'
  },
  legend: {
    data: ['Change_MK']
  },
  grid: {
    left: '3%',
    right: '4%',
    bottom: '3%',
    containLabel: true
  },
  toolbox: {
    feature: {
      saveAsImage: {}
    }
  },
  xAxis: {
    type: 'category',
    boundaryGap: false,
    data: _rawData.Data,
    axisLine: { onZero: false },
    splitLine: { show: false },
    min: 'dataMin',
    max: 'dataMax',
    axisPointer: {
      z: 100
    }
  },
  yAxis: {
    type: 'value'
  },
  series: [
    {
      name: 'Change_MK',
      type: 'line',
      stack: 'Total',
      data: _rawData.Change_MK,
    }
  ]
};
  Change_MK.setOption(option);
}
option && Change_MK.setOption(option);


// 以下為BBAND

var chartDom = document.getElementById('BBAND');
var BBAND = echarts.init(chartDom, 'dark');
var option;


function getData_BBAND() {
$.ajax({

url:'/BBAND',
data:{},
type:'POST',
async:false,
dataType:'json',

success:function(data) {
// 成功取得資料後進行資料預處理
var data = splitData_BBAND(data);
console.log(typeof(data));
console.log(data);
console.log(data.value);

// 開始繪圖
BBAND_lin(data);
},
error:function (msg) {
console.log(msg);
alert('系統發生錯誤');
}
})
};

function BBAND_lin(data) {
  option = {
      animation: false,
      title: {
        text: 'BBAND'
      },
      legend: {
        bottom: 10,
        left: 'center',
        data: [data.name[0], 'upper', 'middle', 'lower']
      },
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'cross'
        },
        borderWidth: 1,
        borderColor: '#ccc',
        padding: 10,
        textStyle: {
          color: '#000'
        },
        position: function (pos, params, el, elRect, size) {
          const obj = {
            top: 10
          };
          obj[['left', 'right'][+(pos[0] < size.viewSize[0] / 2)]] = 30;
          return obj;
        }
        // extraCssText: 'width: 170px'
      },
      axisPointer: {
        link: [
          {
            xAxisIndex: 'all'
          }
        ],
        label: {
          backgroundColor: '#777'
        }
      },
      toolbox: {
        feature: {
          dataZoom: {
            yAxisIndex: false
          },
          brush: {
            type: ['lineX', 'clear']
          }
        }
      },
      brush: {
        xAxisIndex: 'all',
        brushLink: 'all',
        outOfBrush: {
          colorAlpha: 0.1
        }
      },
      visualMap: {
        show: false,
        seriesIndex: 5,
        dimension: 2,
        pieces: [
          {
            value: 1,
            color: downColor,
          },
          {
            value: -1,
            color: upColor,

          }
        ],

      },
      grid: [
        {
          left: '10%',
          right: '8%',
          height: '50%'
        },
        {
          left: '10%',
          right: '8%',
          top: '63%',
          height: '16%'
        }
      ],
      xAxis: [
        {
          type: 'category',
          data: data.categoryData,
          boundaryGap: false,
          axisLine: { onZero: false },
          splitLine: { show: false },
          min: 'dataMin',
          max: 'dataMax',
          axisPointer: {
            z: 100
          }
        },
        {
          type: 'category',
          gridIndex: 1,
          data: data.categoryData,
          boundaryGap: false,
          axisLine: { onZero: false },
          axisTick: { show: false },
          splitLine: { show: false },
          axisLabel: { show: false },
          min: 'dataMin',
          max: 'dataMax'
        }
      ],
      yAxis: [
        {
          scale: true,
          splitArea: {
            show: true
          }
        },
        {
          scale: true,
          gridIndex: 1,
          splitNumber: 2,
          axisLabel: { show: false },
          axisLine: { show: false },
          axisTick: { show: false },
          splitLine: { show: false }
        }
      ],
      // 下方橫條設定
      dataZoom: [
        {
          type: 'inside',
          xAxisIndex: [0, 1],
          start: 50,
          end: 100
        },
        {
          show: true,
          xAxisIndex: [0, 1],
          type: 'slider',
          top: '85%',
          start: 98,
          end: 100
        }
      ],
      // 滑鼠移過時顯示的資料設定
      series: [
        {
          name: data.name[0],
          type: 'candlestick',
          data: data.values,
          itemStyle: {
            color: upColor,
            color0: downColor,
            borderColor: undefined,
            borderColor0: undefined,
            opacity: 0.4
          },
          tooltip: {
            formatter: function (param) {
              param = param[0];
              return [
                'Date: ' + param.name + '<hr size=1 style="margin: 3px 0">',
                'Open: ' + param.data[0] + '<br/>',
                'Close: ' + param.data[1] + '<br/>',
                'Lowest: ' + param.data[2] + '<br/>',
                'Highest: ' + param.data[3] + '<br/>'
              ].join('');
            }
          }
        },
        {
          name: 'upper',
          type: 'line',
          data: data.upper,
          // smooth: true,
          lineStyle: {
            opacity: 1
          }
        },
        {
          name: 'middle',
          type: 'line',
          data: data.middle,
          // smooth: true,
          lineStyle: {
            opacity: 1
          }
        },
        {
          name: 'lower',
          type: 'line',
          data: data.lower,
          // smooth: true,
          lineStyle: {
            opacity: 1,
            type:'solid'
          }
        },
        // {
        //   name: 'Volume',
        //   type: 'bar',
        //   xAxisIndex: 1,
        //   yAxisIndex: 1,
        //   data: data.volumes
        // }
      ]
    };
  BBAND.setOption(option);
}
option && BBAND.setOption(option);

