Object.defineProperty(Array.prototype, 'chunk', {
    value: function (size) {
        let sets = [], chunks, i = 0;
        chunks = this.length / size;

        while (i < chunks) {
            sets[i] = this.splice(0, size);
            i++;
        }

        return sets;
    },
    writable: true,
    configurable: true,
    enumerable: false
});


const STRUCTURE = {
    'experience': ['company', 'period', 'position', 'duties'],
    'education': ['educational_institution', 'specialization', 'year_of_ending'],
    'courses': ['company', 'specialization', 'year_of_ending'],
};

function add(param, pk) {
    let html = STRUCTURE[param].map((p) => '<p class="field">' +
        '<span class="text fw-bold">' + p[0].toUpperCase() + p.substring(1) + ': ' + '</span>' +
        '<input type="text" name="' + p + '" />' +
        '</p>');
    if (pk) {
        html.push('<input type="hidden" name="pk" value="0" />');
    }
    let card_html = '<div class="card-body border m-3 w-25">' + html.join(' ') +
        '<button class="btn btn-danger" type="button" onclick="remove(this)">X</button>' +
        '</div>'
    $("." + param).append(card_html);
}

function remove(el) {
    $(el).parent().remove();
}

function save() {
    const fields = Object.fromEntries(Object.keys(STRUCTURE).map((key) => [
        key,
        $('#resume .' + key + ' input').map((i, e) => [
            [
                $(e).attr('name'),
                $(e).val(),
            ],
        ]).get().chunk(STRUCTURE[key].length).map((e) => Object.fromEntries(e)),
    ]));

    const data = {
        title: $('#id_title').val(),
        status: $('#id_status').val(),
        fields,
    };

    $.ajax({
        url: '/employee/profile/resumes/create/',
        type: 'post',
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify(data),
    });
}

function update() {
    const fields = Object.fromEntries(Object.keys(STRUCTURE).map((key) => [
        key,
        $('.' + key + ' input').map((i, e) => [
            [
                $(e).attr('name'),
                $(e).val(),
            ],
        ]).get().chunk(STRUCTURE[key].length + 1).map((e) => Object.fromEntries(e)),
    ]));

    const data = {
        pk: window.location.href.match(/\/(\d+)\/$/)?.[1],
        title: $('#id_title').val(),
        status: $('#id_status').val(),
        fields,
    };

    $.ajax({
        url: '/employee/profile/resumes/edit/' + data.pk + '/',
        type: 'post',
        dataType: 'json',
        contentType: 'application/json',
        success: function () {
            window.location.reload();
        },
        data: JSON.stringify(data),
    });
}

function delete_instance(el) {
    const data = {
        model: $(el).parent().parent().attr('class').match(/(\w+)$/)?.[1],
        pk: $(el).parent().children('input[name="pk"]').val(),
    };
    console.log(data)

    $.ajax({
        url: '/employee/profile/resume/entity_delete/',
        type: 'post',
        dataType: 'json',
        contentType: 'application/json',
        success: function () {
            window.location.reload();
        },
        data: JSON.stringify(data),
    });
}