const form = document.getElementById("createPostForm");
const btnCreate = form.querySelector("button[type=submit]");
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

    setTimeout(() => {
        form.submit();
    }, 1000);
});
