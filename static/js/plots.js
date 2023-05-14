$('#column_name_select').on('change',function(){

    $.ajax({
        url: "/plot",
        type: "GET",
        contentType: 'application/json;charset=UTF-8',
        data: {
            'selected': document.getElementById('column_name_select').value

        },
        dataType:"json",
        success: function (data) {
            Plotly.newPlot('bargraph', data );
        }
    });
})

$('#column_name_select').on('change',function(){

    $.ajax({
        url: "/plot",
        type: "GET",
        contentType: 'application/json;charset=UTF-8',
        data: {
            'selected': document.getElementById('column_name_select').value

        },
        dataType:"json",
        success: function (data) {
            Plotly.newPlot('technicalgraph', data );
        }
    });
})

$('#fileupload').on('click', function(e) {
    e.preventDefault()
    $.ajax({
        url: "/forward",
        type: "GET",
        contentType: 'application/json;charset=UTF-8',
        data: {
            'selected': document.getElementById('file_upload').value

        },
        dataType:"json",
        success: function (data) {
            Plotly.newPlot('bargraph', data );
        }
    });
})

$('#backtest_button').on('click', function(e) {
    var strategyNodes = document.getElementById('backtest_strategy_forms').childNodes;
    var indicator1Array = [];
    var indicator2Array = [];
    var enableFlagArray = [];
    var relationArray = [];
    var form_data = new FormData();
    for(i=1; i<strategyNodes.length; ++i){
        indicator1Array.push(strategyNodes[i].getElementById('indicator1').value);
        indicator2Array.push(strategyNodes[i].getElementById('indicator2').value);
        relationArray.push(strategyNodes[i].getElementById('indicator_relation').value);
        console.log(strategyNodes[i].getElementById('indicator_relation'))
        if(strategyNodes[i].getElementById('strategy_enable') == 'on'){
            enableFlagArray.push('ON');
        }
        else{
            enableFlagArray.push('OFF');
        }
        // enableFlagArray.push(strategyNodes[i].getElementById('strategy_enable').value);
    }
    form_data.append( "indicator1Input", indicator1Array);
    form_data.append( "indicator2Input", indicator2Array);
    form_data.append( "relationInput", relationArray);
    form_data.append( "enableFlagInput", enableFlagArray);
    e.preventDefault()
    $.ajax({
        url: "/runbacktest",
        type: "POSt",
        contentType: 'application/json;charset=UTF-8',
        data: {
            'selected': form_data
        },
        success: function (data) {
        },
        dataType:"json"
    });
})