$(function() {

    $(".js-create-department").click(function() {
        $.ajax({
            url: '/departments/create/',
            type: 'get',
            dataType: 'json',
            beforeSend: function() {
                $("#modal-book").modal("show");
            },
            success: function(data) {
                $("#modal-book .modal-content").html(data.html_form);
            }
        });
    });

    $("#modal-book").on("submit", ".js-department-create-form", function() {
        var form = $(this);
        $.ajax({
            url: form.attr("action"),
            data: form.serialize(),
            type: form.attr("method"),
            dataType: 'json',
            success: function(data) {
                if (data.form_is_valid) {
                    $("#dept-list").html(data.html_dept_list);
                    $("#modal-book").modal("hide");
                } else {
                    $("#modal-book .modal-content").html(data.html_form);
                }
            }
        });
        return false;
    });
    $(".js-create-area").click(function() {
        $.ajax({
            url: '/kpis/create/',
            type: 'get',
            dataType: 'json',
            beforeSend: function() {
                $("#modal-book").modal("show");
            },
            success: function(data) {
                $("#modal-book .modal-content").html(data.html_form);
            }
        });
    });

    $("#modal-book").on("submit", ".js-area-create-form", function() {
        var form = $(this);
        $.ajax({
            url: form.attr("action"),
            data: form.serialize(),
            type: form.attr("method"),
            dataType: 'json',
            success: function(data) {
                if (data.form_is_valid) {
                    $("#area-list").html(data.html_area_list);
                    $("#modal-book").modal("hide");
                } else {
                    $("#modal-book .modal-content").html(data.html_form);
                }
            }
        });
        return false;
    });

});