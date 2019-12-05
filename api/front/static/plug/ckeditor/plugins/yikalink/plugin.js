(function () {
    CKEDITOR.plugins.add("yikalink", {
        init: function (a) {
            a.ui.addButton("yikalink", {
                command: "yikalink",
                label: '超链接',
                //icon: "skins/moono-lisa/surface.png",//在toolbar中的图标
                click: function () {
                    yikalink(1);
                }
            });
        }
    })
})();
