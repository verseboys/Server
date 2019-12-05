(function () {
    CKEDITOR.plugins.add("methods_link", {
        init: function (a) {
            a.ui.addButton("methods_link", {
                command: "methods_link",
                label: '超链接',
                //icon: "skins/moono-lisa/surface.png",//在toolbar中的图标
                click: function () {
                    methods_link();
                }
            });
        }
    })
})();
