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
