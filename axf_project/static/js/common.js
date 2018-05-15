csrf = $('input[name="csrfmiddlewaretoken"]').val();

// 添加商品函数
function add_shop(goods_id) {
    $.ajax({
        url:'/axf/addgoods/',
        type: 'POST',
        data: {'goods_id': goods_id},
        dataType: 'json',
        headers: {'X-CSRFToken': csrf},
        success: function (msg) {
            $('#num_' + goods_id).html(msg.c_num);
            $('#all_prices').html('总价：' + msg.money);
            $('#flag_' + goods_id).html('√');
            if (msg.choose_all_status){
               $('#choose_all').html('√')
           }

        },
        error:function (msg) {
            alert('请求错误')
        }

    });
}


// 减少商品函数
function sub_shop(goods_id) {
    $.ajax({
        url: '/axf/subgoods/',
        type: 'POST',
        data: {'goods_id': goods_id},
        dataType: 'json',
        headers: {'X-CSRFToken': csrf},
        success: function (msg) {
           $('#num_' + goods_id).html(msg.c_num);
           $('#all_prices').html('总计：' + msg.money);
           if(msg.c_num > 0){
               $('#flag_' + goods_id).html('√');
           }else {
               $('#flag_' + goods_id).html('');
           }
           if (msg.choose_all_status){
               $('#choose_all').html('√')
           }
        },
        error: function (msg) {
            alert('请求错误')
        }

    })
}


// 购物时物品选取函数
function change_cart_select(cart_id) {
    $.ajax({
        url:'/axf/change_cart_select/',
        type: 'POST',
        data: {'cart_id': cart_id},
        dataType: 'json',
        headers: {'X-CSRFToken': csrf},
        success:function (msg) {

            var select = $('#flag_' + cart_id);
            if(msg['cart_id'])
            {
                select.html('√');
                if(msg.change)
                {
                $('#choose_all').html('√');
                }
            }else {
                select.html('');
                $('#choose_all').html('');
            }
            $('#all_prices').html('总计：' + msg.money);
        },
        error: function (msg) {
            alert('请求失败')
        }
    })
}


// 购物车物品全选函数
function choose_all() {
    var status = $('#choose_all').html();
    console.log(status);
    $.ajax({
        url: '/axf/choose_all/',
        type: 'POST',
        data: {'status': status},
        dataType: 'json',
        headers: {'X-CSRFToken': csrf},
        success: function (msg) {
            if(msg.status)
            {
                $('#choose_all').html('√');
            } else
            {
                $('#choose_all').html('');
            }
            for(var i = 0; i < msg.flags.length; i++){
                if(msg.status){
                    $('#flag_' + msg.flags[i]).html('√');
                }else {
                    $('#flag_' + msg.flags[i]).html('');
                }
            }

            $('#all_prices').html('总计：' + msg.money);
        },
        error: function (msg) {

        }
    })
}

$(function () {
        $.ajax({
        url: '/axf/money/',
        type: 'GET',
        dataType: 'json',
        headers: {'X-CSRFToken': csrf},
        success:function (msg)
        {
           $('#all_prices').html('总计：' + msg.money);
            if(!msg.status){
               $('#choose_all').html('');
            }else {
               $('#choose_all').html('√');
            }
        },
        error: function (msg) {}
    })

});

//处理支付函数
function pay_money(order_id) {
    alert('付款成功');
    window.location = '/axf/pay_money/?order_id=' + order_id;
}

