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

function add(param) {
    let html = STRUCTURE[param].map((p) => '<div class="field">' +
        '<span>' + p + '</span>' +
        '<input type="text" name="' + p + '" />' +
        '</div>');
    $("." + param).append(html);
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
    console.log(data);

    $.ajax({
        url: '/employee/profile/resumes/create/',
        type: 'post',
        dataType: 'json',
        contentType: 'application/json',
        success: function (response) {
            console.log(response);
        },
        data: JSON.stringify(data),
    });
}