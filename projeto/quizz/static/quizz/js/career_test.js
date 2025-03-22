// let currentPage = 1;
// let receivedQuestionIds = []; // Variável para armazenar os IDs das perguntas já recebidas

// function loadQuestions() {
//     // Cria a query string com os IDs das perguntas já recebidas
//     let queryString = `page=${currentPage}`;
//     if (receivedQuestionIds.length > 0) {
//         queryString += '&received=' + receivedQuestionIds.join('&received=');
//     }

//     $.ajax({
//         url: `/api/questions/?${queryString}`, // Inclui os IDs das perguntas já recebidas
//         method: 'GET',
//         success: function (data) {
//             if (data.results.length > 0) {
//                 data.results.forEach(function (question) {
//                     // Adiciona o ID da pergunta à lista de perguntas recebidas
//                     receivedQuestionIds.push(question.id);

//                     let questionHtml = `
//                         <div class="bg-white p-4 rounded-md shadow-md">
//                             <h2 class="text-xl font-semibold mb-4">${question.text}</h2>
//                             <ul class="space-y-2">
//                     `;

//                     question.alternatives.forEach(function (alternative) {
//                         questionHtml += `
//                             <li class="flex items-center space-x-4">
//                                 <input type="radio" name="question_${question.id}" id="question_${question.id}_alternative_${alternative.id}" class="h-5 w-5">
//                                 <label for="question_${question.id}_alternative_${alternative.id}" class="text-lg">${alternative.text}</label>
//                             </li>
//                         `;
//                     });

//                     questionHtml += `
//                             </ul>
//                         </div>
//                     `;

//                     $('#questions-container').append(questionHtml);
//                 });

//                 currentPage++;
//             } else {
//                 $('#load-more-questions').prop('disabled', true).text('Nenhuma pergunta disponível');
//             }
//         },
//         error: function () {
//             alert('Erro ao carregar perguntas!');
//         }
//     });
// }

// $(document).ready(function () {
//     loadQuestions();

//     $('#load-more-questions').click(function () {
//         loadQuestions();
//     });
// });
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
        error: function () {
            showMessage('Erro ao carregar perguntas!');
        }
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
                alert("Teste finalizado! Obrigado por participar!");
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

    $('#load-more-questions').click(function () {
        let answers = []; // Definir fora do if para garantir o escopo correto

        if ($(this).text() === 'Finalizar teste') {
            if (checkAnsweredQuestions()) {
                $('input[type="radio"]:checked').each(function () {
                    let questionId = $(this).attr('name').split('_')[1];
                    let alternativeId = $(this).attr('id').split('_').pop();
                    answers.push({ question: questionId, alternative: alternativeId });
                });

                // Só faz a requisição AJAX se tiver respostas
                if (answers.length > 0) {
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
                } else {
                    alert('Nenhuma resposta selecionada!');
                }
            } else {
                showMessage('Por favor, responda todas as perguntas antes de finalizar o teste!');
            }
        }
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
