document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('profileForm');
    const inputs = form.querySelectorAll('input');
    const saveButton = form.querySelector('button[type="submit"]');
    const loaderOverlay = document.getElementById("loaderOverlay");

    function setReadonlyState() {
        inputs.forEach(input => {
            if (input.type === 'file') {
                input.disabled = true;
            } else {
                input.setAttribute('readonly', true);
            }
            input.classList.add('bg-gray-100', 'cursor-not-allowed');
        });
        saveButton.disabled = true;
        saveButton.classList.add('opacity-50', 'cursor-not-allowed');
    }

    function setEditableState() {
        inputs.forEach(input => {
            if (input.type === 'file') {
                input.disabled = false;
            } else {
                input.removeAttribute('readonly');
            }
            input.classList.remove('bg-gray-100', 'cursor-not-allowed');
        });
        saveButton.disabled = false;
        saveButton.classList.remove('opacity-50', 'cursor-not-allowed');
    }

    function createEditButton() {
        const editBtn = document.createElement('button');
        editBtn.type = 'button';
        editBtn.textContent = 'Editar';
        editBtn.id = 'editBtn';
        editBtn.className = 'px-4 py-2 bg-yellow-500 text-white rounded hover:bg-yellow-600 transition';
        form.appendChild(editBtn);

        editBtn.addEventListener('click', handleEditClick);
    }

    let originalValues = {};

    function handleEditClick() {
        Swal.fire({
            title: 'Deseja editar seus dados?',
            text: "Você poderá alterar os campos e depois salvar.",
            icon: 'question',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Sim, editar'
        }).then((result) => {
            if (result.isConfirmed) {
                inputs.forEach(input => {
                    if (input.type !== 'file') {
                        originalValues[input.name] = input.value;
                    }
                });
                setEditableState();
                document.getElementById('editBtn').remove();
            }
        });
    }

    form.addEventListener('submit', function (e) {
        e.preventDefault();

        Swal.fire({
            title: 'Salvar alterações?',
            text: "Tem certeza que deseja atualizar seu perfil?",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#16a34a',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Sim, salvar',
            cancelButtonText: 'Cancelar'
        }).then((result) => {
            if (result.isConfirmed) {
                loaderOverlay.classList.remove("hidden");
                setTimeout(() => {
                    form.submit();
                }, 1000);
            } else {
                inputs.forEach(input => {
                    if (input.type !== 'file') {
                        input.value = originalValues[input.name] || '';
                    }
                });
                setReadonlyState();
                if (!document.getElementById('editBtn')) {
                    createEditButton();
                }
            }
        });
    });

    setReadonlyState();
    createEditButton();
});

document.addEventListener('DOMContentLoaded', function () {
    const profilePhoto = document.getElementById('profilePhoto');
    const photoInput = document.getElementById('photoInput');

    profilePhoto.addEventListener('click', () => {
        if (!photoInput.disabled) {
            photoInput.click();
        }
    });

    photoInput.addEventListener('change', () => {
        const file = photoInput.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function (e) {
                profilePhoto.src = e.target.result;
            };
            reader.readAsDataURL(file);
        }
    });
});
