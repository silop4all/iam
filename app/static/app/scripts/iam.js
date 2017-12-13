/**
 * Module:      JS lib
 * Dependency:  jQuery
 * Company:     Singular Logic S.A.
 * Author:      Panagiotis Athanasoulis
 * Email:       pathanasoulis@ep.singularlogic.eu
 * License:     Apache 2.0
 */

var IAM = IAM || (function () {
    var currentForm = null;
    var currentValidator = null;

    var errorClass = "iam-invalid-field";
    var eSettings = {
        validatorClass: "iam-invalid-field",
        highlightClass: 'has-error',
        color: "#bd3232"
    }

    var modalActionsPost = function modalActionsPost(title, content, cancel, confirm, f_cancel, f_success) {
        bootbox.dialog({
            title: title,
            message: content,
            buttons: {
                main: {
                    label: confirm,
                    className: "btn btn-primary btn-custom-submit",
                    callback: f_success
                },
                danger: {
                    label: cancel,
                    className: "btn btn-warning btn-custom-cancel",
                    callback: f_cancel
                }
            },
            closeButton: true,
            onEscape: function () {
                window.close();
            },
            keyboard: true,
        });
    }

    // extend the validation rules
    $.validator.addMethod("username", function (value, element) {
        return this.optional(element) || /^[a-z0-9]+$/i.test(value);
    });

    $.validator.addMethod("notEqualTo", function (value, element, param) {
        return this.optional(element) || (value !== $(param).val() );
    });
    
    $.validator.addMethod("vat", function (value, element) {
        return this.optional(element) || /^[a-zA-Z0-9]+$/i.test(value);
    });

    $.validator.addMethod("password", function (value, element) {
        return this.optional(element) || /^[a-zA-Z0-9@#_&$]+$/i.test(value);
    });

    $.validator.addMethod("question", function (value, element) {
        var q = $("span#literal").text().split("+");
        var sum = parseInt(q[0]) + parseInt(q[1]);
        return this.optional(element) || (parseInt(value) === parseInt(sum));
    });

    // element actions
    $.fn.serializeObject = function () {
        var o = {};
        var a = this.serializeArray();
        $.each(a, function () {
            if (this.value !== "") {
                if (o[this.name] !== undefined) {
                    if (!o[this.name].push) {
                        o[this.name] = [o[this.name]];
                    }
                    o[this.name].push(this.value || '');
                } else {
                    o[this.name] = this.value || '';
                }
            }
        });
        return o;
    };

    $.fn.serializeObjectAll = function () {
        var o = {};
        var a = this.serializeArray();
        $.each(a, function () {
            if (o[this.name] !== undefined) {
                if (!o[this.name].push) {
                    o[this.name] = [o[this.name]];
                }
                o[this.name].push(this.value || '');
            } else {
                o[this.name] = this.value || '';
            }
        });
        return o;
    };

    $.fn.serializeList = function () {
        var o = [];
        var a = this.serializeArray();
        $.each(a, function () {
            if (!isNaN(this.name)) {
                o.push(parseInt(this.name));
            }
        })
        return o;
    };

    $.fn.handleRoles = function () {
        if (this.find('input').is(':checked')) {
            this.find('input').val(true);
            this.addClass('active').css('border', '1px solid white !important');
        }
        else {
            this.find('input').val(false);
            this.removeClass('active').css('border', '1px solid #dddddd');
        }
    }
    
    $.fn.sweetAlertText = function () {
        this.css('line-height', 'inherit');
        this.css('text-align', 'justify');
    }


    $("#view-password").click(function () {
        if ($(this).is(":checked")) {
            $("#userpassword").attr("type", "text");
        }
        else {
            $("#userpassword").attr("type", "password");
        }
    });
    $("#view-old-password").click(function () {
        if ($(this).is(":checked")) {
            $("#currentpassword").attr("type", "text");
        }
        else {
            $("#currentpassword").attr("type", "password");
        }
    });
    $("#username").focus(function () {
        var fname = $("#name").val();
        var lname = $("#surname").val();
        if (fname && lname && !this.value) {
            var usr = fname[0] + lname.substring(0, (lname.length > 8) ? 8 : lname.length);
            this.value = usr.toLowerCase();
        }
    });

    $("#registry-reset").click(function () {
        //regValidator.resetForm();
        currentValidator.resetForm();
        $("." + errorClass ).parent().removeClass("has-error");
        $("span." +errorClass).remove();
    });
    $("#register-app-reset").click(function () {
        //regValidator.resetForm();
        currentValidator.resetForm();
        $("." + errorClass).parent().removeClass("has-error");
        $("span." + errorClass).remove();
    });
    $("#form-reset").click(function () {
        //regValidator.resetForm();
        currentValidator.resetForm();
        $("." + errorClass).parent().removeClass("has-error");
        $("span." + errorClass).remove();
    });


    return {
        login: function (successURL) {
            currentForm = '#loginForm';
            // handle events
            $(document).on('submit', currentForm, function (event) {
                event.preventDefault();
            });
            // validation
            loginValidator = $(currentForm).validate({
                errorClass: eSettings.validatorClass,
                errorElement: "span",
                rules: {
                    username: {
                        required: true,
                        minlength: 4,
                        username: true,
                    },
                    password: {
                        required: true,
                        minlength: 8,
                        password: true
                    }
                },
                messages: {
                    username: {
                        required: "Please enter your username",
                        username: "Please enter only lower characters a-z, digits 0-9 without spaces"
                    },
                    password: {
                        required: "Please enter your password",
                        password: "Please include characters, digits and the special characters @#_&$ without spaces"
                    }
                },
                errorPlacement: function (error, element) {
                    error.insertAfter(element);
                    error.css("color", eSettings.color);
                    element.parent().addClass(eSettings.highlightClass);
                },
                success: function (error) {
                    error.parent().removeClass(eSettings.highlightClass);
                    error.removeClass(errorClass);
                    error.parent().find($("span")).remove();
                },
                submitHandler: function (form) {
                    var payload = $(form).serializeObject();
                    
                    $.ajax({
                        url: $(form).attr('action'),
                        type: "POST",
                        dataType: "json",
                        headers: { "Content-Type": 'application/json' },
                        data: JSON.stringify(payload),
                        success: function (response) {
                            location.href = successURL;
                        },
                        error: function (response, status, errorThrown) {
                            var msg = '<label><span class="glyphicon glyphicon-remove-circle"></span> Invalid credentials. Try again</label>';
                            $("#invalid-credentials").css("color", "white").css("background", eSettings.color).css('border-radius', '4px 4px');
                            $("#invalid-credentials").html(msg);
                        }
                    });
                }
            });
        },
        authorize: function (clientId, redirectUri) {
            currentForm = '#authForm';
            // handle events
            $(document).on('submit', currentForm, function (event) {
                event.preventDefault();
            });
            // validation
            authValidator = $(currentForm).validate({
                errorClass: eSettings.validatorClass,
                errorElement: "span",
                rules: {
                    username: {
                        required: true,
                        minlength: 4,
                        username: true,
                    },
                    password: {
                        required: true,
                        minlength: 8,
                        password: true
                    }
                },
                messages: {
                    username: {
                        required: "Please enter your username",
                        username: "Please enter only lower characters a-z, digits 0-9 without spaces"
                    },
                    password: {
                        required: "Please enter your password",
                        password: "Please include characters, digits and the special characters @#_&$ without spaces"
                    }
                },
                errorPlacement: function (error, element) {
                    error.insertAfter(element);
                    error.css("color", eSettings.color);
                    element.parent().addClass(eSettings.highlightClass);
                },
                success: function (error) {
                    error.parent().removeClass(eSettings.highlightClass);
                    error.removeClass(errorClass);
                    error.parent().find($("span")).remove();
                },
                submitHandler: function (form) {
                    var payload = $(form).serializeObject();
                    payload['client_id'] = clientId;
                    payload['redirect_uri'] = redirectUri;

                    $.ajax({
                        url: $(form).attr('action'),
                        type: $(form).attr("method"),
                        dataType: "json",
                        headers: { "Content-Type": 'application/json' },
                        data: JSON.stringify(payload),
                        success: function (response) {
                            //console.log(response);
                            location.href = response.link;
                        },
                        error: function (response, status, errorThrown) {
                            var msg = '<label><span class="glyphicon glyphicon-remove-circle"></span> Invalid credentials. Try again</label>';
                            $("#invalid-credentials").css("color", "white").css("background", eSettings.color).css('border-radius', '4px 4px');
                            $("#invalid-credentials").html(msg);
                        }
                    });
                }
            });
        },
        preRegister: function (successURL, checkURL) {
            currentForm = '#preRegistrationForm';
            // handle events
            $(document).on('submit', currentForm, function (event) {
                event.preventDefault();
            });
            // validation
            preRegValidator = $(currentForm).validate({
                errorClass: errorClass,
                errorElement: "span",
                rules: {
                    mail: {
                        required: true,
                        email: true,
                        remote: {
                            url: checkURL,
                            type: "GET",
                            data: {
                                mail: function () {
                                    return $("#mail").val();
                                }
                            }
                        }
                    }
                },
                messages: {
                    mail: {
                        required: "Please enter your email address",
                        remote: "The email is already taken.",
                        email: "Your email address must be in the format of name@domain.org"
                    },
                },
                errorPlacement: function (error, element) {
                    error.insertAfter(element);
                    error.css("color", eSettings.color);
                    element.parent().addClass(eSettings.highlightClass);
                },
                success: function (error) {
                    error.parent().removeClass(eSettings.highlightClass);
                    error.removeClass(errorClass);
                    error.parent().find($("span")).remove();
                },
                submitHandler: function (form) {
                    var payload = $(form).serializeObject();
                    $.ajax({
                        url: $(form).attr('action'),
                        type: "POST",
                        dataType: "json",
                        contentType: 'application/json',
                        data: JSON.stringify(payload),
                        success: function (response) {
                            // inform user with what he must do
                            swal({
                                title: "Registration request",
                                text: "The registration request has been sent successfully. Please, check your inbox and follow the instructions.",
                                type: "success",
                                confirmButtonText: "Back to login",
                                confirmButtonColor: "#3a87ad",
                                animation: "slide-from-top",
                            },
                            function (isConfirm) {
                                if (isConfirm) {
                                    // Redirect the user
                                    //location.href = successURL;
                                    window.location.href = successURL;
                                }     
                            });                         
                        },
                        error: function (jqXHR, textStatus, errorThrown) {
                            var message = JSON.parse(jqXHR.responseText).message;
                            swal({
                                title: "Registration request",
                                text: "The registration request has failed. " + message,
                                type: "error",
                                confirmButtonText: "Try again",
                                confirmButtonColor: "#3a87ad",
                                animation: "slide-from-top",   
                            });  
                        }
                    });
                }
            });
        },
        register: function (successURL, checkURL) {
            currentForm = '#registrationForm';
            // handle events
            $(document).on('submit', currentForm, function (event) {
                event.preventDefault();
            });
            // validation
            regValidator = $(currentForm).validate({
                errorClass: errorClass,
                errorElement: "div",
                rules: {
                    name: {
                        required: true,
                        minlength: 2
                    },
                    surname: {
                        required: true,
                        minlength: 2
                    },
                    username: {
                        required: true,
                        minlength: 4,
                        username: true,
                        remote: {
                            url: checkURL,
                            type: "GET",
                            data: {
                                username: function () {
                                    return $("#username").val();
                                }
                            }
                        }
                    },
                    mail: {
                        required: true,
                        email: true,
                        remote: {
                            url: checkURL,
                            type: "GET",
                            data: {
                                mail: function () {
                                    return $("#mail").val();
                                }
                            }
                        }
                    },
                    userpassword: {
                        required: true,
                        minlength: 8,
                        password: true
                    },
                    password_confirm: {
                        required: true,
                        minlength: 8,
                        equalTo: "#userpassword",
                        password: true
                    },
                    skills: {
                        required: true
                    },
                    phone: {
                        required: true,
                        minlength: 10,
                        maxlength: 15,
                        digits: true
                    },
                    gender: {
                        required: true
                    },
                    vat: {
                        required: false,
                        vat: true,
                        minlength: 6
                    },
                    country:{
                        required: true
                    },
                    city: {
                        required: false,
                        minlength: 2
                    },
                    address: {
                        required: false,
                        minlength: 2
                    },
                    postcode: {
                        required: false,
                        minlength: 3,
                        maxlength: 10
                    },
                    crowd_fund_participation: {
                        required: true
                    },
                    crowd_fund_notification: {
                        required: true
                    },
                    language:{
                        required: true
                    },
                    question: {
                        required: true,
                        minlength: 1,
                        maxlength: 2,
                        question: true 
                    }
                },
                messages: {
                    name: {
                        required: "Please enter your firstname"
                    },
                    surname: {
                        required: "Please enter your lastname"
                    },
                    username: {
                        required: "Please enter your username",
                        remote: "The username is already taken.",
                        username: "Please enter only lower characters a-z, digits 0-9 without spaces"
                    },
                    mail: {
                        required: "Please enter your email address",
                        remote: "The email is already taken.",
                        email: "Your email address must be in the format of name@domain.org"
                    },
                    userpassword: {
                        required: "Please enter your password",
                        password: "Please include characters, digits and the special characters @#_&$ without spaces"
                    },
                    password_confirm: {
                        required: "Please confirm your password",
                        equalTo: "Please enter the same password in the related fields",
                        password: "Please include characters, digits and the special characters @#_&$ without spaces"
                    },
                    skills: {
                        required: "Please denote the familiarity with the IT services"
                    },
                    phone: {
                        required: "Please enter your phone",
                        minlength: "Please enter at least 10 digits",
                        maxlength: "Please enter at most 15 digits",
                        digits: "Please enter only digits"
                    },
                    country: {
                        required: "Please choose your country"
                    },
                    gender: {
                        required: "Please choose your gender"
                    },
                    vat: {
                        vat: "Please enter only characters a-z/A-Z, digits 0-9 without spaces"
                    },
                    crowd_fund_participation: {
                        required: "Please denote if you are interested to participate in any crowd-funding process"
                    },
                    crowd_fund_notification: {
                        required: "Please denote if you are interested to receive notifications about the crowd-funding processes"
                    },
                    language: {
                        required: "Please select the language you prefer"
                    },
                    question: {
                        required: "Please enter your thought",
                        question: "Please confirm the result"
                    }
                },
                errorPlacement: function (error, element) {
                    
                    if (element.attr('name') === "crowd_fund_notification" || element.attr('name') === "crowd_fund_participation") {
                        error.insertAfter(element.parent().parent());
                    }
                    else {
                        error.insertAfter(element);
                    }
                    error.css("color", eSettings.color);
                    element.parent().addClass(eSettings.highlightClass);
                },
                success: function (error) {
                    error.parent().removeClass(eSettings.highlightClass);
                    error.removeClass(errorClass);
                    error.parent().find($("span")).remove();
                },
                submitHandler: function (form) {
                    var payload = $(form).serializeObject();
                    delete payload['question'];
                    delete payload['password_confirm'];


                    $.ajax({
                        url: $(form).attr('action'),
                        type: "POST",
                        dataType: "json",
                        contentType: 'application/json',
                        data: JSON.stringify(payload),
                        success: function (response) {
                            location.href = successURL;
                        },
                        error: function (response) {
                            alert("Oops, an error is occured!!!");
                        }
                    });
                }
            })
        },
        updateProfile: function (successURL, checkURL) {
            currentForm = '#profileEditForm';
            logoForm = "#logoUpdateForm";

            // events
            $(document).on('submit', currentForm, function (event) {
                event.preventDefault();
            }).on('click', "#edit_user_logo", function () {
                $("#logo").click();
                return false;
            }).on('change', "#logo", function () {
                if (this.files && this.files[0]) {
                    var reader = new FileReader();
                    reader.onload = function (e) {
                    }
                    reader.readAsDataURL(this.files[0]);
                }

                var form = $(logoForm);
                var media = new FormData(form[0]);
                $.ajaxSetup({
                    beforeSend: function (xhr, settings) {
                        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                            xhr.setRequestHeader("X-CSRFToken", new Cookies().getValue('csrftoken'));
                        }
                    }
                });
                $.ajax({
                    type: form.attr('method'),
                    url: form.attr('action'),
                    beforeSend: function (xhr, settings) {
                        $.ajaxSettings.beforeSend(xhr, settings);
                    },
                    cache: false,
                    contentType: false,
                    processData: false,
                    data: media,
                    success: function (response) {
                        location.reload();
                    },
                    error: function (response) {
                        alert("Error in image load. Try again");
                    }
                });
                return false;
            });

            //validation
            profileUpdValidator = $(currentForm).validate({
                errorClass: errorClass,
                errorElement: "span",
                rules: {
                    name: {
                        required: true,
                        minlength: 2
                    },
                    surname: {
                        required: true,
                        minlength: 2
                    },
                    mail: {
                        required: true,
                        email: true,
                        remote: {
                            url: checkURL,
                            type: "GET",
                            data: {
                                mail: function () {
                                    return $("#mail").val();
                                }
                            }
                        }
                    },
                    skills: {
                        required: true
                    },
                    phone: {
                        required: true,
                        minlength: 10,
                        maxlength: 15,
                        digits: true
                    },
                    gender: {
                        required: true
                    },
                    country: {
                        required: true,
                    },
                    city: {
                        required: false,
                        minlength: 2
                    },
                    address: {
                        required: false,
                        minlength: 2
                    },
                    postcode: {
                        required: false,
                        minlength: 3,
                        maxlength: 10
                    },
                    vat: {
                        required: false,
                        vat: true,
                        minlength: 6
                    },
                    crowd_fund_participation: {
                        required: true
                    },
                    crowd_fund_notification: {
                        required: true
                    },
                    language: {
                        required: true
                    }
                },
                messages: {
                    name: {
                        required: "Please enter your firstname"
                    },
                    surname: {
                        required: "Please enter your lastname"
                    },
                    mail: {
                        required: "Please enter your email address",
                        remote: "The email is already taken.",
                        email: "Your email address must be in the format of name@domain.org"
                    },
                    vat: {
                        vat: "Please enter only characters a-z/A-Z, digits 0-9 without spaces"
                    },
                    skills: {
                        required: "Please denote the familiarity with the IT services"
                    },
                    phone: {
                        required: "Please enter your phone",
                        minlength: "Please enter at least 10 digits",
                        maxlength: "Please enter at most 15 digits",
                        digits: "Please enter only digits"
                    },
                    country: {
                        required: "Please choose your country"
                    },
                    gender: {
                        required: "Please choose your gender"
                    },
                    crowd_fund_participation: {
                        required: "Please denote if you are interested to participate in any crowd-funding process"
                    },
                    crowd_fund_notification: {
                        required: "Please denote if you are interested to receive notifications about the crowd-funding processes"
                    },
                    language: {
                        required: "Please select the language you prefer"
                    }
                },
                errorPlacement: function (error, element) {
                    if (element.attr('name') === "crowd_fund_notification" || element.attr('name') === "crowd_fund_participation") {
                        error.insertAfter(element.parent().parent());
                    }
                    else {
                        error.insertAfter(element);
                    }
                    error.css("color", eSettings.color);
                    element.parent().addClass(eSettings.highlightClass);
                },
                success: function (error) {
                    error.parent().removeClass(eSettings.highlightClass);
                    error.removeClass(errorClass);
                    error.parent().find($("span")).remove();
                },
                submitHandler: function (form) {
                    var payload = $(form).serializeObjectAll();

                    $.ajax({
                        url: $(form).attr('action'),
                        type: $(form).attr('method'),
                        dataType: "json",
                        contentType: 'application/json',
                        data: JSON.stringify(payload),
                        success: function (response) {
                            location.href = successURL;
                        },
                        error: function (response) {
                            alert("Oops, an error is occured!!!");
                        }
                    });
                }
            })
        },
        changePassword: function (successURL) {
            currentForm = '#changePwdForm';
            // handle events
            $(document).on('submit', currentForm, function (event) {
                event.preventDefault();
            });
            // validation
            currentValidator = $(currentForm).validate({
                errorClass: errorClass,
                errorElement: "span",
                rules: {
                    currentpassword: {
                        required: true,
                        minlength: 8,
                        password: true
                    },
                    userpassword: {
                        required: true,
                        minlength: 8,
                        notEqualTo: "#currentpassword",
                        password: true
                    },
                    password_confirm: {
                        required: true,
                        minlength: 8,
                        equalTo: "#userpassword",
                        password: true
                    }
                },
                messages: {
                    userpassword: {
                        required: "Please enter your old password",
                        password: "Please include characters, digits and the special characters @#_&$ without spaces"
                    },
                    userpassword: {
                        required: "Please enter your new password",
                        notEqualTo: "Please enter a different password from the old one",
                        password: "Please include characters, digits and the special characters @#_&$ without spaces"
                    },
                    password_confirm: {
                        required: "Please confirm your new password",
                        equalTo: "Please enter the same password in the related fields"
                    }
                },
                errorPlacement: function (error, element) {
                    error.insertAfter(element);
                    error.css("color", eSettings.color);
                    element.parent().addClass(eSettings.highlightClass);
                },
                success: function (error) {
                    error.parent().removeClass(eSettings.highlightClass);
                    error.removeClass(errorClass);
                    error.parent().find($("span")).remove();
                },
                submitHandler: function (form) {
                    var payload = $(form).serializeObject();
                    $.ajax({
                        url: $(form).attr('action'),
                        type: $(form).attr('method'),
                        dataType: "json",
                        contentType: 'application/json',
                        data: JSON.stringify(payload),
                        success: function (response) {
                            swal({
                                html: false,
                                title: "Change password process",
                                text: "Your password has been changed.",
                                type: "info",
                                confirmButtonText: "Continue",
                                confirmButtonColor: "#3a87ad",
                                animation: "slide-from-top"
                            },
                            function (isConfirm) { 
                                if (isConfirm) {
                                    location.href = successURL;
                                }
                            });
                        },
                        error: function (response) {
                            //console.log(response.responseText);
                            swal({
                                html: false,
                                title: "Change password process",
                                text: "The old password you enter is not valid. Try again!",
                                type: "error",
                                confirmButtonText: "Continue",
                                confirmButtonColor: "#d9534f",
                                animation: "slide-from-top"
                            });
                        }
                    });
                }
            })
        },
        registerApplication: function (successURL) {
            currentForm = '#registrationAppForm';
            // handle events
            $(document).on('submit', currentForm, function (event) {
                event.preventDefault();
            });
            // validation
            currentValidator = $(currentForm).validate({
                errorClass: errorClass,
                errorElement: "span",
                rules: {
                    name: {
                        required: true,
                        minlength: 4
                    },
                    description: {
                        required: true,
                        maxlength: 200
                    },
                    logo: {
                        required: false,
                        accept: "image/jpg,image/jpeg,image/png,image/gif"
                    },
                    url: {
                        required: true,
                        url: true
                    },
                    callback_url: {
                        required: true,
                        url: true
                    },
                    callback_url2: {
                        required: false,
                        url: true
                    },
                    mail: {
                        required: true,
                        email: true
                    }
                },
                messages: {
                    name: {
                        required: "Please enter the name of the application"
                    },
                    description: {
                        required: "Please enter a brief description of the application",
                        maxlength: "Please type at most 500 characters"
                    },
                    logo: {
                        required: "Please upload a logo for the application",
                        accept: "Please upload an logo having jpg, jpeg, png or gif format"
                    },
                    url: {
                        required: "Please enter the URL of the application",
                        url: "Please enter a valid callback URL"
                    },
                    callback_url: {
                        required: "Please enter the callback URL of the application",
                        url: "Please enter a valid callback URL"
                    },
                    callback_url2: {
                        url: "Please enter a valid callback URL"
                    },
                    mail: {
                        required: "Please enter the email address of the application's administrator",
                        email: "The email address must be in the format of name@domain.org"
                    }
                },
                errorPlacement: function (error, element) {
                    error.insertAfter(element);
                    error.css("color", eSettings.color);
                    element.parent().addClass(eSettings.highlightClass);
                },
                success: function (error) {
                    error.parent().removeClass(eSettings.highlightClass);
                    error.removeClass(errorClass);
                    error.parent().find($("span")).remove();
                },
                submitHandler: function (form) {
                    var payload = $(form).serializeObject();
                    delete payload['logo'];

                    $.ajax({
                        url: $(form).attr('action'),
                        type: $(form).attr('method'),
                        dataType: "json",
                        contentType: 'application/json',
                        data: JSON.stringify(payload),
                        success: function (response) {
                            location.href = successURL + response.client_id + "/";
                        },
                        error: function (response) {
                            alert("Oops, an error is occured!!!");
                        }
                    });
                }
            })
        },
        updateApplication: function (successURL) {
            currentForm = '#updateAppForm';
            $(document).on('submit', currentForm, function (event) {
                event.preventDefault();
            });
            currentValidator = $(currentForm).validate({
                errorClass: errorClass,
                errorElement: "span",
                rules: {
                    name: {
                        required: true,
                        minlength: 4
                    },
                    description: {
                        required: true,
                        maxlength: 200
                    },
                    logo: {
                        required: false,
                        accept: "image/jpg,image/jpeg,image/png,image/gif"
                    },
                    url: {
                        required: true,
                        url: true
                    },
                    callback_url: {
                        required: true,
                        url: true
                    },
                    callback_url2: {
                        required: false,
                        url: true
                    },
                    mail: {
                        required: true,
                        email: true
                    }
                },
                messages: {
                    name: {
                        required: "Please enter the name of the application"
                    },
                    description: {
                        required: "Please enter a brief description of the application",
                        maxlength: "Please type at most 500 characters"
                    },
                    logo: {
                        required: "Please upload a logo for the application",
                        accept: "Please upload an logo having jpg, jpeg, png or gif format"
                    },
                    url: {
                        required: "Please enter the URL of the application",
                        url: "Please enter a valid callback URL"
                    },
                    callback_url: {
                        required: "Please enter the callback URL of the application",
                        url: "Please enter a valid callback URL"
                    },
                    callback_url2: {
                        url: "Please enter a valid callback URL"
                    },
                    mail: {
                        required: "Please enter the email address of the application's administrator",
                        email: "The email address must be in the format of name@domain.org"
                    }
                },
                errorPlacement: function (error, element) {
                    error.insertAfter(element);
                    error.css("color", eSettings.color);
                    element.parent().addClass(eSettings.highlightClass);
                },
                success: function (error) {
                    error.parent().removeClass(eSettings.highlightClass);
                    error.removeClass(errorClass);
                    error.parent().find($("span")).remove();
                },
                submitHandler: function (form) {
                    var payload = $(form).serializeObject();
                    delete payload['logo'];

                    $.ajax({
                        url: $(form).attr('action'),
                        type: $(form).attr('method'),
                        dataType: "json",
                        contentType: 'application/json',
                        data: JSON.stringify(payload),
                        success: function (response) {
                            location.href = successURL; //+ response.username + "/";
                        },
                        error: function (response) {
                            alert("An error has occured. Try again!");
                        }
                    });
                }
            })
        },
        deleteApplication: function (actionURL, successURL) {
            swal({
                html: false,
                title: "Application removal",
                text: "Do you want to delete this application?",
                type: "info",
                showCancelButton: true,
                confirmButtonClass: "btn-primary",
                confirmButtonText: "Yes",
                cancelButtonText: "No",
                cancelButtonClass: "btn-danger",
                closeOnConfirm: false,
                closeOnCancel: false,
                animation: "slide-from-top"
            },
            function (isConfirm) {
                if (isConfirm) {
                    $.ajax({
                        url: actionURL,
                        type: "DELETE",
                        dataType: "json",
                        contentType: 'application/json',
                        success: function (response) {
                            //console.log(response);
                            location.href = successURL;
                        },
                        error: function (response) {
                            console.error("Error in app deletion");
                        }
                    });
                } else {
                    swal({
                        html: false,
                        title: "Application removal",
                        text: "The deletion of this application has been canceled!",
                        type: "info",
                        confirmButtonText: "Continue",
                        confirmButtonColor: "#3a87ad"
                    });
                }
            });
        },
        authenticatedApps: function (tokensURL) {

            $.ajax({
                url: tokensURL,
                type: "GET",
                dataType: "json",
                contentType: 'application/json',
                success: function (response) {
                    var d = response.result;
                    for (var token in d) {
                        d[token]["id"] = d[token]["id"][0];
                        d[token]["revoke_access"] = "<span data-href='" + tokensURL + "' data-id='"+ d[token]["id"] + "' class='fa fa-remove text-danger cursor-pointer revoke-token'><span>";
                        //console.log(d[token]["revoke_access"]);
                    }
                    $("#authorized_apps").bootstrapTable('destroy').bootstrapTable({ data: d });

                    $(".revoke-token").click(function () {
                        $.ajax({
                            url: $(this).data('href') + "/" + $(this).data('id'),
                            type: "DELETE",
                            dataType: "json",
                            contentType: 'application/json',
                            success: function (response) {
                                //console.info("DELETE token: " + $(this).data('id'));
                            },
                            error: function (response) {
                                console.error(response);
                            },
                            complete: function (response) {
                                location.reload()
                            }
                        });
                    });

                },
                error: function (response) {
                    alert("Oops, an error is occured!!!");
                },
                complete: function () {
                    $(".fixed-table-body").css("height", "auto");
                }
            });
            $("body").on('all.bs.table', '#my_apps', function (name, args) {
                $("td").each(function () {
                    $(this).css("vertical-align", "middle");
                });
            });
        },
        myApplications: function (endpoint, baseURL) {
            $.ajax({
                url: endpoint,
                type: "GET",
                dataType: "json",
                contentType: 'application/json',
                success: function (response) {
                    var d = response.results;
                    for (var app in d) {
                        d[app]["name"] += " <a href='" + baseURL + d[app]["client_id"] + "/' title='View information for " + d[app]["name"] + "' class='cursor-pointer app-preview'><span class='fa fa-external-link fa-xs'></span> </a>";
                        d[app]["edit"] = "<a href='" + baseURL + d[app]["client_id"] + "/edit/' class='text-info cursor-pointer app-edit'><span class='fa fa-edit text-primary'><span> </a>";
                        d[app]["roles"] = "<a href='" + baseURL + d[app]["client_id"] + "/roles/' class='cursor-pointer app-roles'><span class='fa fa-key text-primary'><span> </a>";
                        d[app]["users"] = "<a href='" + baseURL + d[app]["client_id"] + "/members/' class='cursor-pointer app-auth-users'><span class='fa fa-group text-primary'><span> </a>";
                    }

                    $("#my_apps").bootstrapTable('destroy').bootstrapTable({ data: d });

                },
                error: function (response) {
                    console.error("Error in apps loading");
                    $("#my_apps").bootstrapTable('destroy').bootstrapTable({ data: [] });
                },
                complete: function () {
                    $(".fixed-table-body").css("height", "auto");
                }
            });
            $("body").on('all.bs.table', '#my_apps', function (name, args) {
                $("td").each(function () {
                    $(this).css("vertical-align", "middle");
                });
            });
        },
        setApplicationRoles: function (addRoleURL) {
            currentValidator = $('#setRolesForm').validate({
                submitHandler: function (form) {
                    var payload = $(form).serializeList();
                    $.ajax({
                        url: $(form).attr('action'),
                        type: $(form).attr('method'),
                        dataType: "json",
                        contentType: 'application/json',
                        data: JSON.stringify(payload),
                        success: function (response) {
                            location.reload();
                        },
                        error: function (response) {
                            console.error('Error in roles\' selection');
                        }
                    });
                }
            });

            // handle events
            $(document).on('submit', '#setRolesForm', function (event) {
                event.preventDefault();
            }).on('submit', '#addRoleForm', function (event) {
                event.preventDefault();
            }).on('click', '.list-group-item', function () {
                $(this).handleRoles();
            }).on('click', '#set-roles-reset', function (event) {
                event.preventDefault();
                $('#setRolesForm')[0].reset();
                $.each($('.list-group-item'), function () {
                    $(this).handleRoles();
                });
            }).on('click', '#add-role', function (event) {
                event.preventDefault();
                var form = '#addRoleForm';
                var html = [
                    '<div class="row col-sm-12 col-md-12 col-lg-12">',
                        '<form action="'+ addRoleURL +'" method="post" id="addRoleForm" name="addRoleForm" role="form">',
                            '<div class="row">',
                                '<div class="col-sm-4 col-md-4 col-lg-4 col-xs-12">',
                                    '<label class="padding-left-20 control-label" for="type">Name<span style="color:red">*</span></label>',
                                '</div>',
                                '<div class="col-md-8 col-sm-8 col-lg-8 col-xs-12">',
                                    '<input type="text" class="form-control" name="type" id="type" maxlength="64" placeholder="enter a name i.e. developers" required/>',
                                '</div>',
                            '</div>',
                            '<br>',
                            '<div class="row">',
                                '<div class="col-sm-4 col-md-4 col-lg-4 col-xs-12">',
                                    '<label class="padding-left-20 control-label" for="description">Description<span style="color:red">*</span></label>',
                                '</div>',
                                '<div class="col-md-8 col-sm-8 col-lg-8 col-xs-12">',
                                    '<textarea class="form-control" rows="6" name="description" id="description" autocomplete="off" maxlength="500" placeholder="describe the role" required></textarea>',
                                '</div>',
                            '</div>',
                        '</form>',
                    '</div>'
                ].join('');

                modalActionsPost("Register a role", html, "Cancel", "Submit",
                    function () {
                        window.close();
                    },
                    function () {
                        $('#addRoleForm').validate({
                            errorClass: errorClass,
                            errorElement: "span",
                            rules: {
                                type: {
                                    required: true,
                                    minlength: 4,
                                    remote: {
                                        url: addRoleURL,
                                        type: "GET",
                                        data: {
                                            type: function () {
                                                return $("#type").val();
                                            }
                                        }
                                    }
                                },
                                description: {
                                    required: true,
                                    maxlength: 500
                                }
                            },
                            messages: {
                                type: {
                                    required: "Please enter the name of the role: ",
                                    minlength: "Please enter at least four characters",
                                    remote: "This name has already taken."
                                },
                                description: {
                                    required: "Please enter a brief description of the role - 500 characters maximum",
                                    maxlength: "Please type at most 500 characters"
                                }
                            },
                            errorPlacement: function (error, element) {
                                error.insertAfter(element);
                                error.css("color", eSettings.color);
                                element.parent().addClass(eSettings.highlightClass);
                            },
                            success: function (error) {
                                error.parent().removeClass(eSettings.highlightClass);
                                error.removeClass(errorClass);
                                error.parent().find($("span")).remove();
                            }
                        });
                        if (!$(form).valid()) {
                            return false;
                        }
                        else {
                            $.ajax({
                                url: $(form).attr('action'),
                                type: $(form).attr('method'),
                                dataType: "json",
                                contentType: 'application/json',
                                data: JSON.stringify($(form).serializeObjectAll()),
                                success: function (response) {
                                    location.reload();
                                },
                                error: function (response) {
                                    alert("Oops, an error is occured!!!");
                                }
                            });
                        }
                    }
                );
            });
        },
        setApplicationMembership: function (applicationName) {
            currentForm = '#addMemberForm'
            $(currentForm).validate({
                errorClass: errorClass,
                errorElement: "div",
                rules: {
                    member: {
                        required: true
                    },
                    terms_member: {
                        required: true
                    }
                },
                messages: {
                    member: {
                        required: "Please choose one of potential answers",
                    },
                    terms_member: {
                        required: "Please read the <strong>Terms of usage</strong> and if you agree with it, then check the box",
                    }
                },
                errorPlacement: function (error, element) {
                    if (element.attr('id') === "terms_member") {
                        error.insertAfter(element);
                    }
                    else {
                        error.insertAfter($(currentForm).find("fieldset"));
                    }
                    error.css("color", eSettings.color);
                    element.parent().addClass(eSettings.highlightClass);
                },
                success: function (error) {
                    error.parent().removeClass(eSettings.highlightClass);
                    error.removeClass(errorClass);
                    error.parent().find($("span")).remove();
                },
                submitHandler: function (form) {
                    var payload = $(form).serializeObjectAll();

                    $.ajax({
                        url: $(form).attr('action'),
                        type: (parseInt(payload['member'])) ? $(form).attr('method') : "DELETE",
                        dataType: "json",
                        contentType: 'application/json',
                        success: function (response) {
                            location.reload();
                        },
                        error: function (response) {
                            console.error("Error in member's registration");
                        }
                    });
                }
            });

            $(document).on('click', "#use_member_agreement", function (event) {
                event.preventDefault();
                swal({
                    html: true,
                    title: "Terms of usage:<br>membership",
                    text: "By checking this box, you grant with permission the P4ALL Identity & Access Manager to share your profile with the " + applicationName + " application.",
                    type: "info",
                    animation: "slide-from-top",
                    confirmButtonText: "Continue",
                    confirmButtonColor: "#3a87ad"
                });
                $(".sweet-alert p").sweetAlertText();
            });


        },
        setMemberApplicationRoles: function (applicationName) {
            currentForm = '#memberRolesForm';

            currentValidator = $(currentForm).validate({
                errorClass: errorClass,
                errorElement: "div",
                rules: {
                    terms_usage: {
                        required: true
                    }
                },
                messages: {
                    terms_usage: {
                        required: "Please read the <strong>Terms of usage</strong> and then check on the box",
                    }
                },
                errorPlacement: function (error, element) {
                    error.insertAfter(element);
                    error.css("color", eSettings.color);
                    element.parent().addClass(eSettings.highlightClass);
                },
                success: function (error) {
                    error.parent().removeClass(eSettings.highlightClass);
                    error.removeClass(errorClass);
                    error.parent().find($("span")).remove();
                },
                submitHandler: function (form) {
                    var payload = { "roles": $(form).serializeList(), "application_member": $("#application_member").val() };
                    $.ajax({
                        url: $(form).attr('action'),
                        type: $(form).attr('method'),
                        dataType: "json",
                        contentType: 'application/json',
                        data: JSON.stringify(payload),
                        success: function (response) {
                            location.reload();
                        },
                        error: function (response) {
                            console.error("Error in roles\' selection");
                        }
                    });
                }
            });

            // handle events
            $(document).on('submit', currentForm, function (event) {
                event.preventDefault();
            }).on('click', '.list-group-item', function () {
                $(this).handleRoles();
            }).on('click', '#reset-member-roles', function (event) {
                event.preventDefault();
                $(currentForm)[0].reset();
                $.each($('.list-group-item'), function () { $(this).handleRoles(); });
            }).on('click', "#use_agreement", function (event) {
                event.preventDefault();
                swal({
                    html: true,
                    title: "Terms of usage:<br>roles",
                    text: "By checking this box, you grant with permission the P4ALL Identity & Access Manager to share your role(s) related to the " + applicationName + " application on it.",
                    type: "info",
                    animation: "slide-from-top",
                    confirmButtonText: "Continue",
                    confirmButtonColor: "#3a87ad"
                });
                $(".sweet-alert p").sweetAlertText();
            });
        }
    };

})();