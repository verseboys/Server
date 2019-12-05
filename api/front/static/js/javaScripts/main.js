
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


    window.ajax_type = true;

//option [{
// 'ev':'',
//  el:'',
//  cl:''  <br />
// }]

    function CKEDITOR_str(str) {
        if (str.lastIndexOf('&nbsp;') === str.length - 6) {
            var b = str.slice(0, str.length - 6 - 1)
            return CKEDITOR_str(b)
        } else if (str.lastIndexOf('<br />') === str.length - 6) {
            var b = str.slice(0, str.length - 6 - 1)
            return CKEDITOR_str(b)
        } else if (str.lastIndexOf(' ') === str.length - 1) {
            var b = str.slice(0, str.length - 1 )
            return CKEDITOR_str(b)
        }
        if (str.indexOf('&nbsp;') === 0) {
            var n = str.indexOf('&nbsp;')
            var b = str.slice(n + 6 + 1, str.length);
            return CKEDITOR_str(b)
        } else if (str.indexOf('<br />') === 0) {
            var n = str.indexOf('<br />')
            var b = str.slice(n + 6 + 1, str.length);
            return CKEDITOR_str(b)
        } else if (str.indexOf(' ') === 0) {
            var n = str.indexOf(' ')
            var b = str.slice(n + 1 + 1, str.length);
            return CKEDITOR_str(b)
        }
        return str
    }
    function tag_class(option) {
        option.forEach(function (t) {
            t.ev === true ? t.ev : t.ev = 'click';
            $(document.body).on(t.ev, t.el, function (e) {
                $(this).addClass(t.cl).siblings().removeClass(t.cl)
                if (t.fn) {
                    t.fn(e)
                }
                return false
            })
        })
    }

    /*
    * user
    *
    * */
    function getUrlParam(n) {
        var t;
        return t = window.location.search.substr(1).match(new RegExp("(^|&)" + n + "=([^&]*)(&|$)")), null !== t ? unescape(t[2]) : null
    }
    var USER_LISR={};
    $.sign_on = function () {
        window.location.href = '/login/#1'
        //check_type(1)
    }
    Vue.component('pc-state-box', {
        template: '<div class="neko_shadow_box" v-if="check_type===1">\n' +
        '        <div class="logo_box">\n' +
        // '            <div class="logo"></div>\n' +
        '            <div class="logo_text">登录医咖会</div>\n' +
        '            <div class="error_tip">\n' +
        '                 <div class="error-tip" style="background-color: #e46d7c;text-align: center;color: #fff;display: none;">账号或密码错误</div>\n' +
        '            </div>\n' +
        '        </div>\n' +
        '        <div class="input_box neko_login">\n' +
        '            <div class="input_item" style="margin-top: 4px;"><input class="neko_input username user_name_succ" placeholder="请输入用户名/手机号/邮箱" v-model="login.username_or_email">\n' +
        // '                <div v-bind:class="[login.username_or_email ? cla.activeClass :  cla.errorClass]" @click="clearInput(1)"></div>\n' +
        // '                <div class="name_state"></div>\n' +
        // '                <div class="warning_message" v-show="!login.username_or_email">{{error.login.username_or_email}}</div>\n' +
        '            </div>\n' +
        '            <div class="input_item"><input class="neko_input password password_fail" type="password" placeholder="请输入密码" v-model="login.password">\n' +
        // '                <div v-bind:class="[login.password ? cla.activeClass :  cla.errorClass]" @click="clearInput(2)"></div>\n' +
        // '                <div class="password_state"></div>\n' +
        // '                <div class="warning_message" v-show="!login.password">{{error.login.password}}</div>\n' +
        '            </div>\n' +
        //'            <div class="up_warning">{{error.login.error}}</div>\n' +
        '        </div>\n' +
        '        <div class="tool_box">\n' +
        // '            <div class="forgot" @click="close(4)" v-show="is_name_exist===true">忘记密码？点击这里！</div>\n' +
        // '            <div class="forgot" style="color:black;line-height:25px;" v-show="is_name_exist===false">登录不成功？赶快联系小咖帮你解决！<br>(小咖微信：xys2018ykf)</div>\n' +
        '            <div class="neko_btn" style="height: 40px;line-height: 40px;font-size: 14px;">\n' +
        // '                <input type="checkbox" value="" style="vertical-align: middle;">'+
        // '                <div class="neko_regist">下次自动登录</div>\n' +
        '                <div class="forget forget-pwd" style="float: right;color: #45a0ea;cursor: pointer;" @click="close(4)">忘记密码</div>\n' +
        '            </div>\n' +
        '        </div>\n' +
        '        <div class="neko_login submit_login shadow_btn" @click="click_tag(1)">登录</div>\n' +
        '        <div class="neko_btn" style="padding-top:20px;display: flex;justify-content: space-between;font-size: 14px;">\n' +
        '            <div class="neko_regist register" @click="close(2)" style="color: #45a0ea;cursor: pointer;">注册</div>\n' +
        '            <div class="forget" @click="close(3)" style="color: #45a0ea;cursor: pointer;">短信登录</div>\n' +
        '        </div>\n' +
        '    </div>' +
        // '<div class="neko_shadow_box" v-else-if="check_type===2">\n' +  
        // '        <div class="logo_box">\n' +
        // '            <div class="logo"></div>\n' +
        // '            <div class="logo_text">欢迎加入医咖会！</div>\n' +
        // '        </div>\n' +
        // '        <div class="input_box neko_box">\n' +
        // '            <div class="input_item"><input class="neko_input user_name" placeholder="输入用户名" v-model="register.username">\n' +
        // '                <div v-bind:class="[register.username ? cla.activeClass :  cla.errorClass]" @click="clearInput(3)"></div>\n' +
        // '                <div class="name_state"></div>\n' +
        // '                <div class="warning_message name" >{{error.register.username}}</div>\n' +
        // '            </div>\n' +
        // '            <div class="input_item"><input class="neko_input reg_email" placeholder="输入 Email" v-model="register.email">\n' +
        // '                <div v-bind:class="[register.email ? cla.activeClass :  cla.errorClass]" @click="clearInput(4)"></div>\n' +
        // '                <div class="email_state"></div>\n' +
        // '                <div class="warning_message email" >{{error.register.email}}</div>\n' +
        // '            </div>\n' +
        // '            <div class="neko_password_box">\n' +
        // '                <div class="input_item"><input class="neko_input password" type="password" placeholder="输入密码" v-model="register.password">\n' +
        // '                     <div v-bind:class="[register.password ? cla.activeClass :  cla.errorClass]" @click="clearInput(5)"></div>\n' +
        // '                    <div class="password_state"></div>\n' +
        // '                    <div class="warning_message password" >{{error.register.password}}</div>\n' +
        // '                </div>\n' +
        // '                <div class="input_item"><input class="neko_input re_password" type="password" placeholder="确认输入密码" v-model="register.repeat_password">\n' +
        // '                    <div v-bind:class="[register.repeat_password ? cla.activeClass :  cla.errorClass]" @click="clearInput(6)"></div><div class="password_state"></div><div class="warning_message re_password" >{{error.register.repeat_password}}</div>\n' +
        // '                </div>\n' +
        // '            </div>\n' +
        // '            <div class="input_item vc_input_box"><input class="neko_input vc_input" placeholder="确认输入验证码" v-model="register.captcha"><div v-bind:class="[register.captcha ? cla.activeClass :  cla.errorClass]" @click="clearInput(7)"></div>\n' +
        // '            </div>\n' +
        // '            <div class="vc_box img_captcha" style="background-image: url(/extends/captcha/);"  @click="img_captcha">\n' +
        // '                <div class="vc_warning" >{{error.register.captcha}}</div>\n' +
        // '            </div>\n' +
        // '        </div>\n' +
        // '        <div class="tool_box">\n' +
        // '            <div class="tip_msg_box">\n' +
        // '                <div class="msg">点击下一步，即同意</div>\n' +
        // '                <div class="jump_msg" @click="close(11,$event)">《 医咖会协议 》</div>\n' +
        // '            </div>\n' +
        // '            <div class="neko_btn">\n' +
        // '                <div class="neko_regist regist_login" @click="close(1)">登录</div>\n' +
        // '                <div class="neko_login regist_submit shadow_btn" @click="click_tag(2)">下一步</div>\n' +
        // '            </div>\n' +
        // '        </div>\n' +
        // '    </div>' +
        ' <div class="neko_shadow_box addition" style="height: 471px;" v-else-if="check_type===3">\n' +
        '        <div class="logo_box">\n' +
        // '            <div class="logo"></div>\n' +
        '            <div class="logo_text">信息完善</div>\n' +
        '        </div>\n' +
        '            <div style="width: 377px;height: 26px;">\n' +
        '                 <div class="error-tip" style="background-color: #e46d7c;line-height: 26px;text-align: center;color: #fff;font-size: 14px;display: none;">账号或密码错误</div>\n' +
        '            </div>\n' +
        '        <div class="input_box">\n' +
        '            <div class="input_item" style="margin-top:10px;"><input class="neko_input" placeholder="姓名" v-model="usr_id.fullname">\n' +
        '            </div>\n' +
        '        </div>\n' +
        '        <div class="input_box">\n' +
        '            <div class="input_item addition_input" style="margin-top: 15px;"><input class="neko_input company" placeholder="单位" v-model="usr_id.corporation">\n' +
        // '<div v-bind:class="[usr_id.corporation ? cla.activeClass :  cla.errorClass]" @click="clearInput(8)"></div>\n' +
        // '<div class="warning_message">{{error.usr.corporation}}</div>\n' +
        '            </div>\n' +
        '        </div>\n' +
        '        <div class="chooser_box">\n' +
        '            <div class="chooser_item profession" act="0" prid="">\n' +
        '                <input class="chooser_text" @click="show_list(1)" placeholder="选择专业科室" v-model="usr.profession_id" readonly="readonly"><div class="chooser_img" @click="show_list(1)"></div>\n' +
        // '<div class="warning_message" v-show="!usr_id.profession_id">{{error.usr.profession_id}}</div>\n' +
        '                   <div class="chooser_list" v-show="usr_type.profession_id">\n' +
        '                       <div v-for="list in usr_list.profession_id" class="list_item"  @click="nextList(1,list)">\n' +
        '                           <div class="list_name">{{list.department_name}}</div><div class="list_img"></div>\n' +
        '                       </div>\n' +
        '                  </div>\n' +
        '            </div>\n' +
        '            <div class="chooser_item job" act="0" joid="">\n' +
        '                <input class="chooser_text" @click="show_list(2)" placeholder="选择职称" v-model="usr.job_id" readonly="readonly">\n' +
        '<div class="chooser_img" @click="show_list(2)"></div>\n' +
        // '<div class="warning_message" v-show="!usr_id.job_id">{{error.usr.job_id}}</div>\n' +
        '                   <div class="chooser_list" v-show="usr_type.job_id">\n' +
        '                       <div v-for="lista in usr_list.job_id" class="list_item" @click="nextList(2,lista)">\n' +
        '                           <div class="list_name">{{lista.job_name}}</div><div class="list_img"></div>\n' +
        '                       </div>\n' +
        '                  </div>\n' +
        '            </div>\n' +
        '            <div class="chooser_item gender">\n' +
        '                <input class="chooser_text" @click="show_list(3)" placeholder="选择性别" v-model="usr.gender" readonly="readonly"><div class="chooser_img" @click="show_list(3)"></div>\n' +
        // '<div class="warning_message" v-show="!usr_id.gender">{{error.usr.gender}}</div>\n' +
        '                   <div class="chooser_list as" v-show="usr_type.gender">\n' +
        '                       <div v-for="list in usr_list.gender" class="list_item" @click="nextList(3,list)">\n' +
        '                           <div class="list_name">{{list.sex}}</div><div class="list_img"></div>\n' +
        '                       </div>\n' +
        '                  </div>\n' +
        '            </div>\n' +
        '        </div>\n' +
        '        <div class="tool_box">\n' +
        '            <div class="long_submit_btn shadow_btn addition_submit_btn" @click="click_tag(3)">完成</div>\n' +
        '        </div>\n' +
        '        <div class="jump-over" style="text-align: right;font-size: 14px;color: #999;padding-top: 18px;cursor:pointer;" @click="close(100)">跳过</div>\n' +
        '    </div>' +
        ' <div class="neko_shadow_box" v-else-if="check_type===4">\n' +
        '        <div class="logo_box">\n' +
        '            <div class="logo_text">输入 Email 以找回您的密码</div>\n' +
        '        </div>\n' +
        '        <div class="input_box">\n' +
        '            <div class="input_item"><input class="neko_input email" placeholder="输入 Email" v-model="forget.email" >\n' +
        '                <div></div>\n' +
        '                <div class="warning_message" >{{error.email.email}}</div>\n' +
        '            </div>\n' +
        '        </div>\n' +
        '        <div class="tool_box">\n' +
        '            <div class="neko_btn">\n' +
        '                <div class="neko_login forgot_submit_btn shadow_btn" @click="click_tag(4)">发送</div>\n' +
        '            </div>\n' +
        '        </div>\n' +
        '    </div>\n' +
        ' <div class="neko_shadow_box" v-else-if="check_type===5">\n' +
        '        <div class="logo_box">\n' +
        '            <div class="logo mail_succ_logo"></div>\n' +
        '            <div class="logo_text mail_succ_text">邮件已发送至您的 Email，请您查收</div>\n' +
        '        </div>\n' +
        '        <div class="tool_box">\n' +
        '            <div class="neko_btn mail_succ_btn">\n' +
        '                <div class="neko_login mail_succ_btn shadow_btn" @click="close(100)">确认</div>\n' +
        '            </div>\n' +
        '        </div>\n' +
        '    </div>'+
        '<div id="yika_agreement" v-else-if="check_type===11"><pre class="agreement_info"><center>《医咖会使用协议》</center>'+
        '一、总则\n' +
        '1、为了保护网络信息安全，保障公民、法人和其他组织的合法权益，维护国家安全和社会公共利益，根据国家法律法规，医咖会制定并按照本协议提供网络服务。用户应当充分阅读并同意本协议的全部条款并按照页面上的提示完成全部的注册程序（未成年人应与法定监护人共同完成）。用户在注册过程中点击“同意”按钮即表示用户完全接受本协议项下的全部条款，用户选择访问或使用医咖会有关服务，将视为同意接受本协议全部条款的约束。\n' +
        '2、除非另有明确规定，医咖会所推出的新产品、新功能和新服务，均无条件的适用本协议。\n' +
        '3、医咖会保留在任何时候修改本协议条款的权利，且无需另行通知。用户在使用服务时应关注并遵守。\n' +
        '4、用户在使用医咖会提供的各项服务之前，应仔细阅读本协议。如果您不同意本协议，可以主动取消医咖会提供的服务；如果您继续使用医咖会服务，则视为您已经接受本协议全部内容，包括医咖会对本协议所做的任何修改。\n' +
        '5、用户无论通过何种方式使用医咖会服务，均受本协议约束。\n' +
        '\n' +
        '二、用户账号\n' +
        '1、用户可以通过注册账号使用医咖会提供的各项服务。用户注册成功后，医咖会将给予用户一个账号及相应的密码，在医咖会审核通过后，每个账号对应一个唯一的名字（或昵称、用户名）。医咖会账号（包括名字、昵称、用户名等）的所有权归医咖会，用户完成申请注册手续后，获得医咖会账号的使用权，但仅限为个人而非商业目的使用。\n' +
        '2、用户自行保管其账号和密码。用户账号、密码使用权仅属于初始申请注册人，禁止赠与、借用、租用、转让或者售卖。' +
        '3、用户应提供完整、真实、准确和最新的个人资料，该资料对于使用医咖会的服务以及找回丢失的医咖会账号和密码至关重要。如因注册信息不真实而引起的问题由用户本人承担，医咖会不负任何责任并有权暂停或终止用户的账号。\n' +
        '4、用户账号和密码遭到他人非法使用或发生其他任何安全问题，用户应当立即通知医咖会。因黑客行为或用户的过错导致账号、密码被他人非法使用，医咖会不承担任何责任。\n' +
        '    \n' +
        '三、使用规则\n' +
        '    1、用户对以其账号发生的或通过其账号发生的一切活动和事件（包括但不限于用户发表的任何内容以及由此产生的任何结果）负全部法律责任。\n' +
        '2、用户在使用医咖会服务时，必须遵守中华人民共和国相关法律法规的规定，用户应同意将不会利用医咖会进行任何违法或不正当的活动，包括但不限于下列行为：\n' +
        '(1) 上载、下载、张贴、以电子邮件发送、传输、存储或以其他方式提供任何非法、有害、胁迫、骚扰、侵权、中伤、粗俗、猥亵、诽谤、淫秽、暴力、侵害他人隐私、种族歧视或其他令人不快的包括但不限于资讯、资料、文字、软件、音乐、照片、图形、信息或其他资料（以下简称内容）。\n' +
        '(2) 以任何方式危害他人。\n' +
        '(3) 冒充任何人或机构，或以虚伪不实的方式谎称或使人误认为与任何人或任何机构有关。\n' +
        '(4) 伪造标题或以其他方式操控识别资料，使他人产生误解。\n' +
        '(5) 上载、张贴、发送电子邮件或以其他方式传送无权传送的内容。\n' +
        '(6) 侵犯他人著作权或其他知识产权，或违反保密、雇佣或不披露协议披露他人商业秘密或保密信息。\n' +
        '(7) 张贴、发送、传输或以其他方式提供任何未经收件人请求或授权的电子邮件信息、广告、促销资料、垃圾邮件等，包括但不限于大批量的商业广告和信息公告。\n' +
        '(8) 上载、张贴、以电子邮件发送、传输、存储或以其他方式提供包含病毒或包含旨在危害、干扰、破坏或限制有关服务（或其任何部分）或任何其他计算机软件、硬件或通讯设备之正常运行的任何其他计算机代码、文档或程序的任何资料。\n' +
        '(9) 干扰或破坏有关服务，或与有关服务连接的任何服务器或网络，或与有关服务连接之网络的任何政策、要求或规定。\n' +
        '(10)采集并存储涉及有关服务任何其他用户的个人信息，以用于任何上述被禁止的活动。\n' +
        '(11)故意或非故意违反任何相关的中国法律、法规、规章、条例等其他具有法律效力的规范。\n' +
        '    \n' +
        '四、知识产权\n' +
        '    1、医咖会服务中包含的任何文字、图表、音频、视频或软件（包括但不限于软件中包含的图表、动画、音频、视频、界面实际、数据和程序、代码、文档）等信息或材料均受著作权法、商标法或其它法律法规的保护，未经相关权利人书面同意，用户不得以任何方式使用该等信息或材料，但出于使用医咖会服务目的而使用的除外。\n' +
        '2、本协议未授予用户使用医咖会任何商标、服务标记、标识、域名和其他显著品牌特征的权利。\n' +
        '3、除本协议明确允许的以外，用户不得以任何形式或任何方式对医咖会服务部分或全部内容进行修改、出租、租赁、出借、出售、分发、复制、创作衍生品或用于任何商业用途。\n' +
        '4、用户在医咖会上发布的信息不得侵犯任何第三人的知识产权，未经相关权利人之事先书面同意，用户不得以任何方式上传、发布、修改、传播或复制任何受著作权保护的材料、商标或属于其他人的专有信息。\n' +
        '5、用户同意，对于其上传到医咖会的任何内容，医咖会在全世界范围内不限形式和载体地享有永久的、不可撤销的、免费的、非独家的使用权和转授权的权利，包括但不限于修改、复制、发行、展览、改编、汇编、出版、翻译、信息网络传播、广播、表演和再创作及著作权法等法律法规确定的其他权利。\n' +
        '    \n' +
        '五、隐私权\n' +
        '    1、保护用户的隐私是医咖会的一项基本政策。\n' +
        '2、用户在使用医咖会服务时，会向医咖会提供个人信息，例如姓名、电子邮件地址、电话号码。用户同意后，医咖会在用户使用服务的过程中获取信息。此类信息包括但不限于：\n' +
        '    （1）设备信息--例如用户的硬件型号、操作系统版本、唯一设备识别码以及包括电话号码在内的移动网络信息。\n' +
        '    （2）位置信息--例如来自用户设备的传感器数据就可以提供附近 Wi-Fi 接入点和基站的信息。\n' +
        '    （3）本地存储--使用浏览器网络存储等机制（包括 HTML 5）和应用程序数据缓存，在用户的设备上收集信息（包括个人信息）并进行本地存储。\n' +
        '    （4）医生用户在医咖会上发布、储存的信息。\n' +
        '    \n' +
        '    \n' +
        '六、免责声明\n' +
        '    1、鉴于网络服务的特殊性，医咖会不保证网络服务的及时性、安全性和准确性，用户同意医咖会有权不经事先通知，随时变更、中断或终止部分或全部的网络服务而无论同意与否，医咖会对用户和任何第三人均无需承担任何责任。\n' +
        '2、对于经由医咖会服务而传送的内容，医咖会不保证前述内容的正确性、完整性或品质。用户在接受有关服务时，有可能会接触到令人不快、不适当或令人厌恶的内容。在任何情况下，医咖会均不对任何内容负责，包括但不限于任何内容发生任何错误或纰漏以及衍生的任何损失或损害。医咖会有权（但无义务）自行拒绝或删除经由本服务提供的任何内容。用户使用上述内容，应自行承担风险。\n' +
        '3、用户可通过医咖会有关网络服务获得第三方的某些内容，或者医咖会可能为方便用户而提供通往第三方网站的链接，但医咖会不负责检查或评估任何该等第三方材料、产品、服务或网站内容的准确性，并且，医咖会对此不作保证、不承担任何责任、也不负有任何义务。用户对此自行加以判断，并承担因使用该等内容而引起的所有风险，包括但不限于因对内容的正确性、完整性或实用性的依赖而产生的风险。\n' +
        '4、用户经由医咖会服务与广告商进行通讯联系或商业往来或参与促销活动，完全属于用户与广告商之间的行为，与医咖会没有任何关系，若因商业行为所产生之任何损害或损失，医咖会不承担任何责任。\n' +
        '5、用户明确同意其使用医咖会服务所存在的风险及其后果将完全由其自己承担，医咖会对用户不承担任何责任。如因用户违反有关法律、法规或本协议项下的任何条款而给医咖会或任何其他第三人造成损失，用户同意承担由此造成的损害赔偿责任。\n' +
        '    \n' +
        '七、其他\n' +
        '    1、本协议的版权归医咖会所有，医咖会保留对本协议的一切解释和修改权利。\n' +
        '2、本协议的订立、执行和争议的解决均应适用中华人民共和国法律。如双方就本协议内容或其执行发生任何争议，双方应尽量友好协商解决；协商不成时，任何一方均可向医咖会所在地有管辖权的人民法院提起诉讼。\n' +
        '3、医咖会未行使本协议的任何权利或规定，不构成对前述权利之放弃。\n' +
        '4、如本协议中的任何条款完全或部分无效，本协议的其余条款仍有效并且有约束力。</pre><div class="agreement_btn" >确认</div></div>',
        props: ['check_type'],
        data: function () {
            return {
                is_name_exist:null,
                cla: {
                    activeClass: 'v_show cancel_input',
                    errorClass: 'cancel_input'
                },
                //接口
                url: {
                    login: '/front/login/',
                    register: '/register/',
                    captcha: 'extends/captcha',
                    forget: 'front/forget_password/',
                    usr: '/user_info/'
                },
                error: {
                    login: {
                        username_or_email: '',
                        password: '',
                        error: ''
                    },
                    register: {
                        username: '',
                        email: '',
                        password: '',
                        repeat_password: '',
                        captcha: ''
                    },
                    captcha: {},
                    usr: {
                        fullname: '',
                        corporation: '',
                        profession_id: '',
                        gender: '',
                        job_id: ''
                    },
                    email: {
                        email: ''
                    }
                },//登录
                login: {
                    username_or_email: '',
                    password: ''
                },//忘记密码
                forget: {
                    email: ''
                },//注册
                register: {
                    username: '',
                    email: '',
                    password: '',
                    repeat_password: '',
                    captcha: '',
                },
                //信息
                usr: {
                    profession_id: '',
                    gender: '',
                    job_id: ''
                },
                usr_id: {
                    fullname:'',
                    corporation: '',
                    profession_id: '',
                    gender: '',
                    job_id: ''
                },
                usr_type: {
                    profession_id: false,
                    gender: false,
                    job_id: false
                },
                usr_list: {
                    profession_id: [
                        {
                            "section_grade": 2,
                            "professional_section_id": 2,
                            "id": 29,
                            "department_name": "中医内科"
                        },
                        {
                            "section_grade": 2,
                            "professional_section_id": 2,
                            "id": 30,
                            "department_name": "中医外科"
                        },

                    ],
                    job_id: [
                        {
                            "job_grade": 2,
                            "job_title_id": 2,
                            "id": 8,
                            "job_name": "住院医师"
                        },
                        {
                            "job_grade": 2,
                            "job_title_id": 2,
                            "id": 9,
                            "job_name": "药师"
                        },

                    ],
                    gender: [
                        {
                            "id": 0,
                            "sex": "男"
                        },
                        {
                            "id": 1,
                            "sex": "女"
                        },
                        {
                            "id": 2,
                            "sex": "保密"
                        }
                    ]
                },
                email: {
                    email: ''
                },
            }
        },
        methods: {
            close: function (item) {
                var search=''
                var redirect='/'
                if (window.location.search != ''){
                   search=window.location.search+window.location.hash
                }
                var pair_value = getParameterByName('next')
                if (pair_value != null){
                    redirect = pair_value
                }

                if (item === 2) {
                    window.location.href = '/register/'+search
                    return
                }
                if (item === 3) {
                    window.location.href = '/phone_login/'+search
                    return
                }
                // TODO 登录页 忘记密码 
                if (item === 4) {
                    window.location.href = '/forget_password/'
                    return
                }
                if(item===100){
                    window.location.href = redirect
                    return
                }
                check_type(item)
            },
            clearInput: function (num) {
                switch (num) {
                    case 1:
                        this.login.username_or_email = '';
                        break;
                    case 2:
                        this.login.password = '';
                        break;
                    case 3:
                        this.register.username = '';
                        break;
                    case 4:
                        this.register.email = '';
                        break;
                    case 5:
                        this.register.password = '';
                        break;
                    case 6:
                        this.register.repeat_password = '';
                        break;
                    case 7:
                        this.register.captcha = '';
                        break;
                    case 8:
                        this.usr_id.corporation = '';
                        break;
                }
            },
            nextList: function (item, list) {
                var _self = this;

                if (item === 1) {
                    AJAX({
                        type: 'get',
                        url: '/front_professional_sections/'+ list.id +'/',
                        data: '',
                        fn: function (data) {
                            if (data.data.professionalSections.length > 1) {
                                _self.usr_list.profession_id = data.data.professionalSections;
                            } else {
                                _self.usr.profession_id = list.department_name;
                                _self.usr_id.profession_id = list.id;
                                _self.usr_list.profession_id = '';
                                _self.usr_type.profession_id = false;
                                _self.error.usr.profession_id = "";
                            }
                        },
                        error: function () {
                            _self.usr.profession_id = list.department_name;
                            _self.usr_id.profession_id = list.id;
                            // _self.usr_list.profession_id='';
                            _self.usr_type.profession_id = false;
                            _self.error.usr.profession_id = "";
                        }
                    })

                } else if (item === 2) {
                    AJAX({
                        type: 'get',
                        url: '/front_job_title/'+ list.id+'/',
                        data: '',
                        fn: function (data) {
                            if (data.data.jobTitles.length > 1) {
                                _self.usr_list.job_id = data.data.jobTitles;
                            } else {
                                _self.usr.job_id = list.job_name;
                                _self.usr_id.job_id = list.id;
                                _self.usr_list.job_id = '';
                                _self.usr_type.job_id = false;
                                _self.error.usr.job_id = "";
                            }
                        },
                        error: function () {
                            _self.usr.job_id = list.job_name;
                            _self.usr_id.job_id = list.id;
                            // _self.usr_list.job_id='';
                            _self.usr_type.job_id = false;
                            _self.error.usr.job_id = "请选择职称";
                        }
                    })
                } else if (item === 3) {
                    _self.usr_id.gender = list.id;
                    _self.usr.gender = list.sex;
                    _self.usr_type.gender = false;
                    _self.error.usr.gender = ""
                }
            },
            show_list: function (item) {
                var _self = this
                switch (item) {
                    case 1:
                        if (!_self.usr_type.profession_id) {
                            _self.usr_type.profession_id = true;
                            _self.usr_type.gender = false;
                            _self.usr_type.job_id = false;
                            AJAX({
                                url:'/front_professional_sections/0/',
                                type:"get",
                                data:'',
                                fn:function (data) {
                                            if(data.code===200){
                                                _self.usr_list.profession_id=data.data.professionalSections;
                                            }
                                }
                            })

                        } else {
                            _self.usr_type.profession_id = false;
                        }
                        break
                    case 2:
                        if (!_self.usr_type.job_id) {
                            _self.usr_type.job_id = true;
                            _self.usr_type.gender = false;
                            _self.usr_type.profession_id = false;
                            AJAX({
                                url: '/front_job_title/0/',
                                type: "get",
                                data: '',
                                fn: function (data) {
                                    if (data.code === 200) {
                                        _self.usr_list.job_id = data.data.jobTitles;
                                    }
                                }
                            })
                        } else {
                            _self.usr_type.job_id = false;
                        }
                        break
                    case 3:
                        if (!_self.usr_type.gender) {
                            _self.usr_type.gender = true;
                            _self.usr_type.job_id = false;
                            _self.usr_type.profession_id = false;
                            // AJAX()
                        } else {
                            _self.usr_type.gender = false;
                        }
                        break
                }
            },
            click_tag: function (item) {
                var _self = this;
                var ePattern = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/; // 邮箱正则匹配
                var telPattern = /^[1]([3-9])[0-9]{9}$/; // 手机号正则匹配
                switch (item) {
                    case 1://登录
                        // 手机号校验
                        if ($('.username').val()==='') {
                            $('.error-tip').html('手机号或邮箱不能为空');
                            $('.error-tip').fadeIn(1000);
                            return false;
                        } else if (ePattern.test($('.username').val() === false) || telPattern.test($('.username').val() === false)) {
                            $('.error-tip').html('手机号或邮箱格式错误');
                            $('.error-tip').fadeIn(1000);
                            return false;
                        }
                        // 密码校验
                        if(!$('.password').val()){
                            $('.error-tip').html('密码不能为空');
                            $('.error-tip').fadeIn(1000);
                            return false;
                        }
                        if ($('.username').val() && $('.password').val()) {
                            AJAX({
                                type: 'post',
                                url: "/front_login/",
                                data: {
                                    username: $('.username').val(),
                                    password: $('.password').val(),
                                },
                                fn: function (data) {
                                    if (data.code === 200) {
                                        //成功
                                        if(data.data.redirect){
                                            window.location.href = data.data.redirect
                                        }
                                        else if(getUrlParam('next')){
                                            window.location.href= getUrlParam('next')
                                        }
                                        else{
                                           window.location.href = '/'
                                        }
                                        // check_type(0);
                                    } else {
                                        //失败
                                        data = data.data;
                                        $('.error-tip').html(data.message)
                                        $('.error-tip').fadeIn(1000)
                                    }
                                }
                            });
                        }
                        break;
                    case 2://注册
                        if (_self.register.username && _self.register.password && _self.register.repeat_password && _self.register.captcha && _self.register.email) {
                            AJAX({
                                type: 'post',
                                url: _self.url.register,
                                data: _self.register,
                                fn: function (data) {
                                    if (data.code === 200) {
                                        //成功
                                        // window.location.reload()
                                        check_type(3);
                                    } else {
                                        //失败
                                        data = data.data;
                                        data.username ? _self.error.register.username = data.username:_self.error.register.username ='';
                                        data.password ? _self.error.register.repeat_password = data.password:_self.error.register.repeat_password ='';
                                        data.captcha ? _self.error.register.captcha = data.captcha:_self.error.register.captcha ='';
                                        data.email ? _self.error.register.email = data.email:_self.error.register.email ='';

                                    }

                            }})
                        } else {
                            if (!_self.register.username) {
                                _self.error.register.username = "请输入用户名";
                            }
                            ;
                            if (!_self.register.password) {
                                _self.error.register.password = "请输入密码";
                            }
                            ;
                            if (!_self.register.repeat_password) {
                                _self.error.register.repeat_password = "请再次输入密码";
                            }
                            ;
                            if (!_self.register.captcha) {
                                _self.error.register.captcha = "请输入验证码";
                            }
                            ;
                            if (!_self.register.email) {
                                _self.error.register.email = "请输入邮箱";
                            }
                            ;
                        }
                        break
                    case 3://补全信息
                        // 测试BUG: 信息完善页面，只填写部分后，点击“完成”按钮，应该是跳转首页（登录状态）
                        if (_self.usr_id.profession_id && _self.usr_id.gender!=="" && _self.usr_id.job_id) {
                            AJAX({
                                type: 'post',
                                url: '/user_info/',
                                data: _self.usr_id,
                                fn: function (data) {
                                    if(data.code===200){
                                        var redirect='/'
                                        var pair_value = getParameterByName('next')
                                        if (pair_value != null){
                                            redirect = pair_value
                                        }
                                        window.location.href = redirect;
                                    }else{
                                        data = data.data;
                                        data.corporation ? _self.error.usr.corporation = data.corporation : _self.error.usr.corporation = '';
                                    }
                                }
                            })
                        } else {
                            if (_self.usr_id.gender === '') {
                                $('.error-tip').html("请选择性别")
                                $('.error-tip').fadeIn(1000)
                            };
                            if (!_self.usr_id.job_id) {
                                $('.error-tip').html("请选择职称")
                                $('.error-tip').fadeIn(1000)
                            };
                            if (!_self.usr_id.profession_id || _self.usr_id.profession_id === '') {
                                $('.error-tip').html("请选择专业科室")
                                $('.error-tip').fadeIn(1000)
                            };
                        }
                        break
                    case 4:
                        if (_self.forget.email) {
                            // check_type(5)
                            AJAX({
                                url: "/forget_password/",
                                type: "post",
                                data: {"email": _self.forget.email},
                                fn: function (data) {
                                    if(data.code===200){
                                    _self.close(5)
                                    _self.error.email.email = ""
                                    }else{
                                        _self.error.email.email=data.message;
                                    }
                                }
                            })

                        } else if (!_self.forget.email) {
                            _self.error.email.email = "请输入邮箱"
                        }

                }

            },
            login: function () {

            },
            register: function () {

            },
            img_captcha: img_captcha
        }
    })
    function img_captcha() {
        var num=Math.random()
        $('.img_captcha').css('background-image','url(/extends/captcha/?='+ num+')')
    }

    Vue.component('pc-collect-add',{
        template: '<div v-if="check_type===6" class="neko_shadow_box">\n' +
        '            <div class="pc2_collect">\n' +
        '                <div class="text-cen font-24 line-height36 pad-top28 pad-bot30">创建收藏夹</div>\n' +
        '                <div class="mar-top20"><input type="text" placeholder="名称" v-model="pc2_collect.val.collect_category">\n' +
        '                    <div class="error">{{pc2_collect.error.name}}</div>\n' +
        '                </div>\n' +
        '                <div class="mar-bot40 mar-top20"><textarea name="" id=" " placeholder="收藏描述（可选）" v-model="pc2_collect.val.summary"></textarea></div>\n' +
        '                <div class="text-cen">\n' +
        '                    <div class="btn-collect-close inline align-cen" @click="pc2_coll_close(old)">返回</div>\n' +
        '                    <div class="mar-left20 btn-collect inline align-cen" @click="pc2_coll_collect(old)">创建</div>\n' +
        '                </div>\n' +
        '            </div>\n' +
        '        </div>',
        props: ['check_type', 'old'],
        data: function () {
            return {
                pc2_collect: {
                    val: {
                        collect_category: "",
                        summary: ""

                    },
                    error: {
                        name: ''
                    }
                }
            }
        },
        methods: {
            pc2_coll_close: function (item) {
                this.pc2_collect.val.collect_category = '';
                this.pc2_collect.val.collect_content = '';
//                    this.check_type=0;
                check_type(item)

            },
            pc2_coll_collect: function (num) {
                var _self = this
                AJAX({
                    url: '/create_user_collect_category/',
                    type: 'post',
                    data: _self.pc2_collect.val,
                    fn: function (data) {
                        // _self.pc2_collect.val.collect_category = '';
                        // _self.pc2_collect.val.summary = '';
                        // check_type(num);
                        _self.pc2_collect.val.collect_category = '';
                        _self.pc2_collect.val.summary = '';
                        try {
                            $.ajax({
                                url: '/user_collect_category_list/',
                                type: 'get',
                                success: function (data) {
                                    var list = data.data.user_collect_category_list
                                    box.collect_lists = list;
                                    check_type(num);
                                }

                            })
                        }
                        catch (e) {

                        }
                    }
                })
            }
        }
    })

    var collection=Vue.component('pc-collect-list', {
        template: '  <div v-if="check_type===7" class="neko_shadow_box">\n' +
        '                    <div class="pc2_collect">\n' +
        '                    <div class="text-cen font-24 line-height36 pad-top28 ">添加到收藏夹</div>\n' +
        // '                    <div class="font-18 line-height25 mar-top10 pad-bot20 color-liter-grey f-200"></div>\n' +
        '                        <div class="height-323">\n' +
        '                                        <ul class="collect_list">\n' +
        '                                <li v-for="list in lists"><span class="inline" v-html="list.collect_category"></span><span class="color-link inline align-top font-14 right pointer video_top" @click="change_coll($event,list.id)" >收藏</span></li>\n' +
        '                            </ul>\n' +
        '                            <div class="push-coll mar-top10 line-height36 color-link font-16 text-left"><span @click="chose_item(6,7)" class="pointer" style="font-weight: 400">+创建收藏夹</span></div>\n' +
        '                        </div>\n' +
        '                   <div class="text-cen">\n' +
        // '                        <div class="btn-collect-close inline align-cen" @click="pc2_coll_list_close(old)">取消</div>\n' +
        '                        <div class="mar-left20 btn-collect inline align-cen" @click="pc2_coll_list_collect()">提交</div>\n' +
        '                    </div>\n' +
        '            </div>\n' +
        '        </div>',
        props: ['check_type', 'lists', 'old', 'user','video'],
        data: function () {
            return {
                chose: {},
                tag: ''
            }
        },
        methods: {
            pc2_coll_list_close: function (num) {
                box.coollect_list = ''
                check_type(num)
            },
            pc2_coll_list_collect: function () {
                if (!$('.login-on')[0]) {
                    window.location.href = '/login/?next=' + window.location.pathname+'#1'
                   // check_type(1)
                    return
                }
                var _self = this;
                if(!_self.tag){
                    $().alert_box('请选择收藏夹')
                    return
                }
                if(this.video){
                    $.ajax({
                        url:"/front_favorites/"+video_id+"/"+ _self.tag+"/3/",
                        type:"get",
                        success:function (data) {
                            console.log(data)
                            if(data.data.is_collect==1){
                                check_type(0)
                                $(".collect_button").data("collectId",_self.tag)
                                $(".star_gray").addClass("hide")
                                $(".star_light").removeClass("hide")
                            }
                        }
                    })
                }else {
                    AJAX({
                        url: '/collect_answer/' + _self.user.ans_id + '/' + _self.tag + '/',
                        type: 'get',
                        data: {},
                        fn: function () {
                            var s = _self.user.tar.html();
                            _self.user.tar.html(s.replace('收藏', '取消收藏'));
                            if (_self.user.fn) {
                                _self.user.fn();
                            }
                            // _self.user.tar.attr('ans_tag', _self.tag);
                            check_type(0)
                        }
                    })
                }
            },
            chose_item: function (item, old) {
                box.old_check = old
                check_type(item)
            },
            change_coll: function (e, i) {
                this.tag = i;
                $(e.target).addClass('checked').parents('li').siblings().find('.pointer').removeClass('checked')
            }
        }
    })


    Vue.component('pc-collect-chage', {
        template: '<div v-if="check_type===23" class="neko_shadow_box">\n' +
        '            <div class="pc2_collect">\n' +
        '                <div class="text-cen font-24 line-height36 pad-top28 pad-bot30">编辑收藏夹</div>\n' +
        '                <div class="mar-top20"><input type="text" placeholder="名称" v-model="val.collect_category">\n' +
        '                    <div class="error">{{pc2_collect.error.name}}</div>\n' +
        '                </div>\n' +
        '                <div class="mar-bot40 mar-top20"><textarea name="" id=" " placeholder="收藏描述（可选）" v-model="val.summary"></textarea></div>\n' +
        '                <div class="text-cen">\n' +
        '                    <div class="btn-collect-close inline align-cen" @click="pc2_coll_close(old)">返回</div>\n' +
        '                    <div class="mar-left20 btn-collect inline align-cen" @click="pc2_coll_collect(old)">保存</div>\n' +
        '                </div>\n' +
        '            </div>\n' +
        '        </div>',
        props: ['check_type', 'old', 'val'],
        data: function () {
            return {
                pc2_collect: {
                    val: {
                        collect_category: this.val.collect_category,
                        summary: "",
                        id: ''
                    },
                    error: {
                        name: ''
                    }
                }
            }
        },
        methods: {
            pc2_coll_close: function (item) {
                this.pc2_collect.val.collect_category = '';
                this.pc2_collect.val.collect_content = '';
                //  this.check_type=0;
                check_type(item)

            },
            pc2_coll_collect: function (num) {
                var _self = this;
               if(_self.val.collect_category===""){
                   $().alert_box('请输入分类名称')
                   return
               }
                AJAX({
                    url: '/alter_collect_category/'+_self.val.id+'/',
                    type: 'post',
                    data:{collect_category:_self.val.collect_category, summary:_self.val.summary},
                    fn: function (data) {
                        try {
                            $.ajax({
                                url: '/user_collect_category_list/',
                                type: 'get',
                                success: function (data) {
                                    if(data.code==200){
                                        var list = data.data.user_collect_category_list
                                        box.collect_lists = list;
                                        check_type(num);
                                    }else {
                                        $().alert_box(data.message)
                                    }

                                }
                            })
                        }
                        catch (e) {

                        }

                    }
                })
            }
        }
    })
// 上线前要将路径修改
    // var video_player=Vue.component('videoContainer',{
    //     template:`
   
    //     `,
    //     props:['vid'],
    //     data:function(){
    //         return{
    //             //播放器实例
    //             player:null,
    //             //视频列表
    //             video_list_vm:null,
    //             //当前视频vid
    //             vid_vm:this.vid,
    //             //当前视频是否免费
    //             is_free_vm:this.is_free,
    //             //视频标题
    //             study_title_vm:null,
    //             //右侧视频菜单列表
    //             menu_button:{content:"目录<<",open_state:false},
    //             //收藏栏显示状态
    //             isCollectionShow:false,
    //             //内嵌组件参数
    //             check_type:7,

    //             //当前视频被收藏状态
    //             isTargetVideoCollected:false,
    //             //当前播放的视频组
    //             video_group_vm:null
    //         }
    //     },
    //     methods: {
    //         //更换播放视频
    //         changeVideo:function(video,group_name){
    //             // this.video_group_vm=group_name
    //             // this.is_free_vm=video.is_free
    //             // this.vid_vm=video.vid
    //             // this.player.HTML5.changeVid ({vid:video.vid})
    //             // this.study_title_vm=group_name+"—"+video.name
    //             // //切换下方本期要点
    //             // $(`[data-vid="${video.vid}"]`).show().siblings().hide()
    //             location.replace("http://localhost:8000/method_vidoe/e8888b74d1229efec6b4712e17cb6b7a_e/")
    //         },
    //         // 自动换行
    //         autoWrap:function(video_name){
    //             if(video_name.length<7){
    //                 return video_name
    //             }else{
    //                 let newName=video_name.split("");
    //                 newName.splice(7,0,..."<br>")
    //                 return newName.join("")
    //             }
    //         },
    //         //开关课程目录
    //         toggle_video_list(){
    //             if(this.menu_button.open_state){
    //                 this.menu_button.open_state=false
    //                 this.menu_button.content="目录<<"

    //             }else{
    //                 this.menu_button.open_state=true
    //                 this.menu_button.content="目录>>"
    //             }
    //         },
    //         //打开收藏栏
    //         open_collection(){
    //             this.isCollectionShow=true
    //             //todo获取收藏状态
    //             this.isTargetVideoCollected=!this.isTargetVideoCollected
    //         },
    //         //关闭收藏栏
    //         close_collection(){
    //             this.isCollectionShow=false
    //         }
    //     },
    //     // 整理video_group group_video的结构
    //     beforeMount:function(){
    //         let vm=this;
    //         new Promise(function(resolve,reject){
    //             $.ajax({
    //                 url:"http://10.10.1.117:8000/video_detail/"+vm.vid_vm+"/",
    //                 type:"get",
    //                 headers: {
    //                     'X-Requested-With':'XMLHttpRequest'
    //                 },
    //                 success:function(data){
    //                     resolve(data.data)
    //                 }
    //             })
    //         }).then(function(data){
    //             console.log(data)
    //             let video_group_hash={}
    //             for(var val of data.course_section){
    //                     video_group_hash[val.course]=val.video_list
    //             }
    //             vm.video_list_vm=video_group_hash
    //             for(var a in video_group_hash){
    //                 vm.video_group_vm=a;
    //                 break;
    //             }
    //             vm.study_title_vm=data.course+"-"+data.title
    //             vm.player = polyvPlayer({
    //                 wrap: '#player',
    //                 width: 1155,
    //                 height:512,
    //                 vid:data.code,
    //                 code:data.code,
    //                 speed:false,
    //                 hideSwitchPlayer:true,
    //                 playsafe: function(vid, next) {
    //                     $.ajax({
    //                       type:"POST",
    //                       url: '自定义获取token的请求地址',
    //                       data: {
    //                         vid:vid
    //                       }
    //                     }).done(function(res) {
    //                       next(res.playsafe);
    //                     });
    //                 },
    //                 // logo: {
    //                 //     // 宽  默认 'auto'
    //                 //     logo_width: 200,
    //                 //     // 高  默认 'auto'
    //                 //     logo_height: 'auto',
    //                 //     // logo地址
    //                 //     logo_url: "/static/images/20171213113454.png",
    //                 //     // 位置 0,1,2,3,4 (隐藏、左上、右上、左下、右下)
    //                 //     logo_pos: 4,
    //                 //     // 跳转链接 (选填)
    //                 //     logo_link: 'http://www.polyv.net/',
    //                 //     // 透明度 (0~100)
    //                 //     logo_alpha: 50,
    //                 //     //logo偏移（根据左上角为原点的坐标，单位 % ，只在位置1，2生效）
    //                 //     logoOffset: '40,50'
    //                 //   }
    //               });
    //         })
    //         //             video_list='[{"name":"课程1","vid":"d81a899efa04df410e7adcbebeb064b1_d","is_free":true,"video_group_title":"Stata入门"},{"name":"课程2","vid":"456","is_free":true,"video_group_title":"Stata入门"},{"name":"课程3","vid":"d81a899efa04df410e7adcbebeb064b1_d","is_free":false,"video_group_title":"创建数据集"}]'

    //     },
    //     mounted:function(){
    //         let vm=this

    //     },
    //     components:{
    //         "pc-collect-list":collection
    //     }
    // })

    function AJAX(option) {
        $.ajax({
            type: option.type,  //提交方式
            url: option.url,//路径
            data: option.data,//数据
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

    function check_type(item) {
        if (item === 10) {
            window.location.href = '/ask_question/?next=' + window.location.pathname + '&_=' + Math.random();
            return
        }
        box.check_type = item;
        item === 0 ? $('#pc-state-box').addClass('hide') : $('#pc-state-box').removeClass('hide');
        switch (item) {
            case 0:
                break
            case 1:
                break;
            case 2:
                img_captcha()
                break;
            case 3:
                break;
            case 4:
                break;
            case 5:
                break;
            case 6:
                break;
            case 7:
                break;
            case 8:
                break;
            case 11:
                $(document.body).on('click','.agreement_btn',reg)
                function reg() {
                    check_type(2);
                    $(document.body).off('click','.agreement_btn',reg)
                }
                break
        }
        window.location.hash=item
    }
    $(document).on('click','#login',function () {
        window.location.href = '/login/?next=' + window.location.pathname + '#1'
    })
    $(document).on('click','#register',function () {
        // check_type(2)
        window.location.href = '/register/'
    })
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

    /*底部沉底*/
    $(document).ready(function () {
        $(document.body).trigger('click')
        $(window).resize(function () {
            fix_foot()
        })
    })
    function fix_foot() {
        $('#footer').css('position', function () {
            var a = document.body.clientHeight, b = $(window).height()
a=$(document.body).height()
            $('#footer').css('position', function () {
                if (b >= a && (b-a)>57) {
                    // $('#footer').removeClass('hide')
                    return 'fixed'
                } else {
                    return 'static'
                }
            })

            // var win_hei = $(window).height();
            // var con_hei
            // if ($('#container')[0]) {
            //     con_hei = $('#container').height() + 93;
            // } else if ($('#questions-pc2').height()) {
            //     con_hei = $('#questions-pc2').height() + 106
            // } else {
            //     return 'static'
            // }
            //
            // var top_hei = $('#header-pc2').next().height()
            // if (win_hei - con_hei >= 67) {
            //     // $('#footer').removeClass('hide')
            //     return 'fixed'
            // } else {
            //     return 'static'
            // }
        })
    }
    $(document).on('click', function () {
        var set_foot = window.setTimeout(function () {
            fix_foot();
            window.clearTimeout(set_foot)
        }, 200)
    });
    //
    $(document).ready(function () {
        /*
        * 消息
        * */


        $(document).on('click', '.masg_list .masg_list_top .icon-meun-hov', function () {
            var type = $(this).find('span').attr('type')
            $(this).addClass('checked').siblings().removeClass('checked');
            $('.masg_list .masg_ans_list ul[type=' + type + ']').removeClass('hide').siblings().addClass('hide');
            $('.masg .masg_list').css('display', 'block')
        })
        $(document).on('click', '.masg_list .masg_list_top .icon-meun-hov span', function () {
            var type = $(this).parent().find('span').attr('type')
            $(this).parent().addClass('checked').siblings().removeClass('checked');
            $('.masg_list .masg_ans_list ul[type=' + type + ']').removeClass('hide').siblings().addClass('hide');
            $('.masg .masg_list').css('display', 'block')
        })
        $(document).on('click', '.masg_list a', function () {
            window.open($(this).attr('href'))
            $('.masg .masg_list').toggle()
            return false

        })
        $(document).on('click', '.masg_list span', function () {
            if($(this).attr('link')){
                window.open($(this).attr('link'))
                $('.masg .masg_list').toggle()
            }
            if($(this).hasClass('clear_message')){
                $.ajax({
                    url:'/delete_my_messages_info/',
                    type:'get',
                    success:function (data) {
                        if(data.code !=200){
                            return
                        }
                        $('.masg_ans_list ul[type="ans"]').html('');
                        $('.masg_head i').html('')
                        $('.masg .masg_list').toggle()
                        return
                    }
                })
            }
            return false

        })
        $(document).on('click', '.masg_list *', function () {
            $('.masg .masg_list').css('display', 'block')
            return false

        })
        $(document).on('click', function (e) {
            // return false
            if ($(e.target)[0].tagName.toLowerCase() === 'i' && $(e.target).parent().hasClass('masg_head')) {
                $(e.target).parent().next().toggle()
            } else if ($(e.target).hasClass('masg_head') || $(e.target).parent().hasClass('masg_head')) {
                $(e.target).next().toggle()
            } else if (!$(e.target).hasClass('icon-meun-hov') || !$(e.target).hasClass('masg_list_top') || !$(e.target).hasClass('masg_list_top')) {
                $('.masg .masg_list').css('display', 'none')
            }
        })
    })


    $.prototype.alert_box = function (str) {
        var s = '<div id="alert_shadow_box" style="">\n' +
            '    <div class="show neko_shadow_box">\n' +
            '        <div id="model_alert_box">\n' +
            '            <div>\n' +
            '                <div  class="alert_box_content">' + str + '</div>\n' +
            '                <div class="model_btn block-center " id="alert_box_19829495">确认</div>\n' +
            '            </div>\n' +
            '        </div>\n' +
            '    </div>\n' +
            '</div>';
        $(document).on('click', '#alert_box_19829495', function () {
            $('#alert_shadow_box').remove()
        })
        $(document.body).append(s);
    }

    $.prototype.user_info_alert_box = function(){
        var html = '<div id="user_download_alert_container" style="position:fixed;height:100%;background:rgba(53, 53, 53, 0.9);width:100%;top:0;left:0;z-index:10000;font-family: -apple-system-font, Helvetica Neue, PingFang SC, Hiragino Sans GB, Microsoft YaHei, sans-serif;">'
                  +'      <div class="user_download_alert" style="width:400px;height:200px;text-align:center;position:fixed;top:50%;left:50%;background:#fff;margin-top:-100px;margin-left:-200px;font-size: 18px;font-weight:400;color: #4a4a4a;border-radius:2px;">'
                  +'          <div style="margin-top:50px;margin-bottom:20px;font-weight: 300;font-size:18px;line-height:27px">请先到个人中心<br>补充完善个人资料信息</div>'
                  +'          <div id="cancel_user_download_alert" style="display:inline-block;width:120px;height:40px;vertical-align:top;line-height:40px;font-size: 18px;line-height:40px;cursor:pointer;font-weight: 500;border-radius: 4px;background-color: #bcc1cc;">取消</div>'
                  +'          <div id="go_to_personal_center" style="display:inline-block;width:120px;height:40px;margin-left:10px;background-color: rgb(55, 174, 242);font-size: 18px;line-height:40px;color: #f8fafd;cursor:pointer;font-weight: 500;border-radius: 4px;" >确定</div>'
                  +'      </div>'
                  +'  </div>';
            $(document.body).append(html);
            $("#go_to_personal_center").click(function(){
                window.location.href="/user/?t=user"
            })
            $("#cancel_user_download_alert").click(function(){
                $("#user_download_alert_container").remove()
            })
    }   

    //点赞
    var fig_click=function () {
        if (!$('.login-on')[0]) {
            window.location.href = '/login/?next=' + window.location.pathname+'#1'
           // check_type(1)
            return
        }
        var self = $(this);
        var ques = $(this).attr('ques_id');
        if($(this).attr('typ')==='false'||!$(this).attr('typ')) {
            $(this).attr('typ', 'true');
            $.ajax({
                url: '/praise_answer/' + ques + '/',
                type: 'get',
                success: function (data) {
                    if (data.data.is_praise === 1) {
                        var st = self.html();
                        var num = 0
                        st.replace(new RegExp('(<[^>]+>)', 'g'), '').replace(/\d+/, function (item) {
                            num = Number(item);
                            return item + 1
                        })
                        self.html(st.replace(new RegExp(num, 'g'), '已赞 ' + (num + 1)))
                    } else {
                        var st = self.html();
                        var num = 0
                        st.replace(new RegExp('(<[^>]+>)', 'g'), '').replace(/\d+/, function (item) {
                            num = Number(item);
                            return item - 1
                        })
                        self.html(st.replace(new RegExp(num, 'g'), num - 1).replace(/已赞/g , ''))
                    }
                }
            });
        }else {
            var timera=window.setTimeout(function () {
                self.attr('typ', 'false')
                window.clearTimeout(timera)
            },1000)
        }
    }
    $(document).on('click', '.user-fig', fig_click)

    $(document).on('click','.login_log',function () {
        window.location.href = '/login/?next='+window.location.pathname+'#1'
        //check_type(1)
    })

    
