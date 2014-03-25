<%inherit file="microblog:templates/layout.mako"/>
<%
from pyramid.security import authenticated_userid
user_id = authenticated_userid(request)
%>
% if user_id:
    Welcome <strong>${user_id}</strong> ::
    <a href="${request.route_url('auth', action='out')}">Sign Out</a>
%else:
    <form action="${request.route_url('auth', action='in')}" method="post">
    <label>User</label><input type="text" name="username">
    <label>Password</label><input type="password" name="password">
    <input type="submit" value="Sign In">
    </form>
    <a href="${request.route_url('register')}">Register</a>
%endif

% if paginator.items:

    ${paginator.pager()}

    <h2>Blog entries</h2>

    <ul>
    % for post in paginator.items:
    <li>
    <a href="${request.route_url('blog', id=post.id, slug=post.slug)}">
    ${post.title}</a><br>
    ${post.body}
    </li>
    % endfor
    </ul>

    ${paginator.pager()}

% else:

<p>No blog entries found.</p>

%endif

<p><a href="${request.route_url('blog_create',action='create')}">
Create a new blog entry</a></p>