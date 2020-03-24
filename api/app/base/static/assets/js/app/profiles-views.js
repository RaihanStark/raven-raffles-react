$(document).ready(function () {
    // Data Tables init
    $('#profiles-list').DataTable({
        ajax: '/v1/profiles',
        columns: [{
                'data': 'id'
            },
            {
                'data': 'profilename'
            }, {
                'data': 'cardno'
            }, {
                'data': 'id',
                render: function (data, type, row) {
                    return String.format('<a type="button" class="btn btn-info btn-sm" href="/profiles/{0}">Edit</a> <button type="button" class="btn btn-danger btn-sm delete-profile" data-id="{0}">Delete</button>', data)
                }
            }
        ],
        scrollY: '50vh',
        scrollCollapse: true,
    });



    $('input[type="file"]').change(function (e) {
        var fileName = e.target.files[0].name;
        $('.custom-file-label').text(fileName)
    });


    // Post Settings
    $('form.profilepage').submit(function (e) {
        e.preventDefault()
        // Get Profiles
        if (e['target']['name'] == 'getprofile') {
            let formdata = {
                "profilename": $('input[name=profilename]').val(),
                "firstname": $('input[name=firstname]').val(),
                "lastname": $('input[name=lastname]').val(),
                "email": $('input[name=email]').val(),
                "phonenumber": $('input[name=phonenumber]').val(),
                "address": $('input[name=address]').val(),
                "housenumber": $('input[name=housenumber]').val(),
                "aptsuite": $('input[name=aptsuite]').val(),
                "city": $('input[name=city]').val(),
                "stateprovince": $('input[name=stateprovince]').val(),
                "country": $('input[name=country]').val(),
                "zipcode": $('input[name=zipcode]').val(),
                "cardno": $('input[name=cardno]').val(),
                "expmonth": $('input[name=expmonth]').val(),
                "expyear": $('input[name=expyear]').val(),
                "cvv": $('input[name=cvv]').val()
            };
            for (const data in formdata) {
                if (formdata.hasOwnProperty(data)) {
                    const element = formdata[data];
                    if (element === '') {
                        Swal.fire({
                            position: 'center',
                            icon: 'error',
                            title: 'You must fill all fields!',
                            showConfirmButton: false,
                            timer: 1500
                        })
                        return
                    };
                }
            };
            $.ajax({
                type: "post",
                url: "/v1/profiles",
                data: formdata,
                dataType: 'json',
                success: function (response) {
                    Swal.fire({
                        position: 'center',
                        icon: 'success',
                        title: 'Profiles Added!',
                        showConfirmButton: false,
                        timer: 1500
                    })


                    setTimeout(() => {
                        location.reload();
                    }, 1000);
                }
            });
        }
        if (e['target']['name'] == 'fileinfo') {
            var fd = new FormData($("#fileinfo")[0]);
            // fd.append('file_name', 'lmao')
            console.log(fd)
            $.ajax({
                type: 'POST',
                url: '/v1/import',
                data: fd,
                contentType: false,
                cache: false,
                processData: false,
                success: function (data) {
                    Swal.fire({
                        position: 'center',
                        icon: 'success',
                        title: 'Profiles Imported!',
                        showConfirmButton: false,
                        timer: 1500
                    });
                    setTimeout(function () {
                        window.location.reload(true);
                    }, 1000)

                },
                statusCode: {
                    400: function () {
                        Swal.fire({
                            position: 'center',
                            icon: 'error',
                            title: 'You must input .csv files',
                            showConfirmButton: false,
                            timer: 1500
                        })
                    }
                }
            });
        }
    })
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
    // Delete Button
    $(document).on('click', '.delete-profile', function () {
        var data = {
            'id': $(this).attr('data-id')
        }
        $.ajax({
            type: 'DELETE', // define the type of HTTP verb we want to use (POST for our form)
            url: '/v1/profiles',
            contentType: "application/json",
            data: JSON.stringify(data)
            // the url where we want to POST
        });
        // log data to the console so we can see
        Toast.fire({
            icon: 'success',
            title: "Delete Profiles Successful (" + $(this).attr('data-id') + ")"
        });

        setTimeout(() => {
            location.reload();
        }, 1000);

        event.preventDefault();
    });
    // Delete Function

});