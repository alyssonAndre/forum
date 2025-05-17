// Palavrões para censura
const badWords = [
    "merda",
    "porra",
    "caralho",
    "fdp",
    "foda",
    "puta",
    "pqp",
    "cacete",
];

function formatDateTime(isoDate) {
    const date = new Date(isoDate);
    const timeStr = date.toLocaleTimeString("pt-BR", {
        hour: "2-digit",
        minute: "2-digit",
    });
    return `${date.toLocaleDateString("pt-BR")}, ${timeStr}`;
}

function censorBadWords(text) {
    return text
        .split(/\s+/)
        .map((word) => {
            const normalized = word.toLowerCase().replace(/[^\w]/g, "");
            if (badWords.includes(normalized)) {
                return word[0] + "*".repeat(word.length - 1);
            }
            return word;
        })
        .join(" ");
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === name + "=") {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie("csrftoken");
const postId = document.getElementById("postMain").dataset.postId;

$(document).ready(function () {
    // Atualiza contador de caracteres
    $("#commentInput").on("input", function () {
        const len = $(this).val().length;
        $("#charCount").text(`${len}/250`);
    });

    // Envio do comentário
    $("#sendComment").click(function () {
        let content = $("#commentInput").val().trim();
        if (content === "" || content.length > 250) return;

        content = censorBadWords(content);

        const sendBtn = $("#sendComment");
        sendBtn.prop("disabled", true).text("Enviando...");
        $("#loaderOverlay").removeClass("hidden");

        $.ajax({
            url: `/api/forum/posts/${postId}/comments/`,
            method: "POST",
            headers: { "X-CSRFToken": csrftoken },
            contentType: "application/json",
            data: JSON.stringify({ content: content, post: postId }),
            success: function (data) {
                const newComment = $(`
                  <div class="bg-white p-4 rounded-lg shadow-md relative" style="display:none;">
                    <p class="text-sm text-gray-600 mb-5"><strong>${data.author.username}</strong>: ${data.content}</p>
                    <span class="absolute bottom-2 right-3 text-xs text-gray-400">${formatDateTime(data.created_at)}</span>
                  </div>
                `);

                $("#comments").prepend(newComment);
                newComment.fadeIn(500);

                $("#commentInput").val("");
                $("#charCount").text("0/250");
                sendBtn.prop("disabled", false).text("Enviar Comentário");
                $("#loaderOverlay").addClass("hidden");

                Swal.fire({
                    toast: true,
                    position: "bottom-end",
                    icon: "success",
                    title: "Comentário adicionado com sucesso!",
                    showConfirmButton: false,
                    timer: 5000,
                    timerProgressBar: true,
                    didOpen: (toast) => {
                        toast.addEventListener("mouseenter", Swal.stopTimer);
                        toast.addEventListener("mouseleave", Swal.resumeTimer);
                    },
                });
                $("#comments").scrollTop(0);
            },
            error: function (xhr) {
                alert("Erro ao enviar comentário: " + xhr.responseText);
                sendBtn.prop("disabled", false).text("Enviar Comentário");
                $("#loaderOverlay").addClass("hidden");
            },
        });
    });

    // Atualiza a lista de comentários a cada 30s
    function updateComments() {
        $("#loaderOverlay").removeClass("hidden"); // mostra loader

        $.ajax({
            url: `/api/forum/posts/${postId}/comments/`,
            method: "GET",
            success: function (data) {
                $("#comments").empty();
                data.reverse().forEach(function (comment) {
                    const newComment = `
                <div class="bg-white p-4 rounded-lg shadow-md relative">
                  <p class="text-sm text-gray-600 mb-5"><strong>${comment.author.username}</strong>: ${comment.content}</p>
                  <span class="absolute bottom-2 right-3 text-xs text-gray-400">${formatDateTime(comment.created_at)}</span>
                </div>`;
                    $("#comments").append(newComment);
                });
                $("#loaderOverlay").addClass("hidden"); // esconde loader após sucesso
            },
            error: function (xhr) {
                alert("Erro ao carregar comentários: " + xhr.responseText);
                $("#loaderOverlay").addClass("hidden"); // esconde loader em erro também
            },
        });
    }

    setInterval(updateComments, 30000);
});
