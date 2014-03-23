<%inherit file="microblog:templates/layout.mako"/>

<form action="${request.route_url('register')}" method="post">


% for error in form.name.errors:
    <div class="error">${ error }</div>
% endfor

<div><label>${form.name.label}</label>${form.name()}</div>

% for error in form.password.errors:
<div class="error">${error}</div>
% endfor

<div><label>${form.password.label}</label>${form.password()}</div>

% for error in form.email.errors:
    <div class="error">${ error }</div>
% endfor

<div><label>${form.email.label}</label>${form.email()}</div>
<div><input type="submit" value="Submit"></div>
</form>
<p><a href="${request.route_url('home')}">Go Back</a></p>

<style type="text/css">
form{
    text-align: left;
}
label{
    min-width: 150px;
    vertical-align: top;
    text-align: right;
    display: inline-block;
}
input[type=text]{
    min-width: 505px;
}
textarea{
    color: #222;
    border: 1px solid #CCC;
    font-family: sans-serif;
    font-size: 12px;
    line-height: 16px;
    min-width: 505px;
    min-height: 100px;
}
.error{
    font-weight: bold;
    color: red;
}
</style>