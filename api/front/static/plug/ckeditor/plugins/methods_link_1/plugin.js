(function () {
    CKEDITOR.plugins.add("methods_link_1", {
        init: function (a) {
            a.ui.addButton("methods_link_1", {
                command: "methods_link_1",
                label: '超链接',
                //icon: "skins/moono-lisa/surface.png",//在toolbar中的图标
                click: function () {
                    console.log(2)
                    methods_link_1();
                }
            });
        }
    })
})();
