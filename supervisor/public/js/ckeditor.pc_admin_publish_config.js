CKEDITOR.editorConfig = function (config) {
    // config.filebrowserUploadUrl = "ask.upload";
    config.language = "zh-cn";
    config.height = '482px';
    config.toolbar = [
        ['Undo', 'Redo', '-', 'FontSize', '-', 'TextColor', 'BGColor', '-', 'Bold', 'Italic', 'Underline', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'Link', 'Unlink', '-', 'Subscript', 'Superscript', '-', 'Source', '-', 'yikaimage']
    ];
    config.skin = 'moono-lisa';
    config.allowedContent = true;
    config.enterMode = CKEDITOR.ENTER_P;
    // config.removePlugins = 'elementspath,resize';
    config.format_tags = 'p;h1;h2;h3;pre';
    // config.removeDialogTabs = 'image:advanced;link:advanced;image:Link';
    config.extraPlugins = 'yikaimage';
    // CKEDITOR.addCss(".cke_editable{-webkit-overflow-scrolling: touch;background-color: #F2F3F4;font-size:1rem;word-break:break-all;white-space:normal;overflow-y:visible;-webkit-tap-highlight-color:rgba(0, 0, 0, 0);}");
    CKEDITOR.addCss(".cke_editable img{max-height: 200px}");
    // CKEDITOR.addCss(".cke_editable::-webkit-scrollbar{width:.29rem;background-color: #F2F3F4;}");
    // CKEDITOR.addCss(".cke_editable::-webkit-scrollbar-thumb{width:.29rem;opacity: 0.5;background-color: #BCC1CC;border-radius: 100px;}")
};