let page = 1;
let load = () => $.get('/?page=' + ++page, (data) => {
    const html = $.parseHTML(data);
    if (!$('.more', html).length) {
        $('.more').hide()
    }
    $('.infinite-container').append($('.infinite-container', html).html());
});
