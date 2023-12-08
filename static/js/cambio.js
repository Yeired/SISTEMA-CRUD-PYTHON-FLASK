document.getElementById("register-link").addEventListener("click", function(event) {
    event.preventDefault(); // Evita que se siga el enlace

    document.getElementById("login-form").classList.add("hidden");
    document.getElementById("register-form").classList.remove("hidden");
  });

  document.getElementById("back-to-login").addEventListener("click", function(event) {
    event.preventDefault(); // Evita que se siga el enlace

    document.getElementById("register-form").classList.add("hidden");
    document.getElementById("login-form").classList.remove("hidden");
  });