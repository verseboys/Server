$(document).ready(function () {
    window.nav_type = false;
    window.head_top_type = true;
    window.SCROLL_OLD_SIZE = window.scrollY;
    window.SCROLL_TOP_SIZE = $('#header').height() - 10 + 'px';
    var SCROLL_OLD_SIZE = document.body.scrollTop;
    $(window).on('scroll', function (e) {
        if (nav_type !== true) {
            if (head_top_type) {
                if (window.scrollY > SCROLL_OLD_SIZE && window.scrollY > 0) {
                    $('#header-pc2').css('top', '-' + SCROLL_TOP_SIZE)
                } else if ((window.scrollY < SCROLL_OLD_SIZE) || window.scrollY <= 0) {
                    $('#header-pc2').css('top', '0px');
                }
            }
        }
        SCROLL_OLD_SIZE = window.scrollY;
//             fix_foot()
    })

    $.ajax({
        url: '/hold_news/1/',
        success: function (data) {
            if (data.code == 200) {
                var list = data.data.hold_news, str = '';
                for (var i = 0; i < list.length; i++) {
                    str += '<li>' +
                        '<a href="/news_detail/' + list[i].id + '/1/" title="' + list[i].title + '" target="_blank">' +
                        '<h4>' + list[i].title + '</h4>' +
                        '<div>' + list[i].create_time + '</div>' +
                        '</a>' +
                        '</li>'
                }
                $('.body-right .hot-list ul').html(str);
            }
        }
    })

    $.ajax({
        url: '/hold_news/2/',
        async: false,
        success: function (data) {
            if (data.code == 200) {
                var list = data.data.hold_news, str = '';
                for (var i = 0; i < list.length; i++) {
                    str += '<li >' +
                        '<div class="banner-img"><a href="/news_detail/' + list[i].id + '/1/" title="' + list[i].title + '" target="_blank"><div class="bg-img"style="background-image: url(/images/article_images/' + list[i].thumbnail + ')"></div></a></div> ' +
                        '<div class="banner-text"> ' +
                        '<a href="/news_detail/' + list[i].id + '/1/" title="' + list[i].title + '" target="_blank"> ' +
                        '<h2>' + list[i].title + '</h2> ' +
                        '</a> ' +
                        '<p>' + list[i].summary + '</p>' +
                        //'<div class="banner-data">' + list[i].create_time + '</div> ' +
                        '</div> ' +
                        '</li>'
                }
                $('.banner ul').html(str);
                $('.banner li').eq(0).addClass("active");


            }
        }
    })
    var banner = {
        option: {
            max_step: $('.banner li').length,
            index: $('.banner li.active').index(),
            step: $('.banner li.active').index(),
            move_type: true
        },
        eventBind: function () {
            var that = this
            $('.banner .banner-item').html(function () {
                var str = ''
                for (var i = 0; i < that.option.max_step; i++) {
                    if (i === that.option.index) {
                        str += '<span class="active"></span>'
                    } else {
                        str += '<span></span>'
                    }
                }
                return str
            })
            $('.banner-item span').click(function () {
                if (!$(this).hasClass('active')) {
                    window.clearInterval(timer)
                    that.option.step = $(this).index();
                    $(this).addClass('active').siblings().removeClass('active');
                    $('.banner li').eq(that.option.step).addClass('active').siblings().removeClass('active')
                    // that.loop()
                }
            })
            $('.banner').hover(function () {
                // that.option.move_type = false;
                window.clearInterval(timer)
            }, function () {
                that.loop()
                // that.option.move_type = true
            })
            this.loop();
        },
        loop: function () {
            var self = $('.banner');
            var that = this
            window.timer = setInterval(function () {
                if (that.option.move_type) {
                    that.run()
                }
            }, 5000)
        }
        , run: function () {
            this.option.step++
            if (this.option.step >= this.option.max_step) {
                this.option.step = 0
            }
            $('.banner-item span').eq(this.option.step).addClass('active').siblings().removeClass('active');
            $('.banner li').eq(this.option.step).addClass('active').siblings().removeClass('active')
        }
    }
    banner.eventBind()
    // $(document).on('click','#login',function () {
    //     //check_type(1)
    //     window.location.href = '/login/#1'
    // })
    // $(document).on('click','#register',function () {
    //     //check_type(2)
    //     window.location.href = '/register/'
    // })
})