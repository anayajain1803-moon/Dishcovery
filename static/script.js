document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("ingredientsForm");
  const button = document.getElementById("find-dish-btn");

  form.addEventListener("submit", (event) => {
    const ingredients = document.getElementById("ingredients").value.trim();

    if (!ingredients) {
      event.preventDefault();
      alert("Please enter some ingredients!");
      return;
    }

    button.textContent = "Finding Recipes...";
    button.disabled = true;
  });
});
