
function radar_test(wbc=0,crp=0,seg=0,band=0,sea=0) {
       var meanStd
       var max = [22000, 240, 100, 2, 1]
       var min = [0, 0, 0, 0, 0]
       //ajax to get meanStd
       $.ajax({
              url: "/getMeanStd?type=NF",
              type: "GET",
              data: {}
       }).done(function (data) {
              
             meanStd=JSON.parse(data)
              
              // meanStd=data
              console.log("meanStd", meanStd)
              mean = data.mean
              std = data.std
              doRadar(meanStd)
       }).fail(function (jqXHR, textStatus, errorThrown) {
              console.log("error")
       });
function doRadar(meanStd) {
       let chartStatus = Chart.getChart("radarChart"); // <canvas> id
if (chartStatus != undefined) {
  chartStatus.destroy();
}
       var radarChart = document.getElementById("radarChart");
       
       // setup 
       console.log("RADAR ",wbc,crp,seg,band)
       console.log(meanStd)
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
                     borderWidth: 3,
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
                     borderColor: "rgba(33,200,48,1)",                //邊框綠色不透明
                     borderWidth: 3,
                     pointHoverBackgroundColor: "#FBED37",            //滑鼠經過時座標點時 鵝黃色
                     pointBorderWidth: 0.5,                           //座標點的邊框粗細
                     pointRadius: 3,                                  //座標點的半徑
                     pointHoverRadius: 5,                             //滑鼠經過時座標點的半徑，動態變大
                     pointStyle: 'circle',                            //座標點的圖形樣式-圓形
                     hidden: false,                                   //預設不要隱藏
              },
              {
                     label: '目前病患',
                     data: [(wbc-min[0] ) /(max[0]-min[0])>1? 1:(wbc - min[0]) /(max[0]-min[0]),
                            (crp-min[1] ) /(max[1]-min[1])>1? 1:(crp - min[1]) /(max[1]-min[1]),
                            (seg -min[2]) /(max[2]-min[2])>1? 1:(seg - min[2]) /(max[2]-min[2]),
                            (band-min[3] ) /(max[3]-min[3])>1? 1:(band - min[3]) /(max[3]-min[3]),
                            (sea -min[4]) /(max[4]-min[4])>1? 1:(sea - min[4]) /(max[4]-min[4])],
                     backgroundColor: 'rgba(30,50,200,1)',             //不填滿 全透明
                     pointBackgroundColor: "rgba(255,255,255,1)",     //座標點的顏色，白色
                     borderColor: "rgba(56,50,140,1)",                //邊框藍色不透明
                     borderWidth: 3,
                     pointHoverBackgroundColor: "#FBED37",            //滑鼠經過時座標點時 鵝黃色
                     pointBorderWidth: 1,                           //座標點的邊框粗細
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
                            backgroundColor: "rgba(125,0,125,0.3)",   //背景紫紅色，半透明
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
}