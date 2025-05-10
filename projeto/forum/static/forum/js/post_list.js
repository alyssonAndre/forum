function renderPosts(posts) {
    const container = document.getElementById('posts-container');
    container.innerHTML = '';

    posts.forEach(post => {
        const postHtml = `
        <div class="bg-white shadow-md rounded-lg p-6 mb-6">
            <h2 class="text-2xl font-semibold text-gray-800">${post.title}</h2>
            <p class="text-gray-600 mt-2">${post.content.substring(0, 200)}</p>
            <p class="text-sm text-gray-500 mt-2">Autor: ${post.author.username} |
                ${new Date(post.created_at).toLocaleString('pt-BR')}</p>

            <div class="flex items-center space-x-4 mt-2">
                <button class="like-btn text-green-600 hover:text-green-800" data-id="${post.id}">
                    <span class="ml-2">${post.like_count}</span> Likes
                </button>
                <button class="dislike-btn text-red-600 hover:text-red-800" data-id="${post.id}">
                    <span class="ml-2">${post.dislike_count}</span> Dislikes
                </button>
            </div>

            <a href="/forum/post/${post.id}/" class="text-blue-600 hover:text-blue-800 mt-4 inline-block">Ver mais...</a>
        </div>`;
        container.innerHTML += postHtml;
    });

    attachLikeDislikeHandlers();
}

function fetchPosts() {
    fetch('/api/forum/posts/')
        .then(response => response.json())
        .then(data => {
            renderPosts(data);
        })
        .catch(error => console.error('Erro ao buscar posts:', error));
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function attachLikeDislikeHandlers() {
    const csrftoken = getCookie('csrftoken');

    document.querySelectorAll('.like-btn').forEach(button => {
        button.addEventListener('click', () => {
            const postId = button.getAttribute('data-id');
            fetch(`/api/forum/posts/${postId}/like/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                }
            })
                .then(res => res.json())
                .then(data => {
                    fetchPosts();
                });
        });
    });

    document.querySelectorAll('.dislike-btn').forEach(button => {
        button.addEventListener('click', () => {
            const postId = button.getAttribute('data-id');
            fetch(`/api/forum/posts/${postId}/dislike/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                }
            })
                .then(res => res.json())
                .then(data => {
                    fetchPosts();
                });
        });
    });
}


setInterval(fetchPosts, 30000);

fetchPosts();
