webpackJsonp([2], {
    15: function (e, t, n) {
        var r = n(56);
        "string" == typeof r && (r = [[e.i, r, ""]]);
        var i = {};
        i.transform = void 0;
        n(2)(r, i);
        r.locals && (e.exports = r.locals)
    }, 27: function (e, t, n) {
        (function (e) {
            var t, n, r;
            window.jQuery = e, t = !1, r = !0, n = 0, e(document).ready(function () {
                try{
                    e(document).on("change", "#yika_img_up_2", function () {
                        var oMyForm;
                        var _self = this;
                        if (!this['value'].match(/.jpg|.gif|.png|.bmp|.JPEG|svg|/i)) {
                            return
                        }
                        var oMyForm = new FormData();
                        oMyForm.append("imgFile", $('#yika_img_up_2')[0].files[0]);
                        $.ajax({
                            type: 'post',
                            url: '/extends/image_storage/webapp_images/',
                            data: oMyForm,
                            dataType: 'json',
                            contentType: false,
                            processData: false,
                            success: function (e) {
                                CKEDITOR.instances.ask_ar_2.insertHtml("<img src='http://www.mediecogroup.com/images/webapp_images/" + e.data + "'>")

                            }

                        })
                    })
                    CKEDITOR.replace("ask_ar_2", {customConfig: "../ckeditor.wechat2.js"}, CKEDITOR.on("instanceCreated", function (n) {
                        return n.editor.on("change", function (n) {
                            // return (CKEDITOR.instances.ask_area_2.getData().length > 0 && post_tag !== null) ?
                            //     $('#model_ask_ques .model_btn').css('background-color', '#37aef2').css('cursor', 'pointer') : $('#model_ask_ques .model_btn').css('background-color', '#ccc').css('cursor', 'no-drop')
                        })
                    }))
                }catch (e){

                }
                try {
                    e(document).on("change", "#yika_img_upload", function () {
                        var oMyForm;
                        var _self = this;
                        if (!this['value'].match(/.jpg|.gif|.png|.bmp|.JPEG|svg|/i)) {
                            return
                        }
                        var oMyForm = new FormData();
                        oMyForm.append("imgFile", $('#yika_img_upload')[0].files[0]);
                        $.ajax({
                            type: 'post',
                            url: '/extends/image_storage/webapp_images/',
                            data: oMyForm,
                            dataType: 'json',
                            contentType: false,
                            processData: false,
                            success: function (e) {
                                var s = CKEDITOR.instances.ask_area.getData().replace('<div style="color: #C3C3C3">请仔细阅读右方提问注意事项后再提问</div>', '').replace(new RegExp(' ', 'g'), '').replace('\n', '')
                                if (s.length <= 0) {
                                    CKEDITOR.instances.ask_area.setData("<img src='http://www.mediecogroup.com/images/webapp_images/" + e.data + "'>")
                                } else {
                                    CKEDITOR.instances.ask_area.insertHtml("<img src='http://www.mediecogroup.com/images/webapp_images/" + e.data + "'>")
                                }
                            }
                        })
                    })
                    var n = e(window).height();
                    window.askarea_key=true;
                    window.ajax_key_search=true
                    CKEDITOR.replace("ask_area", {customConfig: "../ckeditor.wechat_answer_config.js"}, CKEDITOR.on("instanceCreated", function (n) {
                        n.editor.on("blur", function (n) {
                            if(!window.askarea_key){
                                return
                            }
                            var s= CKEDITOR.instances.ask_area.getData().replace('<div style="color: #C3C3C3">请仔细阅读右方提问注意事项后再提问</div>','').replace(new RegExp(' ','g'),'').replace('\n', '')
                            if(s.length<=0){
                                CKEDITOR.instances.ask_area.setData('<div style="color: #C3C3C3">请仔细阅读右方提问注意事项后再提问</div>')
                            }
                        })
                        n.editor.on("focus", function (n) {
                            var s= CKEDITOR.instances.ask_area.getData().replace('<div style="color: #C3C3C3">请仔细阅读右方提问注意事项后再提问</div>','').replace(new RegExp(' ','g'),'').replace('\n', '')
                            if(s.length<=0){
                                CKEDITOR.instances.ask_area.setData('')
                            }
                        })
                        n.editor.on('change',function () {
                            if(window.ajax_key_search) {
                                if (CKEDITOR.instances.ask_area.getData().replace('<div style="color: #C3C3C3">请仔细阅读右方提问注意事项后再提问</div>', '').replace(new RegExp(' ', 'g'), '').replace(new RegExp('(<[^>]+>)', 'g'), '').replace(new RegExp('\n', 'g'), '').replace(new RegExp('&nbsp;', 'g'), '').length > 0) {
                                    // window.ajax_key_search=false
                                    $.ajax({
                                        url: '/search_key_word/',
                                        type: 'post',
                                        data: {search_key_word: CKEDITOR.instances.ask_area.getData().replace('<div style="color: #C3C3C3">请仔细阅读右方提问注意事项后再提问</div>', '').replace(new RegExp(' ', 'g'), '').replace(new RegExp('(<[^>]+>)', 'g'), '').replace(new RegExp('\n', 'g'), '').replace(new RegExp('&nbsp;', 'g'), '')},
                                        success: function (data) {
                                            // var key_search=window.setTimeout(function () {
                                            //     window.ajax_key_search=true;
                                            //     window.clearTimeout(key_search)
                                            // },100)
                                            if (data.code == 200) {
                                                var list = data.data.articles, str = '';
                                                if (list.length > 0) {
                                                    for (var i = 0; i < list.length; i++) {
                                                        if (list[i].type === 1 ) {
                                                            if (list[i].category_id ===13){
                                                                str += '<li><a href="/method_topic_article_detail/' + list[i].id + '/" title="' + list[i].title + '" target="_blank">' + list[i].title + '</a></li>'
                                                                continue
                                                            }
                                                            if (list[i].rank === 0) {
                                                                str += '<li><a href="/method_article_detail/' + list[i].id + '/" title="' + list[i].title + '" target="_blank">' + list[i].title + '</a></li>'
                                                            } else if (list[i].rank === 1) {
                                                                str += '<li><a href="/method_article_detail/' + list[i].id + '/" title="' + list[i].title + '" target="_blank">' + list[i].title + '  (最新)</a></li>'
                                                            } else if (list[i].rank === 2) {
                                                                str += '<li><a href="/method_article_detail/' + list[i].id + '/" title="' + list[i].title + '" target="_blank">' + list[i].title + '  (简单版)</a></li>'
                                                            } else if (list[i].rank === 3) {
                                                                str += '<li><a href="/method_article_detail/' + list[i].id + '/" title="' + list[i].title + '" target="_blank">' + list[i].title + '  (详细版)</a></li>'
                                                            }
                                                        } else {
                                                            str += '<li><a href="/method_topic_detail/' + list[i].id + '/1/" title="' + list[i].title + '" target="_blank">' + list[i].title + '</a></li>'
                                                        }
                                                    }
                                                    $('#ask-key-box ul').html(str);
                                                    $('#ask-key-box').removeClass('hide');
                                                }
                                            }
                                        }
                                    })
                                }
                            }

                        })
                    }))
                    CKEDITOR.instances.ask_area.setData('<div style="color: #C3C3C3">请仔细阅读右方提问注意事项后再提问</div>')

                } catch (e) {

                }
            })


            window.yikalink = function (num) {
window.askarea_key=false
                return e("body").append('<div id="shadow_box"><div class="tips_box tps_link"><div class="content_area content_link"><div class="link_name"><input placeholder="请输入内容..."/></div><div class="link_address"><input placeholder="请输入链接..."/></div></div><div class="box_btn_area"><div class="box_btn_multi_left cancel">取消</div><div class="box_btn_multi_right submit submit1">添加</div></div></div></div>'), e(document).on("click", ".submit1", function () {
                    var t;

                    return t = new RegExp(/http(s)?:\/\/([\w-]+\.)+[\w-]+(\/[\w- .\/?%&=]*)?/), t.test(e(".link_address input").val()) ? (CKEDITOR.instances.ask_area.insertHtml("<a href='" + e(".link_address input").val() + "' target='_blank'>" + escapeHtml(e(".link_name input").val()) + "</a>"), e("#shadow_box").remove(),window.askarea_key=true) : (e(".wrong_image,.wrong_link").remove(), e(".content_link").append('<div class="wrong_image"></div><div class="wrong_link">超链接格式错误</div>'), e(".tps_link").css("min-height", "13.36rem"))
                }), e(document).on("click", ".cancel", function () {
                    return e("#shadow_box").remove(), e(document).off("click", ".cancel")
                })

            },
                window.yikali2 = function () {
                    return e("body").append('<div id="shadow_box"><div class="tips_box tps_link"><div class="content_area content_link"><div class="link_name"><input placeholder="请输入内容..."/></div><div class="link_address"><input placeholder="请输入链接..."/></div></div><div class="box_btn_area"><div class="box_btn_multi_left cancel">取消</div><div class="box_btn_multi_right submit submit2">添加</div></div></div></div>'), e(document).on("click", ".submit2", function () {
                        var t;
                        return t = new RegExp(/http(s)?:\/\/([\w-]+\.)+[\w-]+(\/[\w- .\/?%&=]*)?/), t.test(e(".link_address input").val()) ? (CKEDITOR.instances.ask_ar_2.insertHtml("<a href='" + e(".link_address input").val() + "'  target='_blank'>" + escapeHtml(e(".link_name input").val()) + "</a>"), e("#shadow_box").remove()) : (e(".wrong_image,.wrong_link").remove(), e(".content_link").append('<div class="wrong_image"></div><div class="wrong_link">超链接格式错误</div>'), e(".tps_link").css("min-height", "13.36rem"))
                    }), e(document).on("click", ".cancel", function () {
                        return e("#shadow_box").remove(), e(document).off("click", ".cancel")
                    })
                }
        }).call(t, n(76))
    }, 39: function (e, t, n) {
        (function () {
            n(1), n(27), n(0), n(8), n(5), n(10), n(6), n(15)
        }).call(this)
    }, 56: function (e, t, n) {
        t = e.exports = n(3)(void 0), t.push([e.i, '\n\n.submit,\n.cancel,\n.promt_btn {\n  cursor: pointer; }\n\n#promt_btn {\n  padding-top: 2.14rem; }\n\n#shadow_box .content_area {\n  padding: 1.29rem 1.57rem 0rem 1.57rem; }\n\n#shadow_box .tips_box {\n  min-height: 11.36rem; }\n\n#shadow_box .tps_link {\n  min-height: 11.36rem; }\n\n#shadow_box .link_name {\n  margin-bottom: 1.07rem; }\n\n#shadow_box .link_name,\n#shadow_box .link_address {\n  height: 2.14rem;\n  background-color: #F2F3F4;\n  border: 1px solid #EAEAF1;\n  border-radius: 2px; }\n  #shadow_box .link_name input,\n  #shadow_box .link_address input {\n    height: 100%;\n    background-color: rgba(255, 255, 255, 0);\n    width: 100%;\n    font-size: .86rem;\n    padding-left: .71rem;\n    box-sizing: border-box; }\n\n#shadow_box .wrong_link {\n  padding-top: .86rem;\n  color: #F05E32;\n  font-size: .86rem;\n  display: inline-block;\n  vertical-align: top; }\n\n#shadow_box .wrong_image {\n  background: url("/wechat_2.0/img/wrong_orange.svg") no-repeat;\n  display: inline-block;\n  width: 1.07rem;\n  height: 1rem;\n  margin-top: 0.86rem;\n  padding-right: .43rem; }\n', ""])
    }, 76: function (e, t, n) {
        var r, i;
        !function (t, n) {
            "use strict";
            "object" == typeof e && "object" == typeof e.exports ? e.exports = t.document ? n(t, !0) : function (e) {
                if (!e.document) throw new Error("jQuery requires a window with a document");
                return n(e)
            } : n(t)
        }("undefined" != typeof window ? window : this, function (n, o) {
            "use strict";

            function a(e, t) {
                t = t || ae;
                var n = t.createElement("script");
                n.text = e, t.head.appendChild(n).parentNode.removeChild(n)
            }

            function s(e) {
                var t = !!e && "length" in e && e.length, n = ye.type(e);
                return "function" !== n && !ye.isWindow(e) && ("array" === n || 0 === t || "number" == typeof t && t > 0 && t - 1 in e)
            }

            function u(e, t) {
                return e.nodeName && e.nodeName.toLowerCase() === t.toLowerCase()
            }

            function l(e, t, n) {
                return ye.isFunction(t) ? ye.grep(e, function (e, r) {
                    return !!t.call(e, r, e) !== n
                }) : t.nodeType ? ye.grep(e, function (e) {
                    return e === t !== n
                }) : "string" != typeof t ? ye.grep(e, function (e) {
                    return fe.call(t, e) > -1 !== n
                }) : Ee.test(t) ? ye.filter(t, e, n) : (t = ye.filter(t, e), ye.grep(e, function (e) {
                    return fe.call(t, e) > -1 !== n && 1 === e.nodeType
                }))
            }

            function c(e, t) {
                for (; (e = e[t]) && 1 !== e.nodeType;) ;
                return e
            }

            function f(e) {
                var t = {};
                return ye.each(e.match(Ae) || [], function (e, n) {
                    t[n] = !0
                }), t
            }

            function d(e) {
                return e
            }

            function p(e) {
                throw e
            }

            function h(e, t, n, r) {
                var i;
                try {
                    e && ye.isFunction(i = e.promise) ? i.call(e).done(t).fail(n) : e && ye.isFunction(i = e.then) ? i.call(e, t, n) : t.apply(void 0, [e].slice(r))
                } catch (e) {
                    n.apply(void 0, [e])
                }
            }

            function g() {
                ae.removeEventListener("DOMContentLoaded", g), n.removeEventListener("load", g), ye.ready()
            }

            function m() {
                this.expando = ye.expando + m.uid++
            }

            function v(e) {
                return "true" === e || "false" !== e && ("null" === e ? null : e === +e + "" ? +e : Pe.test(e) ? JSON.parse(e) : e)
            }

            function y(e, t, n) {
                var r;
                if (void 0 === n && 1 === e.nodeType) if (r = "data-" + t.replace(Re, "-$&").toLowerCase(), "string" == typeof(n = e.getAttribute(r))) {
                    try {
                        n = v(n)
                    } catch (e) {
                    }
                    Fe.set(e, t, n)
                } else n = void 0;
                return n
            }

            function x(e, t, n, r) {
                var i, o = 1, a = 20, s = r ? function () {
                        return r.cur()
                    } : function () {
                        return ye.css(e, t, "")
                    }, u = s(), l = n && n[3] || (ye.cssNumber[t] ? "" : "px"),
                    c = (ye.cssNumber[t] || "px" !== l && +u) && Me.exec(ye.css(e, t));
                if (c && c[3] !== l) {
                    l = l || c[3], n = n || [], c = +u || 1;
                    do {
                        o = o || ".5", c /= o, ye.style(e, t, c + l)
                    } while (o !== (o = s() / u) && 1 !== o && --a)
                }
                return n && (c = +c || +u || 0, i = n[1] ? c + (n[1] + 1) * n[2] : +n[2], r && (r.unit = l, r.start = c, r.end = i)), i
            }

            function b(e) {
                var t, n = e.ownerDocument, r = e.nodeName, i = Ue[r];
                return i || (t = n.body.appendChild(n.createElement(r)), i = ye.css(t, "display"), t.parentNode.removeChild(t), "none" === i && (i = "block"), Ue[r] = i, i)
            }

            function w(e, t) {
                for (var n, r, i = [], o = 0, a = e.length; o < a; o++) r = e[o], r.style && (n = r.style.display, t ? ("none" === n && (i[o] = Oe.get(r, "display") || null, i[o] || (r.style.display = "")), "" === r.style.display && $e(r) && (i[o] = b(r))) : "none" !== n && (i[o] = "none", Oe.set(r, "display", n)));
                for (o = 0; o < a; o++) null != i[o] && (e[o].style.display = i[o]);
                return e
            }

            function T(e, t) {
                var n;
                return n = void 0 !== e.getElementsByTagName ? e.getElementsByTagName(t || "*") : void 0 !== e.querySelectorAll ? e.querySelectorAll(t || "*") : [], void 0 === t || t && u(e, t) ? ye.merge([e], n) : n
            }

            function C(e, t) {
                for (var n = 0, r = e.length; n < r; n++) Oe.set(e[n], "globalEval", !t || Oe.get(t[n], "globalEval"))
            }

            function k(e, t, n, r, i) {
                for (var o, a, s, u, l, c, f = t.createDocumentFragment(), d = [], p = 0, h = e.length; p < h; p++) if ((o = e[p]) || 0 === o) if ("object" === ye.type(o)) ye.merge(d, o.nodeType ? [o] : o); else if (Ge.test(o)) {
                    for (a = a || f.appendChild(t.createElement("div")), s = (Xe.exec(o) || ["", ""])[1].toLowerCase(), u = Ve[s] || Ve._default, a.innerHTML = u[1] + ye.htmlPrefilter(o) + u[2], c = u[0]; c--;) a = a.lastChild;
                    ye.merge(d, a.childNodes), a = f.firstChild, a.textContent = ""
                } else d.push(t.createTextNode(o));
                for (f.textContent = "", p = 0; o = d[p++];) if (r && ye.inArray(o, r) > -1) i && i.push(o); else if (l = ye.contains(o.ownerDocument, o), a = T(f.appendChild(o), "script"), l && C(a), n) for (c = 0; o = a[c++];) Ke.test(o.type || "") && n.push(o);
                return f
            }

            function E() {
                return !0
            }

            function D() {
                return !1
            }

            function S() {
                try {
                    return ae.activeElement
                } catch (e) {
                }
            }

            function j(e, t, n, r, i, o) {
                var a, s;
                if ("object" == typeof t) {
                    "string" != typeof n && (r = r || n, n = void 0);
                    for (s in t) j(e, s, n, r, t[s], o);
                    return e
                }
                if (null == r && null == i ? (i = n, r = n = void 0) : null == i && ("string" == typeof n ? (i = r, r = void 0) : (i = r, r = n, n = void 0)), !1 === i) i = D; else if (!i) return e;
                return 1 === o && (a = i, i = function (e) {
                    return ye().off(e), a.apply(this, arguments)
                }, i.guid = a.guid || (a.guid = ye.guid++)), e.each(function () {
                    ye.event.add(this, t, i, r, n)
                })
            }

            function N(e, t) {
                return u(e, "table") && u(11 !== t.nodeType ? t : t.firstChild, "tr") ? ye(">tbody", e)[0] || e : e
            }

            function A(e) {
                return e.type = (null !== e.getAttribute("type")) + "/" + e.type, e
            }

            function _(e) {
                var t = nt.exec(e.type);
                return t ? e.type = t[1] : e.removeAttribute("type"), e
            }

            function q(e, t) {
                var n, r, i, o, a, s, u, l;
                if (1 === t.nodeType) {
                    if (Oe.hasData(e) && (o = Oe.access(e), a = Oe.set(t, o), l = o.events)) {
                        delete a.handle, a.events = {};
                        for (i in l) for (n = 0, r = l[i].length; n < r; n++) ye.event.add(t, i, l[i][n])
                    }
                    Fe.hasData(e) && (s = Fe.access(e), u = ye.extend({}, s), Fe.set(t, u))
                }
            }

            function L(e, t) {
                var n = t.nodeName.toLowerCase();
                "input" === n && ze.test(e.type) ? t.checked = e.checked : "input" !== n && "textarea" !== n || (t.defaultValue = e.defaultValue)
            }

            function H(e, t, n, r) {
                t = le.apply([], t);
                var i, o, s, u, l, c, f = 0, d = e.length, p = d - 1, h = t[0], g = ye.isFunction(h);
                if (g || d > 1 && "string" == typeof h && !ve.checkClone && tt.test(h)) return e.each(function (i) {
                    var o = e.eq(i);
                    g && (t[0] = h.call(this, i, o.html())), H(o, t, n, r)
                });
                if (d && (i = k(t, e[0].ownerDocument, !1, e, r), o = i.firstChild, 1 === i.childNodes.length && (i = o), o || r)) {
                    for (s = ye.map(T(i, "script"), A), u = s.length; f < d; f++) l = i, f !== p && (l = ye.clone(l, !0, !0), u && ye.merge(s, T(l, "script"))), n.call(e[f], l, f);
                    if (u) for (c = s[s.length - 1].ownerDocument, ye.map(s, _), f = 0; f < u; f++) l = s[f], Ke.test(l.type || "") && !Oe.access(l, "globalEval") && ye.contains(c, l) && (l.src ? ye._evalUrl && ye._evalUrl(l.src) : a(l.textContent.replace(rt, ""), c))
                }
                return e
            }

            function O(e, t, n) {
                for (var r, i = t ? ye.filter(t, e) : e, o = 0; null != (r = i[o]); o++) n || 1 !== r.nodeType || ye.cleanData(T(r)), r.parentNode && (n && ye.contains(r.ownerDocument, r) && C(T(r, "script")), r.parentNode.removeChild(r));
                return e
            }

            function F(e, t, n) {
                var r, i, o, a, s = e.style;
                return n = n || at(e), n && (a = n.getPropertyValue(t) || n[t], "" !== a || ye.contains(e.ownerDocument, e) || (a = ye.style(e, t)), !ve.pixelMarginRight() && ot.test(a) && it.test(t) && (r = s.width, i = s.minWidth, o = s.maxWidth, s.minWidth = s.maxWidth = s.width = a, a = n.width, s.width = r, s.minWidth = i, s.maxWidth = o)), void 0 !== a ? a + "" : a
            }

            function P(e, t) {
                return {
                    get: function () {
                        return e() ? void delete this.get : (this.get = t).apply(this, arguments)
                    }
                }
            }

            function R(e) {
                if (e in dt) return e;
                for (var t = e[0].toUpperCase() + e.slice(1), n = ft.length; n--;) if ((e = ft[n] + t) in dt) return e
            }

            function I(e) {
                var t = ye.cssProps[e];
                return t || (t = ye.cssProps[e] = R(e) || e), t
            }

            function M(e, t, n) {
                var r = Me.exec(t);
                return r ? Math.max(0, r[2] - (n || 0)) + (r[3] || "px") : t
            }

            function W(e, t, n, r, i) {
                var o, a = 0;
                for (o = n === (r ? "border" : "content") ? 4 : "width" === t ? 1 : 0; o < 4; o += 2) "margin" === n && (a += ye.css(e, n + We[o], !0, i)), r ? ("content" === n && (a -= ye.css(e, "padding" + We[o], !0, i)), "margin" !== n && (a -= ye.css(e, "border" + We[o] + "Width", !0, i))) : (a += ye.css(e, "padding" + We[o], !0, i), "padding" !== n && (a += ye.css(e, "border" + We[o] + "Width", !0, i)));
                return a
            }

            function $(e, t, n) {
                var r, i = at(e), o = F(e, t, i), a = "border-box" === ye.css(e, "boxSizing", !1, i);
                return ot.test(o) ? o : (r = a && (ve.boxSizingReliable() || o === e.style[t]), "auto" === o && (o = e["offset" + t[0].toUpperCase() + t.slice(1)]), (o = parseFloat(o) || 0) + W(e, t, n || (a ? "border" : "content"), r, i) + "px")
            }

            function B(e, t, n, r, i) {
                return new B.prototype.init(e, t, n, r, i)
            }

            function U() {
                ht && (!1 === ae.hidden && n.requestAnimationFrame ? n.requestAnimationFrame(U) : n.setTimeout(U, ye.fx.interval), ye.fx.tick())
            }

            function z() {
                return n.setTimeout(function () {
                    pt = void 0
                }), pt = ye.now()
            }

            function X(e, t) {
                var n, r = 0, i = {height: e};
                for (t = t ? 1 : 0; r < 4; r += 2 - t) n = We[r], i["margin" + n] = i["padding" + n] = e;
                return t && (i.opacity = i.width = e), i
            }

            function K(e, t, n) {
                for (var r, i = (Y.tweeners[t] || []).concat(Y.tweeners["*"]), o = 0, a = i.length; o < a; o++) if (r = i[o].call(n, t, e)) return r
            }

            function V(e, t, n) {
                var r, i, o, a, s, u, l, c, f = "width" in t || "height" in t, d = this, p = {}, h = e.style,
                    g = e.nodeType && $e(e), m = Oe.get(e, "fxshow");
                n.queue || (a = ye._queueHooks(e, "fx"), null == a.unqueued && (a.unqueued = 0, s = a.empty.fire, a.empty.fire = function () {
                    a.unqueued || s()
                }), a.unqueued++, d.always(function () {
                    d.always(function () {
                        a.unqueued--, ye.queue(e, "fx").length || a.empty.fire()
                    })
                }));
                for (r in t) if (i = t[r], gt.test(i)) {
                    if (delete t[r], o = o || "toggle" === i, i === (g ? "hide" : "show")) {
                        if ("show" !== i || !m || void 0 === m[r]) continue;
                        g = !0
                    }
                    p[r] = m && m[r] || ye.style(e, r)
                }
                if ((u = !ye.isEmptyObject(t)) || !ye.isEmptyObject(p)) {
                    f && 1 === e.nodeType && (n.overflow = [h.overflow, h.overflowX, h.overflowY], l = m && m.display, null == l && (l = Oe.get(e, "display")), c = ye.css(e, "display"), "none" === c && (l ? c = l : (w([e], !0), l = e.style.display || l, c = ye.css(e, "display"), w([e]))), ("inline" === c || "inline-block" === c && null != l) && "none" === ye.css(e, "float") && (u || (d.done(function () {
                        h.display = l
                    }), null == l && (c = h.display, l = "none" === c ? "" : c)), h.display = "inline-block")), n.overflow && (h.overflow = "hidden", d.always(function () {
                        h.overflow = n.overflow[0], h.overflowX = n.overflow[1], h.overflowY = n.overflow[2]
                    })), u = !1;
                    for (r in p) u || (m ? "hidden" in m && (g = m.hidden) : m = Oe.access(e, "fxshow", {display: l}), o && (m.hidden = !g), g && w([e], !0), d.done(function () {
                        g || w([e]), Oe.remove(e, "fxshow");
                        for (r in p) ye.style(e, r, p[r])
                    })), u = K(g ? m[r] : 0, r, d), r in m || (m[r] = u.start, g && (u.end = u.start, u.start = 0))
                }
            }

            function G(e, t) {
                var n, r, i, o, a;
                for (n in e) if (r = ye.camelCase(n), i = t[r], o = e[n], Array.isArray(o) && (i = o[1], o = e[n] = o[0]), n !== r && (e[r] = o, delete e[n]), (a = ye.cssHooks[r]) && "expand" in a) {
                    o = a.expand(o), delete e[r];
                    for (n in o) n in e || (e[n] = o[n], t[n] = i)
                } else t[r] = i
            }

            function Y(e, t, n) {
                var r, i, o = 0, a = Y.prefilters.length, s = ye.Deferred().always(function () {
                    delete u.elem
                }), u = function () {
                    if (i) return !1;
                    for (var t = pt || z(), n = Math.max(0, l.startTime + l.duration - t), r = n / l.duration || 0, o = 1 - r, a = 0, u = l.tweens.length; a < u; a++) l.tweens[a].run(o);
                    return s.notifyWith(e, [l, o, n]), o < 1 && u ? n : (u || s.notifyWith(e, [l, 1, 0]), s.resolveWith(e, [l]), !1)
                }, l = s.promise({
                    elem: e,
                    props: ye.extend({}, t),
                    opts: ye.extend(!0, {specialEasing: {}, easing: ye.easing._default}, n),
                    originalProperties: t,
                    originalOptions: n,
                    startTime: pt || z(),
                    duration: n.duration,
                    tweens: [],
                    createTween: function (t, n) {
                        var r = ye.Tween(e, l.opts, t, n, l.opts.specialEasing[t] || l.opts.easing);
                        return l.tweens.push(r), r
                    },
                    stop: function (t) {
                        var n = 0, r = t ? l.tweens.length : 0;
                        if (i) return this;
                        for (i = !0; n < r; n++) l.tweens[n].run(1);
                        return t ? (s.notifyWith(e, [l, 1, 0]), s.resolveWith(e, [l, t])) : s.rejectWith(e, [l, t]), this
                    }
                }), c = l.props;
                for (G(c, l.opts.specialEasing); o < a; o++) if (r = Y.prefilters[o].call(l, e, c, l.opts)) return ye.isFunction(r.stop) && (ye._queueHooks(l.elem, l.opts.queue).stop = ye.proxy(r.stop, r)), r;
                return ye.map(c, K, l), ye.isFunction(l.opts.start) && l.opts.start.call(e, l), l.progress(l.opts.progress).done(l.opts.done, l.opts.complete).fail(l.opts.fail).always(l.opts.always), ye.fx.timer(ye.extend(u, {
                    elem: e,
                    anim: l,
                    queue: l.opts.queue
                })), l
            }

            function Q(e) {
                return (e.match(Ae) || []).join(" ")
            }

            function J(e) {
                return e.getAttribute && e.getAttribute("class") || ""
            }

            function Z(e, t, n, r) {
                var i;
                if (Array.isArray(t)) ye.each(t, function (t, i) {
                    n || Et.test(e) ? r(e, i) : Z(e + "[" + ("object" == typeof i && null != i ? t : "") + "]", i, n, r)
                }); else if (n || "object" !== ye.type(t)) r(e, t); else for (i in t) Z(e + "[" + i + "]", t[i], n, r)
            }

            function ee(e) {
                return function (t, n) {
                    "string" != typeof t && (n = t, t = "*");
                    var r, i = 0, o = t.toLowerCase().match(Ae) || [];
                    if (ye.isFunction(n)) for (; r = o[i++];) "+" === r[0] ? (r = r.slice(1) || "*", (e[r] = e[r] || []).unshift(n)) : (e[r] = e[r] || []).push(n)
                }
            }

            function te(e, t, n, r) {
                function i(s) {
                    var u;
                    return o[s] = !0, ye.each(e[s] || [], function (e, s) {
                        var l = s(t, n, r);
                        return "string" != typeof l || a || o[l] ? a ? !(u = l) : void 0 : (t.dataTypes.unshift(l), i(l), !1)
                    }), u
                }

                var o = {}, a = e === qt;
                return i(t.dataTypes[0]) || !o["*"] && i("*")
            }

            function ne(e, t) {
                var n, r, i = ye.ajaxSettings.flatOptions || {};
                for (n in t) void 0 !== t[n] && ((i[n] ? e : r || (r = {}))[n] = t[n]);
                return r && ye.extend(!0, e, r), e
            }

            function re(e, t, n) {
                for (var r, i, o, a, s = e.contents, u = e.dataTypes; "*" === u[0];) u.shift(), void 0 === r && (r = e.mimeType || t.getResponseHeader("Content-Type"));
                if (r) for (i in s) if (s[i] && s[i].test(r)) {
                    u.unshift(i);
                    break
                }
                if (u[0] in n) o = u[0]; else {
                    for (i in n) {
                        if (!u[0] || e.converters[i + " " + u[0]]) {
                            o = i;
                            break
                        }
                        a || (a = i)
                    }
                    o = o || a
                }
                if (o) return o !== u[0] && u.unshift(o), n[o]
            }

            function ie(e, t, n, r) {
                var i, o, a, s, u, l = {}, c = e.dataTypes.slice();
                if (c[1]) for (a in e.converters) l[a.toLowerCase()] = e.converters[a];
                for (o = c.shift(); o;) if (e.responseFields[o] && (n[e.responseFields[o]] = t), !u && r && e.dataFilter && (t = e.dataFilter(t, e.dataType)), u = o, o = c.shift()) if ("*" === o) o = u; else if ("*" !== u && u !== o) {
                    if (!(a = l[u + " " + o] || l["* " + o])) for (i in l) if (s = i.split(" "), s[1] === o && (a = l[u + " " + s[0]] || l["* " + s[0]])) {
                        !0 === a ? a = l[i] : !0 !== l[i] && (o = s[0], c.unshift(s[1]));
                        break
                    }
                    if (!0 !== a) if (a && e.throws) t = a(t); else try {
                        t = a(t)
                    } catch (e) {
                        return {state: "parsererror", error: a ? e : "No conversion from " + u + " to " + o}
                    }
                }
                return {state: "success", data: t}
            }

            var oe = [], ae = n.document, se = Object.getPrototypeOf, ue = oe.slice, le = oe.concat, ce = oe.push,
                fe = oe.indexOf, de = {}, pe = de.toString, he = de.hasOwnProperty, ge = he.toString,
                me = ge.call(Object), ve = {}, ye = function (e, t) {
                    return new ye.fn.init(e, t)
                }, xe = function (e, t) {
                    return t.toUpperCase()
                };
            ye.fn = ye.prototype = {
                jquery: "3.2.1", constructor: ye, length: 0, toArray: function () {
                    return ue.call(this)
                }, get: function (e) {
                    return null == e ? ue.call(this) : e < 0 ? this[e + this.length] : this[e]
                }, pushStack: function (e) {
                    var t = ye.merge(this.constructor(), e);
                    return t.prevObject = this, t
                }, each: function (e) {
                    return ye.each(this, e)
                }, map: function (e) {
                    return this.pushStack(ye.map(this, function (t, n) {
                        return e.call(t, n, t)
                    }))
                }, slice: function () {
                    return this.pushStack(ue.apply(this, arguments))
                }, first: function () {
                    return this.eq(0)
                }, last: function () {
                    return this.eq(-1)
                }, eq: function (e) {
                    var t = this.length, n = +e + (e < 0 ? t : 0);
                    return this.pushStack(n >= 0 && n < t ? [this[n]] : [])
                }, end: function () {
                    return this.prevObject || this.constructor()
                }, push: ce, sort: oe.sort, splice: oe.splice
            }, ye.extend = ye.fn.extend = function () {
                var e, t, n, r, i, o, a = arguments[0] || {}, s = 1, u = arguments.length, l = !1;
                for ("boolean" == typeof a && (l = a, a = arguments[s] || {}, s++), "object" == typeof a || ye.isFunction(a) || (a = {}), s === u && (a = this, s--); s < u; s++) if (null != (e = arguments[s])) for (t in e) n = a[t], r = e[t], a !== r && (l && r && (ye.isPlainObject(r) || (i = Array.isArray(r))) ? (i ? (i = !1, o = n && Array.isArray(n) ? n : []) : o = n && ye.isPlainObject(n) ? n : {}, a[t] = ye.extend(l, o, r)) : void 0 !== r && (a[t] = r));
                return a
            }, ye.extend({
                expando: "jQuery" + ("3.2.1" + Math.random()).replace(/\D/g, ""),
                isReady: !0,
                error: function (e) {
                    throw new Error(e)
                },
                noop: function () {
                },
                isFunction: function (e) {
                    return "function" === ye.type(e)
                },
                isWindow: function (e) {
                    return null != e && e === e.window
                },
                isNumeric: function (e) {
                    var t = ye.type(e);
                    return ("number" === t || "string" === t) && !isNaN(e - parseFloat(e))
                },
                isPlainObject: function (e) {
                    var t, n;
                    return !(!e || "[object Object]" !== pe.call(e)) && (!(t = se(e)) || "function" == typeof(n = he.call(t, "constructor") && t.constructor) && ge.call(n) === me)
                },
                isEmptyObject: function (e) {
                    var t;
                    for (t in e) return !1;
                    return !0
                },
                type: function (e) {
                    return null == e ? e + "" : "object" == typeof e || "function" == typeof e ? de[pe.call(e)] || "object" : typeof e
                },
                globalEval: function (e) {
                    a(e)
                },
                camelCase: function (e) {
                    return e.replace(/^-ms-/, "ms-").replace(/-([a-z])/g, xe)
                },
                each: function (e, t) {
                    var n, r = 0;
                    if (s(e)) for (n = e.length; r < n && !1 !== t.call(e[r], r, e[r]); r++) ; else for (r in e) if (!1 === t.call(e[r], r, e[r])) break;
                    return e
                },
                trim: function (e) {
                    return null == e ? "" : (e + "").replace(/^[\s\uFEFF\xA0]+|[\s\uFEFF\xA0]+$/g, "")
                },
                makeArray: function (e, t) {
                    var n = t || [];
                    return null != e && (s(Object(e)) ? ye.merge(n, "string" == typeof e ? [e] : e) : ce.call(n, e)), n
                },
                inArray: function (e, t, n) {
                    return null == t ? -1 : fe.call(t, e, n)
                },
                merge: function (e, t) {
                    for (var n = +t.length, r = 0, i = e.length; r < n; r++) e[i++] = t[r];
                    return e.length = i, e
                },
                grep: function (e, t, n) {
                    for (var r = [], i = 0, o = e.length, a = !n; i < o; i++) !t(e[i], i) !== a && r.push(e[i]);
                    return r
                },
                map: function (e, t, n) {
                    var r, i, o = 0, a = [];
                    if (s(e)) for (r = e.length; o < r; o++) null != (i = t(e[o], o, n)) && a.push(i); else for (o in e) null != (i = t(e[o], o, n)) && a.push(i);
                    return le.apply([], a)
                },
                guid: 1,
                proxy: function (e, t) {
                    var n, r, i;
                    if ("string" == typeof t && (n = e[t], t = e, e = n), ye.isFunction(e)) return r = ue.call(arguments, 2), i = function () {
                        return e.apply(t || this, r.concat(ue.call(arguments)))
                    }, i.guid = e.guid = e.guid || ye.guid++, i
                },
                now: Date.now,
                support: ve
            }), "function" == typeof Symbol && (ye.fn[Symbol.iterator] = oe[Symbol.iterator]), ye.each("Boolean Number String Function Array Date RegExp Object Error Symbol".split(" "), function (e, t) {
                de["[object " + t + "]"] = t.toLowerCase()
            });
            var be = function (e) {
                function t(e, t, n, r) {
                    var i, o, a, s, u, c, d, p = t && t.ownerDocument, h = t ? t.nodeType : 9;
                    if (n = n || [], "string" != typeof e || !e || 1 !== h && 9 !== h && 11 !== h) return n;
                    if (!r && ((t ? t.ownerDocument || t : I) !== _ && A(t), t = t || _, L)) {
                        if (11 !== h && (u = ge.exec(e))) if (i = u[1]) {
                            if (9 === h) {
                                if (!(a = t.getElementById(i))) return n;
                                if (a.id === i) return n.push(a), n
                            } else if (p && (a = p.getElementById(i)) && P(t, a) && a.id === i) return n.push(a), n
                        } else {
                            if (u[2]) return Y.apply(n, t.getElementsByTagName(e)), n;
                            if ((i = u[3]) && b.getElementsByClassName && t.getElementsByClassName) return Y.apply(n, t.getElementsByClassName(i)), n
                        }
                        if (b.qsa && !U[e + " "] && (!H || !H.test(e))) {
                            if (1 !== h) p = t, d = e; else if ("object" !== t.nodeName.toLowerCase()) {
                                for ((s = t.getAttribute("id")) ? s = s.replace(xe, be) : t.setAttribute("id", s = R), c = k(e), o = c.length; o--;) c[o] = "#" + s + " " + f(c[o]);
                                d = c.join(","), p = me.test(e) && l(t.parentNode) || t
                            }
                            if (d) try {
                                return Y.apply(n, p.querySelectorAll(d)), n
                            } catch (e) {
                            } finally {
                                s === R && t.removeAttribute("id")
                            }
                        }
                    }
                    return D(e.replace(oe, "$1"), t, n, r)
                }

                function n() {
                    function e(n, r) {
                        return t.push(n + " ") > w.cacheLength && delete e[t.shift()], e[n + " "] = r
                    }

                    var t = [];
                    return e
                }

                function r(e) {
                    return e[R] = !0, e
                }

                function i(e) {
                    var t = _.createElement("fieldset");
                    try {
                        return !!e(t)
                    } catch (e) {
                        return !1
                    } finally {
                        t.parentNode && t.parentNode.removeChild(t), t = null
                    }
                }

                function o(e, t) {
                    for (var n = e.split("|"), r = n.length; r--;) w.attrHandle[n[r]] = t
                }

                function a(e, t) {
                    var n = t && e, r = n && 1 === e.nodeType && 1 === t.nodeType && e.sourceIndex - t.sourceIndex;
                    if (r) return r;
                    if (n) for (; n = n.nextSibling;) if (n === t) return -1;
                    return e ? 1 : -1
                }

                function s(e) {
                    return function (t) {
                        return "form" in t ? t.parentNode && !1 === t.disabled ? "label" in t ? "label" in t.parentNode ? t.parentNode.disabled === e : t.disabled === e : t.isDisabled === e || t.isDisabled !== !e && Te(t) === e : t.disabled === e : "label" in t && t.disabled === e
                    }
                }

                function u(e) {
                    return r(function (t) {
                        return t = +t, r(function (n, r) {
                            for (var i, o = e([], n.length, t), a = o.length; a--;) n[i = o[a]] && (n[i] = !(r[i] = n[i]))
                        })
                    })
                }

                function l(e) {
                    return e && void 0 !== e.getElementsByTagName && e
                }

                function c() {
                }

                function f(e) {
                    for (var t = 0, n = e.length, r = ""; t < n; t++) r += e[t].value;
                    return r
                }

                function d(e, t, n) {
                    var r = t.dir, i = t.next, o = i || r, a = n && "parentNode" === o, s = W++;
                    return t.first ? function (t, n, i) {
                        for (; t = t[r];) if (1 === t.nodeType || a) return e(t, n, i);
                        return !1
                    } : function (t, n, u) {
                        var l, c, f, d = [M, s];
                        if (u) {
                            for (; t = t[r];) if ((1 === t.nodeType || a) && e(t, n, u)) return !0
                        } else for (; t = t[r];) if (1 === t.nodeType || a) if (f = t[R] || (t[R] = {}), c = f[t.uniqueID] || (f[t.uniqueID] = {}), i && i === t.nodeName.toLowerCase()) t = t[r] || t; else {
                            if ((l = c[o]) && l[0] === M && l[1] === s) return d[2] = l[2];
                            if (c[o] = d, d[2] = e(t, n, u)) return !0
                        }
                        return !1
                    }
                }

                function p(e) {
                    return e.length > 1 ? function (t, n, r) {
                        for (var i = e.length; i--;) if (!e[i](t, n, r)) return !1;
                        return !0
                    } : e[0]
                }

                function h(e, n, r) {
                    for (var i = 0, o = n.length; i < o; i++) t(e, n[i], r);
                    return r
                }

                function g(e, t, n, r, i) {
                    for (var o, a = [], s = 0, u = e.length, l = null != t; s < u; s++) (o = e[s]) && (n && !n(o, r, i) || (a.push(o), l && t.push(s)));
                    return a
                }

                function m(e, t, n, i, o, a) {
                    return i && !i[R] && (i = m(i)), o && !o[R] && (o = m(o, a)), r(function (r, a, s, u) {
                        var l, c, f, d = [], p = [], m = a.length, v = r || h(t || "*", s.nodeType ? [s] : s, []),
                            y = !e || !r && t ? v : g(v, d, e, s, u), x = n ? o || (r ? e : m || i) ? [] : a : y;
                        if (n && n(y, x, s, u), i) for (l = g(x, p), i(l, [], s, u), c = l.length; c--;) (f = l[c]) && (x[p[c]] = !(y[p[c]] = f));
                        if (r) {
                            if (o || e) {
                                if (o) {
                                    for (l = [], c = x.length; c--;) (f = x[c]) && l.push(y[c] = f);
                                    o(null, x = [], l, u)
                                }
                                for (c = x.length; c--;) (f = x[c]) && (l = o ? J(r, f) : d[c]) > -1 && (r[l] = !(a[l] = f))
                            }
                        } else x = g(x === a ? x.splice(m, x.length) : x), o ? o(null, a, x, u) : Y.apply(a, x)
                    })
                }

                function v(e) {
                    for (var t, n, r, i = e.length, o = w.relative[e[0].type], a = o || w.relative[" "], s = o ? 1 : 0, u = d(function (e) {
                        return e === t
                    }, a, !0), l = d(function (e) {
                        return J(t, e) > -1
                    }, a, !0), c = [function (e, n, r) {
                        var i = !o && (r || n !== S) || ((t = n).nodeType ? u(e, n, r) : l(e, n, r));
                        return t = null, i
                    }]; s < i; s++) if (n = w.relative[e[s].type]) c = [d(p(c), n)]; else {
                        if (n = w.filter[e[s].type].apply(null, e[s].matches), n[R]) {
                            for (r = ++s; r < i && !w.relative[e[r].type]; r++) ;
                            return m(s > 1 && p(c), s > 1 && f(e.slice(0, s - 1).concat({value: " " === e[s - 2].type ? "*" : ""})).replace(oe, "$1"), n, s < r && v(e.slice(s, r)), r < i && v(e = e.slice(r)), r < i && f(e))
                        }
                        c.push(n)
                    }
                    return p(c)
                }

                function y(e, n) {
                    var i = n.length > 0, o = e.length > 0, a = function (r, a, s, u, l) {
                        var c, f, d, p = 0, h = "0", m = r && [], v = [], y = S, x = r || o && w.find.TAG("*", l),
                            b = M += null == y ? 1 : Math.random() || .1, T = x.length;
                        for (l && (S = a === _ || a || l); h !== T && null != (c = x[h]); h++) {
                            if (o && c) {
                                for (f = 0, a || c.ownerDocument === _ || (A(c), s = !L); d = e[f++];) if (d(c, a || _, s)) {
                                    u.push(c);
                                    break
                                }
                                l && (M = b)
                            }
                            i && ((c = !d && c) && p--, r && m.push(c))
                        }
                        if (p += h, i && h !== p) {
                            for (f = 0; d = n[f++];) d(m, v, a, s);
                            if (r) {
                                if (p > 0) for (; h--;) m[h] || v[h] || (v[h] = V.call(u));
                                v = g(v)
                            }
                            Y.apply(u, v), l && !r && v.length > 0 && p + n.length > 1 && t.uniqueSort(u)
                        }
                        return l && (M = b, S = y), m
                    };
                    return i ? r(a) : a
                }

                var x, b, w, T, C, k, E, D, S, j, N, A, _, q, L, H, O, F, P, R = "sizzle" + 1 * new Date,
                    I = e.document, M = 0, W = 0, $ = n(), B = n(), U = n(), z = function (e, t) {
                        return e === t && (N = !0), 0
                    }, X = {}.hasOwnProperty, K = [], V = K.pop, G = K.push, Y = K.push, Q = K.slice, J = function (e, t) {
                        for (var n = 0, r = e.length; n < r; n++) if (e[n] === t) return n;
                        return -1
                    },
                    Z = "checked|selected|async|autofocus|autoplay|controls|defer|disabled|hidden|ismap|loop|multiple|open|readonly|required|scoped",
                    ee = "[\\x20\\t\\r\\n\\f]", te = "(?:\\\\.|[\\w-]|[^\0-\\xa0])+",
                    ne = "\\[" + ee + "*(" + te + ")(?:" + ee + "*([*^$|!~]?=)" + ee + "*(?:'((?:\\\\.|[^\\\\'])*)'|\"((?:\\\\.|[^\\\\\"])*)\"|(" + te + "))|)" + ee + "*\\]",
                    re = ":(" + te + ")(?:\\((('((?:\\\\.|[^\\\\'])*)'|\"((?:\\\\.|[^\\\\\"])*)\")|((?:\\\\.|[^\\\\()[\\]]|" + ne + ")*)|.*)\\)|)",
                    ie = new RegExp(ee + "+", "g"),
                    oe = new RegExp("^" + ee + "+|((?:^|[^\\\\])(?:\\\\.)*)" + ee + "+$", "g"),
                    ae = new RegExp("^" + ee + "*," + ee + "*"),
                    se = new RegExp("^" + ee + "*([>+~]|" + ee + ")" + ee + "*"),
                    ue = new RegExp("=" + ee + "*([^\\]'\"]*?)" + ee + "*\\]", "g"), le = new RegExp(re),
                    ce = new RegExp("^" + te + "$"), fe = {
                        ID: new RegExp("^#(" + te + ")"),
                        CLASS: new RegExp("^\\.(" + te + ")"),
                        TAG: new RegExp("^(" + te + "|[*])"),
                        ATTR: new RegExp("^" + ne),
                        PSEUDO: new RegExp("^" + re),
                        CHILD: new RegExp("^:(only|first|last|nth|nth-last)-(child|of-type)(?:\\(" + ee + "*(even|odd|(([+-]|)(\\d*)n|)" + ee + "*(?:([+-]|)" + ee + "*(\\d+)|))" + ee + "*\\)|)", "i"),
                        bool: new RegExp("^(?:" + Z + ")$", "i"),
                        needsContext: new RegExp("^" + ee + "*[>+~]|:(even|odd|eq|gt|lt|nth|first|last)(?:\\(" + ee + "*((?:-\\d)?\\d*)" + ee + "*\\)|)(?=[^-]|$)", "i")
                    }, de = /^(?:input|select|textarea|button)$/i, pe = /^h\d$/i, he = /^[^{]+\{\s*\[native \w/,
                    ge = /^(?:#([\w-]+)|(\w+)|\.([\w-]+))$/, me = /[+~]/,
                    ve = new RegExp("\\\\([\\da-f]{1,6}" + ee + "?|(" + ee + ")|.)", "ig"), ye = function (e, t, n) {
                        var r = "0x" + t - 65536;
                        return r !== r || n ? t : r < 0 ? String.fromCharCode(r + 65536) : String.fromCharCode(r >> 10 | 55296, 1023 & r | 56320)
                    }, xe = /([\0-\x1f\x7f]|^-?\d)|^-$|[^\0-\x1f\x7f-\uFFFF\w-]/g, be = function (e, t) {
                        return t ? "\0" === e ? "�" : e.slice(0, -1) + "\\" + e.charCodeAt(e.length - 1).toString(16) + " " : "\\" + e
                    }, we = function () {
                        A()
                    }, Te = d(function (e) {
                        return !0 === e.disabled && ("form" in e || "label" in e)
                    }, {dir: "parentNode", next: "legend"});
                try {
                    Y.apply(K = Q.call(I.childNodes), I.childNodes), K[I.childNodes.length].nodeType
                } catch (e) {
                    Y = {
                        apply: K.length ? function (e, t) {
                            G.apply(e, Q.call(t))
                        } : function (e, t) {
                            for (var n = e.length, r = 0; e[n++] = t[r++];) ;
                            e.length = n - 1
                        }
                    }
                }
                b = t.support = {}, C = t.isXML = function (e) {
                    var t = e && (e.ownerDocument || e).documentElement;
                    return !!t && "HTML" !== t.nodeName
                }, A = t.setDocument = function (e) {
                    var t, n, r = e ? e.ownerDocument || e : I;
                    return r !== _ && 9 === r.nodeType && r.documentElement ? (_ = r, q = _.documentElement, L = !C(_), I !== _ && (n = _.defaultView) && n.top !== n && (n.addEventListener ? n.addEventListener("unload", we, !1) : n.attachEvent && n.attachEvent("onunload", we)), b.attributes = i(function (e) {
                        return e.className = "i", !e.getAttribute("className")
                    }), b.getElementsByTagName = i(function (e) {
                        return e.appendChild(_.createComment("")), !e.getElementsByTagName("*").length
                    }), b.getElementsByClassName = he.test(_.getElementsByClassName), b.getById = i(function (e) {
                        return q.appendChild(e).id = R, !_.getElementsByName || !_.getElementsByName(R).length
                    }), b.getById ? (w.filter.ID = function (e) {
                        var t = e.replace(ve, ye);
                        return function (e) {
                            return e.getAttribute("id") === t
                        }
                    }, w.find.ID = function (e, t) {
                        if (void 0 !== t.getElementById && L) {
                            var n = t.getElementById(e);
                            return n ? [n] : []
                        }
                    }) : (w.filter.ID = function (e) {
                        var t = e.replace(ve, ye);
                        return function (e) {
                            var n = void 0 !== e.getAttributeNode && e.getAttributeNode("id");
                            return n && n.value === t
                        }
                    }, w.find.ID = function (e, t) {
                        if (void 0 !== t.getElementById && L) {
                            var n, r, i, o = t.getElementById(e);
                            if (o) {
                                if ((n = o.getAttributeNode("id")) && n.value === e) return [o];
                                for (i = t.getElementsByName(e), r = 0; o = i[r++];) if ((n = o.getAttributeNode("id")) && n.value === e) return [o]
                            }
                            return []
                        }
                    }), w.find.TAG = b.getElementsByTagName ? function (e, t) {
                        return void 0 !== t.getElementsByTagName ? t.getElementsByTagName(e) : b.qsa ? t.querySelectorAll(e) : void 0
                    } : function (e, t) {
                        var n, r = [], i = 0, o = t.getElementsByTagName(e);
                        if ("*" === e) {
                            for (; n = o[i++];) 1 === n.nodeType && r.push(n);
                            return r
                        }
                        return o
                    }, w.find.CLASS = b.getElementsByClassName && function (e, t) {
                        if (void 0 !== t.getElementsByClassName && L) return t.getElementsByClassName(e)
                    }, O = [], H = [], (b.qsa = he.test(_.querySelectorAll)) && (i(function (e) {
                        q.appendChild(e).innerHTML = "<a id='" + R + "'></a><select id='" + R + "-\r\\' msallowcapture=''><option selected=''></option></select>", e.querySelectorAll("[msallowcapture^='']").length && H.push("[*^$]=" + ee + "*(?:''|\"\")"), e.querySelectorAll("[selected]").length || H.push("\\[" + ee + "*(?:value|" + Z + ")"), e.querySelectorAll("[id~=" + R + "-]").length || H.push("~="), e.querySelectorAll(":checked").length || H.push(":checked"), e.querySelectorAll("a#" + R + "+*").length || H.push(".#.+[+~]")
                    }), i(function (e) {
                        e.innerHTML = "<a href='' disabled='disabled'></a><select disabled='disabled'><option/></select>";
                        var t = _.createElement("input");
                        t.setAttribute("type", "hidden"), e.appendChild(t).setAttribute("name", "D"), e.querySelectorAll("[name=d]").length && H.push("name" + ee + "*[*^$|!~]?="), 2 !== e.querySelectorAll(":enabled").length && H.push(":enabled", ":disabled"), q.appendChild(e).disabled = !0, 2 !== e.querySelectorAll(":disabled").length && H.push(":enabled", ":disabled"), e.querySelectorAll("*,:x"), H.push(",.*:")
                    })), (b.matchesSelector = he.test(F = q.matches || q.webkitMatchesSelector || q.mozMatchesSelector || q.oMatchesSelector || q.msMatchesSelector)) && i(function (e) {
                        b.disconnectedMatch = F.call(e, "*"), F.call(e, "[s!='']:x"), O.push("!=", re)
                    }), H = H.length && new RegExp(H.join("|")), O = O.length && new RegExp(O.join("|")), t = he.test(q.compareDocumentPosition), P = t || he.test(q.contains) ? function (e, t) {
                        var n = 9 === e.nodeType ? e.documentElement : e, r = t && t.parentNode;
                        return e === r || !(!r || 1 !== r.nodeType || !(n.contains ? n.contains(r) : e.compareDocumentPosition && 16 & e.compareDocumentPosition(r)))
                    } : function (e, t) {
                        if (t) for (; t = t.parentNode;) if (t === e) return !0;
                        return !1
                    }, z = t ? function (e, t) {
                        if (e === t) return N = !0, 0;
                        var n = !e.compareDocumentPosition - !t.compareDocumentPosition;
                        return n || (n = (e.ownerDocument || e) === (t.ownerDocument || t) ? e.compareDocumentPosition(t) : 1, 1 & n || !b.sortDetached && t.compareDocumentPosition(e) === n ? e === _ || e.ownerDocument === I && P(I, e) ? -1 : t === _ || t.ownerDocument === I && P(I, t) ? 1 : j ? J(j, e) - J(j, t) : 0 : 4 & n ? -1 : 1)
                    } : function (e, t) {
                        if (e === t) return N = !0, 0;
                        var n, r = 0, i = e.parentNode, o = t.parentNode, s = [e], u = [t];
                        if (!i || !o) return e === _ ? -1 : t === _ ? 1 : i ? -1 : o ? 1 : j ? J(j, e) - J(j, t) : 0;
                        if (i === o) return a(e, t);
                        for (n = e; n = n.parentNode;) s.unshift(n);
                        for (n = t; n = n.parentNode;) u.unshift(n);
                        for (; s[r] === u[r];) r++;
                        return r ? a(s[r], u[r]) : s[r] === I ? -1 : u[r] === I ? 1 : 0
                    }, _) : _
                }, t.matches = function (e, n) {
                    return t(e, null, null, n)
                }, t.matchesSelector = function (e, n) {
                    if ((e.ownerDocument || e) !== _ && A(e), n = n.replace(ue, "='$1']"), b.matchesSelector && L && !U[n + " "] && (!O || !O.test(n)) && (!H || !H.test(n))) try {
                        var r = F.call(e, n);
                        if (r || b.disconnectedMatch || e.document && 11 !== e.document.nodeType) return r
                    } catch (e) {
                    }
                    return t(n, _, null, [e]).length > 0
                }, t.contains = function (e, t) {
                    return (e.ownerDocument || e) !== _ && A(e), P(e, t)
                }, t.attr = function (e, t) {
                    (e.ownerDocument || e) !== _ && A(e);
                    var n = w.attrHandle[t.toLowerCase()],
                        r = n && X.call(w.attrHandle, t.toLowerCase()) ? n(e, t, !L) : void 0;
                    return void 0 !== r ? r : b.attributes || !L ? e.getAttribute(t) : (r = e.getAttributeNode(t)) && r.specified ? r.value : null
                }, t.escape = function (e) {
                    return (e + "").replace(xe, be)
                }, t.error = function (e) {
                    throw new Error("Syntax error, unrecognized expression: " + e)
                }, t.uniqueSort = function (e) {
                    var t, n = [], r = 0, i = 0;
                    if (N = !b.detectDuplicates, j = !b.sortStable && e.slice(0), e.sort(z), N) {
                        for (; t = e[i++];) t === e[i] && (r = n.push(i));
                        for (; r--;) e.splice(n[r], 1)
                    }
                    return j = null, e
                }, T = t.getText = function (e) {
                    var t, n = "", r = 0, i = e.nodeType;
                    if (i) {
                        if (1 === i || 9 === i || 11 === i) {
                            if ("string" == typeof e.textContent) return e.textContent;
                            for (e = e.firstChild; e; e = e.nextSibling) n += T(e)
                        } else if (3 === i || 4 === i) return e.nodeValue
                    } else for (; t = e[r++];) n += T(t);
                    return n
                }, w = t.selectors = {
                    cacheLength: 50,
                    createPseudo: r,
                    match: fe,
                    attrHandle: {},
                    find: {},
                    relative: {
                        ">": {dir: "parentNode", first: !0},
                        " ": {dir: "parentNode"},
                        "+": {dir: "previousSibling", first: !0},
                        "~": {dir: "previousSibling"}
                    },
                    preFilter: {
                        ATTR: function (e) {
                            return e[1] = e[1].replace(ve, ye), e[3] = (e[3] || e[4] || e[5] || "").replace(ve, ye), "~=" === e[2] && (e[3] = " " + e[3] + " "), e.slice(0, 4)
                        }, CHILD: function (e) {
                            return e[1] = e[1].toLowerCase(), "nth" === e[1].slice(0, 3) ? (e[3] || t.error(e[0]), e[4] = +(e[4] ? e[5] + (e[6] || 1) : 2 * ("even" === e[3] || "odd" === e[3])), e[5] = +(e[7] + e[8] || "odd" === e[3])) : e[3] && t.error(e[0]), e
                        }, PSEUDO: function (e) {
                            var t, n = !e[6] && e[2];
                            return fe.CHILD.test(e[0]) ? null : (e[3] ? e[2] = e[4] || e[5] || "" : n && le.test(n) && (t = k(n, !0)) && (t = n.indexOf(")", n.length - t) - n.length) && (e[0] = e[0].slice(0, t), e[2] = n.slice(0, t)), e.slice(0, 3))
                        }
                    },
                    filter: {
                        TAG: function (e) {
                            var t = e.replace(ve, ye).toLowerCase();
                            return "*" === e ? function () {
                                return !0
                            } : function (e) {
                                return e.nodeName && e.nodeName.toLowerCase() === t
                            }
                        }, CLASS: function (e) {
                            var t = $[e + " "];
                            return t || (t = new RegExp("(^|" + ee + ")" + e + "(" + ee + "|$)")) && $(e, function (e) {
                                return t.test("string" == typeof e.className && e.className || void 0 !== e.getAttribute && e.getAttribute("class") || "")
                            })
                        }, ATTR: function (e, n, r) {
                            return function (i) {
                                var o = t.attr(i, e);
                                return null == o ? "!=" === n : !n || (o += "", "=" === n ? o === r : "!=" === n ? o !== r : "^=" === n ? r && 0 === o.indexOf(r) : "*=" === n ? r && o.indexOf(r) > -1 : "$=" === n ? r && o.slice(-r.length) === r : "~=" === n ? (" " + o.replace(ie, " ") + " ").indexOf(r) > -1 : "|=" === n && (o === r || o.slice(0, r.length + 1) === r + "-"))
                            }
                        }, CHILD: function (e, t, n, r, i) {
                            var o = "nth" !== e.slice(0, 3), a = "last" !== e.slice(-4), s = "of-type" === t;
                            return 1 === r && 0 === i ? function (e) {
                                return !!e.parentNode
                            } : function (t, n, u) {
                                var l, c, f, d, p, h, g = o !== a ? "nextSibling" : "previousSibling", m = t.parentNode,
                                    v = s && t.nodeName.toLowerCase(), y = !u && !s, x = !1;
                                if (m) {
                                    if (o) {
                                        for (; g;) {
                                            for (d = t; d = d[g];) if (s ? d.nodeName.toLowerCase() === v : 1 === d.nodeType) return !1;
                                            h = g = "only" === e && !h && "nextSibling"
                                        }
                                        return !0
                                    }
                                    if (h = [a ? m.firstChild : m.lastChild], a && y) {
                                        for (d = m, f = d[R] || (d[R] = {}), c = f[d.uniqueID] || (f[d.uniqueID] = {}), l = c[e] || [], p = l[0] === M && l[1], x = p && l[2], d = p && m.childNodes[p]; d = ++p && d && d[g] || (x = p = 0) || h.pop();) if (1 === d.nodeType && ++x && d === t) {
                                            c[e] = [M, p, x];
                                            break
                                        }
                                    } else if (y && (d = t, f = d[R] || (d[R] = {}), c = f[d.uniqueID] || (f[d.uniqueID] = {}), l = c[e] || [], p = l[0] === M && l[1], x = p), !1 === x) for (; (d = ++p && d && d[g] || (x = p = 0) || h.pop()) && ((s ? d.nodeName.toLowerCase() !== v : 1 !== d.nodeType) || !++x || (y && (f = d[R] || (d[R] = {}), c = f[d.uniqueID] || (f[d.uniqueID] = {}), c[e] = [M, x]), d !== t));) ;
                                    return (x -= i) === r || x % r == 0 && x / r >= 0
                                }
                            }
                        }, PSEUDO: function (e, n) {
                            var i,
                                o = w.pseudos[e] || w.setFilters[e.toLowerCase()] || t.error("unsupported pseudo: " + e);
                            return o[R] ? o(n) : o.length > 1 ? (i = [e, e, "", n], w.setFilters.hasOwnProperty(e.toLowerCase()) ? r(function (e, t) {
                                for (var r, i = o(e, n), a = i.length; a--;) r = J(e, i[a]), e[r] = !(t[r] = i[a])
                            }) : function (e) {
                                return o(e, 0, i)
                            }) : o
                        }
                    },
                    pseudos: {
                        not: r(function (e) {
                            var t = [], n = [], i = E(e.replace(oe, "$1"));
                            return i[R] ? r(function (e, t, n, r) {
                                for (var o, a = i(e, null, r, []), s = e.length; s--;) (o = a[s]) && (e[s] = !(t[s] = o))
                            }) : function (e, r, o) {
                                return t[0] = e, i(t, null, o, n), t[0] = null, !n.pop()
                            }
                        }), has: r(function (e) {
                            return function (n) {
                                return t(e, n).length > 0
                            }
                        }), contains: r(function (e) {
                            return e = e.replace(ve, ye), function (t) {
                                return (t.textContent || t.innerText || T(t)).indexOf(e) > -1
                            }
                        }), lang: r(function (e) {
                            return ce.test(e || "") || t.error("unsupported lang: " + e), e = e.replace(ve, ye).toLowerCase(), function (t) {
                                var n;
                                do {
                                    if (n = L ? t.lang : t.getAttribute("xml:lang") || t.getAttribute("lang")) return (n = n.toLowerCase()) === e || 0 === n.indexOf(e + "-")
                                } while ((t = t.parentNode) && 1 === t.nodeType);
                                return !1
                            }
                        }), target: function (t) {
                            var n = e.location && e.location.hash;
                            return n && n.slice(1) === t.id
                        }, root: function (e) {
                            return e === q
                        }, focus: function (e) {
                            return e === _.activeElement && (!_.hasFocus || _.hasFocus()) && !!(e.type || e.href || ~e.tabIndex)
                        }, enabled: s(!1), disabled: s(!0), checked: function (e) {
                            var t = e.nodeName.toLowerCase();
                            return "input" === t && !!e.checked || "option" === t && !!e.selected
                        }, selected: function (e) {
                            return e.parentNode && e.parentNode.selectedIndex, !0 === e.selected
                        }, empty: function (e) {
                            for (e = e.firstChild; e; e = e.nextSibling) if (e.nodeType < 6) return !1;
                            return !0
                        }, parent: function (e) {
                            return !w.pseudos.empty(e)
                        }, header: function (e) {
                            return pe.test(e.nodeName)
                        }, input: function (e) {
                            return de.test(e.nodeName)
                        }, button: function (e) {
                            var t = e.nodeName.toLowerCase();
                            return "input" === t && "button" === e.type || "button" === t
                        }, text: function (e) {
                            var t;
                            return "input" === e.nodeName.toLowerCase() && "text" === e.type && (null == (t = e.getAttribute("type")) || "text" === t.toLowerCase())
                        }, first: u(function () {
                            return [0]
                        }), last: u(function (e, t) {
                            return [t - 1]
                        }), eq: u(function (e, t, n) {
                            return [n < 0 ? n + t : n]
                        }), even: u(function (e, t) {
                            for (var n = 0; n < t; n += 2) e.push(n);
                            return e
                        }), odd: u(function (e, t) {
                            for (var n = 1; n < t; n += 2) e.push(n);
                            return e
                        }), lt: u(function (e, t, n) {
                            for (var r = n < 0 ? n + t : n; --r >= 0;) e.push(r);
                            return e
                        }), gt: u(function (e, t, n) {
                            for (var r = n < 0 ? n + t : n; ++r < t;) e.push(r);
                            return e
                        })
                    }
                }, w.pseudos.nth = w.pseudos.eq;
                for (x in{radio: !0, checkbox: !0, file: !0, password: !0, image: !0}) w.pseudos[x] = function (e) {
                    return function (t) {
                        return "input" === t.nodeName.toLowerCase() && t.type === e
                    }
                }(x);
                for (x in{submit: !0, reset: !0}) w.pseudos[x] = function (e) {
                    return function (t) {
                        var n = t.nodeName.toLowerCase();
                        return ("input" === n || "button" === n) && t.type === e
                    }
                }(x);
                return c.prototype = w.filters = w.pseudos, w.setFilters = new c, k = t.tokenize = function (e, n) {
                    var r, i, o, a, s, u, l, c = B[e + " "];
                    if (c) return n ? 0 : c.slice(0);
                    for (s = e, u = [], l = w.preFilter; s;) {
                        r && !(i = ae.exec(s)) || (i && (s = s.slice(i[0].length) || s), u.push(o = [])), r = !1, (i = se.exec(s)) && (r = i.shift(), o.push({
                            value: r,
                            type: i[0].replace(oe, " ")
                        }), s = s.slice(r.length));
                        for (a in w.filter) !(i = fe[a].exec(s)) || l[a] && !(i = l[a](i)) || (r = i.shift(), o.push({
                            value: r,
                            type: a,
                            matches: i
                        }), s = s.slice(r.length));
                        if (!r) break
                    }
                    return n ? s.length : s ? t.error(e) : B(e, u).slice(0)
                }, E = t.compile = function (e, t) {
                    var n, r = [], i = [], o = U[e + " "];
                    if (!o) {
                        for (t || (t = k(e)), n = t.length; n--;) o = v(t[n]), o[R] ? r.push(o) : i.push(o);
                        o = U(e, y(i, r)), o.selector = e
                    }
                    return o
                }, D = t.select = function (e, t, n, r) {
                    var i, o, a, s, u, c = "function" == typeof e && e, d = !r && k(e = c.selector || e);
                    if (n = n || [], 1 === d.length) {
                        if (o = d[0] = d[0].slice(0), o.length > 2 && "ID" === (a = o[0]).type && 9 === t.nodeType && L && w.relative[o[1].type]) {
                            if (!(t = (w.find.ID(a.matches[0].replace(ve, ye), t) || [])[0])) return n;
                            c && (t = t.parentNode), e = e.slice(o.shift().value.length)
                        }
                        for (i = fe.needsContext.test(e) ? 0 : o.length; i-- && (a = o[i], !w.relative[s = a.type]);) if ((u = w.find[s]) && (r = u(a.matches[0].replace(ve, ye), me.test(o[0].type) && l(t.parentNode) || t))) {
                            if (o.splice(i, 1), !(e = r.length && f(o))) return Y.apply(n, r), n;
                            break
                        }
                    }
                    return (c || E(e, d))(r, t, !L, n, !t || me.test(e) && l(t.parentNode) || t), n
                }, b.sortStable = R.split("").sort(z).join("") === R, b.detectDuplicates = !!N, A(), b.sortDetached = i(function (e) {
                    return 1 & e.compareDocumentPosition(_.createElement("fieldset"))
                }), i(function (e) {
                    return e.innerHTML = "<a href='#'></a>", "#" === e.firstChild.getAttribute("href")
                }) || o("type|href|height|width", function (e, t, n) {
                    if (!n) return e.getAttribute(t, "type" === t.toLowerCase() ? 1 : 2)
                }), b.attributes && i(function (e) {
                    return e.innerHTML = "<input/>", e.firstChild.setAttribute("value", ""), "" === e.firstChild.getAttribute("value")
                }) || o("value", function (e, t, n) {
                    if (!n && "input" === e.nodeName.toLowerCase()) return e.defaultValue
                }), i(function (e) {
                    return null == e.getAttribute("disabled")
                }) || o(Z, function (e, t, n) {
                    var r;
                    if (!n) return !0 === e[t] ? t.toLowerCase() : (r = e.getAttributeNode(t)) && r.specified ? r.value : null
                }), t
            }(n);
            ye.find = be, ye.expr = be.selectors, ye.expr[":"] = ye.expr.pseudos, ye.uniqueSort = ye.unique = be.uniqueSort, ye.text = be.getText, ye.isXMLDoc = be.isXML, ye.contains = be.contains, ye.escapeSelector = be.escape;
            var we = function (e, t, n) {
                    for (var r = [], i = void 0 !== n; (e = e[t]) && 9 !== e.nodeType;) if (1 === e.nodeType) {
                        if (i && ye(e).is(n)) break;
                        r.push(e)
                    }
                    return r
                }, Te = function (e, t) {
                    for (var n = []; e; e = e.nextSibling) 1 === e.nodeType && e !== t && n.push(e);
                    return n
                }, Ce = ye.expr.match.needsContext, ke = /^<([a-z][^\/\0>:\x20\t\r\n\f]*)[\x20\t\r\n\f]*\/?>(?:<\/\1>|)$/i,
                Ee = /^.[^:#\[\.,]*$/;
            ye.filter = function (e, t, n) {
                var r = t[0];
                return n && (e = ":not(" + e + ")"), 1 === t.length && 1 === r.nodeType ? ye.find.matchesSelector(r, e) ? [r] : [] : ye.find.matches(e, ye.grep(t, function (e) {
                    return 1 === e.nodeType
                }))
            }, ye.fn.extend({
                find: function (e) {
                    var t, n, r = this.length, i = this;
                    if ("string" != typeof e) return this.pushStack(ye(e).filter(function () {
                        for (t = 0; t < r; t++) if (ye.contains(i[t], this)) return !0
                    }));
                    for (n = this.pushStack([]), t = 0; t < r; t++) ye.find(e, i[t], n);
                    return r > 1 ? ye.uniqueSort(n) : n
                }, filter: function (e) {
                    return this.pushStack(l(this, e || [], !1))
                }, not: function (e) {
                    return this.pushStack(l(this, e || [], !0))
                }, is: function (e) {
                    return !!l(this, "string" == typeof e && Ce.test(e) ? ye(e) : e || [], !1).length
                }
            });
            var De, Se = /^(?:\s*(<[\w\W]+>)[^>]*|#([\w-]+))$/;
            (ye.fn.init = function (e, t, n) {
                var r, i;
                if (!e) return this;
                if (n = n || De, "string" == typeof e) {
                    if (!(r = "<" === e[0] && ">" === e[e.length - 1] && e.length >= 3 ? [null, e, null] : Se.exec(e)) || !r[1] && t) return !t || t.jquery ? (t || n).find(e) : this.constructor(t).find(e);
                    if (r[1]) {
                        if (t = t instanceof ye ? t[0] : t, ye.merge(this, ye.parseHTML(r[1], t && t.nodeType ? t.ownerDocument || t : ae, !0)), ke.test(r[1]) && ye.isPlainObject(t)) for (r in t) ye.isFunction(this[r]) ? this[r](t[r]) : this.attr(r, t[r]);
                        return this
                    }
                    return i = ae.getElementById(r[2]), i && (this[0] = i, this.length = 1), this
                }
                return e.nodeType ? (this[0] = e, this.length = 1, this) : ye.isFunction(e) ? void 0 !== n.ready ? n.ready(e) : e(ye) : ye.makeArray(e, this)
            }).prototype = ye.fn, De = ye(ae);
            var je = /^(?:parents|prev(?:Until|All))/, Ne = {children: !0, contents: !0, next: !0, prev: !0};
            ye.fn.extend({
                has: function (e) {
                    var t = ye(e, this), n = t.length;
                    return this.filter(function () {
                        for (var e = 0; e < n; e++) if (ye.contains(this, t[e])) return !0
                    })
                }, closest: function (e, t) {
                    var n, r = 0, i = this.length, o = [], a = "string" != typeof e && ye(e);
                    if (!Ce.test(e)) for (; r < i; r++) for (n = this[r]; n && n !== t; n = n.parentNode) if (n.nodeType < 11 && (a ? a.index(n) > -1 : 1 === n.nodeType && ye.find.matchesSelector(n, e))) {
                        o.push(n);
                        break
                    }
                    return this.pushStack(o.length > 1 ? ye.uniqueSort(o) : o)
                }, index: function (e) {
                    return e ? "string" == typeof e ? fe.call(ye(e), this[0]) : fe.call(this, e.jquery ? e[0] : e) : this[0] && this[0].parentNode ? this.first().prevAll().length : -1
                }, add: function (e, t) {
                    return this.pushStack(ye.uniqueSort(ye.merge(this.get(), ye(e, t))))
                }, addBack: function (e) {
                    return this.add(null == e ? this.prevObject : this.prevObject.filter(e))
                }
            }), ye.each({
                parent: function (e) {
                    var t = e.parentNode;
                    return t && 11 !== t.nodeType ? t : null
                }, parents: function (e) {
                    return we(e, "parentNode")
                }, parentsUntil: function (e, t, n) {
                    return we(e, "parentNode", n)
                }, next: function (e) {
                    return c(e, "nextSibling")
                }, prev: function (e) {
                    return c(e, "previousSibling")
                }, nextAll: function (e) {
                    return we(e, "nextSibling")
                }, prevAll: function (e) {
                    return we(e, "previousSibling")
                }, nextUntil: function (e, t, n) {
                    return we(e, "nextSibling", n)
                }, prevUntil: function (e, t, n) {
                    return we(e, "previousSibling", n)
                }, siblings: function (e) {
                    return Te((e.parentNode || {}).firstChild, e)
                }, children: function (e) {
                    return Te(e.firstChild)
                }, contents: function (e) {
                    return u(e, "iframe") ? e.contentDocument : (u(e, "template") && (e = e.content || e), ye.merge([], e.childNodes))
                }
            }, function (e, t) {
                ye.fn[e] = function (n, r) {
                    var i = ye.map(this, t, n);
                    return "Until" !== e.slice(-5) && (r = n), r && "string" == typeof r && (i = ye.filter(r, i)), this.length > 1 && (Ne[e] || ye.uniqueSort(i), je.test(e) && i.reverse()), this.pushStack(i)
                }
            });
            var Ae = /[^\x20\t\r\n\f]+/g;
            ye.Callbacks = function (e) {
                e = "string" == typeof e ? f(e) : ye.extend({}, e);
                var t, n, r, i, o = [], a = [], s = -1, u = function () {
                    for (i = i || e.once, r = t = !0; a.length; s = -1) for (n = a.shift(); ++s < o.length;) !1 === o[s].apply(n[0], n[1]) && e.stopOnFalse && (s = o.length, n = !1);
                    e.memory || (n = !1), t = !1, i && (o = n ? [] : "")
                }, l = {
                    add: function () {
                        return o && (n && !t && (s = o.length - 1, a.push(n)), function t(n) {
                            ye.each(n, function (n, r) {
                                ye.isFunction(r) ? e.unique && l.has(r) || o.push(r) : r && r.length && "string" !== ye.type(r) && t(r)
                            })
                        }(arguments), n && !t && u()), this
                    }, remove: function () {
                        return ye.each(arguments, function (e, t) {
                            for (var n; (n = ye.inArray(t, o, n)) > -1;) o.splice(n, 1), n <= s && s--
                        }), this
                    }, has: function (e) {
                        return e ? ye.inArray(e, o) > -1 : o.length > 0
                    }, empty: function () {
                        return o && (o = []), this
                    }, disable: function () {
                        return i = a = [], o = n = "", this
                    }, disabled: function () {
                        return !o
                    }, lock: function () {
                        return i = a = [], n || t || (o = n = ""), this
                    }, locked: function () {
                        return !!i
                    }, fireWith: function (e, n) {
                        return i || (n = n || [], n = [e, n.slice ? n.slice() : n], a.push(n), t || u()), this
                    }, fire: function () {
                        return l.fireWith(this, arguments), this
                    }, fired: function () {
                        return !!r
                    }
                };
                return l
            }, ye.extend({
                Deferred: function (e) {
                    var t = [["notify", "progress", ye.Callbacks("memory"), ye.Callbacks("memory"), 2], ["resolve", "done", ye.Callbacks("once memory"), ye.Callbacks("once memory"), 0, "resolved"], ["reject", "fail", ye.Callbacks("once memory"), ye.Callbacks("once memory"), 1, "rejected"]],
                        r = "pending", i = {
                            state: function () {
                                return r
                            }, always: function () {
                                return o.done(arguments).fail(arguments), this
                            }, catch: function (e) {
                                return i.then(null, e)
                            }, pipe: function () {
                                var e = arguments;
                                return ye.Deferred(function (n) {
                                    ye.each(t, function (t, r) {
                                        var i = ye.isFunction(e[r[4]]) && e[r[4]];
                                        o[r[1]](function () {
                                            var e = i && i.apply(this, arguments);
                                            e && ye.isFunction(e.promise) ? e.promise().progress(n.notify).done(n.resolve).fail(n.reject) : n[r[0] + "With"](this, i ? [e] : arguments)
                                        })
                                    }), e = null
                                }).promise()
                            }, then: function (e, r, i) {
                                function o(e, t, r, i) {
                                    return function () {
                                        var s = this, u = arguments, l = function () {
                                            var n, l;
                                            if (!(e < a)) {
                                                if ((n = r.apply(s, u)) === t.promise()) throw new TypeError("Thenable self-resolution");
                                                l = n && ("object" == typeof n || "function" == typeof n) && n.then, ye.isFunction(l) ? i ? l.call(n, o(a, t, d, i), o(a, t, p, i)) : (a++, l.call(n, o(a, t, d, i), o(a, t, p, i), o(a, t, d, t.notifyWith))) : (r !== d && (s = void 0, u = [n]), (i || t.resolveWith)(s, u))
                                            }
                                        }, c = i ? l : function () {
                                            try {
                                                l()
                                            } catch (n) {
                                                ye.Deferred.exceptionHook && ye.Deferred.exceptionHook(n, c.stackTrace), e + 1 >= a && (r !== p && (s = void 0, u = [n]), t.rejectWith(s, u))
                                            }
                                        };
                                        e ? c() : (ye.Deferred.getStackHook && (c.stackTrace = ye.Deferred.getStackHook()), n.setTimeout(c))
                                    }
                                }

                                var a = 0;
                                return ye.Deferred(function (n) {
                                    t[0][3].add(o(0, n, ye.isFunction(i) ? i : d, n.notifyWith)), t[1][3].add(o(0, n, ye.isFunction(e) ? e : d)), t[2][3].add(o(0, n, ye.isFunction(r) ? r : p))
                                }).promise()
                            }, promise: function (e) {
                                return null != e ? ye.extend(e, i) : i
                            }
                        }, o = {};
                    return ye.each(t, function (e, n) {
                        var a = n[2], s = n[5];
                        i[n[1]] = a.add, s && a.add(function () {
                            r = s
                        }, t[3 - e][2].disable, t[0][2].lock), a.add(n[3].fire), o[n[0]] = function () {
                            return o[n[0] + "With"](this === o ? void 0 : this, arguments), this
                        }, o[n[0] + "With"] = a.fireWith
                    }), i.promise(o), e && e.call(o, o), o
                }, when: function (e) {
                    var t = arguments.length, n = t, r = Array(n), i = ue.call(arguments), o = ye.Deferred(),
                        a = function (e) {
                            return function (n) {
                                r[e] = this, i[e] = arguments.length > 1 ? ue.call(arguments) : n, --t || o.resolveWith(r, i)
                            }
                        };
                    if (t <= 1 && (h(e, o.done(a(n)).resolve, o.reject, !t), "pending" === o.state() || ye.isFunction(i[n] && i[n].then))) return o.then();
                    for (; n--;) h(i[n], a(n), o.reject);
                    return o.promise()
                }
            });
            var _e = /^(Eval|Internal|Range|Reference|Syntax|Type|URI)Error$/;
            ye.Deferred.exceptionHook = function (e, t) {
                n.console && n.console.warn && e && _e.test(e.name) && n.console.warn("jQuery.Deferred exception: " + e.message, e.stack, t)
            }, ye.readyException = function (e) {
                n.setTimeout(function () {
                    throw e
                })
            };
            var qe = ye.Deferred();
            ye.fn.ready = function (e) {
                return qe.then(e).catch(function (e) {
                    ye.readyException(e)
                }), this
            }, ye.extend({
                isReady: !1, readyWait: 1, ready: function (e) {
                    (!0 === e ? --ye.readyWait : ye.isReady) || (ye.isReady = !0, !0 !== e && --ye.readyWait > 0 || qe.resolveWith(ae, [ye]))
                }
            }), ye.ready.then = qe.then, "complete" === ae.readyState || "loading" !== ae.readyState && !ae.documentElement.doScroll ? n.setTimeout(ye.ready) : (ae.addEventListener("DOMContentLoaded", g), n.addEventListener("load", g));
            var Le = function (e, t, n, r, i, o, a) {
                var s = 0, u = e.length, l = null == n;
                if ("object" === ye.type(n)) {
                    i = !0;
                    for (s in n) Le(e, t, s, n[s], !0, o, a)
                } else if (void 0 !== r && (i = !0, ye.isFunction(r) || (a = !0), l && (a ? (t.call(e, r), t = null) : (l = t, t = function (e, t, n) {
                        return l.call(ye(e), n)
                    })), t)) for (; s < u; s++) t(e[s], n, a ? r : r.call(e[s], s, t(e[s], n)));
                return i ? e : l ? t.call(e) : u ? t(e[0], n) : o
            }, He = function (e) {
                return 1 === e.nodeType || 9 === e.nodeType || !+e.nodeType
            };
            m.uid = 1, m.prototype = {
                cache: function (e) {
                    var t = e[this.expando];
                    return t || (t = {}, He(e) && (e.nodeType ? e[this.expando] = t : Object.defineProperty(e, this.expando, {
                        value: t,
                        configurable: !0
                    }))), t
                }, set: function (e, t, n) {
                    var r, i = this.cache(e);
                    if ("string" == typeof t) i[ye.camelCase(t)] = n; else for (r in t) i[ye.camelCase(r)] = t[r];
                    return i
                }, get: function (e, t) {
                    return void 0 === t ? this.cache(e) : e[this.expando] && e[this.expando][ye.camelCase(t)]
                }, access: function (e, t, n) {
                    return void 0 === t || t && "string" == typeof t && void 0 === n ? this.get(e, t) : (this.set(e, t, n), void 0 !== n ? n : t)
                }, remove: function (e, t) {
                    var n, r = e[this.expando];
                    if (void 0 !== r) {
                        if (void 0 !== t) {
                            Array.isArray(t) ? t = t.map(ye.camelCase) : (t = ye.camelCase(t), t = t in r ? [t] : t.match(Ae) || []), n = t.length;
                            for (; n--;) delete r[t[n]]
                        }
                        (void 0 === t || ye.isEmptyObject(r)) && (e.nodeType ? e[this.expando] = void 0 : delete e[this.expando])
                    }
                }, hasData: function (e) {
                    var t = e[this.expando];
                    return void 0 !== t && !ye.isEmptyObject(t)
                }
            };
            var Oe = new m, Fe = new m, Pe = /^(?:\{[\w\W]*\}|\[[\w\W]*\])$/, Re = /[A-Z]/g;
            ye.extend({
                hasData: function (e) {
                    return Fe.hasData(e) || Oe.hasData(e)
                }, data: function (e, t, n) {
                    return Fe.access(e, t, n)
                }, removeData: function (e, t) {
                    Fe.remove(e, t)
                }, _data: function (e, t, n) {
                    return Oe.access(e, t, n)
                }, _removeData: function (e, t) {
                    Oe.remove(e, t)
                }
            }), ye.fn.extend({
                data: function (e, t) {
                    var n, r, i, o = this[0], a = o && o.attributes;
                    if (void 0 === e) {
                        if (this.length && (i = Fe.get(o), 1 === o.nodeType && !Oe.get(o, "hasDataAttrs"))) {
                            for (n = a.length; n--;) a[n] && (r = a[n].name, 0 === r.indexOf("data-") && (r = ye.camelCase(r.slice(5)), y(o, r, i[r])));
                            Oe.set(o, "hasDataAttrs", !0)
                        }
                        return i
                    }
                    return "object" == typeof e ? this.each(function () {
                        Fe.set(this, e)
                    }) : Le(this, function (t) {
                        var n;
                        if (o && void 0 === t) {
                            if (void 0 !== (n = Fe.get(o, e))) return n;
                            if (void 0 !== (n = y(o, e))) return n
                        } else this.each(function () {
                            Fe.set(this, e, t)
                        })
                    }, null, t, arguments.length > 1, null, !0)
                }, removeData: function (e) {
                    return this.each(function () {
                        Fe.remove(this, e)
                    })
                }
            }), ye.extend({
                queue: function (e, t, n) {
                    var r;
                    if (e) return t = (t || "fx") + "queue", r = Oe.get(e, t), n && (!r || Array.isArray(n) ? r = Oe.access(e, t, ye.makeArray(n)) : r.push(n)), r || []
                }, dequeue: function (e, t) {
                    t = t || "fx";
                    var n = ye.queue(e, t), r = n.length, i = n.shift(), o = ye._queueHooks(e, t), a = function () {
                        ye.dequeue(e, t)
                    };
                    "inprogress" === i && (i = n.shift(), r--), i && ("fx" === t && n.unshift("inprogress"), delete o.stop, i.call(e, a, o)), !r && o && o.empty.fire()
                }, _queueHooks: function (e, t) {
                    var n = t + "queueHooks";
                    return Oe.get(e, n) || Oe.access(e, n, {
                        empty: ye.Callbacks("once memory").add(function () {
                            Oe.remove(e, [t + "queue", n])
                        })
                    })
                }
            }), ye.fn.extend({
                queue: function (e, t) {
                    var n = 2;
                    return "string" != typeof e && (t = e, e = "fx", n--), arguments.length < n ? ye.queue(this[0], e) : void 0 === t ? this : this.each(function () {
                        var n = ye.queue(this, e, t);
                        ye._queueHooks(this, e), "fx" === e && "inprogress" !== n[0] && ye.dequeue(this, e)
                    })
                }, dequeue: function (e) {
                    return this.each(function () {
                        ye.dequeue(this, e)
                    })
                }, clearQueue: function (e) {
                    return this.queue(e || "fx", [])
                }, promise: function (e, t) {
                    var n, r = 1, i = ye.Deferred(), o = this, a = this.length, s = function () {
                        --r || i.resolveWith(o, [o])
                    };
                    for ("string" != typeof e && (t = e, e = void 0), e = e || "fx"; a--;) (n = Oe.get(o[a], e + "queueHooks")) && n.empty && (r++, n.empty.add(s));
                    return s(), i.promise(t)
                }
            });
            var Ie = /[+-]?(?:\d*\.|)\d+(?:[eE][+-]?\d+|)/.source,
                Me = new RegExp("^(?:([+-])=|)(" + Ie + ")([a-z%]*)$", "i"), We = ["Top", "Right", "Bottom", "Left"],
                $e = function (e, t) {
                    return e = t || e, "none" === e.style.display || "" === e.style.display && ye.contains(e.ownerDocument, e) && "none" === ye.css(e, "display")
                }, Be = function (e, t, n, r) {
                    var i, o, a = {};
                    for (o in t) a[o] = e.style[o], e.style[o] = t[o];
                    i = n.apply(e, r || []);
                    for (o in t) e.style[o] = a[o];
                    return i
                }, Ue = {};
            ye.fn.extend({
                show: function () {
                    return w(this, !0)
                }, hide: function () {
                    return w(this)
                }, toggle: function (e) {
                    return "boolean" == typeof e ? e ? this.show() : this.hide() : this.each(function () {
                        $e(this) ? ye(this).show() : ye(this).hide()
                    })
                }
            });
            var ze = /^(?:checkbox|radio)$/i, Xe = /<([a-z][^\/\0>\x20\t\r\n\f]+)/i, Ke = /^$|\/(?:java|ecma)script/i,
                Ve = {
                    option: [1, "<select multiple='multiple'>", "</select>"],
                    thead: [1, "<table>", "</table>"],
                    col: [2, "<table><colgroup>", "</colgroup></table>"],
                    tr: [2, "<table><tbody>", "</tbody></table>"],
                    td: [3, "<table><tbody><tr>", "</tr></tbody></table>"],
                    _default: [0, "", ""]
                };
            Ve.optgroup = Ve.option, Ve.tbody = Ve.tfoot = Ve.colgroup = Ve.caption = Ve.thead, Ve.th = Ve.td;
            var Ge = /<|&#?\w+;/;
            !function () {
                var e = ae.createDocumentFragment(), t = e.appendChild(ae.createElement("div")),
                    n = ae.createElement("input");
                n.setAttribute("type", "radio"), n.setAttribute("checked", "checked"), n.setAttribute("name", "t"), t.appendChild(n), ve.checkClone = t.cloneNode(!0).cloneNode(!0).lastChild.checked, t.innerHTML = "<textarea>x</textarea>", ve.noCloneChecked = !!t.cloneNode(!0).lastChild.defaultValue
            }();
            var Ye = ae.documentElement, Qe = /^key/, Je = /^(?:mouse|pointer|contextmenu|drag|drop)|click/,
                Ze = /^([^.]*)(?:\.(.+)|)/;
            ye.event = {
                global: {}, add: function (e, t, n, r, i) {
                    var o, a, s, u, l, c, f, d, p, h, g, m = Oe.get(e);
                    if (m) for (n.handler && (o = n, n = o.handler, i = o.selector), i && ye.find.matchesSelector(Ye, i), n.guid || (n.guid = ye.guid++), (u = m.events) || (u = m.events = {}), (a = m.handle) || (a = m.handle = function (t) {
                        return void 0 !== ye && ye.event.triggered !== t.type ? ye.event.dispatch.apply(e, arguments) : void 0
                    }), t = (t || "").match(Ae) || [""], l = t.length; l--;) s = Ze.exec(t[l]) || [], p = g = s[1], h = (s[2] || "").split(".").sort(), p && (f = ye.event.special[p] || {}, p = (i ? f.delegateType : f.bindType) || p, f = ye.event.special[p] || {}, c = ye.extend({
                        type: p,
                        origType: g,
                        data: r,
                        handler: n,
                        guid: n.guid,
                        selector: i,
                        needsContext: i && ye.expr.match.needsContext.test(i),
                        namespace: h.join(".")
                    }, o), (d = u[p]) || (d = u[p] = [], d.delegateCount = 0, f.setup && !1 !== f.setup.call(e, r, h, a) || e.addEventListener && e.addEventListener(p, a)), f.add && (f.add.call(e, c), c.handler.guid || (c.handler.guid = n.guid)), i ? d.splice(d.delegateCount++, 0, c) : d.push(c), ye.event.global[p] = !0)
                }, remove: function (e, t, n, r, i) {
                    var o, a, s, u, l, c, f, d, p, h, g, m = Oe.hasData(e) && Oe.get(e);
                    if (m && (u = m.events)) {
                        for (t = (t || "").match(Ae) || [""], l = t.length; l--;) if (s = Ze.exec(t[l]) || [], p = g = s[1], h = (s[2] || "").split(".").sort(), p) {
                            for (f = ye.event.special[p] || {}, p = (r ? f.delegateType : f.bindType) || p, d = u[p] || [], s = s[2] && new RegExp("(^|\\.)" + h.join("\\.(?:.*\\.|)") + "(\\.|$)"), a = o = d.length; o--;) c = d[o], !i && g !== c.origType || n && n.guid !== c.guid || s && !s.test(c.namespace) || r && r !== c.selector && ("**" !== r || !c.selector) || (d.splice(o, 1), c.selector && d.delegateCount--, f.remove && f.remove.call(e, c));
                            a && !d.length && (f.teardown && !1 !== f.teardown.call(e, h, m.handle) || ye.removeEvent(e, p, m.handle), delete u[p])
                        } else for (p in u) ye.event.remove(e, p + t[l], n, r, !0);
                        ye.isEmptyObject(u) && Oe.remove(e, "handle events")
                    }
                }, dispatch: function (e) {
                    var t, n, r, i, o, a, s = ye.event.fix(e), u = new Array(arguments.length),
                        l = (Oe.get(this, "events") || {})[s.type] || [], c = ye.event.special[s.type] || {};
                    for (u[0] = s, t = 1; t < arguments.length; t++) u[t] = arguments[t];
                    if (s.delegateTarget = this, !c.preDispatch || !1 !== c.preDispatch.call(this, s)) {
                        for (a = ye.event.handlers.call(this, s, l), t = 0; (i = a[t++]) && !s.isPropagationStopped();) for (s.currentTarget = i.elem, n = 0; (o = i.handlers[n++]) && !s.isImmediatePropagationStopped();) s.rnamespace && !s.rnamespace.test(o.namespace) || (s.handleObj = o, s.data = o.data, void 0 !== (r = ((ye.event.special[o.origType] || {}).handle || o.handler).apply(i.elem, u)) && !1 === (s.result = r) && (s.preventDefault(), s.stopPropagation()));
                        return c.postDispatch && c.postDispatch.call(this, s), s.result
                    }
                }, handlers: function (e, t) {
                    var n, r, i, o, a, s = [], u = t.delegateCount, l = e.target;
                    if (u && l.nodeType && !("click" === e.type && e.button >= 1)) for (; l !== this; l = l.parentNode || this) if (1 === l.nodeType && ("click" !== e.type || !0 !== l.disabled)) {
                        for (o = [], a = {}, n = 0; n < u; n++) r = t[n], i = r.selector + " ", void 0 === a[i] && (a[i] = r.needsContext ? ye(i, this).index(l) > -1 : ye.find(i, this, null, [l]).length), a[i] && o.push(r);
                        o.length && s.push({elem: l, handlers: o})
                    }
                    return l = this, u < t.length && s.push({elem: l, handlers: t.slice(u)}), s
                }, addProp: function (e, t) {
                    Object.defineProperty(ye.Event.prototype, e, {
                        enumerable: !0,
                        configurable: !0,
                        get: ye.isFunction(t) ? function () {
                            if (this.originalEvent) return t(this.originalEvent)
                        } : function () {
                            if (this.originalEvent) return this.originalEvent[e]
                        },
                        set: function (t) {
                            Object.defineProperty(this, e, {enumerable: !0, configurable: !0, writable: !0, value: t})
                        }
                    })
                }, fix: function (e) {
                    return e[ye.expando] ? e : new ye.Event(e)
                }, special: {
                    load: {noBubble: !0}, focus: {
                        trigger: function () {
                            if (this !== S() && this.focus) return this.focus(), !1
                        }, delegateType: "focusin"
                    }, blur: {
                        trigger: function () {
                            if (this === S() && this.blur) return this.blur(), !1
                        }, delegateType: "focusout"
                    }, click: {
                        trigger: function () {
                            if ("checkbox" === this.type && this.click && u(this, "input")) return this.click(), !1
                        }, _default: function (e) {
                            return u(e.target, "a")
                        }
                    }, beforeunload: {
                        postDispatch: function (e) {
                            void 0 !== e.result && e.originalEvent && (e.originalEvent.returnValue = e.result)
                        }
                    }
                }
            }, ye.removeEvent = function (e, t, n) {
                e.removeEventListener && e.removeEventListener(t, n)
            }, ye.Event = function (e, t) {
                if (!(this instanceof ye.Event)) return new ye.Event(e, t);
                e && e.type ? (this.originalEvent = e, this.type = e.type, this.isDefaultPrevented = e.defaultPrevented || void 0 === e.defaultPrevented && !1 === e.returnValue ? E : D, this.target = e.target && 3 === e.target.nodeType ? e.target.parentNode : e.target, this.currentTarget = e.currentTarget, this.relatedTarget = e.relatedTarget) : this.type = e, t && ye.extend(this, t), this.timeStamp = e && e.timeStamp || ye.now(), this[ye.expando] = !0
            }, ye.Event.prototype = {
                constructor: ye.Event,
                isDefaultPrevented: D,
                isPropagationStopped: D,
                isImmediatePropagationStopped: D,
                isSimulated: !1,
                preventDefault: function () {
                    var e = this.originalEvent;
                    this.isDefaultPrevented = E, e && !this.isSimulated && e.preventDefault()
                },
                stopPropagation: function () {
                    var e = this.originalEvent;
                    this.isPropagationStopped = E, e && !this.isSimulated && e.stopPropagation()
                },
                stopImmediatePropagation: function () {
                    var e = this.originalEvent;
                    this.isImmediatePropagationStopped = E, e && !this.isSimulated && e.stopImmediatePropagation(), this.stopPropagation()
                }
            }, ye.each({
                altKey: !0,
                bubbles: !0,
                cancelable: !0,
                changedTouches: !0,
                ctrlKey: !0,
                detail: !0,
                eventPhase: !0,
                metaKey: !0,
                pageX: !0,
                pageY: !0,
                shiftKey: !0,
                view: !0,
                char: !0,
                charCode: !0,
                key: !0,
                keyCode: !0,
                button: !0,
                buttons: !0,
                clientX: !0,
                clientY: !0,
                offsetX: !0,
                offsetY: !0,
                pointerId: !0,
                pointerType: !0,
                screenX: !0,
                screenY: !0,
                targetTouches: !0,
                toElement: !0,
                touches: !0,
                which: function (e) {
                    var t = e.button;
                    return null == e.which && Qe.test(e.type) ? null != e.charCode ? e.charCode : e.keyCode : !e.which && void 0 !== t && Je.test(e.type) ? 1 & t ? 1 : 2 & t ? 3 : 4 & t ? 2 : 0 : e.which
                }
            }, ye.event.addProp), ye.each({
                mouseenter: "mouseover",
                mouseleave: "mouseout",
                pointerenter: "pointerover",
                pointerleave: "pointerout"
            }, function (e, t) {
                ye.event.special[e] = {
                    delegateType: t, bindType: t, handle: function (e) {
                        var n, r = this, i = e.relatedTarget, o = e.handleObj;
                        return i && (i === r || ye.contains(r, i)) || (e.type = o.origType, n = o.handler.apply(this, arguments), e.type = t), n
                    }
                }
            }), ye.fn.extend({
                on: function (e, t, n, r) {
                    return j(this, e, t, n, r)
                }, one: function (e, t, n, r) {
                    return j(this, e, t, n, r, 1)
                }, off: function (e, t, n) {
                    var r, i;
                    if (e && e.preventDefault && e.handleObj) return r = e.handleObj, ye(e.delegateTarget).off(r.namespace ? r.origType + "." + r.namespace : r.origType, r.selector, r.handler), this;
                    if ("object" == typeof e) {
                        for (i in e) this.off(i, t, e[i]);
                        return this
                    }
                    return !1 !== t && "function" != typeof t || (n = t, t = void 0), !1 === n && (n = D), this.each(function () {
                        ye.event.remove(this, e, n, t)
                    })
                }
            });
            var et = /<script|<style|<link/i, tt = /checked\s*(?:[^=]|=\s*.checked.)/i, nt = /^true\/(.*)/,
                rt = /^\s*<!(?:\[CDATA\[|--)|(?:\]\]|--)>\s*$/g;
            ye.extend({
                htmlPrefilter: function (e) {
                    return e.replace(/<(?!area|br|col|embed|hr|img|input|link|meta|param)(([a-z][^\/\0>\x20\t\r\n\f]*)[^>]*)\/>/gi, "<$1></$2>")
                }, clone: function (e, t, n) {
                    var r, i, o, a, s = e.cloneNode(!0), u = ye.contains(e.ownerDocument, e);
                    if (!(ve.noCloneChecked || 1 !== e.nodeType && 11 !== e.nodeType || ye.isXMLDoc(e))) for (a = T(s), o = T(e), r = 0, i = o.length; r < i; r++) L(o[r], a[r]);
                    if (t) if (n) for (o = o || T(e), a = a || T(s), r = 0, i = o.length; r < i; r++) q(o[r], a[r]); else q(e, s);
                    return a = T(s, "script"), a.length > 0 && C(a, !u && T(e, "script")), s
                }, cleanData: function (e) {
                    for (var t, n, r, i = ye.event.special, o = 0; void 0 !== (n = e[o]); o++) if (He(n)) {
                        if (t = n[Oe.expando]) {
                            if (t.events) for (r in t.events) i[r] ? ye.event.remove(n, r) : ye.removeEvent(n, r, t.handle);
                            n[Oe.expando] = void 0
                        }
                        n[Fe.expando] && (n[Fe.expando] = void 0)
                    }
                }
            }), ye.fn.extend({
                detach: function (e) {
                    return O(this, e, !0)
                }, remove: function (e) {
                    return O(this, e)
                }, text: function (e) {
                    return Le(this, function (e) {
                        return void 0 === e ? ye.text(this) : this.empty().each(function () {
                            1 !== this.nodeType && 11 !== this.nodeType && 9 !== this.nodeType || (this.textContent = e)
                        })
                    }, null, e, arguments.length)
                }, append: function () {
                    return H(this, arguments, function (e) {
                        if (1 === this.nodeType || 11 === this.nodeType || 9 === this.nodeType) {
                            N(this, e).appendChild(e)
                        }
                    })
                }, prepend: function () {
                    return H(this, arguments, function (e) {
                        if (1 === this.nodeType || 11 === this.nodeType || 9 === this.nodeType) {
                            var t = N(this, e);
                            t.insertBefore(e, t.firstChild)
                        }
                    })
                }, before: function () {
                    return H(this, arguments, function (e) {
                        this.parentNode && this.parentNode.insertBefore(e, this)
                    })
                }, after: function () {
                    return H(this, arguments, function (e) {
                        this.parentNode && this.parentNode.insertBefore(e, this.nextSibling)
                    })
                }, empty: function () {
                    for (var e, t = 0; null != (e = this[t]); t++) 1 === e.nodeType && (ye.cleanData(T(e, !1)), e.textContent = "");
                    return this
                }, clone: function (e, t) {
                    return e = null != e && e, t = null == t ? e : t, this.map(function () {
                        return ye.clone(this, e, t)
                    })
                }, html: function (e) {
                    return Le(this, function (e) {
                        var t = this[0] || {}, n = 0, r = this.length;
                        if (void 0 === e && 1 === t.nodeType) return t.innerHTML;
                        if ("string" == typeof e && !et.test(e) && !Ve[(Xe.exec(e) || ["", ""])[1].toLowerCase()]) {
                            e = ye.htmlPrefilter(e);
                            try {
                                for (; n < r; n++) t = this[n] || {}, 1 === t.nodeType && (ye.cleanData(T(t, !1)), t.innerHTML = e);
                                t = 0
                            } catch (e) {
                            }
                        }
                        t && this.empty().append(e)
                    }, null, e, arguments.length)
                }, replaceWith: function () {
                    var e = [];
                    return H(this, arguments, function (t) {
                        var n = this.parentNode;
                        ye.inArray(this, e) < 0 && (ye.cleanData(T(this)), n && n.replaceChild(t, this))
                    }, e)
                }
            }), ye.each({
                appendTo: "append",
                prependTo: "prepend",
                insertBefore: "before",
                insertAfter: "after",
                replaceAll: "replaceWith"
            }, function (e, t) {
                ye.fn[e] = function (e) {
                    for (var n, r = [], i = ye(e), o = i.length - 1, a = 0; a <= o; a++) n = a === o ? this : this.clone(!0), ye(i[a])[t](n), ce.apply(r, n.get());
                    return this.pushStack(r)
                }
            });
            var it = /^margin/, ot = new RegExp("^(" + Ie + ")(?!px)[a-z%]+$", "i"), at = function (e) {
                var t = e.ownerDocument.defaultView;
                return t && t.opener || (t = n), t.getComputedStyle(e)
            };
            !function () {
                function e() {
                    if (s) {
                        s.style.cssText = "box-sizing:border-box;position:relative;display:block;margin:auto;border:1px;padding:1px;top:1%;width:50%", s.innerHTML = "", Ye.appendChild(a);
                        var e = n.getComputedStyle(s);
                        t = "1%" !== e.top, o = "2px" === e.marginLeft, r = "4px" === e.width, s.style.marginRight = "50%", i = "4px" === e.marginRight, Ye.removeChild(a), s = null
                    }
                }

                var t, r, i, o, a = ae.createElement("div"), s = ae.createElement("div");
                s.style && (s.style.backgroundClip = "content-box", s.cloneNode(!0).style.backgroundClip = "", ve.clearCloneStyle = "content-box" === s.style.backgroundClip, a.style.cssText = "border:0;width:8px;height:0;top:0;left:-9999px;padding:0;margin-top:1px;position:absolute", a.appendChild(s), ye.extend(ve, {
                    pixelPosition: function () {
                        return e(), t
                    }, boxSizingReliable: function () {
                        return e(), r
                    }, pixelMarginRight: function () {
                        return e(), i
                    }, reliableMarginLeft: function () {
                        return e(), o
                    }
                }))
            }();
            var st = /^(none|table(?!-c[ea]).+)/, ut = /^--/,
                lt = {position: "absolute", visibility: "hidden", display: "block"},
                ct = {letterSpacing: "0", fontWeight: "400"}, ft = ["Webkit", "Moz", "ms"],
                dt = ae.createElement("div").style;
            ye.extend({
                cssHooks: {
                    opacity: {
                        get: function (e, t) {
                            if (t) {
                                var n = F(e, "opacity");
                                return "" === n ? "1" : n
                            }
                        }
                    }
                },
                cssNumber: {
                    animationIterationCount: !0,
                    columnCount: !0,
                    fillOpacity: !0,
                    flexGrow: !0,
                    flexShrink: !0,
                    fontWeight: !0,
                    lineHeight: !0,
                    opacity: !0,
                    order: !0,
                    orphans: !0,
                    widows: !0,
                    zIndex: !0,
                    zoom: !0
                },
                cssProps: {float: "cssFloat"},
                style: function (e, t, n, r) {
                    if (e && 3 !== e.nodeType && 8 !== e.nodeType && e.style) {
                        var i, o, a, s = ye.camelCase(t), u = ut.test(t), l = e.style;
                        if (u || (t = I(s)), a = ye.cssHooks[t] || ye.cssHooks[s], void 0 === n) return a && "get" in a && void 0 !== (i = a.get(e, !1, r)) ? i : l[t];
                        o = typeof n, "string" === o && (i = Me.exec(n)) && i[1] && (n = x(e, t, i), o = "number"), null != n && n === n && ("number" === o && (n += i && i[3] || (ye.cssNumber[s] ? "" : "px")), ve.clearCloneStyle || "" !== n || 0 !== t.indexOf("background") || (l[t] = "inherit"), a && "set" in a && void 0 === (n = a.set(e, n, r)) || (u ? l.setProperty(t, n) : l[t] = n))
                    }
                },
                css: function (e, t, n, r) {
                    var i, o, a, s = ye.camelCase(t);
                    return ut.test(t) || (t = I(s)), a = ye.cssHooks[t] || ye.cssHooks[s], a && "get" in a && (i = a.get(e, !0, n)), void 0 === i && (i = F(e, t, r)), "normal" === i && t in ct && (i = ct[t]), "" === n || n ? (o = parseFloat(i), !0 === n || isFinite(o) ? o || 0 : i) : i
                }
            }), ye.each(["height", "width"], function (e, t) {
                ye.cssHooks[t] = {
                    get: function (e, n, r) {
                        if (n) return !st.test(ye.css(e, "display")) || e.getClientRects().length && e.getBoundingClientRect().width ? $(e, t, r) : Be(e, lt, function () {
                            return $(e, t, r)
                        })
                    }, set: function (e, n, r) {
                        var i, o = r && at(e), a = r && W(e, t, r, "border-box" === ye.css(e, "boxSizing", !1, o), o);
                        return a && (i = Me.exec(n)) && "px" !== (i[3] || "px") && (e.style[t] = n, n = ye.css(e, t)), M(e, n, a)
                    }
                }
            }), ye.cssHooks.marginLeft = P(ve.reliableMarginLeft, function (e, t) {
                if (t) return (parseFloat(F(e, "marginLeft")) || e.getBoundingClientRect().left - Be(e, {marginLeft: 0}, function () {
                    return e.getBoundingClientRect().left
                })) + "px"
            }), ye.each({margin: "", padding: "", border: "Width"}, function (e, t) {
                ye.cssHooks[e + t] = {
                    expand: function (n) {
                        for (var r = 0, i = {}, o = "string" == typeof n ? n.split(" ") : [n]; r < 4; r++) i[e + We[r] + t] = o[r] || o[r - 2] || o[0];
                        return i
                    }
                }, it.test(e) || (ye.cssHooks[e + t].set = M)
            }), ye.fn.extend({
                css: function (e, t) {
                    return Le(this, function (e, t, n) {
                        var r, i, o = {}, a = 0;
                        if (Array.isArray(t)) {
                            for (r = at(e), i = t.length; a < i; a++) o[t[a]] = ye.css(e, t[a], !1, r);
                            return o
                        }
                        return void 0 !== n ? ye.style(e, t, n) : ye.css(e, t)
                    }, e, t, arguments.length > 1)
                }
            }), ye.Tween = B, B.prototype = {
                constructor: B, init: function (e, t, n, r, i, o) {
                    this.elem = e, this.prop = n, this.easing = i || ye.easing._default, this.options = t, this.start = this.now = this.cur(), this.end = r, this.unit = o || (ye.cssNumber[n] ? "" : "px")
                }, cur: function () {
                    var e = B.propHooks[this.prop];
                    return e && e.get ? e.get(this) : B.propHooks._default.get(this)
                }, run: function (e) {
                    var t, n = B.propHooks[this.prop];
                    return this.options.duration ? this.pos = t = ye.easing[this.easing](e, this.options.duration * e, 0, 1, this.options.duration) : this.pos = t = e, this.now = (this.end - this.start) * t + this.start, this.options.step && this.options.step.call(this.elem, this.now, this), n && n.set ? n.set(this) : B.propHooks._default.set(this), this
                }
            }, B.prototype.init.prototype = B.prototype, B.propHooks = {
                _default: {
                    get: function (e) {
                        var t;
                        return 1 !== e.elem.nodeType || null != e.elem[e.prop] && null == e.elem.style[e.prop] ? e.elem[e.prop] : (t = ye.css(e.elem, e.prop, ""), t && "auto" !== t ? t : 0)
                    }, set: function (e) {
                        ye.fx.step[e.prop] ? ye.fx.step[e.prop](e) : 1 !== e.elem.nodeType || null == e.elem.style[ye.cssProps[e.prop]] && !ye.cssHooks[e.prop] ? e.elem[e.prop] = e.now : ye.style(e.elem, e.prop, e.now + e.unit)
                    }
                }
            }, B.propHooks.scrollTop = B.propHooks.scrollLeft = {
                set: function (e) {
                    e.elem.nodeType && e.elem.parentNode && (e.elem[e.prop] = e.now)
                }
            }, ye.easing = {
                linear: function (e) {
                    return e
                }, swing: function (e) {
                    return .5 - Math.cos(e * Math.PI) / 2
                }, _default: "swing"
            }, ye.fx = B.prototype.init, ye.fx.step = {};
            var pt, ht, gt = /^(?:toggle|show|hide)$/, mt = /queueHooks$/;
            ye.Animation = ye.extend(Y, {
                tweeners: {
                    "*": [function (e, t) {
                        var n = this.createTween(e, t);
                        return x(n.elem, e, Me.exec(t), n), n
                    }]
                }, tweener: function (e, t) {
                    ye.isFunction(e) ? (t = e, e = ["*"]) : e = e.match(Ae);
                    for (var n, r = 0, i = e.length; r < i; r++) n = e[r], Y.tweeners[n] = Y.tweeners[n] || [], Y.tweeners[n].unshift(t)
                }, prefilters: [V], prefilter: function (e, t) {
                    t ? Y.prefilters.unshift(e) : Y.prefilters.push(e)
                }
            }), ye.speed = function (e, t, n) {
                var r = e && "object" == typeof e ? ye.extend({}, e) : {
                    complete: n || !n && t || ye.isFunction(e) && e,
                    duration: e,
                    easing: n && t || t && !ye.isFunction(t) && t
                };
                return ye.fx.off ? r.duration = 0 : "number" != typeof r.duration && (r.duration in ye.fx.speeds ? r.duration = ye.fx.speeds[r.duration] : r.duration = ye.fx.speeds._default), null != r.queue && !0 !== r.queue || (r.queue = "fx"), r.old = r.complete, r.complete = function () {
                    ye.isFunction(r.old) && r.old.call(this), r.queue && ye.dequeue(this, r.queue)
                }, r
            }, ye.fn.extend({
                fadeTo: function (e, t, n, r) {
                    return this.filter($e).css("opacity", 0).show().end().animate({opacity: t}, e, n, r)
                }, animate: function (e, t, n, r) {
                    var i = ye.isEmptyObject(e), o = ye.speed(t, n, r), a = function () {
                        var t = Y(this, ye.extend({}, e), o);
                        (i || Oe.get(this, "finish")) && t.stop(!0)
                    };
                    return a.finish = a, i || !1 === o.queue ? this.each(a) : this.queue(o.queue, a)
                }, stop: function (e, t, n) {
                    var r = function (e) {
                        var t = e.stop;
                        delete e.stop, t(n)
                    };
                    return "string" != typeof e && (n = t, t = e, e = void 0), t && !1 !== e && this.queue(e || "fx", []), this.each(function () {
                        var t = !0, i = null != e && e + "queueHooks", o = ye.timers, a = Oe.get(this);
                        if (i) a[i] && a[i].stop && r(a[i]); else for (i in a) a[i] && a[i].stop && mt.test(i) && r(a[i]);
                        for (i = o.length; i--;) o[i].elem !== this || null != e && o[i].queue !== e || (o[i].anim.stop(n), t = !1, o.splice(i, 1));
                        !t && n || ye.dequeue(this, e)
                    })
                }, finish: function (e) {
                    return !1 !== e && (e = e || "fx"), this.each(function () {
                        var t, n = Oe.get(this), r = n[e + "queue"], i = n[e + "queueHooks"], o = ye.timers,
                            a = r ? r.length : 0;
                        for (n.finish = !0, ye.queue(this, e, []), i && i.stop && i.stop.call(this, !0), t = o.length; t--;) o[t].elem === this && o[t].queue === e && (o[t].anim.stop(!0), o.splice(t, 1));
                        for (t = 0; t < a; t++) r[t] && r[t].finish && r[t].finish.call(this);
                        delete n.finish
                    })
                }
            }), ye.each(["toggle", "show", "hide"], function (e, t) {
                var n = ye.fn[t];
                ye.fn[t] = function (e, r, i) {
                    return null == e || "boolean" == typeof e ? n.apply(this, arguments) : this.animate(X(t, !0), e, r, i)
                }
            }), ye.each({
                slideDown: X("show"),
                slideUp: X("hide"),
                slideToggle: X("toggle"),
                fadeIn: {opacity: "show"},
                fadeOut: {opacity: "hide"},
                fadeToggle: {opacity: "toggle"}
            }, function (e, t) {
                ye.fn[e] = function (e, n, r) {
                    return this.animate(t, e, n, r)
                }
            }), ye.timers = [], ye.fx.tick = function () {
                var e, t = 0, n = ye.timers;
                for (pt = ye.now(); t < n.length; t++) (e = n[t])() || n[t] !== e || n.splice(t--, 1);
                n.length || ye.fx.stop(), pt = void 0
            }, ye.fx.timer = function (e) {
                ye.timers.push(e), ye.fx.start()
            }, ye.fx.interval = 13, ye.fx.start = function () {
                ht || (ht = !0, U())
            }, ye.fx.stop = function () {
                ht = null
            }, ye.fx.speeds = {slow: 600, fast: 200, _default: 400}, ye.fn.delay = function (e, t) {
                return e = ye.fx ? ye.fx.speeds[e] || e : e, t = t || "fx", this.queue(t, function (t, r) {
                    var i = n.setTimeout(t, e);
                    r.stop = function () {
                        n.clearTimeout(i)
                    }
                })
            }, function () {
                var e = ae.createElement("input"), t = ae.createElement("select"),
                    n = t.appendChild(ae.createElement("option"));
                e.type = "checkbox", ve.checkOn = "" !== e.value, ve.optSelected = n.selected, e = ae.createElement("input"), e.value = "t", e.type = "radio", ve.radioValue = "t" === e.value
            }();
            var vt, yt = ye.expr.attrHandle;
            ye.fn.extend({
                attr: function (e, t) {
                    return Le(this, ye.attr, e, t, arguments.length > 1)
                }, removeAttr: function (e) {
                    return this.each(function () {
                        ye.removeAttr(this, e)
                    })
                }
            }), ye.extend({
                attr: function (e, t, n) {
                    var r, i, o = e.nodeType;
                    if (3 !== o && 8 !== o && 2 !== o) return void 0 === e.getAttribute ? ye.prop(e, t, n) : (1 === o && ye.isXMLDoc(e) || (i = ye.attrHooks[t.toLowerCase()] || (ye.expr.match.bool.test(t) ? vt : void 0)), void 0 !== n ? null === n ? void ye.removeAttr(e, t) : i && "set" in i && void 0 !== (r = i.set(e, n, t)) ? r : (e.setAttribute(t, n + ""), n) : i && "get" in i && null !== (r = i.get(e, t)) ? r : (r = ye.find.attr(e, t), null == r ? void 0 : r))
                }, attrHooks: {
                    type: {
                        set: function (e, t) {
                            if (!ve.radioValue && "radio" === t && u(e, "input")) {
                                var n = e.value;
                                return e.setAttribute("type", t), n && (e.value = n), t
                            }
                        }
                    }
                }, removeAttr: function (e, t) {
                    var n, r = 0, i = t && t.match(Ae);
                    if (i && 1 === e.nodeType) for (; n = i[r++];) e.removeAttribute(n)
                }
            }), vt = {
                set: function (e, t, n) {
                    return !1 === t ? ye.removeAttr(e, n) : e.setAttribute(n, n), n
                }
            }, ye.each(ye.expr.match.bool.source.match(/\w+/g), function (e, t) {
                var n = yt[t] || ye.find.attr;
                yt[t] = function (e, t, r) {
                    var i, o, a = t.toLowerCase();
                    return r || (o = yt[a], yt[a] = i, i = null != n(e, t, r) ? a : null, yt[a] = o), i
                }
            });
            var xt = /^(?:input|select|textarea|button)$/i, bt = /^(?:a|area)$/i;
            ye.fn.extend({
                prop: function (e, t) {
                    return Le(this, ye.prop, e, t, arguments.length > 1)
                }, removeProp: function (e) {
                    return this.each(function () {
                        delete this[ye.propFix[e] || e]
                    })
                }
            }), ye.extend({
                prop: function (e, t, n) {
                    var r, i, o = e.nodeType;
                    if (3 !== o && 8 !== o && 2 !== o) return 1 === o && ye.isXMLDoc(e) || (t = ye.propFix[t] || t, i = ye.propHooks[t]), void 0 !== n ? i && "set" in i && void 0 !== (r = i.set(e, n, t)) ? r : e[t] = n : i && "get" in i && null !== (r = i.get(e, t)) ? r : e[t]
                }, propHooks: {
                    tabIndex: {
                        get: function (e) {
                            var t = ye.find.attr(e, "tabindex");
                            return t ? parseInt(t, 10) : xt.test(e.nodeName) || bt.test(e.nodeName) && e.href ? 0 : -1
                        }
                    }
                }, propFix: {for: "htmlFor", class: "className"}
            }), ve.optSelected || (ye.propHooks.selected = {
                get: function (e) {
                    var t = e.parentNode;
                    return t && t.parentNode && t.parentNode.selectedIndex, null
                }, set: function (e) {
                    var t = e.parentNode;
                    t && (t.selectedIndex, t.parentNode && t.parentNode.selectedIndex)
                }
            }), ye.each(["tabIndex", "readOnly", "maxLength", "cellSpacing", "cellPadding", "rowSpan", "colSpan", "useMap", "frameBorder", "contentEditable"], function () {
                ye.propFix[this.toLowerCase()] = this
            }), ye.fn.extend({
                addClass: function (e) {
                    var t, n, r, i, o, a, s, u = 0;
                    if (ye.isFunction(e)) return this.each(function (t) {
                        ye(this).addClass(e.call(this, t, J(this)))
                    });
                    if ("string" == typeof e && e) for (t = e.match(Ae) || []; n = this[u++];) if (i = J(n), r = 1 === n.nodeType && " " + Q(i) + " ") {
                        for (a = 0; o = t[a++];) r.indexOf(" " + o + " ") < 0 && (r += o + " ");
                        s = Q(r), i !== s && n.setAttribute("class", s)
                    }
                    return this
                }, removeClass: function (e) {
                    var t, n, r, i, o, a, s, u = 0;
                    if (ye.isFunction(e)) return this.each(function (t) {
                        ye(this).removeClass(e.call(this, t, J(this)))
                    });
                    if (!arguments.length) return this.attr("class", "");
                    if ("string" == typeof e && e) for (t = e.match(Ae) || []; n = this[u++];) if (i = J(n), r = 1 === n.nodeType && " " + Q(i) + " ") {
                        for (a = 0; o = t[a++];) for (; r.indexOf(" " + o + " ") > -1;) r = r.replace(" " + o + " ", " ");
                        s = Q(r), i !== s && n.setAttribute("class", s)
                    }
                    return this
                }, toggleClass: function (e, t) {
                    var n = typeof e;
                    return "boolean" == typeof t && "string" === n ? t ? this.addClass(e) : this.removeClass(e) : ye.isFunction(e) ? this.each(function (n) {
                        ye(this).toggleClass(e.call(this, n, J(this), t), t)
                    }) : this.each(function () {
                        var t, r, i, o;
                        if ("string" === n) for (r = 0, i = ye(this), o = e.match(Ae) || []; t = o[r++];) i.hasClass(t) ? i.removeClass(t) : i.addClass(t); else void 0 !== e && "boolean" !== n || (t = J(this), t && Oe.set(this, "__className__", t), this.setAttribute && this.setAttribute("class", t || !1 === e ? "" : Oe.get(this, "__className__") || ""))
                    })
                }, hasClass: function (e) {
                    var t, n, r = 0;
                    for (t = " " + e + " "; n = this[r++];) if (1 === n.nodeType && (" " + Q(J(n)) + " ").indexOf(t) > -1) return !0;
                    return !1
                }
            });
            ye.fn.extend({
                val: function (e) {
                    var t, n, r, i = this[0];
                    {
                        if (arguments.length) return r = ye.isFunction(e), this.each(function (n) {
                            var i;
                            1 === this.nodeType && (i = r ? e.call(this, n, ye(this).val()) : e, null == i ? i = "" : "number" == typeof i ? i += "" : Array.isArray(i) && (i = ye.map(i, function (e) {
                                return null == e ? "" : e + ""
                            })), (t = ye.valHooks[this.type] || ye.valHooks[this.nodeName.toLowerCase()]) && "set" in t && void 0 !== t.set(this, i, "value") || (this.value = i))
                        });
                        if (i) return (t = ye.valHooks[i.type] || ye.valHooks[i.nodeName.toLowerCase()]) && "get" in t && void 0 !== (n = t.get(i, "value")) ? n : (n = i.value, "string" == typeof n ? n.replace(/\r/g, "") : null == n ? "" : n)
                    }
                }
            }), ye.extend({
                valHooks: {
                    option: {
                        get: function (e) {
                            var t = ye.find.attr(e, "value");
                            return null != t ? t : Q(ye.text(e))
                        }
                    }, select: {
                        get: function (e) {
                            var t, n, r, i = e.options, o = e.selectedIndex, a = "select-one" === e.type,
                                s = a ? null : [], l = a ? o + 1 : i.length;
                            for (r = o < 0 ? l : a ? o : 0; r < l; r++) if (n = i[r], (n.selected || r === o) && !n.disabled && (!n.parentNode.disabled || !u(n.parentNode, "optgroup"))) {
                                if (t = ye(n).val(), a) return t;
                                s.push(t)
                            }
                            return s
                        }, set: function (e, t) {
                            for (var n, r, i = e.options, o = ye.makeArray(t), a = i.length; a--;) r = i[a], (r.selected = ye.inArray(ye.valHooks.option.get(r), o) > -1) && (n = !0);
                            return n || (e.selectedIndex = -1), o
                        }
                    }
                }
            }), ye.each(["radio", "checkbox"], function () {
                ye.valHooks[this] = {
                    set: function (e, t) {
                        if (Array.isArray(t)) return e.checked = ye.inArray(ye(e).val(), t) > -1
                    }
                }, ve.checkOn || (ye.valHooks[this].get = function (e) {
                    return null === e.getAttribute("value") ? "on" : e.value
                })
            });
            var wt = /^(?:focusinfocus|focusoutblur)$/;
            ye.extend(ye.event, {
                trigger: function (e, t, r, i) {
                    var o, a, s, u, l, c, f, d = [r || ae], p = he.call(e, "type") ? e.type : e,
                        h = he.call(e, "namespace") ? e.namespace.split(".") : [];
                    if (a = s = r = r || ae, 3 !== r.nodeType && 8 !== r.nodeType && !wt.test(p + ye.event.triggered) && (p.indexOf(".") > -1 && (h = p.split("."), p = h.shift(), h.sort()), l = p.indexOf(":") < 0 && "on" + p, e = e[ye.expando] ? e : new ye.Event(p, "object" == typeof e && e), e.isTrigger = i ? 2 : 3, e.namespace = h.join("."), e.rnamespace = e.namespace ? new RegExp("(^|\\.)" + h.join("\\.(?:.*\\.|)") + "(\\.|$)") : null, e.result = void 0, e.target || (e.target = r), t = null == t ? [e] : ye.makeArray(t, [e]), f = ye.event.special[p] || {}, i || !f.trigger || !1 !== f.trigger.apply(r, t))) {
                        if (!i && !f.noBubble && !ye.isWindow(r)) {
                            for (u = f.delegateType || p, wt.test(u + p) || (a = a.parentNode); a; a = a.parentNode) d.push(a), s = a;
                            s === (r.ownerDocument || ae) && d.push(s.defaultView || s.parentWindow || n)
                        }
                        for (o = 0; (a = d[o++]) && !e.isPropagationStopped();) e.type = o > 1 ? u : f.bindType || p, c = (Oe.get(a, "events") || {})[e.type] && Oe.get(a, "handle"), c && c.apply(a, t), (c = l && a[l]) && c.apply && He(a) && (e.result = c.apply(a, t), !1 === e.result && e.preventDefault());
                        return e.type = p, i || e.isDefaultPrevented() || f._default && !1 !== f._default.apply(d.pop(), t) || !He(r) || l && ye.isFunction(r[p]) && !ye.isWindow(r) && (s = r[l], s && (r[l] = null), ye.event.triggered = p, r[p](), ye.event.triggered = void 0, s && (r[l] = s)), e.result
                    }
                }, simulate: function (e, t, n) {
                    var r = ye.extend(new ye.Event, n, {type: e, isSimulated: !0});
                    ye.event.trigger(r, null, t)
                }
            }), ye.fn.extend({
                trigger: function (e, t) {
                    return this.each(function () {
                        ye.event.trigger(e, t, this)
                    })
                }, triggerHandler: function (e, t) {
                    var n = this[0];
                    if (n) return ye.event.trigger(e, t, n, !0)
                }
            }), ye.each("blur focus focusin focusout resize scroll click dblclick mousedown mouseup mousemove mouseover mouseout mouseenter mouseleave change select submit keydown keypress keyup contextmenu".split(" "), function (e, t) {
                ye.fn[t] = function (e, n) {
                    return arguments.length > 0 ? this.on(t, null, e, n) : this.trigger(t)
                }
            }), ye.fn.extend({
                hover: function (e, t) {
                    return this.mouseenter(e).mouseleave(t || e)
                }
            }), ve.focusin = "onfocusin" in n, ve.focusin || ye.each({
                focus: "focusin",
                blur: "focusout"
            }, function (e, t) {
                var n = function (e) {
                    ye.event.simulate(t, e.target, ye.event.fix(e))
                };
                ye.event.special[t] = {
                    setup: function () {
                        var r = this.ownerDocument || this, i = Oe.access(r, t);
                        i || r.addEventListener(e, n, !0), Oe.access(r, t, (i || 0) + 1)
                    }, teardown: function () {
                        var r = this.ownerDocument || this, i = Oe.access(r, t) - 1;
                        i ? Oe.access(r, t, i) : (r.removeEventListener(e, n, !0), Oe.remove(r, t))
                    }
                }
            });
            var Tt = n.location, Ct = ye.now(), kt = /\?/;
            ye.parseXML = function (e) {
                var t;
                if (!e || "string" != typeof e) return null;
                try {
                    t = (new n.DOMParser).parseFromString(e, "text/xml")
                } catch (e) {
                    t = void 0
                }
                return t && !t.getElementsByTagName("parsererror").length || ye.error("Invalid XML: " + e), t
            };
            var Et = /\[\]$/, Dt = /^(?:submit|button|image|reset|file)$/i, St = /^(?:input|select|textarea|keygen)/i;
            ye.param = function (e, t) {
                var n, r = [], i = function (e, t) {
                    var n = ye.isFunction(t) ? t() : t;
                    r[r.length] = encodeURIComponent(e) + "=" + encodeURIComponent(null == n ? "" : n)
                };
                if (Array.isArray(e) || e.jquery && !ye.isPlainObject(e)) ye.each(e, function () {
                    i(this.name, this.value)
                }); else for (n in e) Z(n, e[n], t, i);
                return r.join("&")
            }, ye.fn.extend({
                serialize: function () {
                    return ye.param(this.serializeArray())
                }, serializeArray: function () {
                    return this.map(function () {
                        var e = ye.prop(this, "elements");
                        return e ? ye.makeArray(e) : this
                    }).filter(function () {
                        var e = this.type;
                        return this.name && !ye(this).is(":disabled") && St.test(this.nodeName) && !Dt.test(e) && (this.checked || !ze.test(e))
                    }).map(function (e, t) {
                        var n = ye(this).val();
                        return null == n ? null : Array.isArray(n) ? ye.map(n, function (e) {
                            return {name: t.name, value: e.replace(/\r?\n/g, "\r\n")}
                        }) : {name: t.name, value: n.replace(/\r?\n/g, "\r\n")}
                    }).get()
                }
            });
            var jt = /^(.*?):[ \t]*([^\r\n]*)$/gm, Nt = /^(?:about|app|app-storage|.+-extension|file|res|widget):$/,
                At = /^(?:GET|HEAD)$/, _t = {}, qt = {}, Lt = "*/".concat("*"), Ht = ae.createElement("a");
            Ht.href = Tt.href, ye.extend({
                active: 0,
                lastModified: {},
                etag: {},
                ajaxSettings: {
                    url: Tt.href,
                    type: "GET",
                    isLocal: Nt.test(Tt.protocol),
                    global: !0,
                    processData: !0,
                    async: !0,
                    contentType: "application/x-www-form-urlencoded; charset=UTF-8",
                    accepts: {
                        "*": Lt,
                        text: "text/plain",
                        html: "text/html",
                        xml: "application/xml, text/xml",
                        json: "application/json, text/javascript"
                    },
                    contents: {xml: /\bxml\b/, html: /\bhtml/, json: /\bjson\b/},
                    responseFields: {xml: "responseXML", text: "responseText", json: "responseJSON"},
                    converters: {"* text": String, "text html": !0, "text json": JSON.parse, "text xml": ye.parseXML},
                    flatOptions: {url: !0, context: !0}
                },
                ajaxSetup: function (e, t) {
                    return t ? ne(ne(e, ye.ajaxSettings), t) : ne(ye.ajaxSettings, e)
                },
                ajaxPrefilter: ee(_t),
                ajaxTransport: ee(qt),
                ajax: function (e, t) {
                    function r(e, t, r, s) {
                        var l, d, p, b, w, T = t;
                        c || (c = !0, u && n.clearTimeout(u), i = void 0, a = s || "", C.readyState = e > 0 ? 4 : 0, l = e >= 200 && e < 300 || 304 === e, r && (b = re(h, C, r)), b = ie(h, b, C, l), l ? (h.ifModified && (w = C.getResponseHeader("Last-Modified"), w && (ye.lastModified[o] = w), (w = C.getResponseHeader("etag")) && (ye.etag[o] = w)), 204 === e || "HEAD" === h.type ? T = "nocontent" : 304 === e ? T = "notmodified" : (T = b.state, d = b.data, p = b.error, l = !p)) : (p = T, !e && T || (T = "error", e < 0 && (e = 0))), C.status = e, C.statusText = (t || T) + "", l ? v.resolveWith(g, [d, T, C]) : v.rejectWith(g, [C, T, p]), C.statusCode(x), x = void 0, f && m.trigger(l ? "ajaxSuccess" : "ajaxError", [C, h, l ? d : p]), y.fireWith(g, [C, T]), f && (m.trigger("ajaxComplete", [C, h]), --ye.active || ye.event.trigger("ajaxStop")))
                    }

                    "object" == typeof e && (t = e, e = void 0), t = t || {};
                    var i, o, a, s, u, l, c, f, d, p, h = ye.ajaxSetup({}, t), g = h.context || h,
                        m = h.context && (g.nodeType || g.jquery) ? ye(g) : ye.event, v = ye.Deferred(),
                        y = ye.Callbacks("once memory"), x = h.statusCode || {}, b = {}, w = {}, T = "canceled", C = {
                            readyState: 0, getResponseHeader: function (e) {
                                var t;
                                if (c) {
                                    if (!s) for (s = {}; t = jt.exec(a);) s[t[1].toLowerCase()] = t[2];
                                    t = s[e.toLowerCase()]
                                }
                                return null == t ? null : t
                            }, getAllResponseHeaders: function () {
                                return c ? a : null
                            }, setRequestHeader: function (e, t) {
                                return null == c && (e = w[e.toLowerCase()] = w[e.toLowerCase()] || e, b[e] = t), this
                            }, overrideMimeType: function (e) {
                                return null == c && (h.mimeType = e), this
                            }, statusCode: function (e) {
                                var t;
                                if (e) if (c) C.always(e[C.status]); else for (t in e) x[t] = [x[t], e[t]];
                                return this
                            }, abort: function (e) {
                                var t = e || T;
                                return i && i.abort(t), r(0, t), this
                            }
                        };
                    if (v.promise(C), h.url = ((e || h.url || Tt.href) + "").replace(/^\/\//, Tt.protocol + "//"), h.type = t.method || t.type || h.method || h.type, h.dataTypes = (h.dataType || "*").toLowerCase().match(Ae) || [""], null == h.crossDomain) {
                        l = ae.createElement("a");
                        try {
                            l.href = h.url, l.href = l.href, h.crossDomain = Ht.protocol + "//" + Ht.host != l.protocol + "//" + l.host
                        } catch (e) {
                            h.crossDomain = !0
                        }
                    }
                    if (h.data && h.processData && "string" != typeof h.data && (h.data = ye.param(h.data, h.traditional)), te(_t, h, t, C), c) return C;
                    f = ye.event && h.global, f && 0 == ye.active++ && ye.event.trigger("ajaxStart"), h.type = h.type.toUpperCase(), h.hasContent = !At.test(h.type), o = h.url.replace(/#.*$/, ""), h.hasContent ? h.data && h.processData && 0 === (h.contentType || "").indexOf("application/x-www-form-urlencoded") && (h.data = h.data.replace(/%20/g, "+")) : (p = h.url.slice(o.length), h.data && (o += (kt.test(o) ? "&" : "?") + h.data, delete h.data), !1 === h.cache && (o = o.replace(/([?&])_=[^&]*/, "$1"), p = (kt.test(o) ? "&" : "?") + "_=" + Ct++ + p), h.url = o + p), h.ifModified && (ye.lastModified[o] && C.setRequestHeader("If-Modified-Since", ye.lastModified[o]), ye.etag[o] && C.setRequestHeader("If-None-Match", ye.etag[o])), (h.data && h.hasContent && !1 !== h.contentType || t.contentType) && C.setRequestHeader("Content-Type", h.contentType), C.setRequestHeader("Accept", h.dataTypes[0] && h.accepts[h.dataTypes[0]] ? h.accepts[h.dataTypes[0]] + ("*" !== h.dataTypes[0] ? ", " + Lt + "; q=0.01" : "") : h.accepts["*"]);
                    for (d in h.headers) C.setRequestHeader(d, h.headers[d]);
                    if (h.beforeSend && (!1 === h.beforeSend.call(g, C, h) || c)) return C.abort();
                    if (T = "abort", y.add(h.complete), C.done(h.success), C.fail(h.error), i = te(qt, h, t, C)) {
                        if (C.readyState = 1, f && m.trigger("ajaxSend", [C, h]), c) return C;
                        h.async && h.timeout > 0 && (u = n.setTimeout(function () {
                            C.abort("timeout")
                        }, h.timeout));
                        try {
                            c = !1, i.send(b, r)
                        } catch (e) {
                            if (c) throw e;
                            r(-1, e)
                        }
                    } else r(-1, "No Transport");
                    return C
                },
                getJSON: function (e, t, n) {
                    return ye.get(e, t, n, "json")
                },
                getScript: function (e, t) {
                    return ye.get(e, void 0, t, "script")
                }
            }), ye.each(["get", "post"], function (e, t) {
                ye[t] = function (e, n, r, i) {
                    return ye.isFunction(n) && (i = i || r, r = n, n = void 0), ye.ajax(ye.extend({
                        url: e,
                        type: t,
                        dataType: i,
                        data: n,
                        success: r
                    }, ye.isPlainObject(e) && e))
                }
            }), ye._evalUrl = function (e) {
                return ye.ajax({url: e, type: "GET", dataType: "script", cache: !0, async: !1, global: !1, throws: !0})
            }, ye.fn.extend({
                wrapAll: function (e) {
                    var t;
                    return this[0] && (ye.isFunction(e) && (e = e.call(this[0])), t = ye(e, this[0].ownerDocument).eq(0).clone(!0), this[0].parentNode && t.insertBefore(this[0]), t.map(function () {
                        for (var e = this; e.firstElementChild;) e = e.firstElementChild;
                        return e
                    }).append(this)), this
                }, wrapInner: function (e) {
                    return ye.isFunction(e) ? this.each(function (t) {
                        ye(this).wrapInner(e.call(this, t))
                    }) : this.each(function () {
                        var t = ye(this), n = t.contents();
                        n.length ? n.wrapAll(e) : t.append(e)
                    })
                }, wrap: function (e) {
                    var t = ye.isFunction(e);
                    return this.each(function (n) {
                        ye(this).wrapAll(t ? e.call(this, n) : e)
                    })
                }, unwrap: function (e) {
                    return this.parent(e).not("body").each(function () {
                        ye(this).replaceWith(this.childNodes)
                    }), this
                }
            }), ye.expr.pseudos.hidden = function (e) {
                return !ye.expr.pseudos.visible(e)
            }, ye.expr.pseudos.visible = function (e) {
                return !!(e.offsetWidth || e.offsetHeight || e.getClientRects().length)
            }, ye.ajaxSettings.xhr = function () {
                try {
                    return new n.XMLHttpRequest
                } catch (e) {
                }
            };
            var Ot = {0: 200, 1223: 204}, Ft = ye.ajaxSettings.xhr();
            ve.cors = !!Ft && "withCredentials" in Ft, ve.ajax = Ft = !!Ft, ye.ajaxTransport(function (e) {
                var t, r;
                if (ve.cors || Ft && !e.crossDomain) return {
                    send: function (i, o) {
                        var a, s = e.xhr();
                        if (s.open(e.type, e.url, e.async, e.username, e.password), e.xhrFields) for (a in e.xhrFields) s[a] = e.xhrFields[a];
                        e.mimeType && s.overrideMimeType && s.overrideMimeType(e.mimeType), e.crossDomain || i["X-Requested-With"] || (i["X-Requested-With"] = "XMLHttpRequest");
                        for (a in i) s.setRequestHeader(a, i[a]);
                        t = function (e) {
                            return function () {
                                t && (t = r = s.onload = s.onerror = s.onabort = s.onreadystatechange = null, "abort" === e ? s.abort() : "error" === e ? "number" != typeof s.status ? o(0, "error") : o(s.status, s.statusText) : o(Ot[s.status] || s.status, s.statusText, "text" !== (s.responseType || "text") || "string" != typeof s.responseText ? {binary: s.response} : {text: s.responseText}, s.getAllResponseHeaders()))
                            }
                        }, s.onload = t(), r = s.onerror = t("error"), void 0 !== s.onabort ? s.onabort = r : s.onreadystatechange = function () {
                            4 === s.readyState && n.setTimeout(function () {
                                t && r()
                            })
                        }, t = t("abort");
                        try {
                            s.send(e.hasContent && e.data || null)
                        } catch (e) {
                            if (t) throw e
                        }
                    }, abort: function () {
                        t && t()
                    }
                }
            }), ye.ajaxPrefilter(function (e) {
                e.crossDomain && (e.contents.script = !1)
            }), ye.ajaxSetup({
                accepts: {script: "text/javascript, application/javascript, application/ecmascript, application/x-ecmascript"},
                contents: {script: /\b(?:java|ecma)script\b/},
                converters: {
                    "text script": function (e) {
                        return ye.globalEval(e), e
                    }
                }
            }), ye.ajaxPrefilter("script", function (e) {
                void 0 === e.cache && (e.cache = !1), e.crossDomain && (e.type = "GET")
            }), ye.ajaxTransport("script", function (e) {
                if (e.crossDomain) {
                    var t, n;
                    return {
                        send: function (r, i) {
                            t = ye("<script>").prop({
                                charset: e.scriptCharset,
                                src: e.url
                            }).on("load error", n = function (e) {
                                t.remove(), n = null, e && i("error" === e.type ? 404 : 200, e.type)
                            }), ae.head.appendChild(t[0])
                        }, abort: function () {
                            n && n()
                        }
                    }
                }
            });
            var Pt = [], Rt = /(=)\?(?=&|$)|\?\?/;
            ye.ajaxSetup({
                jsonp: "callback", jsonpCallback: function () {
                    var e = Pt.pop() || ye.expando + "_" + Ct++;
                    return this[e] = !0, e
                }
            }), ye.ajaxPrefilter("json jsonp", function (e, t, r) {
                var i, o, a,
                    s = !1 !== e.jsonp && (Rt.test(e.url) ? "url" : "string" == typeof e.data && 0 === (e.contentType || "").indexOf("application/x-www-form-urlencoded") && Rt.test(e.data) && "data");
                if (s || "jsonp" === e.dataTypes[0]) return i = e.jsonpCallback = ye.isFunction(e.jsonpCallback) ? e.jsonpCallback() : e.jsonpCallback, s ? e[s] = e[s].replace(Rt, "$1" + i) : !1 !== e.jsonp && (e.url += (kt.test(e.url) ? "&" : "?") + e.jsonp + "=" + i), e.converters["script json"] = function () {
                    return a || ye.error(i + " was not called"), a[0]
                }, e.dataTypes[0] = "json", o = n[i], n[i] = function () {
                    a = arguments
                }, r.always(function () {
                    void 0 === o ? ye(n).removeProp(i) : n[i] = o, e[i] && (e.jsonpCallback = t.jsonpCallback, Pt.push(i)), a && ye.isFunction(o) && o(a[0]), a = o = void 0
                }), "script"
            }), ve.createHTMLDocument = function () {
                var e = ae.implementation.createHTMLDocument("").body;
                return e.innerHTML = "<form></form><form></form>", 2 === e.childNodes.length
            }(), ye.parseHTML = function (e, t, n) {
                if ("string" != typeof e) return [];
                "boolean" == typeof t && (n = t, t = !1);
                var r, i, o;
                return t || (ve.createHTMLDocument ? (t = ae.implementation.createHTMLDocument(""), r = t.createElement("base"), r.href = ae.location.href, t.head.appendChild(r)) : t = ae), i = ke.exec(e), o = !n && [], i ? [t.createElement(i[1])] : (i = k([e], t, o), o && o.length && ye(o).remove(), ye.merge([], i.childNodes))
            }, ye.fn.load = function (e, t, n) {
                var r, i, o, a = this, s = e.indexOf(" ");
                return s > -1 && (r = Q(e.slice(s)), e = e.slice(0, s)), ye.isFunction(t) ? (n = t, t = void 0) : t && "object" == typeof t && (i = "POST"), a.length > 0 && ye.ajax({
                    url: e,
                    type: i || "GET",
                    dataType: "html",
                    data: t
                }).done(function (e) {
                    o = arguments, a.html(r ? ye("<div>").append(ye.parseHTML(e)).find(r) : e)
                }).always(n && function (e, t) {
                    a.each(function () {
                        n.apply(this, o || [e.responseText, t, e])
                    })
                }), this
            }, ye.each(["ajaxStart", "ajaxStop", "ajaxComplete", "ajaxError", "ajaxSuccess", "ajaxSend"], function (e, t) {
                ye.fn[t] = function (e) {
                    return this.on(t, e)
                }
            }), ye.expr.pseudos.animated = function (e) {
                return ye.grep(ye.timers, function (t) {
                    return e === t.elem
                }).length
            }, ye.offset = {
                setOffset: function (e, t, n) {
                    var r, i, o, a, s, u, l, c = ye.css(e, "position"), f = ye(e), d = {};
                    "static" === c && (e.style.position = "relative"), s = f.offset(), o = ye.css(e, "top"), u = ye.css(e, "left"), l = ("absolute" === c || "fixed" === c) && (o + u).indexOf("auto") > -1, l ? (r = f.position(), a = r.top, i = r.left) : (a = parseFloat(o) || 0, i = parseFloat(u) || 0), ye.isFunction(t) && (t = t.call(e, n, ye.extend({}, s))), null != t.top && (d.top = t.top - s.top + a), null != t.left && (d.left = t.left - s.left + i), "using" in t ? t.using.call(e, d) : f.css(d)
                }
            }, ye.fn.extend({
                offset: function (e) {
                    if (arguments.length) return void 0 === e ? this : this.each(function (t) {
                        ye.offset.setOffset(this, e, t)
                    });
                    var t, n, r, i, o = this[0];
                    if (o) return o.getClientRects().length ? (r = o.getBoundingClientRect(), t = o.ownerDocument, n = t.documentElement, i = t.defaultView, {
                        top: r.top + i.pageYOffset - n.clientTop,
                        left: r.left + i.pageXOffset - n.clientLeft
                    }) : {top: 0, left: 0}
                }, position: function () {
                    if (this[0]) {
                        var e, t, n = this[0], r = {top: 0, left: 0};
                        return "fixed" === ye.css(n, "position") ? t = n.getBoundingClientRect() : (e = this.offsetParent(), t = this.offset(), u(e[0], "html") || (r = e.offset()), r = {
                            top: r.top + ye.css(e[0], "borderTopWidth", !0),
                            left: r.left + ye.css(e[0], "borderLeftWidth", !0)
                        }), {
                            top: t.top - r.top - ye.css(n, "marginTop", !0),
                            left: t.left - r.left - ye.css(n, "marginLeft", !0)
                        }
                    }
                }, offsetParent: function () {
                    return this.map(function () {
                        for (var e = this.offsetParent; e && "static" === ye.css(e, "position");) e = e.offsetParent;
                        return e || Ye
                    })
                }
            }), ye.each({scrollLeft: "pageXOffset", scrollTop: "pageYOffset"}, function (e, t) {
                var n = "pageYOffset" === t;
                ye.fn[e] = function (r) {
                    return Le(this, function (e, r, i) {
                        var o;
                        if (ye.isWindow(e) ? o = e : 9 === e.nodeType && (o = e.defaultView), void 0 === i) return o ? o[t] : e[r];
                        o ? o.scrollTo(n ? o.pageXOffset : i, n ? i : o.pageYOffset) : e[r] = i
                    }, e, r, arguments.length)
                }
            }), ye.each(["top", "left"], function (e, t) {
                ye.cssHooks[t] = P(ve.pixelPosition, function (e, n) {
                    if (n) return n = F(e, t), ot.test(n) ? ye(e).position()[t] + "px" : n
                })
            }), ye.each({Height: "height", Width: "width"}, function (e, t) {
                ye.each({padding: "inner" + e, content: t, "": "outer" + e}, function (n, r) {
                    ye.fn[r] = function (i, o) {
                        var a = arguments.length && (n || "boolean" != typeof i),
                            s = n || (!0 === i || !0 === o ? "margin" : "border");
                        return Le(this, function (t, n, i) {
                            var o;
                            return ye.isWindow(t) ? 0 === r.indexOf("outer") ? t["inner" + e] : t.document.documentElement["client" + e] : 9 === t.nodeType ? (o = t.documentElement, Math.max(t.body["scroll" + e], o["scroll" + e], t.body["offset" + e], o["offset" + e], o["client" + e])) : void 0 === i ? ye.css(t, n, s) : ye.style(t, n, i, s)
                        }, t, a ? i : void 0, a)
                    }
                })
            }), ye.fn.extend({
                bind: function (e, t, n) {
                    return this.on(e, null, t, n)
                }, unbind: function (e, t) {
                    return this.off(e, null, t)
                }, delegate: function (e, t, n, r) {
                    return this.on(t, e, n, r)
                }, undelegate: function (e, t, n) {
                    return 1 === arguments.length ? this.off(e, "**") : this.off(t, e || "**", n)
                }
            }), ye.holdReady = function (e) {
                e ? ye.readyWait++ : ye.ready(!0)
            }, ye.isArray = Array.isArray, ye.parseJSON = JSON.parse, ye.nodeName = u, r = [], void 0 !== (i = function () {
                return ye
            }.apply(t, r)) && (e.exports = i);
            var It = n.jQuery, Mt = n.$;
            return ye.noConflict = function (e) {
                return n.$ === ye && (n.$ = Mt), e && n.jQuery === ye && (n.jQuery = It), ye
            }, o || (n.jQuery = n.$ = ye), ye
        })
    }
}, [39]);
