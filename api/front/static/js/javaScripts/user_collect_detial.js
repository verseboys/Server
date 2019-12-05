$('.user-menu').append(function () {
    var str = '';
    str += ' <div class="user-menu-list" data-link="collect">\n' +

        '        </div>'
    return str;
});

$.ajax({
    url: 'collect',
    type: 'post',
    success: function (data) {

    }
    , error: function () {

        $('.user-menu .user-menu-list[data-link="collect"]').append(function () {

            var str = '';
            if (true) {
                str += '            <div>\n' +
                    '                <div class="user-collect-top">\n' +
                    '                    <div class="user-collect-title">我的收藏</div>\n' +
                    '                    <div class="user-collect-tag">\n' +
                    '                        <span>分类</span>\n' +
                    '                        <ul class="row user_tag_change_collect">\n' +
                    '                            <li class="checked" ajax-url="1">全部</li>\n' +
                    '                            <li ajax-url="2">META分析</li>\n' +
                    '                            <li ajax-url="3">不错的分析方法</li>\n' +
                    '                            <li ajax-url="4">这是自定义</li>\n' +
                    '                            <li ajax-url="5">META分析</li>\n' +
                    '                        </ul>\n' +
                    '                    </div>\n' +
                    '                </div>\n' +
                    '                    <ul class="user-collect-list">\n' +
                    '                        <li>\n' +
                    '                            <a href=""><div class="user-collect-list-title">一般线性模型</div></a>\n' +
                    '                            <div class="inline user-collect-list-img"><a href="user_detail.html?u=1"><span class="user"></span></a></div>\n' +
                    '                            <div class="inline user-collect-list-text">\n' +
                    '                                <a href="user_detail.html?u=1"><div class="user-collect-list-name">名字hehe </div></a>\n' +
                    '                                <div class="user-collect-list-artic">一项新的治疗措施是否值得临床推广，除了要求具备足够的疗效外，还应当要求具备一定的安全性。疗效和安全性对于治疗措施的评价是同等重要的，在研究过程中研究者需要综合权衡，然后判断该措施是否可以应用于。</div>\n' +
                    '                                <div class="user-collect-list-tag"><span>2小时前</span><span class="user-comm">评论 4</span><span class="user-fig">20</span><span class="user-coll">取消收藏</span></div>\n' +
                    '                            </div>\n' +
                    '                        </li>\n' +
                    '                        <li>\n' +
                    '                            <a href=""><div class="user-collect-list-title">一般线性模型</div></a>\n' +
                    '                            <div class="inline user-collect-list-img"><a href="user_detail.html?u=1"><span class="user"></span></a></div>\n' +
                    '                            <div class="inline user-collect-list-text">\n' +
                    '                                <a href="user_detail.html?u=1"><div class="user-collect-list-name">名字hehe </div></a>\n' +
                    '                                <div class="user-collect-list-artic">一项新的治疗措施是否值得临床推广，除了要求具备足够的疗效外，还应当要求具备一定的安全性。疗效和安全性对于治疗措施的评价是同等重要的，在研究过程中研究者需要综合权衡，然后判断该措施是否可以应用于。</div>\n' +
                    '                                <div class="user-collect-list-tag"><span>2小时前</span><span class="user-comm">评论 4</span><span class="user-fig">20</span><span class="user-coll">取消收藏</span></div>\n' +
                    '                            </div>\n' +
                    '                        </li>\n' +
                    '                    </ul>\n' +
                    '        </div>'
            } else {
                str += '<div class="no_comment">\n' +
                    '                <div class="no_comment_img"></div>\n' +
                    '                <div class="no_comment_text">目前暂无收藏~</div>\n' +
                    '            </div>'
            }
            return str;
        });
        $('.user-menu .user-menu-list[data-link="collect"]').siblings().addClass('hide')
    }
});
var user_collect_url = 'user'
$(document.body).on('click', '.user_tag_change_collect li', function () {
    $(this).addClass('checked').siblings().removeClass('checked');
    user_collect_url = $(this).attr('ajax-url')
    $.ajax({
        url: user_collect_url,
        type: 'post',
        data: '',
        success: function (data) {

        }
        , error: function () {
            $('.user-menu .user-menu-list[data-link="collect"] .user-collect-list ').html(user_collect_data());
        }
    })
});

/*
* 收藏数据拼接
* */
function user_collect_data(data) {
    var str = '';


    str += '                        <li>\n' +
        '                            <div class="user-collect-list-title">一般线性模型</div>\n' +
        '                            <div class="inline user-collect-list-img"><a href="user_detail.html?u=1"><span class="user"></span></a></div>\n' +
        '                            <div class="inline user-collect-list-text">\n' +
        '                                <a href="user_detail.html?u=1"><div class="user-collect-list-name">名字hehe </div></a>\n' +
        '                                <div class="user-collect-list-artic">一项新的治疗措施是否值得临床推广，除了要求具备足够的疗效外，还应当要求具备一定的安全性。疗效和安全性对于治疗措施的评价是同等重要的，在研究过程中研究者需要综合权衡，然后判断该措施是否可以应用于。</div>\n' +
        '                                <div class="user-collect-list-tag"><span>2小时前</span><span class="user-comm">评论 4</span><span class="user-fig">20</span><span class="user-coll">取消收藏</span></div>\n' +
        '                            </div>\n' +
        '                        </li>\n' +
        '                        <li>\n' +
        '                            <div class="user-collect-list-title">一般线性模型</div>\n' +
        '                            <div class="inline user-collect-list-img"><a href="user_detail.html?u=1"><span class="user"></span></a></div>\n' +
        '                            <div class="inline user-collect-list-text">\n' +
        '                                <a href="user_detail.html?u=1"><div class="user-collect-list-name">名字hehe </div></a>\n' +
        '                                <div class="user-collect-list-artic">一项新的治疗措施是否值得临床推广，除了要求具备足够的疗效外，还应当要求具备一定的安全性。疗效和安全性对于治疗措施的评价是同等重要的，在研究过程中研究者需要综合权衡，然后判断该措施是否可以应用于。</div>\n' +
        '                                <div class="user-collect-list-tag"><span>2小时前</span><span class="user-comm">评论 4</span><span class="user-fig">20</span><span class="user-coll">取消收藏</span></div>\n' +
        '                            </div>\n' +
        '                        </li>'

    return str;
}
