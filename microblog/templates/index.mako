<%inherit file="pyramid_blogr:templates/layout.mako"/>

% if paginator.items:

    ${paginator.pager()}

    <h2>Blog entries</h2>

    <ul>
    % for post in paginator.items:
    <li>
    <a href="${request.route_url('blog', id=post.id, slug=post.slug)}">
    ${post.title}</a>
    </li>
    % endfor
    </ul>

    ${paginator.pager()}

% else:

<p>No blog entries found.</p>

%endif

<p><a href="${request.route_url('blog_action',action='create')}">
Create a new blog entry</a></p>