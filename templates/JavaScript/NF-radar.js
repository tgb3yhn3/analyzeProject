function radar_test() {
       var radarChart = document.getElementById("radarChart");
       var value_max = [108000, 709.31, 96.6, 31.5, 1]
       var value_min = [1100, 0.5, 5.3, 0, 0]
       // setup 
       const data = {
              labels: ['WBC(0-22000)', 'CRP(0-240)', 'SEG(0-100)', 'Band(0-2)', 'Sea Water(0、1)'],
              datasets: [{
                     label: 'NF中位數',
                     data: [0.120673527
                            , 0.178990138
                            , 0.850492881
                            , 0.015873016
                            , 0.385057471],
                     //borderColor: "rgba(238,50,30,0.9)",            //邊框紅色，微透明  
                     backgroundColor: 'rgba(238,50,30,0)',             //不填滿 全透明
                     pointBackgroundColor: "rgba(255,255,255,1)",     //座標點的顏色，白色
                     borderColor: "rgba(238,50,30,1)",                //邊框紅色不透明
                     borderWidth: 1,
                     pointHoverBackgroundColor: "#FBED37",            //滑鼠經過時座標點時 鵝黃色
                     pointBorderWidth: 0.5,                           //座標點的邊框粗細
                     pointRadius: 3,                                  //座標點的半徑
                     pointHoverRadius: 5,                             //滑鼠經過時座標點的半徑，動態變大
                     pointStyle: 'circle',                            //座標點的圖形樣式-圓形
                     hidden: false,                                   //預設不要隱藏
              },
              {
                     label: 'non-NF中位數',
                     data: [0.080449018
                            , 0.041125266
                            , 0.774370208
                            , 0
                            , 0.149073328],
                     backgroundColor: 'rgba(238,50,30,0)',             //不填滿 全透明
                     pointBackgroundColor: "rgba(255,255,255,1)",     //座標點的顏色，白色
                     borderColor: "rgba(33,113,48,1)",                //邊框綠色不透明
                     borderWidth: 1,
                     pointHoverBackgroundColor: "#FBED37",            //滑鼠經過時座標點時 鵝黃色
                     pointBorderWidth: 0.5,                           //座標點的邊框粗細
                     pointRadius: 3,                                  //座標點的半徑
                     pointHoverRadius: 5,                             //滑鼠經過時座標點的半徑，動態變大
                     pointStyle: 'circle',                            //座標點的圖形樣式-圓形
                     hidden: false,                                   //預設不要隱藏
              },
              {
                     label: '目前病患',
                     data: [(wbc - value_min[0]) / (value_max[0] - value_min[0]),
                     (crp - value_min[1]) / (value_max[1] - value_min[1]),
                     (seg - value_min[2]) / (value_max[2] - value_min[2]),
                     (band - value_min[3]) / (value_max[3] - value_min[3]),
                     (sea - value_min[4]) / (value_max[4] - value_min[4])],
                     backgroundColor: 'rgba(238,50,30,0)',             //不填滿 全透明
                     pointBackgroundColor: "rgba(255,255,255,1)",     //座標點的顏色，白色
                     borderColor: "rgba(56,99,186,1)",                //邊框藍色不透明
                     borderWidth: 1,
                     pointHoverBackgroundColor: "#FBED37",            //滑鼠經過時座標點時 鵝黃色
                     pointBorderWidth: 0.5,                           //座標點的邊框粗細
                     pointRadius: 3,                                  //座標點的半徑
                     pointHoverRadius: 5,                             //滑鼠經過時座標點的半徑，動態變大
                     pointStyle: 'circle',                            //座標點的圖形樣式-圓形
                     hidden: false,
              }]
       };

       var chartRadarOptions = {
              scales: {            //刻度控制項目
                     r: {          //r軸，只要繞一圈的都適用r，折線圖長條圖則適用x軸、y軸
                            beginAtZero: true,          //數值是否從0開始依比例繪製
                            min: 0,                      //r軸數值的最小值
                            max: 1,                      //r軸數值的最大值
                            ticks: {      //刻度標記(ex:20,40,60,80這樣的刻度標記)
                                   font: {              //字體
                                          size: 10      //大小
                                   },
                                   color: '#611D5B',    //葉綠色
                                   maxTicksLimit: 10    //刻度標記數量，最大的數量上限(注意!0也算1個)
                            },
                            pointLabels: {       //labels，軸的文字標籤(ex:攻擊)
                                   font: {
                                          size: 13,     //大小
                                          weight: 700   //粗細
                                   },
                                   color: '#611D5B'     //青色
                            },
                            angleLines: {        //輻射狀軸線，蜘蛛網的軸線
                                   color: '#9a9a9a'     //灰色
                            },
                            grid: {              //刻度標記線，蜘蛛網的橫線
                                   color: '#9a9a9a'     //黑色
                            }
                     }
              },
              plugins: {           //額外項目
                     legend: {     //腳色的標籤
                            display: true,       //要不要顯示標籤
                            labels: {
                                   color: 'rgba(0,0,0,1)'      //黑色
                            }
                     },
                     tooltip: {    //數據回應方格，滑鼠經過時會出現(以下都指此回應方格內)
                            backgroundColor: "rgba(125,0,125,0.8)",   //背景紫紅色，半透明
                            titleFont: {         //上方labels的字體
                                   size: 14,      //大小
                            },
                            titleColor: "#ffffff",      //上方labels的字體顏色
                            bodyFont: {                 //下方數值的字體
                                   size: 12              //大小
                            },
                            bodyColor: "#ffffff",       //下方數值的字體顏色
                            usePointStyle: true,        //是否啟用座標點外觀樣式，為true時pointStyle設定才會生效
                            displayColors: false        //是否顯示座標點的顏色方塊
                     }
              }
       };

       var options = {
              scale: {
                     ticks: {
                            suggestedMin: 0,
                            suggestedMax: 1,
                            stepSize: 0.2,
                     }
              },
              title: {
                     display: true,
                     text: '壞死筋膜炎危險因素數值分析圖',
                     fontColor: 'black',
                     fontSize: "4vmin"
              }
       };
       var radarChart = new Chart(radarChart, {
              type: 'radar',
              data: data,
              options: chartRadarOptions
       });
}