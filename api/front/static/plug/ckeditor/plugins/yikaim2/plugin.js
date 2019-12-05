(function () {
    CKEDITOR.plugins.add("yikaim2", {
        init: function (a) {
            a.ui.addButton("yikaim2", {
                command: "yikaim2",
                label:'插入图片',
                //icon: "skins/moono-lisa/surface.png",//在toolbar中的图标
                click: function () {
                    $("#yika_img_up_2").trigger("click")
                }
            });
        }
    })
})();
