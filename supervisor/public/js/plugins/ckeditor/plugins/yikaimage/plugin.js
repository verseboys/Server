(function () {
    CKEDITOR.plugins.add("yikaimage", {
        init: function (a) {
            a.ui.addButton("yikaimage", {
                command: "yikaimage",
                label:'插入图片',
                //icon: "skins/moono-lisa/surface.png",//在toolbar中的图标
                click: function () {
                    $("#yika_img_upload").trigger("click")
                }
            });
        }
    })
})();
