/**
 * Created by Selience on 2017/11/25.
 */

function query_asset_by_sn(ths){
    var var1 = $(ths).parent().prev().prev().prev().text();

    $.ajax({
        url: "/cmdb/page/query_asset_detail/",
        type: "get",
        dataType: "json",
        data: { "sn": var1 },
        success: function (data) {
            alert(data);
        },
        errpr: function (data) {

        },
        complete: function (XMLHttpRequest, textStatus) {
            console.log(XMLHttpRequest.status);
            console.log(textStatus.toString());
        }
    });
}

