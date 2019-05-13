let timer;
let url;

function update_ranking_list(data) {
    let rank;
    $('#ranking').empty()
    for (var i = 0; i < data.length; i++) {
        rank = data[i];
        $('#ranking').append(`
            <div class="downloaded">
                <i class="material-icons downloaded-${rank.position}">arrow_drop_${rank.position}</i>
                <span>${rank.title}</span>
            </div>
        `)
    }
}

$('#input-url').keyup(function(event) {
    if (timer !== undefined) {
        clearTimeout(timer);
    }

    $('#tracked-video').removeClass('display-flex');
    $('#tracked-video').addClass('display-none');
    url = $('#input-url').val()
    timer = setTimeout(() => {
        $.ajax({
            url: 'http://localhost:5000/api/v1/download',
            type: 'GET',
            dataType: 'json',
            data: { url },
            beforeSend: function() {
                $('#spinner').removeClass('display-none');
            },
            success: function(data) {
                data = JSON.parse(data);
                $('#title').empty().append(data.title);
                $('#thumbnail').attr('src', data.thumbnail);
                $('#download-options').empty();

                let fmt;
                let high = false;
                for (var i = 0; i < data.formats.length; i++) {
                    fmt = data.formats[i];
                    if (fmt.quality === 'medium') {
                        $('#download-options').prepend(`<a href="${fmt.url}" download>Download 360p</a>`);
                    } else if (fmt.quality === 'high' && !high) {
                        $('#download-options').append(`<a href="${fmt.url}" download>Download 720p</a>`);
                        high = true;
                    }

                }

                for (var i = 0; i < data.formats.length; i++) {
                    fmt = data.formats[i];
                    if (fmt.quality === undefined) {
                        $('#download-options').append(`<a href="${fmt.url}" download>Download audio</a>`);
                    }
                }

                $('#tracked-video').removeClass('display-none');
                $('#tracked-video').addClass('display-flex');

                $('#spinner').removeClass('display-block')
                $('#spinner').addClass('display-none')

                update_ranking_list(data.ranking);
            },
            error: function(e) {
                console.log(e)
            }
        })
    }, 1000)
});

$(document).ready(function() {
    $(function() {
        $.get('http://localhost:5000/api/v1/ranking', function(data) {
            data = JSON.parse(data);
            update_ranking_list(data);
        });
    })
});