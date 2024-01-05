function togglePassword(id_pass, id_show) {
    var passwordField = document.getElementById(id_pass);
    var checkbox = document.getElementById(id_show);
    // Kiểm tra xem passwordField và checkbox có tồn tại hay không trước khi sử dụng
    if (passwordField && checkbox) {
        if (checkbox.checked) {
            passwordField.type = "text";
        } else {
            passwordField.type = "password";
        }
    } else {
        console.error("Không tìm thấy phần tử passwordField hoặc checkbox.");
    }
}


$(document).ready(function() {
    // Lấy chiều cao của footer
    var footerHeight = $('.footer').outerHeight();

    // Ẩn footer khi trang tải lên
    $('.footer').css('bottom', -footerHeight);

    // Xác định hành vi cuộn trang
    $(window).scroll(function() {
        var scrollPos = $(document).scrollTop();
        var windowHeight = $(window).height();

        // Hiển thị hoặc ẩn footer dựa trên vị trí cuộn trang
        if (scrollPos + windowHeight >= $(document).height() - footerHeight) {
            $('.footer').css('bottom', 0);
        } else {
            $('.footer').css('bottom', -footerHeight);
        }
    });
});

$(document).ready(function() {
    // Bắt sự kiện khi nút được bấm
    $("#loginButton").click(function() {
        // Lấy giá trị từ một trường input (hoặc bất kỳ phần tử nào khác)
        var username = $("#username").val();
        var password = $("#password").val();
        var csrftoken = $('[name="csrfmiddlewaretoken"]').val();
        // Gửi yêu cầu Ajax đến server
        $.ajax({
            type: "POST", // Hoặc "GET" tùy thuộc vào yêu cầu của bạn
            url: "/login/", // Đường dẫn đến endpoint Django của bạn
            data: {
                username: username,
                password: password,
                csrfmiddlewaretoken: csrftoken
            }, // Dữ liệu bạn muốn gửi
            success: function(response) {
                success = response['success']
                errorMessages = document.getElementsByClassName('error-message')
                if (success) {
                    return window.location.href = '/home/'
                } else {
                    if (errorMessages.length > 0) {
                        for (var i = 0; i < errorMessages.length; i++) {
                            errorMessages[i].style.display = 'block';
                        }
                    }
                }
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});

$(document).ready(function () {
    $(".category-link").click(function (event) {
        event.preventDefault();  // Prevent the default link behavior
        var selectedCategory = $(this).data("category");
        window.location.href = '/findmovie/?genreID=' + selectedCategory;
    });
});