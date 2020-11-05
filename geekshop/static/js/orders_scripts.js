window.onload = function () {

    var _quantity, _price, orderitem_num, delta_quantity, orderitem_quantity, delta_cost;
    var quantity_arr = [];
    var price_arr = [];

    var TOTAL_FORMS = parseInt($('input[name="orderitems-TOTAL_FORMS"]').val());
    var order_total_quantity = parseInt($('.order_total_quantity').text()) || 0;
    var order_total_cost = parseFloat($('.order_total_cost').text().replace(',','.')) || 0;

    console.log(TOTAL_FORMS, order_total_quantity, order_total_cost);

    for ( var i=0; i < TOTAL_FORMS; i++) {
        _quantity = parseInt($('input[name="orderitems-' + i + '-quantity"]').val());
        _price = parseFloat($('.orderitems-' + i + '-price').text().replace(',', '.'));

        quantity_arr[i] = _quantity;
        if(_price) {
            price_arr[i] = _price;
        } else {
            price_arr[i] = 0;
        }
    }
    console.log(price_arr, quantity_arr);

    if(!order_total_quantity) {
        for (var i=0; i<TOTAL_FORMS; i++){
            order_total_quantity += quantity_arr[i];
            order_total_cost += price_arr[i] * quantity_arr[i];
        }
        $('.order_total_quantity').html(order_total_quantity.toString());
        $('.order_total_cost').html(Number(order_total_cost.toFixed(2)).toString());
        console.log(order_total_quantity, order_total_cost);
    }

    $('.order_form').on('click', 'input[type="number"]', function () {
   var target = event.target;
   orderitem_num = parseInt(target.name.replace('orderitems-', '').replace('-quantity', ''));
   if (price_arr[orderitem_num]) {
       orderitem_quantity = parseInt(target.value);
       delta_quantity = orderitem_quantity - quantity_arr[orderitem_num];
       quantity_arr[orderitem_num] = orderitem_quantity;
       orderSummaryUpdate(price_arr[orderitem_num], delta_quantity);
    }
    });

    $('.order_form').on('click', 'input[type="checkbox"]', function () {
       var target = event.target;
       orderitem_num = parseInt(target.name.replace('orderitems-', '').replace('-DELETE', ''));
       if (target.checked) {
           delta_quantity = -quantity_arr[orderitem_num];
       } else {
           delta_quantity = quantity_arr[orderitem_num];
       }
       orderSummaryUpdate(price_arr[orderitem_num], delta_quantity);
    });

    function orderSummaryUpdate(orderitem_price, delta_quantity) {
       delta_cost = orderitem_price * delta_quantity;

       order_total_cost = Number((order_total_cost + delta_cost).toFixed(2));
       order_total_quantity = order_total_quantity + Number(delta_quantity);

       $('.order_total_cost').html(order_total_cost.toString());
       $('.order_total_quantity').html(order_total_quantity.toString());
    }

$("select").change(function(){

        var target_href = event.target;
        console.log('target_href ->', target_href);
        var selectedIndex = target_href.selectedIndex;
        var product_name = target_href[selectedIndex].innerText.split('(')[0].trim();
        var children = target_href.parentNode.parentNode.children[2];
        var num_class = target_href.id.split('-')[1]

        var quantity = document.getElementById('id_orderitems-'+ num_class +'-quantity')
        console.log('name ->','orderitems-'+ num_class +'-quantity');
        console.log('quantity.value - >',quantity.value);
        /*
        if (quantity.value == 0){
            quantity.value = 1;
            order_total_quantity + =1;
            $('.order_total_cost').html(order_total_cost.toString());
        }
        */
        /*
        console.log('вобран товар - >', product_name);
        console.log('цена в объекте класса - >', children);
        console.log('номер класса - >', num_class);
        */
        console.log('номер товара в списке - >', selectedIndex);

        console.log('вобран товар - >', product_name);
        if (target_href) {
            $.ajax({
                url: "/order/price/" + num_class + "/" + selectedIndex +"/",

                success: function (data) {
                    if (children.childElementCount > 0) { //если делаем перевыбор товара в существующей строчке

                        price_old = parseFloat($('.orderitems-' + num_class + '-price').text().replace(',', '.'));
                        console.log('price_old - >', price_old);
                        order_total_quantity = order_total_quantity - quantity.value;
                        order_total_cost = order_total_cost - quantity.value * price_old;
                        quantity.value = 0;
                        quantity_arr[num_class] = 0;

                        while (children.firstChild) {
                            children.removeChild(children.firstChild);
                        };
                    }
                    children.insertAdjacentHTML('afterBegin',data.result);
                    /*children.insertAdjacentHTML('afterBegin',data.result);
                    children.InnerText = data.result;*/
                    console.log('ajax done');
                    TOTAL_FORMS +=1;
                    price_arr[num_class] = 0;
                    price_arr[num_class] = parseFloat($('.orderitems-' + num_class + '-price').text().replace(',', '.'));

                    orderSummaryUpdate(price_arr[num_class], quantity.value);
                },
            });

        }
        event.preventDefault();
});



$('.formset_row').formset({
   addText: 'добавить продукт',
   deleteText: 'удалить',
   prefix: 'orderitems',
   removed: deleteOrderItem
});


    function deleteOrderItem(row) {
       var target_name= row[0].querySelector('input[type="number"]').name;
       orderitem_num = parseInt(target_name.replace('orderitems-', '').replace('-quantity', ''));
       delta_quantity = -quantity_arr[orderitem_num];
       orderSummaryUpdate(price_arr[orderitem_num], delta_quantity);
    };


}