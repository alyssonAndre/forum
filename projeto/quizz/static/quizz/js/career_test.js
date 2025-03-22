let currentPage = 1;
let receivedQuestionIds = [];

function loadQuestions() {

    let queryString = `page=${currentPage}`;
    if (receivedQuestionIds.length > 0) {
        queryString += '&received=' + receivedQuestionIds.join('&received=');
    }

    $.ajax({
        url: `/api/questions/?${queryString}`,
        method: 'GET',
        success: function (data) {

            if (data.results.length > 0) {
                data.results.forEach(function (question) {
                    receivedQuestionIds.push(question.id);

                    let questionHtml = `
                        <div class="bg-white p-4 rounded-md shadow-md">
                            <h2 class="text-xl font-semibold mb-4">${question.text}</h2>
                            <ul class="space-y-2">
                    `;

                    question.alternatives.forEach(function (alternative) {
                        questionHtml += `
                            <li class="flex items-center space-x-4">
                                <input type="radio" name="question_${question.id}" id="question_${question.id}_alternative_${alternative.id}" class="h-5 w-5">
                                <label for="question_${question.id}_alternative_${alternative.id}" class="text-lg">${alternative.text}</label>
                            </li>
                        `;
                    });

                    questionHtml += `</ul></div>`;
                    $('#questions-container').append(questionHtml);
                });

                currentPage++;
            } else {
                $('#load-more-questions').prop('disabled', true).text('Nenhuma pergunta disponível');
            }
        },
        error: function (xhr, status, error) {
        }
    });
}

$(document).ready(function () {
    loadQuestions();

    $('#load-more-questions').click(function () {
        loadQuestions();
    });

    $(document).on('change', 'input[type="radio"]', function () {
        let allAnswered = $('input[type="radio"]:checked').length === receivedQuestionIds.length;
        if (allAnswered) {
            $('#submit-answers').removeClass('hidden');
        }
    });

    $('#submit-answers').click(function () {
        let answers = [];

        $('input[type="radio"]:checked').each(function () {
            let questionId = $(this).attr('name').split('_')[1];
            let alternativeId = $(this).attr('id').split('_').pop();
            answers.push({ question: questionId, alternative: alternativeId });
        });


        $.ajax({
            url: '/api/submit-answers/',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ answers: answers }),
            headers: { "X-CSRFToken": getCookie("csrftoken") },
            success: function (data) {

                if (data.recommended_course) {
                    alert(`Seu curso recomendado é: ${data.recommended_course}`);
                } else if (data.recommended_courses) {
                    alert(`Seu perfil se relaciona com esses dois cursos: ${data.recommended_courses.join(' e ')}`);
                } else {
                    alert("Erro: Nenhum curso recomendado.");
                }

                location.reload();
            },
            error: function () {
                alert('Erro ao enviar respostas!');
            }
        });



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
