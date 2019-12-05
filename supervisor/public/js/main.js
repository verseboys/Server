
    /*!
    * JavaScript Cookie v2.1.4
    * https://github.com/js-cookie/js-cookie
    *
    * Copyright 2006, 2015 Klaus Hartl & Fagner Brack
    * Released under the MIT license
    */
    ;(function (factory) {
        var registeredInModuleLoader = false;
        if (typeof define === 'function' && define.amd) {
            define(factory);
            registeredInModuleLoader = true;
        }
        if (typeof exports === 'object') {
            module.exports = factory();
            registeredInModuleLoader = true;
        }
        if (!registeredInModuleLoader) {
            var OldCookies = window.Cookies;
            var api = window.Cookies = factory();
            api.noConflict = function () {
                window.Cookies = OldCookies;
                return api;
            };
        }
    }(function () {
        function extend() {
            var i = 0;
            var result = {};
            for (; i < arguments.length; i++) {
                var attributes = arguments[i];
                for (var key in attributes) {
                    result[key] = attributes[key];
                }
            }
            return result;
        }

        function init(converter) {
            function api(key, value, attributes) {
                var result;
                if (typeof document === 'undefined') {
                    return;
                }

                // Write

                if (arguments.length > 1) {
                    attributes = extend({
                        path: '/'
                    }, api.defaults, attributes);

                    if (typeof attributes.expires === 'number') {
                        var expires = new Date();
                        expires.setMilliseconds(expires.getMilliseconds() + attributes.expires * 864e+5);
                        attributes.expires = expires;
                    }

                    // We're using "expires" because "max-age" is not supported by IE
                    attributes.expires = attributes.expires ? attributes.expires.toUTCString() : '';

                    try {
                        result = JSON.stringify(value);
                        if (/^[\{\[]/.test(result)) {
                            value = result;
                        }
                    } catch (e) {
                    }

                    if (!converter.write) {
                        value = encodeURIComponent(String(value))
                            .replace(/%(23|24|26|2B|3A|3C|3E|3D|2F|3F|40|5B|5D|5E|60|7B|7D|7C)/g, decodeURIComponent);
                    } else {
                        value = converter.write(value, key);
                    }

                    key = encodeURIComponent(String(key));
                    key = key.replace(/%(23|24|26|2B|5E|60|7C)/g, decodeURIComponent);
                    key = key.replace(/[\(\)]/g, escape);

                    var stringifiedAttributes = '';

                    for (var attributeName in attributes) {
                        if (!attributes[attributeName]) {
                            continue;
                        }
                        stringifiedAttributes += '; ' + attributeName;
                        if (attributes[attributeName] === true) {
                            continue;
                        }
                        stringifiedAttributes += '=' + attributes[attributeName];
                    }
                    return (document.cookie = key + '=' + value + stringifiedAttributes);
                }

                // Read

                if (!key) {
                    result = {};
                }

                // To prevent the for loop in the first place assign an empty array
                // in case there are no cookies at all. Also prevents odd result when
                // calling "get()"
                var cookies = document.cookie ? document.cookie.split('; ') : [];
                var rdecode = /(%[0-9A-Z]{2})+/g;
                var i = 0;

                for (; i < cookies.length; i++) {
                    var parts = cookies[i].split('=');
                    var cookie = parts.slice(1).join('=');

                    if (cookie.charAt(0) === '"') {
                        cookie = cookie.slice(1, -1);
                    }

                    try {
                        var name = parts[0].replace(rdecode, decodeURIComponent);
                        cookie = converter.read ?
                            converter.read(cookie, name) : converter(cookie, name) ||
                            cookie.replace(rdecode, decodeURIComponent);

                        if (this.json) {
                            try {
                                cookie = JSON.parse(cookie);
                            } catch (e) {
                            }
                        }

                        if (key === name) {
                            result = cookie;
                            break;
                        }

                        if (!key) {
                            result[name] = cookie;
                        }
                    } catch (e) {
                    }
                }

                return result;
            }

            api.set = api;
            api.get = function (key) {
                return api.call(api, key);
            };
            api.getJSON = function () {
                return api.apply({
                    json: true
                }, [].slice.call(arguments));
            };
            api.defaults = {};

            api.remove = function (key, attributes) {
                api(key, '', extend(attributes, {
                    expires: -1
                }));
            };

            api.withConverter = init;

            return api;
        }

        return init(function () {
        });
    }));


    var doc = document.body || document.documentElement;
    window.ajax_type = true;

//option [{
// 'ev':'',
//  el:'',
//  cl:''
// }]

    function tag_class(option) {
        option.forEach(function (t) {
            t.ev === true ? t.ev : t.ev = 'click';
            $(document.body).on(t.ev, t.el, function (e) {
                $(this).addClass(t.cl).siblings().removeClass(t.cl)
                if (t.fn) {
                    t.fn(e)
                }
            })
        })
    }

    /*
    * user
    *
    * */

    function AJAX(option) {
        $.ajax({
            type: option.type,  //提交方式
            url: option.url,//路径
            data: option.data,//数据
            beforeSend: function (XMLHttpRequest) {
               if(option.before) {
                   XMLHttpRequest.setRequestHeader();
               }
            },
            success: function (data) {//返回数据根据结果进行相应的处理
                option.fn(data)
            },
            error: function () {
                if (option.error) {
                    option.error()
                }
            }
        });
    }

    function load_ajax(fn) {

        $(window).scroll(function () {
            var scrollTop = $(document).scrollTop(),
                scrollHeight = $(document).height(),
                windowHeight = $(window)[0].innerHeight;
            if (scrollHeight - windowHeight - scrollTop < 2) {
                if (ajax_type) {
                    window.ajax_type = false;
                    fn();
                }
            }
        })
    }

    /*计算字节长度*/
    function getBt(str) {
        var char = str.match(/[^\x00-\xff]/ig);
        return str.length + (char == null ? 0 : char.length);
    }
    function autoAddEllipsis(pStr, pLen) {

        var _ret = cutString(pStr, pLen);
        var _cutFlag = _ret.cutflag;
        var _cutStringn = _ret.cutstring;

        if ("1" == _cutFlag) {
            return _cutStringn + "...";
        } else {
            return _cutStringn;
        }
    }

    /*
     * 取得指定长度的字符串
     * 注：半角长度为1，全角长度为2
     *
     * pStr:字符串
     * pLen:截取长度
     *
     * return: 截取后的字符串
     */
    function cutString(pStr, pLen) {

        // 原字符串长度
        var _strLen = pStr.length;

        var _tmpCode;

        var _cutString;

        // 默认情况下，返回的字符串是原字符串的一部分
        var _cutFlag = "1";

        var _lenCount = 0;

        var _ret = false;

        if (_strLen <= pLen / 2) {
            _cutString = pStr;
            _ret = true;
        }

        if (!_ret) {
            for (var i = 0; i < _strLen; i++) {
                if (isFull(pStr.charAt(i))) {
                    _lenCount += 2;
                } else {
                    _lenCount += 1;
                }

                if (_lenCount > pLen) {
                    _cutString = pStr.substring(0, i);
                    _ret = true;
                    break;
                } else if (_lenCount == pLen) {
                    _cutString = pStr.substring(0, i + 1);
                    _ret = true;
                    break;
                }
            }
        }

        if (!_ret) {
            _cutString = pStr;
            _ret = true;
        }

        if (_cutString.length == _strLen) {
            _cutFlag = "0";
        }

        return {"cutstring": _cutString, "cutflag": _cutFlag};
    }

    /*
     * 判断是否为全角
     *
     * pChar:长度为1的字符串
     * return: true:全角
     *          false:半角
     */
    function isFull(pChar) {
        if ((pChar.charCodeAt(0) > 128)) {
            return true;
        } else {
            return false;
        }
    }

// mouseSheel(scrollFunc)
    function mouseSheel(fn) {

        if (document.addEventListener) {
            document.addEventListener('DOMMouseScroll', fn, false);
        }
        if (document.attachEvent) {
            document.attachEvent('onmousewheel', fn);
        }
        window.onmousewheel = document.onmousewheel = fn;//IE/Opera/Chrome/Safari
    }

    function scrollFunc(e) {
        e = e || window.event;

        if (e.preventDefault) {
            e.preventDefault();
            e.stopPropagation();
        } else {
            // IE
            e.cancelBubble = true;
            e.returnValue = false;
        }
        var srco = document.body || document.documentElement;
        if (e.wheelDelta) {//IE/Opera/Chrome
            if (e.wheelDelta > 0) {
                if (e.preventDefault) {
                    // Firefox
                    if (document.documentElement) {
                        document.documentElement.scrollTop -= 50;
                    } else if (document.body) {
                        document.body.scrollTop -= 50
                    }
                    srco.scrollTop -= 50;
                } else {
                    // IE
                    srco.scrollTop -= 50
                }
            } else {
                //console.log(5)
                if (e.preventDefault) {
                    // Firefox
                    if (document.documentElement) {
                        document.documentElement.scrollTop += 50;
                    } else if (document.body) {
                        document.body.scrollTop += 50
                    }
                    srco.scrollTop += 50;
                } else {
                    // IE
                    srco.scrollTop += 50
                }

            }


        }
        else if (e.detail) {//Firefox
            if (e.detail > 0) {
                //console.log(5)
                if (e.preventDefault) {
                    // Firefox
                    if (document.documentElement) {
                        document.documentElement.scrollTop += 50;
                    } else if (document.body) {
                        document.body.scrollTop += 50
                    }
                    srco.scrollTop += 50;
                } else {
                    // IE
                    srco.scrollTop += 50
                }
            } else {
                if (e.preventDefault) {
                    // Firefox
                    if (document.documentElement) {
                        document.documentElement.scrollTop -= 50;
                    } else if (document.body) {
                        document.body.scrollTop -= 50
                    }
                    srco.scrollTop -= 50;
                } else {
                    // IE
                    srco.scrollTop -= 50
                }
            }
        }

    }
function mouse_heel(option) {
  var ele=  option.el?option.el:document;
    if (document.addEventListener) {
        ele.addEventListener('DOMMouseScroll', scrollFunc, false);
        return;
    }
    if (document.attachEvent) {
        ele.attachEvent('onmousewheel', scrollFunc);
        return;
    }
    window.onmousewheel = ele.onmousewheel = scrollFunc;
    function scrollFunc(e) {
        e = e || window.event;

        if (e.preventDefault) {
            e.preventDefault();
            e.stopPropagation();
        } else {
            // IE
            e.cancelBubble = true;
            e.returnValue = false;
        }
        if (e.wheelDelta) {//IE/Opera/Chrome
            if (e.wheelDelta > 0) {
                if (e.preventDefault) {
                    // Firefox
                    if (document.documentElement) {
                        ele.scrollTop -= 50;
                    } else if (document.body) {
                        ele.scrollTop -= 50;
                        return
                    }
                    ele.scrollTop -= 50;
                } else {
                    // IE
                    ele.scrollTop -= 50
                }
            } else {
                //console.log(5)
                if (e.preventDefault) {
                    // Firefox
                    if (document.documentElement) {
                        ele.scrollTop += 50;
                    } else if (document.body) {
                        ele.scrollTop += 50
                        return
                    }
                    ele.scrollTop += 50;
                } else {
                    // IE
                    ele.scrollTop += 50
                }

            }


        }
        else if (e.detail) {//Firefox
            if (e.detail > 0) {
                //console.log(5)
                if (e.preventDefault) {
                    // Firefox
                    if (document.documentElement) {
                        ele.scrollTop += 50;
                    } else if (document.body) {
                        ele.scrollTop += 50;
                        return
                    }
                    ele.scrollTop += 50;
                } else {
                    // IE
                    ele.scrollTop += 50
                }
            } else {
                if (e.preventDefault) {
                    // Firefox
                    if (document.documentElement) {
                        document.documentElement.scrollTop -= 50;
                    } else if (document.body) {
                        document.body.scrollTop -= 50;
                        return
                    }
                    ele.scrollTop -= 50;
                } else {
                    // IE
                    ele.scrollTop -= 50
                }
            }
        }

    }
}

    /*
    * 时间格式化 （）new Date().format('yyyy-MM-dd hh:mm:ss')
    * */
    Date.prototype.format = function (format) {
        var o = {
            "M+": this.getMonth() + 1, //month
            "d+": this.getDate(), //day
            "h+": this.getHours(), //hour
            "m+": this.getMinutes(), //minute
            "s+": this.getSeconds(), //second
            "q+": Math.floor((this.getMonth() + 3) / 3), //quarter
            "S": this.getMilliseconds() //millisecond
        }
        if (/(y+)/.test(format)) format = format.replace(RegExp.$1,
            (this.getFullYear() + "").substr(4 - RegExp.$1.length));
        for (var k in o) if (new RegExp("(" + k + ")").test(format))
            format = format.replace(RegExp.$1,
                RegExp.$1.length == 1 ? o[k] :
                    ("00" + o[k]).substr(("" + o[k]).length));
        return format;
    }

    //全局验证开关
    window.LOGIN_TYPE=false;
    //菜单
    var MEUN_SIZE=0,MEUN_TYPR=true;
    function MEUN_MOVE() {

    }
    var u=''
    var nav_list = [
        {
            title: '研究方法',
            list: [
                {
                    title: '关键词关联',
                    url: 'methods_key.html'
                },
                {
                    title: '文章管理',
                    url: 'methods.html'
                }, {
                    title: '分类管理',
                    url: 'methods_class.html'
                },
                {
                    title: '专题管理',
                    url: 'methods_special.html'
                }, {
                    title: '标签管理',
                    url: 'methods_article_tag.html'
                },
                {
                    title: '首页推荐',
                    url: 'methods_recommend.html'
                },
                {
                    title: '首页banner管理',
                    url: 'banner.html'
                },
                {
                    title:'视频课程',
                    url: 'video.html',
                },
                {
                    title:'新管理后台',
                    url:'new_manager'
                }
            ]
        },{
            title: '研究进展',
            list: [
                {
                    title: '文章管理',
                    url: 'research_progress.html'
                }
                , {
                    title: '分类管理',
                    url: 'progress_class.html'
                },
                // {
                //     title:'标签管理',
                //     url:''
                // },
                {
                    title: '首页推荐',
                    url: 'progress_recommend.html'
                }
            ]
        },
        {
            title: '内容管理',
            list: [
                {
                    title: '评论管理',
                    url: 'comment.html'
                }, {
                    title: '文章标签管理',
                    url: 'article_tag.html'
                },
            ]
        },
        {
            title: '问答管理',
            list: [{
                title: '问题管理',
                url: 'question.html'
            }, {
                title: '问题标签管理',
                url: 'questions_tag.html'
            }
            ]
        },
        {
            title: '用户管理',
            list: [{
                title: '用户列表',
                url: 'user.html'
            },
            ]
        },
        {
            title: '微信自定义菜单',
            list: [{
                title: '文章管理',
                url: 'custom_menu.html'
            }, {
                title: '分类管理',
                url: 'custom_menu_tag.html'
            }]
        },
        {
            title: '资源分发管理',
            list: [{
                title: '分类管理',
                url: 'resources_type.html'
            }]
        }
    ]
    // $(document.body).append('<div id="move_nav"></div>')
    if(Cookies.get('admin_login_name')){
        var nav_str='<ul>'
        for(var i=0;i<nav_list.length;i++){
            var nav_item=nav_list[i];
           var lis=nav_item.list
            nav_str+='<li>';
                nav_str+='<span>'+nav_item.title+'</span>';
            nav_str+='<ul>';
                for(var j=0;j<lis.length;j++){
                    if(lis[j].title=="新管理后台"){
                        nav_str+='<li data-url="'+'/new_manager/'+'">'+lis[j].title+'</li>';
                    }else{
                        nav_str+='<li data-url="'+lis[j].url+'">'+lis[j].title+'</li>';
                    }

                }
            nav_str+='</ul>';
            nav_str+='</li>';
        }
        nav_str+='</ul>';
        $('#nav').html(nav_str)
        $('#header .user_name').html(Cookies.get('admin_login_name'));
        $(document.body).removeClass('hide');
        var window_width=window.innerWidth;
        if(window_width<1250){
            MEUN_SIZE=0
            $('#nav').css('left','-224px');
            $('#content').css('left','24px')
            if( MEUN_TYPR){
                $(document.body).append('<div id="move_nav"></div>');
            }
            MEUN_TYPR=false;
        }else {
            MEUN_SIZE=224
        }
        $('#content').css('width',(window_width-MEUN_SIZE-25)+'px')
        $(window).resize(function () {
            window_width=window.innerWidth;
            if(window_width<1250){
                MEUN_SIZE=0
                $('#nav').css('left','-224px');
                $('#content').css('left','24px')
               if( MEUN_TYPR){
                   $(document.body).append('<div id="move_nav"></div>');
               }
                MEUN_TYPR=false
            }
            $('#content').css('width', (window_width - MEUN_SIZE - 25) + 'px')
        })
        var path_name=window.location.pathname.split('/');
        var ul_add=CHOSE_URL_CHECK(path_name[path_name.length-1])
        $('#nav li li').each(function (item) {
            if($(this).attr('data-url')===ul_add){
                $(this).addClass('checked')
            }
            $(this).click(function () {
                window.location.href=$(this).attr('data-url');
            })
        })
        $(document.body).on('click','.log_out',function () {
            $.ajax({
                url:'/supervisor/logout/',
                type:'get',
                success:function (data) {
                    if(data.code===200){
                        Cookies.remove('admin_login_name');
                        window.location.href = 'login.html';
                    }else {
                        alert(data.message)
                    }
                }
            })

        })
        $(document).on('click','#move_nav',function () {
            $('#nav').css('left','0');
            $('#content').css('left','250px')
            $('#content').css('width', (window_width - 224 - 25) + 'px')
        })
        $(document).on('mouseleave','#nav',function () {
            if(!MEUN_TYPR){
                $('#nav').css('left','-224px');
                $('#content').css('left','24px')
                $('#content').css('width', (window_width - 0- 25) + 'px')
            }
        })


    }else{
        var path_name=window.location.pathname.split('/');
        if(path_name[path_name.length-1]!=='login.html') {
            Cookies.set('loca_href',path_name[path_name.length-1])
            window.location.href = 'login.html';
        }
    }

    var SCROLL_OLD_SIZE = window.scrollY;
    $(document).ready(function () {


    $('#content')[0].onscroll = function (e) {
        if (this.scrollTop > SCROLL_OLD_SIZE && this.scrollTop>0) {
            $('#header').css('top','-53px');
            $('#nav').css('padding-top', '4px')
            // $('#content').css('padding-top', '40px')
        } else if ((this.scrollTop < SCROLL_OLD_SIZE) || this.scrollTop<=0) {
            $('#header').css('top', '0px')
            $('#nav').css('padding-top', '57px');
            // $('#content').css('padding-top', '93px')
        }
        SCROLL_OLD_SIZE = this.scrollTop;
    }
    })
    function windoes_scroll() {
        if(!/mac|MAC|Mac/.test(window.navigator.userAgent)){
            var sty=document.createElement('style');
            sty.innerHTML='::-webkit-scrollbar{\n' +
                '    width:6px;\n' +
                '    height:6px;\n' +
                '}\n' +
                '::-webkit-scrollbar:hover{\n' +
                '    background-color:#eee;\n' +
                '}\n' +
                '::-webkit-scrollbar-thumb{\n' +
                '    min-height:5px;\n' +
                '    min-width:5px;\n' +
                '    -webkit-border-radius:20px;\n' +
                '    border:none;\n' +
                '::-webkit-border-radius:1px;\n' +
                '    background-color: #c0c0c0;\n' +
                '}\n' +
                '::-webkit-scrollbar-thumb:hover{\n' +
                '    min-height:5px;\n' +
                '    min-width:5px;\n' +
                '    -webkit-border-radius:20px;\n' +
                '    border:none;\n' +
                '    background-color: #727272;\n' +
                '}\n' +
                '::-webkit-scrollbar-thumb:active{\n' +
                '    -webkit-border-radius:20px;\n' +
                '    border:none;\n' +
                '    background-color: #727272;\n' +
                '}';
            document.head.appendChild(sty);
        }
    }
function page_list() {
    
}
function CHOSE_URL_CHECK(val) {
        switch (val) {
            case 'research_method.html':
                return 'research_method.html'
                break
            case 'research_progress.html':
                return 'research_progress.html'
                break
            case 'comment.html':
                return 'comment.html'
                break
            case 'article_tag.html':
                return 'article_tag.html'
                break
            case 'question.html':
                return 'question.html'
                break
            case 'questions_tag.html':
                return 'questions_tag.html'
                break
            case 'user.html':
                return 'user.html'
                break
            case 'question_detil.html':
                return 'question.html'
                break
            case 'custom_menu.html':
                return 'custom_menu.html'
                break
            case 'custom_menu_tag.html':
                return 'custom_menu_tag.html'
                break
            case 'resources_type.html':
                return 'resources_type.html'
                break
            case  'methods_class.html':
                return 'methods_class.html'
                break
            case 'methods_article_tag.html':
                return 'methods_article_tag.html'
                break
            case 'methods_recommend.html' :
                return 'methods_recommend.html'
                break
            case 'methods.html':
                return 'methods.html'
                break
            case 'methods_article.html':
                return 'methods.html'
                break
            case 'banner.html':
                return 'banner.html'
                break
            case 'methods_special.html':
                return 'methods_special.html'
                break
            case 'method_special_article.html':
                return 'methods_special.html'
                break
            case 'progress_recommend.html':
                return "progress_recommend.html"
                break
            case 'progress_class.html':
                return 'progress_class.html'
                break
            case 'methods_key.html':
                return 'methods_key.html'
                break
            case 'methods_key_article.html':
                return 'methods_key.html'
                break
            default:
                return ''
        }
    }