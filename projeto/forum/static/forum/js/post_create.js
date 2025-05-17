const form = document.getElementById("createPostForm");
const btnCreate = document.getElementById("btnCreate");
const btnCreateText = document.getElementById("btnCreateText");
const loaderOverlay = document.getElementById("loaderOverlay");

const initialData = {
    title: "",
    content: "",
};

form.addEventListener("input", () => {
    const title = form.title.value.trim();
    const content = form.content.value.trim();
    btnCreate.disabled = !(
        title &&
        content &&
        (title !== initialData.title || content !== initialData.content)
    );
});

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const result = await Swal.fire({
        title: "Confirmar",
        text: "Deseja publicar este post?",
        icon: "question",
        showCancelButton: true,
        confirmButtonText: "Sim, publicar",
        cancelButtonText: "Cancelar",
        confirmButtonColor: "#2563EB",
        cancelButtonColor: "#aaa",
    });

    if (!result.isConfirmed) return;

    loaderOverlay.classList.remove("hidden");

    const formData = {
        title: form.title.value.trim(),
        content: form.content.value.trim(),
    };

    console.log("Post a ser enviado:", formData); // Aqui entra o fetch/axios depois

    await new Promise((r) => setTimeout(r, 2000)); // simula backend

    loaderOverlay.classList.add("hidden");

    Swal.fire({
        toast: true,
        position: "bottom-end",
        icon: "success",
        title: "Post criado e publicado com sucesso!",
        showConfirmButton: false,
        timer: 5000,
        timerProgressBar: true,
    });

    form.reset();
    btnCreate.disabled = true;
});