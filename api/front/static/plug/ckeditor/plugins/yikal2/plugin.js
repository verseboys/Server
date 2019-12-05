(function () {
    CKEDITOR.plugins.add("yikal2", {
        init: function (a) {
            a.ui.addButton("yikal2", {
                command: "yikal2",
                label: '超链接',
                //icon: "skins/moono-lisa/surface.png",//在toolbar中的图标
                click: function () {
                    yikali2();
                }
            });
        }
    })
})();
