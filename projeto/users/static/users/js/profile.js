 const form = document.getElementById("profileForm");
      const btnSave = document.getElementById("btnSave");
      const btnSaveSpinner = document.getElementById("btnSaveSpinner");
      const btnSaveText = document.getElementById("btnSaveText");
      const loaderOverlay = document.getElementById("loaderOverlay");

      const initialData = {};
      for (const input of form.querySelectorAll("input")) {
        initialData[input.name] = input.value;
      }

      function checkChanges() {
        for (const input of form.querySelectorAll("input")) {
          if (input.value !== initialData[input.name]) {
            btnSave.disabled = false;
            return;
          }
        }
        btnSave.disabled = true;
      }

      form.addEventListener("input", checkChanges);

      form.addEventListener("submit", async (e) => {
        e.preventDefault();

        // Confirmar se deseja salvar
        const result = await Swal.fire({
          title: "Confirmar",
          text: "Deseja salvar as modificações?",
          icon: "question",
          showCancelButton: true,
          confirmButtonText: "Sim, salvar",
          cancelButtonText: "Cancelar",
          confirmButtonColor: "#2563EB",
          cancelButtonColor: "#aaa",
        });

        if (!result.isConfirmed) {
          // Cancelou
          return;
        }

        // Mostra loader tela inteira
        loaderOverlay.classList.remove("hidden");

        // Começa loading botão também
        btnSave.disabled = true;
        btnSaveSpinner.classList.remove("hidden");
        btnSaveText.textContent = "Salvando...";

        // Simula chamada ao backend - aqui que vai seu fetch / axios
        const formData = {};
        for (const input of form.querySelectorAll("input")) {
          formData[input.name] = input.value;
        }
        console.log("Dados a enviar para o backend:", formData);

        // Simulação de delay da chamada
        await new Promise((r) => setTimeout(r, 2000));

        // Esconde loader
        loaderOverlay.classList.add("hidden");

        // Fim do loading botão
        btnSaveSpinner.classList.add("hidden");
        btnSaveText.textContent = "Salvar";

        // Atualiza dados iniciais para bloquear o botão salvar
        for (const input of form.querySelectorAll("input")) {
          initialData[input.name] = input.value;
        }
        btnSave.disabled = true;

        // Mostra sucesso
        Swal.fire({
          toast: true,
          position: "bottom-end",
          icon: "success",
          title: "Dados do perfil atualizados com sucesso!",
          showConfirmButton: false,
          timer: 5000,
          timerProgressBar: true,
          didOpen: (toast) => {
            toast.addEventListener("mouseenter", Swal.stopTimer);
            toast.addEventListener("mouseleave", Swal.resumeTimer);
          },
        });
      });