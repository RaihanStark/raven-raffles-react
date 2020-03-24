const Toast = Swal.mixin({
    toast: true,
    position: 'top-end',
    showConfirmButton: false,
    timer: 3000,
    timerProgressBar: true,
    onOpen: (toast) => {
        toast.addEventListener('mouseenter', Swal.stopTimer)
        toast.addEventListener('mouseleave', Swal.resumeTimer)
    }
})
$(document).ready(function () {

    $('button.delete-task').on('click', function () {
        var data = {
            'id': $(this).attr('data-id')
        }
        console.log(data)
        $.ajax({
            type: 'DELETE', // define the type of HTTP verb we want to use (POST for our form)
            url: '/v1/tasks',
            contentType: "application/json",
            data: JSON.stringify(data)
            // the url where we want to POST
        });
        // log data to the console so we can see
        Toast.fire({
            icon: 'success',
            title: "Delete Task Successful (" + $(this).attr('data-id') + ")"
        });

        setTimeout(() => {
            location.reload();
        }, 1000);

        event.preventDefault();
        // here we will handle errors and validation messages
    });

    $('a#start-tasks').on('click', function () {

        $('#start-tasks').addClass('disabled');

        let tasks = $(".delete-task").map(function () {
            return this.getAttribute('data-id');
        }).get();

        console.log(tasks)
        let numberIterate = 0;
        tasks.forEach(id => {
            if (numberIterate < 1) {
                $('#statustasks-' + id).text('Status: Running...')
            } else {
                $('#statustasks-' + id).removeClass('badge-primary')
                $('#statustasks-' + id).addClass('badge-info')
                $('#statustasks-' + id).text('Status: Queued...')

            }
            numberIterate += 1;
        });

        $.ajax({
            type: "GET",
            url: "/tasks/start",
            beforeSend: function () {
                Toast.fire({
                    icon: 'success',
                    title: "Task Started"
                });

                // setTimeout(() => {
                //     window.location.replace("/index");
                // }, 1000);

            },
            success: function (response) {
                console.log(response)
            }
        });

        tasks.forEach(id => {
            console.log('Iterate to id: ' + id)
            if ($('#statustasks-' + id).text() == "Status: Queued...") {
                console.log('queue')
                setTimeout(() => {
                    $('#statustasks-' + id).removeClass('badge-primary')
                    $('#statustasks-' + id).addClass('badge-info')
                    $('#statustasks-' + id).text('Status: Running...')
                }, Math.floor(Math.random() * 15000) + 7000);
            }
            setTimeout(() => {
                $('#statustasks-' + id).removeClass('badge-info')
                $('#statustasks-' + id).addClass('badge-success')
                $('#statustasks-' + id).text('Status: Finished...')
            }, Math.floor(Math.random() * 15000) + 7000);


        });

        Toast.fire({
            icon: 'success',
            title: "Task Finished"
        });

    })
});