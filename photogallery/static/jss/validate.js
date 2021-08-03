$(function () {
        $('#filevalidation').bootstrapValidator({
            message: 'This value is not valid',
            fields: {
                images: {
                    validators: {
                        file: {
                            extension: 'jpg,png,jpeg',
                            maxSize: 5 * 1024 * 1024, // 5 MB
                            alert: 'Please upload a .jpg, .jpeg or .png file - max. size 5MB'
                        },
                        notEmpty: {
                            alert: 'Please select Image File'
                        }
                    }
                },
            }
        });

    });