<%inherit file="microblog:templates/layout.mako"/>

<h1>${post.title}</h1>
<hr/>
<p>${post.body}</p>
<hr/>
<p>Created <strong title="${post.created}">
${post.created_in_words}</strong> ago</p>

<p><a href="${request.route_url('home')}">Go Back</a> ::
<a href="${request.route_url('blog_action', action='edit',
id=post.id)}">Edit Entry</a> ::
<a href="${request.route_url('blog_action', action='del',
id=post.id)}">Delete Entry</a>

</p>