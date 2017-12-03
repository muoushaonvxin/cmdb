/**
 * Created by Selience on 2017/11/25.
 */


/**
 *
 * 根据sn号查看详细信息
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
            // 跳转到详细信息页面
            window.location.href = "/cmdb/page/query_asset_detail/";
            window.location.target = "mainFrame";
        },
        error: function (data) {
            console.log("render tiao zhuan bu liao.");
        },
        complete: function (XMLHttpRequest, textStatus) {

        }
    });
}


/**
 *
 * 根据sn号删除该资产
 */

function delete_asset_by_sn(ths) {
    var var1 = $(ths).parent().prev().prev().prev().prev().text();

    $.ajax({
        cache: false,
        url: "/cmdb/page/delete_asset/",
        type: "post",
        dataType: "json",
        data: {"sn": var1},
        async: true,
        success: function (data) {
            // 如果返回success，页面跳转到资产列表页面
            if (data.status == "success") {
                window.location.href = "/cmdb/page/asset_list/";
                window.location.target = "mainFrame";
            }
        },
        error: function (data) {

        },
        complete: function (XMLHttpRequest, textStatus) {

        }
    });
}



