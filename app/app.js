// Simple helper for showing validation errors
function setError(field, message) {
  const span = document.querySelector(`.error-message[data-error-for="${field.id}"]`);
  if (span) {
    span.textContent = message || "";
  }
}

function clearErrors(form) {
  form.querySelectorAll(".error-message").forEach((el) => (el.textContent = ""));
}

function validateRequired(field, label) {
  if (!field.value.trim()) {
    setError(field, `${label} is required`);
    return false;
  }
  return true;
}

function validateEmail(field, label) {
  if (!field.value.trim()) {
    setError(field, `${label} is required`);
    return false;
  }
  const re = /\S+@\S+\.\S+/;
  if (!re.test(field.value)) {
    setError(field, `Enter a valid ${label.toLowerCase()}`);
    return false;
  }
  return true;
}

// Contact form behavior
(function setupContactForm() {
  const form = document.getElementById("contact-form");
  if (!form) return;

  const successMessage = form.querySelector('[data-testid="contact-success"]');

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    clearErrors(form);
    if (successMessage) {
      successMessage.hidden = true;
    }

    const name = document.getElementById("name");
    const email = document.getElementById("email");
    const topic = document.getElementById("topic");
    const message = document.getElementById("message");

    let valid = true;
    valid = validateRequired(name, "Name") && valid;
    valid = validateEmail(email, "Email") && valid;
    valid = validateRequired(topic, "Topic") && valid;
    valid = validateRequired(message, "Message") && valid;

    if (!valid) return;

    // Simulate "submission"
    if (successMessage) {
      successMessage.hidden = false;
    }
    form.reset();
  });
})();

// Login modal behavior
(function setupLoginModal() {
  const modal = document.getElementById("login-modal");
  if (!modal) return;

  const openBtn = document.querySelector("[data-open-login]");
  const closeBtn = modal.querySelector("[data-close-login]");
  const form = document.getElementById("login-form");
  const successMessage = modal.querySelector('[data-testid="login-success"]');
  const userLabel = document.getElementById("login-user-label");

  function openModal() {
    modal.setAttribute("aria-hidden", "false");
  }

  function closeModal() {
    modal.setAttribute("aria-hidden", "true");
    clearErrors(form);
    if (successMessage) successMessage.hidden = true;
    form.reset();
  }

  openBtn?.addEventListener("click", openModal);
  closeBtn?.addEventListener("click", closeModal);

  modal.addEventListener("click", (e) => {
    if (e.target === modal) closeModal();
  });

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    clearErrors(form);
    if (successMessage) successMessage.hidden = true;

    const email = document.getElementById("login-email");
    const password = document.getElementById("login-password");

    let valid = true;
    valid = validateEmail(email, "Email") && valid;
    valid = validateRequired(password, "Password") && valid;

    if (!valid) return;

    // "Login" rule: password must be at least 4 chars – already enforced
    if (userLabel) {
      userLabel.textContent = email.value.trim();
    }
    if (successMessage) {
      successMessage.hidden = false;
    }
  });
})();

