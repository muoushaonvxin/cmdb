/**
 * Created by Selience on 2017/11/25.
 */

function query_asset_by_sn(ths){
    var var1 = $(ths).parent().prev().prev().prev().text();

    $.ajax({
        cache: false,
        url: "/cmdb/page/query_asset_detail_by_sn/",
        type: "get",
        dataType: "json",
        data: { "sn": var1 },
        async: true,
        success: function (data) {
            window.location.href = "/cmdb/page/query_asset_detail/";
            window.location.target = "mainFrame";
            console.log(data.sn);
            console.log(data.create_date);
        },
        error: function (data) {
            console.log("render tiao zhuan bu liao.");
        },
        complete: function (XMLHttpRequest, textStatus) {
            console.log(XMLHttpRequest.status);
            console.log(textStatus.toString());
        }
    });
}

