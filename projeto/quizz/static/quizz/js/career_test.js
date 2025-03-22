let currentPage = 1;
let receivedQuestionIds = []; // Variável para armazenar os IDs das perguntas já recebidas

function loadQuestions() {
    // Cria a query string com os IDs das perguntas já recebidas
    let queryString = `page=${currentPage}`;
    if (receivedQuestionIds.length > 0) {
        queryString += '&received=' + receivedQuestionIds.join('&received=');
    }

    $.ajax({
        url: `/api/questions/?${queryString}`, // Inclui os IDs das perguntas já recebidas
        method: 'GET',
        success: function (data) {
            if (data.results.length > 0) {
                data.results.forEach(function (question) {
                    // Adiciona o ID da pergunta à lista de perguntas recebidas
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

                    questionHtml += `
                            </ul>
                        </div>
                    `;

                    $('#questions-container').append(questionHtml);
                });

                currentPage++;
            } else {
                $('#load-more-questions').prop('disabled', true).text('Nenhuma pergunta disponível');
            }
        },
        error: function () {
            alert('Erro ao carregar perguntas!');
        }
    });
}

$(document).ready(function () {
    loadQuestions();

    $('#load-more-questions').click(function () {
        loadQuestions();
    });
});