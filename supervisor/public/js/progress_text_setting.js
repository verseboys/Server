CKEDITOR.editorConfig = function (config) {
    config.filebrowserUploadUrl = "answer.upload";
    config.language = "zh-cn";
    // config.height = '18rem';
    config.extraPlugins ='autogrow';
    config.autoGrow_minHeight = 200;
    config.autoGrow_bottomSpace = 50;
    config.toolbar = [
        // ['Undo', 'Redo', '-', 'Bold', 'Italic', 'Underline', '-', 'yikalink', '-', 'yikaimage']
        ['Undo', 'Redo', '-', 'FontSize', '-', 'TextColor', 'BGColor', '-', 'Bold', 'Italic', 'Underline', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-',  'Subscript', 'Superscript', '-', 'Source','-','yikalink', '-', '-', 'yikaimage',]
    ];
    config.skin = 'moono-lisa';
    config.allowedContent = true;
    config.enterMode = CKEDITOR.ENTER_P;
    // config.removePlugins = 'elementspath,resize';
    // config.removePlugins = 'elementspath';
    config.format_tags = 'p;h1;h2;h3;pre';
    config.removeDialogTabs = 'image:advanced;link:advanced;image:Link';
    config.extraPlugins = 'yikaimage,yikalink';
    CKEDITOR.addCss(".cke_editable{-webkit-overflow-scrolling: touch;background-color: #fff;font-size:1rem;word-break:break-all;white-space:normal;overflow-y:visible;-webkit-tap-highlight-color:rgba(0, 0, 0, 0);}");
    CKEDITOR.addCss(".cke_editable img{max-width: 50%;;margin: 0 auto;display: block;}");
    CKEDITOR.addCss(".cke_editable::-webkit-scrollbar{width:.29rem;background-color: #F2F3F4;}");
    CKEDITOR.addCss(".cke_editable::-webkit-scrollbar-thumb{width:.29rem;opacity: 0.5;background-color: #BCC1CC;border-radius: 100px;}")
};