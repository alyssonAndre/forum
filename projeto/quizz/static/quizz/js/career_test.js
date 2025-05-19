let currentPage = 1;
let receivedQuestionIds = []; // Variável para armazenar os IDs das perguntas já recebidas
let questionCount = 0; // Contador de perguntas carregadas

function loadQuestions() {
    // Cria a query string com os IDs das perguntas já recebidas
    let queryString = `page=${currentPage}`;
    if (receivedQuestionIds.length > 0) {
        queryString += '&received=' + receivedQuestionIds.join('&received=');
    }

    $.ajax({
        url: `/api/questions/?${queryString}`, // Inclui os IDs das perguntas já recebidas
        method: 'GET',
        error: function (xhr) {
            let msg = "Você já atingiu o limite de 3 tentativas para o teste vocacional.";
            if (xhr.responseJSON?.error) {
                msg = xhr.responseJSON.error;
            }

            $("#error-message").removeClass("hidden").text(msg);

            if (msg === "Você já atingiu o limite de 3 tentativas para o teste vocacional.") {
                $('#load-more-questions')
                    .text("Voltar para a Home")
                    .removeClass("bg-blue-600 hover:bg-blue-700")
                    .addClass("bg-red-600 hover:bg-red-700")
                    .off("click")
                    .on("click", function () {
                        window.location.href = "/quiz/";
                    });
            }
        },
        success: function (data) {
            if (data.results.length > 0) {
                const question = data.results[0]; // Carrega apenas a primeira pergunta do lote retornado
                // Adiciona o ID da pergunta à lista de perguntas recebidas
                receivedQuestionIds.push(question.id);

                // Incrementa o contador de perguntas
                questionCount++;

                let questionHtml = `
                    <div class="bg-white p-4 rounded-md shadow-md">
                        <h2 class="text-xl font-semibold mb-4">${questionCount}. ${question.text}</h2>
                        <ul class="space-y-2">
                        <span id="message-container" class="text-red-500 hidden warning-message text-sm"></span>
                `;

                question.alternatives.forEach(function (alternative) {
                    questionHtml += `
                        <li class="flex items-center space-x-4">
                            <input type="radio" name="question_${question.id}" id="question_${question.id}_alternative_${alternative.id}" class="h-5 w-5">
                            <label for="question_${question.id}_alternative_${alternative.id}" class="text-lg">${alternative.text}</label>
                        </li>
                    `;
                });

                questionHtml += `
                        </ul>
                    </div>
                `;

                // Substitui o conteúdo de #questions-container pela nova pergunta
                $('#questions-container').html(questionHtml);

                currentPage++;

                // Atualiza o botão para "Finalizar teste" após a última pergunta
                if (questionCount >= 10) {
                    $('#load-more-questions').text('Finalizar teste');
                }
            } else {
                $('#load-more-questions').prop('disabled', true).text('Nenhuma pergunta disponível');
            }
        },
    });
}

function checkAnsweredQuestions() {
    let allAnswered = true;
    $('div[id^="questions-container"] input[type="radio"]').each(function () {
        let name = $(this).attr('name');
        if (!$(`input[name="${name}"]:checked`).length) {
            allAnswered = false;
            return false; // Para de iterar se encontrar uma pergunta não respondida
        }
    });
    return allAnswered;
}

function showMessage(message) {
    $('#message-container').text(message).removeClass('hidden').fadeIn();
    setTimeout(function () {
        $('#message-container').fadeOut();
    }, 3000);
}

$(document).ready(function () {
    loadQuestions();

    $('#load-more-questions').click(function () {
        if ($(this).text() === 'Finalizar teste') {
            if (checkAnsweredQuestions()) {
                // alert("Teste finalizado! Obrigado por participar!");
            } else {
                showMessage('Por favor, responda a pergunta antes de finalizar o teste!');
            }
        } else if (checkAnsweredQuestions()) {
            loadQuestions();
        } else {
            showMessage('Por favor, responda a pergunta antes de prosseguir!');
        }
    });

    $(document).on('change', 'input[type="radio"]', function () {
        let allAnswered = $('input[type="radio"]:checked').length === receivedQuestionIds.length;
        if (allAnswered) {
            $('#submit-answers').removeClass('hidden');
        }
    });

    let answers = [];
    $('#load-more-questions').click(function () {
        if ($(this).text() === 'Finalizar teste') {
            if (checkAnsweredQuestions()) {

                // Só faz a requisição AJAX se tiver respostas
                if (answers.length > 0) {
                    $.ajax({
                        url: '/api/submit-answers/',
                        method: 'POST',
                        contentType: 'application/json',
                        data: JSON.stringify({ answers: answers }),
                        headers: { "X-CSRFToken": getCookie("csrftoken") },
                        success: function (data) {
                            let course;

                            if (data.recommended_course) {
                                // Caso tenha apenas um curso recomendado
                                window.location.href = `/quiz/score/?course=${encodeURIComponent(data.recommended_course)}&score=${data.score}`;
                            } else if (data.recommended_courses && data.recommended_courses.length > 1) {
                                // Caso de empate entre cursos
                                Swal.fire({
                                    title: 'Empate entre cursos!',
                                    text: 'Escolha o curso que mais combina com você:',
                                    input: 'select',
                                    inputOptions: data.recommended_courses.reduce((options, course) => {
                                        options[course] = course;
                                        return options;
                                    }, {}),
                                    inputPlaceholder: 'Selecione um curso',
                                    showCancelButton: false,
                                    confirmButtonText: 'Confirmar',
                                    allowOutsideClick: false,
                                    preConfirm: (selectedCourse) => {
                                        return selectedCourse;
                                    }
                                }).then((result) => {
                                    if (result.isConfirmed) {
                                        const selectedCourse = result.value;

                                        $.ajax({
                                            url: "/api/set-chosen-course/",
                                            method: "POST",
                                            contentType: "application/json",
                                            headers: { "X-CSRFToken": getCookie("csrftoken") },
                                            data: JSON.stringify({ course: selectedCourse }),
                                            success: function () {
                                                window.location.href = `/quiz/score/?course=${encodeURIComponent(selectedCourse)}&score=${data.score}`;
                                            },
                                            error: function () {
                                                Swal.fire({
                                                    icon: 'error',
                                                    title: 'Erro',
                                                    text: 'Não foi possível salvar o curso selecionado.'
                                                });
                                            }
                                        });
                                    }
                                });
                            } else {
                                Swal.fire({
                                    icon: 'info',
                                    title: 'Resultado',
                                    text: 'Nenhum curso recomendado com base nas suas respostas.'
                                });
                            }
                        },
                        error: function () {
                            alert('Erro ao enviar respostas!');
                        }
                    });
                } else {
                    alert('Nenhuma resposta selecionada!');
                }
            } else {
                showMessage('Por favor, responda todas as perguntas antes de finalizar o teste!');
            }
        }
    });


    $(document).on('change', 'input[type="radio"]', function () {
        let questionId = $(this).attr('name').split('_')[1];
        let alternativeId = $(this).attr('id').split('_').pop();

        answers = answers.filter(ans => ans.question !== questionId);

        answers.push({ question: questionId, alternative: alternativeId });

    });

});


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        document.cookie.split(';').forEach(cookie => {
            let trimmedCookie = cookie.trim();
            if (trimmedCookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(trimmedCookie.split('=')[1]);
            }
        });
    }
    return cookieValue;
}



$(document).ready(function () {
    $.ajax({
        url: "/api/quiz/questions/",
        method: "GET",

    });
});

