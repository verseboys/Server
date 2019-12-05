(function () {
    CKEDITOR.plugins.add("methods_images_1", {
        init: function (a) {
            a.ui.addButton("methods_images", {
                command: "methods_images",
                label:'插入图片',
                //icon: "skins/moono-lisa/surface.png",//在toolbar中的图标
                click: function () {
                    $("#yika_img_methods_1").trigger("click")

                }
            });
        }
    })
})();
